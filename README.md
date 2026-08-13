<p align="center">
  <img src="misc/cover_image.png" alt="QMN, Quantitative Methods in Neuroscience" width="500">
</p>

# Quantitative Methods in Neuroscience (QMN)

Practical notebooks for the **Quantitative Methods in Neuroscience** course, Master in Neuroscience, University of Geneva (2026-27), taught by Prof. Sami El-Boustani.

> **Status (August 2026): development repository.**
> All thirteen teaching weeks now have a draft, written by the teaching team and under review. Notebooks are committed **with their outputs**, so a reviewer can read what a notebook produces without running it, and most of them still contain the solutions. The student-facing repository, with solutions removed, is generated from this one at the end.

## Getting started

See [`SETUP_INSTRUCTIONS.txt`](SETUP_INSTRUCTIONS.txt) for the full setup guide: install conda, create the `qmn` environment from `environment.yml`, register the Jupyter kernel, open a notebook.

To check an install, from `notebooks/` with the environment active:

```
python src/check_env.py
```

or, from inside any notebook, which also tells you whether you picked the right kernel:

```python
from src.check_env import check_environment
check_environment()
```

Every notebook runs in the same environment, `qmn`, and reads its data from `notebooks/data/` through a path that works wherever the notebook is opened from:

```python
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "data").is_dir() else Path.cwd().parent
trials = pd.read_csv(ROOT / "data" / "ibl_2afc.csv.gz")
```

## The weekly notebooks

One folder, one file per week, named `NN_topic[_vN][_TA|_STUDENT].ipynb`. `_TA` carries the solutions, `_STUDENT` is the version handed out. Outdated drafts (kept for reference) are in `notebooks/legacy/`.

| Week | Topic | Notebook |
|---|---|---|
| 1 | Programming and Python fundamentals | `01_programming_fundamentals_v2_TA` |
| 2 | Math refresher and fundamental functions | `02_math_refresher_TA` |
| 3 | Probability and descriptive statistics | `03_probability_descriptive_TA` |
| 4 | Inference I: t-tests, effect size, power | `04_inference_ttests_power_TA` |
| 5 | Inference II: ANOVA and repeated measures | `05a_repeated_measures_practical_STUDENT`, `05b_anova_mechanics_advanced_STUDENT` |
| 6 | Non-parametrics, permutation, bootstrap | `06_nonparametrics_permutation_bootstrap_TA` |
| 7 | Correlation and regression | `07_regression_TA`, `07_regression_STUDENT` |
| 8 | Mixed-effects models | `08_mixed_effects_TA` |
| 9 | Linear algebra fundamentals | `09_linear_algebra_fundamentals_TA` |
| 10 | Linear algebra for statistics | `10_linear_algebra_statistics_TA` |
| 11 | Principal component analysis | `11_pca_alpha_TA` |
| 12 | Time series analysis | `12_time_series_TA` |
| 13 | Fourier analysis | `13_fourier_TA` |

Week 14 is the exam and has no practical.

## Datasets

Three real datasets serve the whole course, and each is used across several weeks so that students meet a new method rather than a new dataset every time. They live in `notebooks/data/` and are read from there, never downloaded and never duplicated.

- `ibl_2afc.csv.gz` and `ibl_2afc_subjects.csv`: behaviour of thirty mice from the International Brain Laboratory, used from Week 3 to Week 8. See `ibl_2afc_datadictionary.md`.
- `alphawaves.npz`: EEG with eyes open and eyes closed, used in Weeks 11 to 13.
- `erpcore_n170.npz`: the ERP CORE N170 face-perception set, for the evoked-response material. See `eeg_datadictionary.md` and the accompanying licence.

Each dataset has an `explore_*.ipynb` beside it in `notebooks/data/`, already run and with its figures, which is the quickest way to see what is inside before writing a practical around it. How each dataset was built is documented in its data dictionary; the build scripts themselves stay on the author's machine, since they need API credentials and warm caches.

`notebooks/data/legacy/` holds material no live notebook reads any more, currently the synthetic 2AFC set that the first version of Notebook 2 was built on.

## Conventions

Proposals from the repository cleanup of 13/08, open for discussion:

**Notebooks.** One folder, `notebooks/`, one file per week, named `NN_topic[_vN][_TA|_STUDENT].ipynb`. The two suffixes are the only capitals: `_TA` carries the solutions, `_STUDENT` is the version handed out, `_vN` marks a competing version while the team decides. Outdated material goes to `notebooks/legacy/`, never deleted and never left next to the live files.

**Environment.** One environment for the whole course, `qmn`, built from `environment.yml`, registered as the kernel `Python (qmn)`. A notebook that needs a new package adds it to `environment.yml` **and** to `REQUIRED` in `src/check_env.py`, so that everyone finds out by running the check rather than by hitting an `ImportError` mid-session (never `pip install` from inside a notebook).

**Data.** One copy of each dataset, in `notebooks/data/`, with its data dictionary beside it. Read it through the root path shown above, never with an absolute path and never by downloading at runtime. Every practical should use one of the two prepackaged datasets, the IBL behaviour or the EEG package. Datasets no longer used by a live notebook move to `notebooks/data/legacy/`.

**Assets and code.** Images live in `notebooks/assets/NN/`, one subfolder per notebook. `notebooks/src/` is for code only: the shared helpers in `qmn_utils.py` and the environment check. Images are committed, never hotlinked from a website, and should be ones we are allowed to redistribute, since this material ends up in front of students.

**Outputs.** Notebooks are committed **with** their outputs while the course is being written, so that a reviewer can read the results without running anything (the `nbstripout` filter is therefore off for now).

**Exercises.** Difficulty tags (one to three stars) on every exercise, and each notebook should include a repair-the-bug exercise and one pipeline written from scratch. The marker that separates a solution from the exercise around it is still being agreed by the team; until it is, follow the notebook you are extending.

## Repository layout

```
QMN_course_2026/
├── README.md                  ← this file
├── SETUP_INSTRUCTIONS.txt     ← detailed setup guide
├── environment.yml            ← conda environment ("qmn")
├── .gitattributes             ← notebook outputs are kept, see the comment inside
├── .gitignore
├── misc/
│   └── cover_image.png
└── notebooks/
    ├── NN_topic_TA.ipynb      ← one per week, see the table above
    ├── assets/                ← images, one subfolder per notebook (assets/09/, ...)
    ├── data/                  ← the course datasets, one copy of each
    │   ├── explore_*.ipynb    ← a tour of each dataset, run and with figures
    │   └── legacy/            ← datasets no live notebook reads
    ├── legacy/                ← superseded drafts, kept for reference
    └── src/
        ├── __init__.py
        ├── check_env.py       ← environment and data check
        └── qmn_utils.py       ← shared helper functions
```
