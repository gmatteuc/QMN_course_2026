# Data dictionary for `ibl_2afc.csv`

## Provenance

This file is a small, course-friendly subset of the **public International
Brain Laboratory (IBL) behavioural data release**, downloaded from the public
Openalyx server and reshaped by `data_prep/build_ibl_dataset.py`.

- Source task: the **IBL visual decision-making task**.
- Primary references:
  - International Brain Laboratory et al. (2021), "Standardized and reproducible
    measurement of decision-making in mice", *eLife* 10:e63711.
  - International Brain Laboratory et al. (2025), "A brain-wide map of neural
    activity during complex behaviour", *Nature* 645:177.

## The task in one paragraph

A head-fixed mouse, with its forepaws on a small steering **wheel**, faces a
screen. On each trial a **Gabor grating** (a striped patch) appears on the
**left or right** of the screen at one of several **contrast** levels. The
wheel is coupled to the grating; the mouse must **turn the wheel to bring the
grating to the centre** within 60 s. A correct turn earns a water reward; an
incorrect turn (or no response) gives a noise burst and a time-out. Difficulty
is set by the contrast: high contrast is easy, 0 % contrast carries no visual
information at all.

## Two task phases (`phase` column)

- **`training`**: the *basic task* (`trainingChoiceWorld`). The stimulus is
  equally likely on either side (`probability_left` = 0.5 throughout). Mice are
  still **learning**; performance improves across sessions.
- **`trained`**: the *full task* (`biasedChoiceWorld`). Well-trained mice; each
  session opens with 90 unbiased trials, then the stimulus-side prior switches
  between blocks (`probability_left` ∈ {0.2, 0.8}). This is the IBL "bias block"
  manipulation.

The file contains **10 mice × 2 phases × 8 sessions each = 160 sessions,
~100,000 trials**. The **same 10 mice appear in both phases**: IBL mice progress
through the pipeline (`trainingChoiceWorld` → `biasedChoiceWorld`), so each
mouse contributes both training-phase and trained-phase sessions, and `phase`
is a genuine within-subject factor.

The 10 mice are a **lab-balanced** set: 5 from **Anne Churchland's lab** 
(Cold Spring Harbor Laboratory; `CSHL…` identifiers) and 5 from
**Dora Angelaki's lab** (New York University; `CSP…` identifiers). They were selected
among the 129 IBL mice based on several performance and reaction-time criteria.
Per-mouse metadata (lab, institution, sex, age, project) is in the companion file
`ibl_2afc_subjects.csv`.

## Columns

| Column | Type | Units | Meaning | IBL source |
|---|---|---|---|---|
| `trial_id` | int | — | Unique row index across the whole file. | — |
| `subject_id` | str | — | Mouse identifier (IBL naming, e.g. `CSHL051`, `CSP028`). Join key to the companion `ibl_2afc_subjects.csv`. | session metadata |
| `phase` | str | — | `training` or `trained` (see above). | task protocol |
| `session` | int | — | Session number within a subject (1–8). | — |
| `trial_in_session` | int | — | Trial position within its session (1…N). | row order |
| `signed_contrast` | float | fraction [−1, 1] | Gabor **contrast**, signed: **positive = stimulus on the right, negative = left, 0 = no stimulus**. Magnitudes are {0, 0.0625, 0.125, 0.25, 0.5, 1.0} i.e. {0, 6.25, 12.5, 25, 50, 100} %. | `contrastRight − contrastLeft` |
| `stimulus_side` | str | — | `'right'`, `'left'` or `'zero'`: the sign of `signed_contrast`, for convenience. | derived |
| `response` | float | 0 / 1 / NaN | The side the mouse **chose**: `1` = right, `0` = left, `NaN` = no-go. | `choice` (see convention below) |
| `correct` | float | 0 / 1 / NaN | `1` if the trial was rewarded, `0` if not, `NaN` on no-go trials. | `feedbackType` |
| `no_go` | bool | — | `True` if the mouse made no choice within the response window. **Kept, not dropped** (see below). | `choice == 0` |
| `reaction_time_s` | float | seconds | **Reaction time**: time from stimulus onset to the **first wheel movement**. **Kept raw** (may be negative or implausibly short; see below). | `firstMovement_times − stimOn_times` |
| `response_time_s` | float | seconds | **Response time**: time from stimulus onset to the moment the **choice threshold was crossed** (the choice was completed). | `response_times − stimOn_times` |
| `probability_left` | float | probability | Block prior: the probability the stimulus is on the left. `0.5` in `training`; `{0.2, 0.5, 0.8}` in `trained` (0.5 only in the 90-trial unbiased intro of each trained session). | `probabilityLeft` |
| `reward_volume` | float | µL | Water delivered on the trial (≈ 1.5 µL on rewarded trials, 0 otherwise). | `rewardVolume` |
| `stim_on_time_s` | float | s (from session start) | Stimulus-onset time. | `stimOn_times` |
| `go_cue_time_s` | float | s | Go-cue (onset tone) time. | `goCue_times` |
| `first_movement_time_s` | float | s | Time of the first detected wheel movement. | `firstMovement_times` |
| `choice_time_s` | float | s | Time the choice threshold was crossed (IBL calls this `response_times`). | `response_times` |
| `feedback_time_s` | float | s | Time reward / noise-burst feedback was delivered. | `feedback_times` |

The five `*_time_s` columns are the **raw event timestamps**; the derived
latencies `reaction_time_s` and `response_time_s` are provided for convenience
but can be re-computed from them.

## The `choice` → `response` convention

The adopted sign convention is the following:

- `choice = −1` → the mouse chose **right** → `response = 1`
- `choice = +1` → the mouse chose **left** → `response = 0`
- `choice =  0` → **no-go** → `response = NaN`

## The dataset is not perfectly "clean" yet.

The dataset is intentionally shipped **uncleaned** in two respects, so that
students can practise real data cleaning.

### 1. Raw reaction times (`reaction_time_s`)

`reaction_time_s` is kept exactly as computed (`firstMovement − stimOn`). It
therefore contains values that are **not valid reaction times**:

- **Negative values**: the first wheel movement began
  *before* stimulus onset. Per the IBL "Working with wheel data" documentation,
  *"negative times mean the onset of the movement occurred before the go cue"* —
  the mouse was already moving the wheel.
- **Implausibly short values** (< 80 ms): a movement that fast cannot be a
  *response to* the stimulus (mouse visual→motor latency is ≥ ~100 ms).
- **Very long values** (up to ~60 s): the mouse dithered for most of the
  response window.

> References for the validity window: IBL 2025 *Nature* paper, Methods "Trials"
> and Fig. 1c caption ("truncated at 80 ms and 2 s; 22.8 % of first
> wheel-movement times occurred under 80 ms"); IBL Brain-Wide-Map 2022 data
> white paper, "Data quality → Trials".

### 2. No-go trials (`no_go`)

Trials where the mouse made no choice within the response window are **kept**
and flagged with `no_go = True` (310 trials). On these, `response` and `correct`
are `NaN`. IBL's own analyses label no-go trials as incorrect.

## Companion file — `ibl_2afc_subjects.csv`

A small **subject-level metadata table**: one row per mouse (10 rows), queried
from the IBL Alyx database. It is the *dimension table* to `ibl_2afc.csv`'s
trial-level *fact table* (the two are joined on `subject_id`).

| Column | Meaning |
|---|---|
| `subject_id` | Mouse identifier (the join key to `ibl_2afc.csv`). |
| `lab` | IBL laboratory code: `churchlandlab` or `angelakilab`. |
| `institution` | The lab's institution: Cold Spring Harbor Laboratory, or New York University. |
| `sex` | `M` or `F`. |
| `birth_date` | Date of birth (`YYYY-MM-DD`). |
| `age_weeks_at_first_session` | Age, in weeks, at the mouse's first training session. |
| `project` | The IBL project the mouse belongs to. |