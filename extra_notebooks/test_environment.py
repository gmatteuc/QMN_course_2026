from __future__ import annotations

import os
import sys
from importlib import import_module
from pathlib import Path

EXPECTED_ENV = "qmn-optional"
PACKAGES = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("pandas", "pandas"),
    ("matplotlib", "matplotlib"),
    ("mne", "mne"),
    ("nilearn", "nilearn"),
    ("nibabel", "nibabel"),
    ("sklearn", "scikit-learn"),
    ("openneuro", "openneuro-py"),
    ("pymatreader", "pymatreader"),
    ("edfio", "edfio"),
    ("h5py", "h5py"),
    ("jupyterlab", "jupyterlab"),
    ("ipywidgets", "ipywidgets"),
]

print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])
print("Conda environment:", os.environ.get("CONDA_DEFAULT_ENV", "not reported"))
print()

failures: list[str] = []
for module_name, package_name in PACKAGES:
    try:
        module = import_module(module_name)
        version = getattr(module, "__version__", "version not exposed")
        print(f"OK  {package_name:16s} {version}")
    except Exception as exc:
        failures.append(f"{package_name}: {type(exc).__name__}: {exc}")
        print(f"FAIL {package_name:16s} {type(exc).__name__}: {exc}")

print()
env_name = Path(sys.prefix).name
if env_name != EXPECTED_ENV:
    failures.append(
        f"Wrong environment: expected {EXPECTED_ENV!r}, but sys.prefix ends in {env_name!r}."
    )

if failures:
    print("ENVIRONMENT TEST FAILED")
    for failure in failures:
        print(" -", failure)
    raise SystemExit(1)

print("ALL IMPORT TESTS PASSED")
