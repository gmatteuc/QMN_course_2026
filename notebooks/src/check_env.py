"""Check that the course environment and the course data are in place.

Run it from a notebook, as the first cell of the setup section:

    from src.check_env import check_environment
    check_environment()

or from a terminal, with the qmn environment active, from the notebooks/ folder:

    python src/check_env.py

It prints one line per package with the version actually installed, one line
per dataset, and a verdict at the end. Nothing here is course-specific beyond
the two lists below: when a notebook starts using a new package, add it to
REQUIRED so that everybody finds out by running this rather than by hitting an
ImportError in the middle of a session.
"""

import importlib
import sys
from pathlib import Path

# Everything the weekly notebooks import. Keep in step with environment.yml.
REQUIRED = [
    ("numpy", "arrays and maths"),
    ("pandas", "tables"),
    ("scipy", "statistics and signal processing"),
    ("matplotlib", "plotting"),
    ("seaborn", "statistical plots"),
    ("statsmodels", "regression, ANOVA, mixed models"),
    ("sklearn", "PCA, regression, cross-validation"),
    ("mne", "scalp topographies, Notebook 11 only"),
    ("ipywidgets", "interactive figures, Notebooks 9 and 10"),
]

# What the notebooks read from notebooks/data/. The behavioural files are needed from Week 1,
# the EEG ones only from Week 10, and they are handed out later because they are large. Their
# absence is not a problem, so it is reported as such rather than as a missing file.
DATASETS = [
    "ibl_2afc.csv.gz",
    "ibl_2afc_subjects.csv",
]
DATASETS_LATER = [
    "alphawaves.npz",
    "erpcore_n170.npz",
]


def course_root():
    """The notebooks/ folder, found from wherever this was started.

    Notebooks always run with the working directory set to their own folder, so
    inside a notebook the one-line idiom in the README is enough. A script is
    different: it gets typed from wherever the student happens to be, most often
    the project root, so it is worth looking around a little.
    """
    here = Path.cwd()
    for candidate in (here, here / "notebooks", here.parent, here.parent.parent):
        if (candidate / "data").is_dir() and (candidate / "src").is_dir():
            return candidate
    return here          # nothing found: report against the current folder


def check_environment(verbose=True):
    """Report the state of the environment and the data. Returns True if all is well."""
    root = course_root()
    missing_packages, missing_data = [], []

    if verbose:
        print(f"python      : {sys.version.split()[0]}")
        print(f"interpreter : {sys.executable}")
        print(f"course root : {root}")
        print()

    for name, purpose in REQUIRED:
        try:
            module = importlib.import_module(name)
            version = getattr(module, "__version__", "installed")
            if verbose:
                print(f"  ok      {name:<12} {version:<10} {purpose}")
        except ImportError:
            missing_packages.append(name)
            if verbose:
                print(f"  MISSING {name:<12} {'':<10} {purpose}")

    if verbose:
        print()

    for filename in DATASETS:
        path = root / "data" / filename
        if path.is_file():
            if verbose:
                size_mb = path.stat().st_size / 1e6
                print(f"  ok      {filename:<24} {size_mb:6.1f} MB")
        else:
            missing_data.append(filename)
            if verbose:
                print(f"  MISSING {filename:<24} expected in {root / 'data'}")

    for filename in DATASETS_LATER:
        path = root / "data" / filename
        if verbose:
            if path.is_file():
                size_mb = path.stat().st_size / 1e6
                print(f"  ok      {filename:<24} {size_mb:6.1f} MB")
            else:
                print(f"  later   {filename:<24} only needed from Week 10, not a problem now")

    ok = not missing_packages and not missing_data
    if verbose:
        print()
        if ok:
            print("All good: the environment and the data are ready.")
        else:
            if missing_packages:
                print("Missing packages :", ", ".join(missing_packages))
                print("  Fix with       : conda env update -f environment.yml")
                print("  and check you selected the qmn environment as the kernel, top right.")
            if missing_data:
                print("Missing data     :", ", ".join(missing_data))
                print("  Fix with       : git pull, and open the notebook from notebooks/")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if check_environment() else 1)
