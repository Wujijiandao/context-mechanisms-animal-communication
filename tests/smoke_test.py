from __future__ import annotations
from pathlib import Path
import os, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy(); ENV["PYTHONPATH"] = str(ROOT / "src")
checks = [
    ("analysis/01_titi_2013_reanalysis.py", [], "bigrams"),
    ("analysis/06_a2_power_simulation.py", ["--reps", "200"], "medium"),
    ("analysis/07_sdt_observational_equivalence.py", [], "fixed target-present response rate"),
]
for script, args, needle in checks:
    out = subprocess.check_output([sys.executable, str(ROOT/script), *args], env=ENV, text=True)
    if needle not in out:
        raise AssertionError(f"{script}: expected token {needle!r}")
    print(f"PASS {script}")
print("All public smoke tests passed.")
