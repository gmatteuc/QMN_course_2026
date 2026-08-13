"""
Generate a small synthetic psychophysics dataset for Notebook 2 (Math Refresher).

Scenario
--------
Simplified 2-alternative forced choice (2AFC) motion-discrimination task.
On each trial the participant sees a random-dot kinematogram with a given
signed motion coherence (negative = leftward, positive = rightward; magnitude
= strength). They must report the perceived direction (left / right) and we
record the response and the reaction time (RT).

Each subject does several training sessions, so the dataset contains a
*learning* dimension: across sessions the perceptual sensitivity grows,
the RTs shorten, and lapses become rarer. This lets the notebook illustrate
learning curves (exponential approach to asymptote) on top of the per-session
psychometric / chronometric analyses.

The file is a *placeholder* used while we wait for a real behavioural dataset
from a partner lab. Generation is deterministic (fixed seed) so the exercises
in the notebook produce stable numbers.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def sigmoid(x, slope=1.0, bias=0.0):
    """Logistic sigmoid: P(right) as a function of signed coherence."""
    return 1.0 / (1.0 + np.exp(-(slope * x - bias)))


def exp_approach(t, y0, y_inf, tau):
    """Exponential approach from y0 (at t=0) to y_inf with time-constant tau."""
    return y_inf + (y0 - y_inf) * np.exp(-t / tau)


def simulate_subject(subject_id, n_sessions, coherences, n_trials_per_cond,
                     slope_0, slope_inf, tau_slope,
                     bias,
                     lapse_0, lapse_inf, tau_lapse,
                     rt_base_0, rt_base_inf, tau_rt,
                     rt_difficulty_gain, rt_log_sigma,
                     rng):
    """Simulate one subject across `n_sessions` training sessions."""
    rows = []
    for session in range(1, n_sessions + 1):
        # Session-level parameters follow exponential learning curves.
        t = session - 1
        slope = exp_approach(t, slope_0, slope_inf, tau_slope)
        lapse = exp_approach(t, lapse_0, lapse_inf, tau_lapse)
        rt_base = exp_approach(t, rt_base_0, rt_base_inf, tau_rt)

        # Build the list of (coherence) trials for this session and shuffle it.
        trial_cohs = np.repeat(coherences, n_trials_per_cond)
        rng.shuffle(trial_cohs)

        for trial_in_session, coh in enumerate(trial_cohs, start=1):
            # Choice model: lapse-corrected logistic.
            p_right_ideal = sigmoid(coh, slope=slope, bias=bias)
            p_right = lapse * 0.5 + (1.0 - lapse) * p_right_ideal
            response = int(rng.binomial(1, p_right))

            # Correctness (NaN at coherence 0: no objectively correct answer).
            if coh > 0:
                correct = int(response == 1)
            elif coh < 0:
                correct = int(response == 0)
            else:
                correct = np.nan

            # RT: log-normal, slower when |coherence| is small (hard trials).
            mu_log = np.log(rt_base + rt_difficulty_gain * (1.0 - abs(coh)))
            rt = float(rng.lognormal(mean=mu_log, sigma=rt_log_sigma))

            rows.append({
                "subject_id": subject_id,
                "session": session,
                "trial_in_session": trial_in_session,
                "coherence": float(coh),
                "response": response,
                "correct": correct,
                "rt_s": rt,
            })
    return rows


def main():
    rng = np.random.default_rng(seed=42)

    coherences = np.array([-0.5, -0.3, -0.15, -0.05, 0.0, 0.05, 0.15, 0.3, 0.5])
    n_trials_per_cond = 20  # per session per coherence
    n_sessions = 8

    # Three subjects with different starting points, asymptotes and learning rates.
    subjects = [
        dict(subject_id="S01",
             slope_0=3.0,  slope_inf=12.0, tau_slope=2.5,
             bias=0.10,
             lapse_0=0.20, lapse_inf=0.03, tau_lapse=2.0,
             rt_base_0=0.55, rt_base_inf=0.30, tau_rt=2.5,
             rt_difficulty_gain=0.35, rt_log_sigma=0.28),
        dict(subject_id="S02",
             slope_0=2.0,  slope_inf=15.0, tau_slope=3.5,
             bias=-0.05,
             lapse_0=0.25, lapse_inf=0.02, tau_lapse=2.5,
             rt_base_0=0.65, rt_base_inf=0.28, tau_rt=3.0,
             rt_difficulty_gain=0.45, rt_log_sigma=0.30),
        dict(subject_id="S03",
             slope_0=4.0,  slope_inf=9.0,  tau_slope=1.8,
             bias=0.0,
             lapse_0=0.15, lapse_inf=0.05, tau_lapse=1.8,
             rt_base_0=0.50, rt_base_inf=0.35, tau_rt=2.0,
             rt_difficulty_gain=0.25, rt_log_sigma=0.22),
    ]

    all_rows = []
    for s in subjects:
        all_rows.extend(simulate_subject(
            n_sessions=n_sessions,
            coherences=coherences,
            n_trials_per_cond=n_trials_per_cond,
            rng=rng,
            **s,
        ))

    df = pd.DataFrame(all_rows)
    # Stable subject/session/trial order in the final file.
    df = df.sort_values(["subject_id", "session", "trial_in_session"]).reset_index(drop=True)
    df.insert(0, "trial_id", np.arange(len(df)))

    out_path = Path(__file__).parent / "data" / "psychophysics_2afc.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} trials ({df['subject_id'].nunique()} subjects, "
          f"{df['session'].nunique()} sessions each) to {out_path}")


if __name__ == "__main__":
    main()
