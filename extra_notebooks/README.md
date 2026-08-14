# Optional neuroimaging notebooks

This small package is independent of the core Week 5 ANOVA notebooks. It contains three optional demonstrations:

- **MNE-Python:** public EEGBCI recording, raw EEG visualization, spectrum, and ICA.
- **Nilearn:** one preprocessed ABIDE resting-state fMRI participant, Schaefer atlas visualization, and parcel time-series extraction.
- **OpenNeuro + MNE:** selected BIDS EEG files from `ds003061`, robust `.set` loading, ICA, and a descriptive auditory oddball/P300 example.

## Installation

Follow `CREATE_ENVIRONMENT_LINUX.txt`. The recommended environment is `qmn-optional` with Python 3.11.

## Data

No external dataset is included. The notebooks download their examples into a local `data/` directory on first execution. Do not commit that downloaded data to GitHub.

## Teaching scope

These notebooks are optional package demonstrations. They introduce data access, file inspection, basic preprocessing, and visualization; they are not complete EEG or fMRI analysis pipelines.
