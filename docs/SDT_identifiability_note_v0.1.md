# SDT identifiability note v0.1

## Purpose

This note formalizes one reason that context-sensitive response rates cannot, by themselves,
identify whether context changed receiver evidence or the decision policy.

Under equal-variance signal detection theory, let

\[
X\mid Z=1 \sim \mathcal N(d'/2,1),
\qquad
X\mid Z=0 \sim \mathcal N(-d'/2,1),
\]

and let the receiver respond when

\[
X>c.
\]

The target-present response rate is

\[
h=P(O=1\mid Z=1)=\Phi(d'/2-c).
\]

Therefore, for any fixed \(h\in(0,1)\),

\[
\boxed{
c=\frac{d'}{2}-\Phi^{-1}(h)
}
\]

defines a continuum of \((d',c)\) pairs with exactly the same response rate.

## Proposition: single-rate non-identifiability

A single binary response rate measured only on target-present trials does not identify
sensitivity \(d'\) and criterion \(c\) separately.

This matters because:

- transmission/access manipulations can alter effective discriminability;
- current inferential priors can alter the internal decision variable or effective criterion;
- payoff/risk/action context can alter the decision criterion.

Thus a context-related change in \(P(O=1)\) cannot localize the route without additional
conditions.

If both hit rate \(h\) and false-alarm rate \(f\) are measured, then under equal-variance
SDT assumptions,

\[
d'=\Phi^{-1}(h)-\Phi^{-1}(f),
\]

\[
c=-\frac{1}{2}
\left[
\Phi^{-1}(h)+\Phi^{-1}(f)
\right].
\]

Catch/control trials therefore add information that a target-present response rate alone
cannot provide.

## Important limitation

Even \(d'\) and \(c\) do not map one-to-one onto P/T/I/H/A. A Bayesian prior can manifest
behaviourally as a criterion shift, and an action-cost manipulation can do the same. SDT is
therefore a local identifiability tool, not a complete mechanism classifier.

The stronger design combines:

1. target-present and target-absent/catch conditions;
2. calibrated receiver-accessible signal evidence;
3. orthogonal manipulation of current evidence and action payoff;
4. cause/category-specific readouts;
5. held-out cue-conflict trials.
