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

# The datasets every notebook reads from notebooks/data/.
DATASETS = [
    "ibl_2afc.csv.gz",
    "ibl_2afc_subjects.csv",
    "alphawaves.npz",
    "erpcore_n170.npz",
]


def course_root():
    """The notebooks/ folder, whether we are inside it or in a subfolder of it."""
    here = Path.cwd()
    return here if (here / "data").is_dir() else here.parent


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

    ok = not missing_packages and not missing_data
    if verbose:
        print()
        if ok:
            print("All good: the environment and the data are ready.")
        else:
            if missing_packages:
                print("Missing packages :", ", ".join(missing_packages))
                print("  Fix with       : conda env update -f environment.yml")
                print("  and check you selected the 'Python (qmn)' kernel, top right.")
            if missing_data:
                print("Missing data     :", ", ".join(missing_data))
                print("  Fix with       : git pull, and open the notebook from notebooks/")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if check_environment() else 1)
