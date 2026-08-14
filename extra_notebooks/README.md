# Extra notebooks

Optional material that sits outside the thirteen weekly practicals: neuroimaging notebooks, other
modalities, and anything we may later use for the exam.

The structure mirrors `notebooks/`, so nothing has to be learned twice:

```
extra_notebooks/
├── assets/     images used by these notebooks
├── data/       see the note inside: heavy data is not committed here
└── src/        shared helpers, if any are needed
```

Two rules differ from the weekly notebooks, on purpose.

**These notebooks may download their own data.** The weekly ones never do, everything comes from
`notebooks/data/`. Here the point is often the opposite: showing how to fetch a dataset from an
online source, with `nilearn`, `mne` or `openneuro-py`. So the data is not committed, the code that
fetches it is.

**Heavy data stays out of the repository.** If a notebook needs a file that cannot be downloaded by
a library, put a short note in `data/` saying what the file is and where it lives, rather than the
file itself. See `data/note.txt`.

These notebooks also need packages the course environment does not carry, such as `nilearn`,
`openneuro-py`, `nibabel` and `edfio`. An environment file for them will live here once we settle
which ones are really needed.
