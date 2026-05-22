"""Build a small, course-friendly CSV out of the public IBL data release.

What it does
------------
- Connects (anonymous) to the IBL public Openalyx server.
- IBL mice progress through the training pipeline: each mouse first does the
  `trainingChoiceWorld` task (learning) and then graduates to the
  `biasedChoiceWorld` task (trained, with bias blocks). So the SAME mouse has
  sessions of both. This script uses a fixed, curated, lab-balanced list of
  10 mice (CURATED_SUBJECTS: see the comment there) and takes the earliest
  N_SESSIONS_PER_MOUSE sessions of each protocol:
    * `trainingChoiceWorld`  → phase "training" (learning curves visible)
    * `biasedChoiceWorld`    → phase "trained"  (post-training, bias blocks)
  The result: the same 10 mice appear in both phases, so `phase` is a genuine
  within-subject factor.
- Applies a single tidy schema across both phases (see map_to_qmn_schema and
  the data dictionary `notebooks/data/ibl_2afc_datadictionary.md` for the
  meaning, units and IBL source field of every column):
    trial_id, subject_id, phase, session, trial_in_session,
    signed_contrast, stimulus_side, response, correct, no_go,
    reaction_time_s, response_time_s, probability_left, reward_volume,
    stim_on_time_s, go_cue_time_s, first_movement_time_s,
    choice_time_s, feedback_time_s
- Runs a self-consistency check (validate()) before writing the CSV 
    (useful if we decide to modify stuff along the way).
- Saves the combined dataframe as `notebooks/data/ibl_2afc.csv`.

Caching: each downloaded session's trials.table is cached as a parquet in
`data_prep/cache/<eid>.pqt`; re-running the script is essentially free as
long as the cache is intact. Delete the cache to redownload.

Run from anywhere:
    python data_prep/build_ibl_dataset.py
"""

from __future__ import annotations

import os
import sys
import time
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from one.api import ONE


# ----------------------- configuration -----------------------------------
# The 10 mice that make up the dataset:
#   5 from the Churchland lab (Cold Spring Harbor Laboratory), prefix CSHL
#   5 from the Angelaki  lab (New York University),            prefix CSP
# All 10 were picked from the 129 IBL mice with >= 8 sessions of both the
# training and biased protocols, scored on a three-axis compromise:
#   1. reaction-time distribution — fraction of RTs in IBL's [0.08, 2.0] s window
#   2. learning curve             — gradual training-phase accuracy gain
#   3. psychometric curve         — steep, monotonic trained psychometric
# Every chosen mouse shows real learning and a clean trained psychometric.

CURATED_SUBJECTS = ["CSHL051", "CSHL054", "CSHL059", "CSHL060", "CSHL_014",
                    "CSP016", "CSP023", "CSP026", "CSP028", "CSP033"]

N_MICE                  = len(CURATED_SUBJECTS)
N_SESSIONS_PER_MOUSE    = 8     # per phase
MIN_TRIALS_PER_SESSION  = 100   # skip very short sessions
SESSION_BUFFER          = 10    # extra candidate sessions per phase

# IBL mice progress through the pipeline training -> biased
TRAINING_PROTOCOL = "_iblrig_tasks_trainingChoiceWorld"   # phase "training"
BIASED_PROTOCOL   = "_iblrig_tasks_biasedChoiceWorld"     # phase "trained"

HERE          = Path(__file__).resolve().parent
CACHE_DIR     = HERE / "cache"
OUT_PATH      = HERE.parent / "notebooks" / "data" / "ibl_2afc.csv"
SUBJECTS_OUT  = HERE.parent / "notebooks" / "data" / "ibl_2afc_subjects.csv"

LAB_INSTITUTION = {
    "angelakilab":   "New York University",
    "churchlandlab": "Cold Spring Harbor Laboratory",
}

# ----------------------- helpers -----------------------------------------
def connect(verbose: bool = True) -> ONE:
    if verbose:
        print("Connecting to https://openalyx.internationalbrainlab.org (anonymous)…", flush=True)
    return ONE(base_url='https://openalyx.internationalbrainlab.org',
               password='international', silent=True)


def _sessions_by_subject(one: ONE, protocol: str) -> dict[str, list]:
    """Return {subject: [eid, …]} for all public sessions of a protocol,
    each subject's list ordered chronologically (earliest session first).
    """
    rows = list(one.alyx.rest('sessions', 'list',
                              task_protocol=protocol,
                              dataset_types='trials.table'))
    by_subject: dict[str, list] = {}
    for row in rows:
        subj = row.get('subject')
        eid  = row.get('url', '').rstrip('/').split('/')[-1] or row.get('id')
        start = row.get('start_time') or ''
        if subj and eid:
            by_subject.setdefault(subj, []).append((start, eid))
    # sort each subject's sessions by start time, keep only the eids
    for subj, items in by_subject.items():
        items.sort()
        by_subject[subj] = [eid for _, eid in items]
    return by_subject


def select_subjects(one: ONE, n_sessions: int) -> dict[str, dict]:
    """Load the curated mice (CURATED_SUBJECTS) and verify each has at least
    n_sessions sessions of BOTH the training and biased protocols. Returns
        {subject: {"training": [eid, …], "trained": [eid, …]}}
    with the earliest sessions of each protocol (plus a buffer of spares so the
    short-session skip in main() can still reach n_sessions good ones).
    """
    print(f"  REST listing {TRAINING_PROTOCOL!r} sessions…", flush=True)
    training = _sessions_by_subject(one, TRAINING_PROTOCOL)
    print(f"  REST listing {BIASED_PROTOCOL!r} sessions…", flush=True)
    biased = _sessions_by_subject(one, BIASED_PROTOCOL)

    take = n_sessions + SESSION_BUFFER
    chosen: dict[str, dict] = {}
    for subj in CURATED_SUBJECTS:
        n_tr = len(training.get(subj, []))
        n_bi = len(biased.get(subj, []))
        if n_tr < n_sessions or n_bi < n_sessions:
            raise RuntimeError(
                f"curated subject {subj!r} has only {n_tr} training / {n_bi} biased "
                f"public sessions (need >= {n_sessions} of each)."
            )
        chosen[subj] = {
            "training": training[subj][:take],
            "trained":  biased[subj][:take],
        }
        print(f"    {subj!r}: {n_tr} training / {n_bi} biased sessions available", flush=True)
    return chosen


def load_trials(one: ONE, eid: str) -> pd.DataFrame | None:
    """Return the trials.table for one session as a DataFrame, using a parquet cache."""
    cache = CACHE_DIR / f"{eid}.pqt"
    if cache.exists():
        try:
            return pd.read_parquet(cache)
        except Exception:
            cache.unlink(missing_ok=True)

    try:
        df = one.load_dataset(eid, '_ibl_trials.table.pqt')
    except Exception as err:
        print(f"    [skip] load_dataset failed for {eid[:8]}: {err}")
        return None

    if not isinstance(df, pd.DataFrame):
        print(f"    [skip] unexpected type from load_dataset for {eid[:8]}: {type(df)}")
        return None

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache)
    return df


def _col(df: pd.DataFrame, name: str) -> pd.Series:
    """Return a float column, or an all-NaN series if the column is absent."""
    if name in df.columns:
        return df[name].astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def map_to_qmn_schema(df: pd.DataFrame, *, subject_id: str, phase: str,
                      session: int) -> pd.DataFrame:
    """Apply the QMN schema mapping to one session's IBL trials table.

    The mapping is deliberately faithful to the IBL conventions — see the
    module docstring and the data dictionary for the rationale of every field.
    """
    # --- signed contrast: contrast on the right minus contrast on the left.
    #     positive = stimulus on the RIGHT, negative = LEFT, 0 = no stimulus.
    cl = df['contrastLeft'].fillna(0.0).astype(float)
    cr = df['contrastRight'].fillna(0.0).astype(float)
    signed_contrast = (cr - cl).round(6)
    stimulus_side = np.where(signed_contrast > 0, 'right',
                     np.where(signed_contrast < 0, 'left', 'zero'))

    # --- choice -> response. IBL convention (verified on 54,877 correct trials):
    #       choice = -1  ->  mouse chose RIGHT  -> response = 1
    #       choice = +1  ->  mouse chose LEFT   -> response = 0
    #       choice =  0  ->  no-go              -> response = NaN
    choice = df['choice'].astype(float)
    response = np.where(choice == -1, 1.0,
                np.where(choice == 1, 0.0, np.nan))
    no_go = (choice == 0).to_numpy()

    # --- correct, from feedbackType (+1 rewarded, -1 error). NaN on no-go.
    fbk = df['feedbackType'].astype(float)
    correct = np.where(no_go, np.nan, np.where(fbk == 1, 1.0, 0.0))

    # --- raw event timestamps (seconds from session start)
    stim_on  = _col(df, 'stimOn_times')
    go_cue   = _col(df, 'goCue_times')
    first_mv = _col(df, 'firstMovement_times')
    choice_t = _col(df, 'response_times')
    feedback = _col(df, 'feedback_times')

    # --- derived latencies
    reaction_time = first_mv - stim_on      # time to first wheel movement
    response_time = choice_t - stim_on      # time to complete the choice

    out = pd.DataFrame({
        "subject_id"            : subject_id,
        "phase"                 : phase,
        "session"               : session,
        "trial_in_session"      : np.arange(1, len(df) + 1),
        "signed_contrast"       : signed_contrast,
        "stimulus_side"         : stimulus_side,
        "response"              : response,
        "correct"               : correct,
        "no_go"                 : no_go,
        "reaction_time_s"       : reaction_time.round(4),
        "response_time_s"       : response_time.round(4),
        "probability_left"      : _col(df, 'probabilityLeft'),
        "reward_volume"         : _col(df, 'rewardVolume'),
        "stim_on_time_s"        : stim_on.round(4),
        "go_cue_time_s"         : go_cue.round(4),
        "first_movement_time_s" : first_mv.round(4),
        "choice_time_s"         : choice_t.round(4),
        "feedback_time_s"       : feedback.round(4),
    })
    return out


def validate(df: pd.DataFrame) -> None:
    """Self-consistency checks. Raise AssertionError on any internal contradiction.

    The key check: on *decidable* trials (non-zero contrast, a real choice),
    a trial is correct if and only if the mouse's response matched the side
    the stimulus was actually on. This cross-checks the `response` mapping
    (derived from `choice`) against `correct` (derived independently from
    `feedbackType`). This would catch an inverted choice/response convention.
    """
    d = df[(df['signed_contrast'] != 0) & (~df['no_go'])]
    resp_is_right = d['response'] == 1
    stim_is_right = d['signed_contrast'] > 0
    derived_correct = (resp_is_right == stim_is_right).astype(float)
    mism = int((derived_correct != d['correct']).sum())
    assert mism == 0, (
        f"VALIDATION FAILED: {mism} decidable trials where "
        f"(response vs stimulus side) disagrees with `correct`. "
        f"The choice->response mapping is probably inverted."
    )
    # No-go bookkeeping must be self-consistent.
    assert (df.loc[df['no_go'], 'response'].isna().all()
            and df.loc[df['no_go'], 'correct'].isna().all()), \
        "VALIDATION FAILED: no_go trials must have NaN response and correct."
    print(f"  validation OK — response x stimulus_side x correct consistent "
          f"on {len(d):,} decidable trials.")


def build_subjects_table(one: ONE, subjects: list[str]) -> pd.DataFrame:
    """One row of metadata per mouse, queried from the IBL Alyx database.

    This is the subject-level companion to the trial-level `ibl_2afc.csv`;
    the two are joined on `subject_id`. Only the fields the public IBL release
    actually populates are included: `strain`, `genotype` and `species` are
    empty in the public data and therefore omitted.
    """
    rows = []
    for subj in subjects:
        rec = list(one.alyx.rest("subjects", "list", nickname=subj))[0]
        # earliest training session = the mouse's first contact with the task
        sess = list(one.alyx.rest("sessions", "list", subject=subj,
                                   task_protocol=TRAINING_PROTOCOL))
        first_start = min((s["start_time"] for s in sess), default=None)
        birth = rec.get("birth_date")
        age_weeks = None
        if birth and first_start:
            age_weeks = round((pd.Timestamp(first_start).tz_localize(None)
                               - pd.Timestamp(birth)).days / 7)
        lab = rec.get("lab")
        rows.append({
            "subject_id":  subj,
            "lab":         lab,
            "institution": LAB_INSTITUTION.get(lab, lab),
            "sex":         rec.get("sex"),
            "birth_date":  birth,
            "age_weeks_at_first_session": age_weeks,
            "project":     ", ".join(rec.get("projects") or []),
        })
    return pd.DataFrame(rows).sort_values("subject_id").reset_index(drop=True)


# ----------------------- main pipeline -----------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true",
                        help="ignore the parquet cache and re-download every session")
    args = parser.parse_args()
    if args.force:
        for p in CACHE_DIR.glob("*.pqt"):
            p.unlink()
        print("cache cleared.")

    one = connect()

    print("\nSelecting the curated mice (same mice appear in both phases)…")
    t0 = time.time()
    chosen = select_subjects(one, N_SESSIONS_PER_MOUSE)
    print(f"  selection done in {time.time() - t0:.1f}s")

    all_rows: list[pd.DataFrame] = []
    for subj_idx, (subject, phases) in enumerate(chosen.items(), start=1):
        print(f"\n[{subj_idx}/{N_MICE}]  subject {subject!r}")
        for phase in ("training", "trained"):
            kept = 0
            for eid in phases[phase]:
                if kept >= N_SESSIONS_PER_MOUSE:
                    break
                df = load_trials(one, eid)
                if df is None or len(df) < MIN_TRIALS_PER_SESSION:
                    continue
                kept += 1
                all_rows.append(map_to_qmn_schema(
                    df, subject_id=subject, phase=phase, session=kept))
                print(f"    {phase:>8}  session {kept}  {eid[:8]}…  {len(df):>5} trials")
            if kept < N_SESSIONS_PER_MOUSE:
                print(f"    WARNING: only {kept}/{N_SESSIONS_PER_MOUSE} good "
                      f"{phase} sessions for {subject!r}", file=sys.stderr)

    if not all_rows:
        print("\nNo data collected. Aborting.", file=sys.stderr)
        sys.exit(1)

    big = pd.concat(all_rows, ignore_index=True)
    big.insert(0, "trial_id", np.arange(len(big)))

    print("\nValidating dataset…")
    validate(big)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    big.to_csv(OUT_PATH, index=False)
    print(f"\nWrote {len(big):,} trials to {OUT_PATH}")
    print(f"  phases     : {sorted(big['phase'].unique())}")
    print(f"  subjects   : {big['subject_id'].nunique()}")
    print(f"  per-phase  : {big.groupby('phase')['subject_id'].nunique().to_dict()}")
    print(f"  no-go      : {int(big['no_go'].sum()):,} trials")
    rt = big['reaction_time_s']
    print(f"  reaction_time_s: median {rt.median():.3f}s, "
          f"{(rt < 0).mean()*100:.1f}% negative, "
          f"{((rt >= 0.08) & (rt <= 2.0)).mean()*100:.1f}% in IBL window [0.08, 2.0]s")
    print(f"  CSV size   : {OUT_PATH.stat().st_size / 1024:.0f} KB")

    # --- subject-level metadata table
    print("\nBuilding subject metadata table…")
    subjects_df = build_subjects_table(one, CURATED_SUBJECTS)
    subjects_df.to_csv(SUBJECTS_OUT, index=False)
    print(f"Wrote {len(subjects_df)} subjects to {SUBJECTS_OUT}")
    print(subjects_df.to_string(index=False))


if __name__ == "__main__":
    main()
