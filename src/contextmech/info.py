from __future__ import annotations

from collections import Counter
import itertools
import math
from typing import Iterable, Sequence

import numpy as np
from scipy import stats


def entropy(values: Sequence[object]) -> float:
    """Empirical Shannon entropy in bits."""
    n = len(values)
    counts = Counter(values)
    return -sum((c / n) * math.log2(c / n) for c in counts.values() if c)


def mutual_information(x: Sequence[object], y: Sequence[object]) -> float:
    """Empirical mutual information I(X;Y) in bits."""
    n = len(x)
    cx, cy, cxy = Counter(x), Counter(y), Counter(zip(x, y))
    out = 0.0
    for (a, b), c in cxy.items():
        pxy = c / n
        out += pxy * math.log2(pxy / ((cx[a] / n) * (cy[b] / n)))
    return out


def weighted_mi(records: Iterable[tuple[object, object, float]]) -> float:
    """Mutual information for (x, y, probability_mass) records."""
    recs = list(records)
    px = Counter()
    py = Counter()
    pxy = Counter()
    for x, y, p in recs:
        px[x] += p
        py[y] += p
        pxy[(x, y)] += p
    out = 0.0
    for (x, y), p in pxy.items():
        if p > 0 and px[x] > 0 and py[y] > 0:
            out += p * math.log2(p / (px[x] * py[y]))
    return out


def exact_signflip_mean(diffs: Sequence[float], alternative: str = "two-sided") -> tuple[float, float]:
    """Exact sign-flip test using the paired mean difference."""
    d = np.asarray(diffs, dtype=float)
    obs = float(d.mean())
    null = np.array([
        np.mean(d * np.asarray(signs, dtype=float))
        for signs in itertools.product([-1, 1], repeat=len(d))
    ])
    if alternative == "greater":
        p = np.mean(null >= obs - 1e-12)
    elif alternative == "less":
        p = np.mean(null <= obs + 1e-12)
    else:
        p = np.mean(np.abs(null) >= abs(obs) - 1e-12)
    return obs, float(p)


def exact_mcnemar(b: int, c: int) -> float:
    """Two-sided exact McNemar/binomial p value from discordant counts."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, j) for j in range(k + 1)) / (2 ** n)
    return float(min(1.0, 2 * tail))


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(stats.beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi
