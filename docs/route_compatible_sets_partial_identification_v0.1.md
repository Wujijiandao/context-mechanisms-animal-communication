# Route-compatible sets and partial identification v0.1

Let

\[
\mathcal R=\{P,T,I,H,A\}.
\]

Because multiple routes can co-activate, candidate mechanisms are subsets

\[
R\subseteq\mathcal R.
\]

For design \(D\), observed/interventional distribution \(P_{\rm obs}\), and admissible model
family \(\mathcal G\), define

\[
\boxed{
\mathfrak C(D,P_{\rm obs})
=
\left\{
R\subseteq\mathcal R:
\exists G_R\in\mathcal G_R
\text{ compatible with }D\text{ and }P_{\rm obs}
\right\}.
}
\]

This is a **route-compatible family**, not a causal-DAG Markov-equivalence class.

Define

\[
R^{+}=\bigcup_{R\in\mathfrak C} R
\]

and

\[
R^{-}=\bigcap_{R\in\mathfrak C} R.
\]

- \(r\notin R^+\): route \(r\) is ruled out within the model family.
- \(r\in R^-\): every compatible mechanism set contains route \(r\).
- \(r\in R^+\setminus R^-\): route \(r\) remains possible but is not necessary.
- \(|\mathfrak C|=1\): one route-set is point-identified within the stated assumptions.

Thus **unresolved is a valid scientific result**.

A generic behavioural contrast may leave

\[
R^+=\{T,I,A\}.
\]

Calibrating receiver-accessible \(Y\) can remove T,

\[
\{T,I,A\}\rightarrow\{I,A\}.
\]

Cause-specific readouts, catch trials, orthogonal payoff manipulations and held-out
cue-conflict tests may shrink the family further. Point identification is not guaranteed.

The logic is related to the standard causal-inference idea that interventions refine
equivalence classes, but the present object is a coarse biological mechanism family rather
than a new theorem about DAG equivalence.
