<p align="center">
  <img src="misc/cover_image.png" alt="QMN — Quantitative Methods in Neuroscience" width="500">
</p>

# Quantitative Methods in Neuroscience (QMN)

Practical notebooks for the **Quantitative Methods in Neuroscience** course — Master in Neuroscience, University of Geneva (2026-27), taught by Prof. Sami El-Boustani.

> **Status (May 2026) — initial development.**
> The repository currently contains a single draft notebook (`notebooks/02_math_refresher.ipynb`) built on a *synthetic* 2AFC behavioural dataset, used to align on the notebook template before the rest of the semester is built out. Real datasets from neuroscience labs in the Geneva area will replace the synthetic placeholder as the material grows. Notebooks for the other 13 weeks will be added by analogy with this first one.

## Getting started

See [`README.txt`](README.txt) for the full setup guide (install conda, create the `qmn` environment, register the Jupyter kernel, run the notebook).

## Repository layout

```
QMN_course_2026/
├── README.md              ← this file
├── README.txt             ← detailed setup guide
├── environment.yml        ← conda environment ("qmn")
├── .gitattributes         ← activates nbstripout for *.ipynb
├── .gitignore
├── misc/
│   └── cover_image.png
└── notebooks/
    ├── 02_math_refresher.ipynb
    ├── data/
    │   └── psychophysics_2afc.csv
    ├── generate_synthetic_data.py
    └── src/
        ├── __init__.py
        └── qmn_utils.py
```
