from __future__ import annotations
import argparse, csv
from collections import defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from contextmech.broja import broja_pid


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def distribution(rows, representation):
    recs = []
    n = len(rows)
    for r in rows:
        z, c = r["predator"], r["location"]
        if representation == "first_call":
            recs.append((z, r["first_AB_call"], c, 1/n))
        elif representation == "all_calls":
            na, nb = int(r["n_A"]), int(r["n_B"])
            total = na + nb
            if total:
                recs.append((z, "A", c, (1/n)*(na/total)))
                recs.append((z, "B", c, (1/n)*(nb/total)))
        elif representation == "bigrams":
            for key, label in [("prop_AA","AA"),("prop_AB","AB"),("prop_BA","BA"),("prop_BB","BB")]:
                p = float(r[key])
                if p > 0:
                    recs.append((z, label, c, (1/n)*p))
        else:
            raise ValueError(representation)
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT/"data/processed_public/titi_2013_core_trials.csv"))
    args = ap.parse_args()

    rows = read_rows(args.input)
    for rep in ["first_call", "all_calls", "bigrams"]:
        out = broja_pid(distribution(rows, rep))
        print(rep, out)


if __name__ == "__main__":
    main()
