from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.stats import norm


def hit_rate(dprime: float, criterion: float) -> float:
    return float(norm.cdf(dprime / 2.0 - criterion))


def false_alarm_rate(dprime: float, criterion: float) -> float:
    return float(norm.cdf(-dprime / 2.0 - criterion))


def criterion_for_fixed_hit(dprime: float, hit: float) -> float:
    return float(dprime / 2.0 - norm.ppf(hit))


def recover_from_hit_fa(hit: float, false_alarm: float) -> tuple[float, float]:
    zh = norm.ppf(hit)
    zf = norm.ppf(false_alarm)
    dprime = float(zh - zf)
    criterion = float(-0.5 * (zh + zf))
    return dprime, criterion


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hit", type=float, default=0.70)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    ds = np.linspace(0.0, 3.0, 13)
    rows = []
    for d in ds:
        c = criterion_for_fixed_hit(float(d), args.hit)
        h = hit_rate(float(d), c)
        f = false_alarm_rate(float(d), c)
        rows.append((float(d), c, h, f))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(["dprime", "criterion_c", "target_present_response_rate", "false_alarm_rate"])
            w.writerows(rows)

    print(f"fixed target-present response rate h={args.hit:.6f}")
    for d, c, h, f in rows[::3]:
        print(f"d'={d:.3f}, c={c:.6f}, hit={h:.6f}, false_alarm={f:.6f}")


if __name__ == "__main__":
    main()
