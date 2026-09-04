from __future__ import annotations

from collections import defaultdict
import math
from typing import Iterable

import numpy as np
from scipy.optimize import minimize


def _mi_from_q(q: np.ndarray, shape: tuple[int, int, int], axes_xy: tuple[int, ...]) -> float:
    arr = q.reshape(shape)
    # axes_xy identifies the variables retained; T is axis 0.
    if axes_xy == (0, 1):
        p = arr.sum(axis=2)
        pt = p.sum(axis=1, keepdims=True)
        ps = p.sum(axis=0, keepdims=True)
    elif axes_xy == (0, 2):
        p = arr.sum(axis=1)
        pt = p.sum(axis=1, keepdims=True)
        ps = p.sum(axis=0, keepdims=True)
    elif axes_xy == (0, 1, 2):
        p = arr
        pt = arr.sum(axis=(1, 2), keepdims=True)
        ps = arr.sum(axis=0, keepdims=True)
    else:
        raise ValueError("unsupported axes")
    mask = p > 0
    if axes_xy == (0, 1, 2):
        denom = pt * ps
    else:
        denom = pt * ps
    return float(np.sum(p[mask] * np.log2(p[mask] / denom[mask])))


def broja_pid(records: Iterable[tuple[object, object, object, float]]) -> dict[str, float]:
    """
    Small discrete BROJA PID via constrained SLSQP.

    records: iterable of (target, source1, source2, probability_mass).
    The optimizer preserves pairwise marginals (T,S1) and (T,S2) and minimizes
    I(T;S1,S2). Suitable for the small categorical systems in this repository.
    """
    recs = list(records)
    T = sorted({r[0] for r in recs}, key=str)
    S1 = sorted({r[1] for r in recs}, key=str)
    S2 = sorted({r[2] for r in recs}, key=str)
    ti = {v:i for i,v in enumerate(T)}
    s1i = {v:i for i,v in enumerate(S1)}
    s2i = {v:i for i,v in enumerate(S2)}
    shape = (len(T), len(S1), len(S2))

    p = np.zeros(shape, dtype=float)
    for t, a, b, mass in recs:
        p[ti[t], s1i[a], s2i[b]] += float(mass)
    p /= p.sum()

    p_ts1 = p.sum(axis=2)
    p_ts2 = p.sum(axis=1)

    def objective(q):
        return _mi_from_q(q, shape, (0,1,2))

    constraints = []
    # Preserve T,S1 marginals.
    for i in range(shape[0]):
        for j in range(shape[1]):
            target = float(p_ts1[i,j])
            idx = [(i*shape[1] + j)*shape[2] + k for k in range(shape[2])]
            constraints.append({
                "type":"eq",
                "fun": lambda q, idx=idx, target=target: float(np.sum(q[idx]) - target)
            })
    # Preserve T,S2 marginals. Skip one redundant equation per T to help conditioning.
    for i in range(shape[0]):
        for k in range(shape[2]-1):
            target = float(p_ts2[i,k])
            idx = [(i*shape[1] + j)*shape[2] + k for j in range(shape[1])]
            constraints.append({
                "type":"eq",
                "fun": lambda q, idx=idx, target=target: float(np.sum(q[idx]) - target)
            })

    x0 = p.ravel().copy()
    res = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * x0.size,
        constraints=constraints,
        options={"ftol":1e-12, "maxiter":5000, "disp":False},
    )
    if not res.success:
        raise RuntimeError(f"BROJA optimization failed: {res.message}")

    qstar = np.clip(res.x, 0, 1)
    qstar /= qstar.sum()

    I1 = _mi_from_q(p.ravel(), shape, (0,1))
    I2 = _mi_from_q(p.ravel(), shape, (0,2))
    I12 = _mi_from_q(p.ravel(), shape, (0,1,2))
    Iminjoint = objective(qstar)
    synergy = I12 - Iminjoint

    # Under BROJA, unique information can be obtained from optimized joint MI:
    # Iminjoint = redundancy + UI1 + UI2, while I1 = redundancy + UI1, I2 = redundancy + UI2.
    redundancy = I1 + I2 - Iminjoint
    ui1 = I1 - redundancy
    ui2 = I2 - redundancy

    # Clean numerical noise.
    def clean(x):
        return 0.0 if abs(x) < 1e-10 else float(x)

    return {
        "I_source1": clean(I1),
        "I_source2": clean(I2),
        "I_joint": clean(I12),
        "U_source1": clean(ui1),
        "U_source2": clean(ui2),
        "redundancy": clean(redundancy),
        "synergy": clean(synergy),
    }
