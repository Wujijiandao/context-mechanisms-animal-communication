from __future__ import annotations
import os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy(); ENV["PYTHONPATH"] = str(ROOT / "src")

def run(script, *args):
    return subprocess.check_output([sys.executable, str(ROOT/script), *args], env=ENV, text=True)
def number(pattern, text):
    m=re.search(pattern,text)
    if not m: raise AssertionError(f"pattern not found: {pattern}\n{text}")
    return float(m.group(1))
def close(a,b,tol=1e-8):
    if abs(a-b)>tol: raise AssertionError(f"{a} != {b} within {tol}")

out=run("analysis/01_titi_2013_reanalysis.py")
line=next(x for x in out.splitlines() if x.startswith("bigrams "))
close(number(r"'I_source1': ([0-9.eE+-]+)",line),0.6054964139843471,1e-9)
close(number(r"'I_joint': ([0-9.eE+-]+)",line),0.7035138286168204,1e-9)
close(number(r"'synergy': ([0-9.eE+-]+)",line),0.09801741463245317,1e-8)
print("PASS titi 2013 numerical regression")

out=run("analysis/06_a2_power_simulation.py","--reps","4000")
for pat,thr in [(r"medium .*\(24, ([0-9.]+)\)",0.8),(r"strong .*\(12, ([0-9.]+)\)",0.8),(r"modest .*\(64, ([0-9.]+)\)",0.8)]:
    v=number(pat,out)
    if v<thr: raise AssertionError(f"power landmark failed {v}")
print("PASS A2 power planning regression")

out=run("analysis/07_sdt_observational_equivalence.py","--hit","0.70")
line=next(x for x in out.splitlines() if x.startswith("d'=1.500"))
close(number(r"c=([0-9.eE+-]+)",line),0.2255994872919594,1e-6)
close(number(r"hit=([0-9.eE+-]+)",line),0.7,1e-12)
print("PASS SDT identifiability regression")
print("ALL PUBLIC NUMERICAL REGRESSION TESTS PASSED")
