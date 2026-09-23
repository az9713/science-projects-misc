# Blind-Spot Pass: QR Factorization and Least Squares

## Topic stack

Study the pieces in this order; each one depends on the one before it.

1. **The problem statement.** Linear least squares: given `A` (m×n, usually m ≥ n) and `b`, find `x` minimizing `||Ax - b||_2`. Understand the normal equations `A^T A x = A^T b` as the calculus solution (gradient of the squared residual set to zero) before touching any algorithm.
2. **Why the normal equations are numerically dangerous.** `A^T A` squares the condition number: `kappa(A^T A) = kappa(A)^2`. This is the single fact that motivates every other method in this topic.
3. **Orthogonal transformations as the fix.** Multiplying by an orthogonal (or unitary) matrix `Q` preserves the 2-norm, so `||Ax - b|| = ||Q^T A x - Q^T b||`. This lets you triangularize `A` without ever forming `A^T A`.
4. **Householder reflections.** The workhorse for dense QR: each step zeros a whole subcolumn below the diagonal using one reflection. Backward stable, the default in LAPACK (`dgeqrf`).
5. **Givens rotations.** Zero one entry at a time. Useful when `A` is sparse or structured (e.g., Hessenberg matrices, updating a QR factorization after a row insertion).
6. **Gram-Schmidt, classical and modified.** The "textbook" orthogonalization, but classical Gram-Schmidt (CGS) loses orthogonality badly; modified Gram-Schmidt (MGS) is much better but still not backward stable like Householder.
7. **Reorthogonalization.** A cheap patch for Gram-Schmidt: redo the projection step. "Twice is enough" is a folk theorem (Kahan, popularized by Parlett) with real numerical grounding.
8. **Column-pivoted QR (QRCP) and rank-revealing QR.** What to do when `A` is rank-deficient or nearly so — plain QR does not reveal this reliably; pivoting does, approximately.
9. **Sensitivity of least squares.** The conditioning of the least-squares solution itself, not just of `A^T A`. This splits into a part that depends on `kappa(A)` and a part that depends on `kappa(A)^2` through the residual.
10. **Rank-deficient and underdetermined problems, minimum-norm solutions.** When `A` doesn't have full column rank, or `m < n`, "the" least-squares solution is not unique; you need the minimum-norm solution, typically via the SVD or a rank-revealing factorization.
11. **Weighted and constrained least squares, Tikhonov regularization.** Generalizations: unequal confidence in residuals (weighted), hard linear constraints, and ridge-type regularization for ill-posed or rank-deficient problems.
12. **Tall-skinny QR (TSQR).** A communication-avoiding algorithm for QR of a matrix with very many rows and few columns, relevant on parallel and distributed systems (MapReduce-style, GPUs, out-of-core).

## Unknown unknowns

These are the things people studying this topic often do not know they should be asking.

- **The normal equations are not just "less accurate" — they can destroy information the original problem still has.** If `kappa(A) ~ 1/sqrt(u)` (`u` is unit roundoff, about `1.1e-16` in double precision), `A^T A` computed in floating point can be numerically singular even though `A` itself is perfectly well-conditioned via QR. "Normal equations vs QR" is not a speed/accuracy tradeoff; it is a threshold effect.
- **QR alone does not solve the whole least-squares sensitivity story.** Even with a backward-stable QR solver, the sensitivity of `x*` to perturbations in `A` and `b` has two terms: one scaling with `kappa(A)`, and one scaling with `kappa(A)^2` multiplied by the **residual norm** `||r|| = ||Ax* - b||`. Small residual (good fit): the `kappa^2` term barely matters. Large residual: it dominates, and a stable algorithm cannot rescue an ill-conditioned problem. "Stable algorithm" and "well-conditioned problem" are different claims.
- **CGS and MGS are mathematically identical in exact arithmetic but differ in rounding-error growth rate, not just a constant factor.** MGS's loss of orthogonality grows roughly like `kappa(A) * u`; CGS's grows roughly like `kappa(A)^2 * u` — a full power of the condition number apart. See Common Misconceptions for the numerical check.
- **Neither CGS nor MGS is backward stable in the strong sense Householder QR is.** MGS is equivalent to Householder QR applied to `A` stacked on an identity block, which gives good normwise least-squares behavior, but its `Q`'s departure from orthogonality is still `kappa(A) * u`, not `u` alone. If `Q` itself must stay orthogonal to machine precision (e.g., reused across many Krylov steps), prefer Householder.
- **Column pivoting does not certify rank; it usually reveals it.** QRCP (Businger-Golub) moves the column of largest remaining norm into the pivot position each step, so `R`'s diagonal usually drops sharply at the true numerical rank. But QRCP can fail on adversarial matrices (the classical Kahan matrix) — it is a heuristic; certified rank-revealing behavior needs strong RRQR (Gu-Eisenstat) or the SVD.
- **Minimum-norm solutions require care about which system you factor.** For underdetermined `Ax = b` (`m < n`, full row rank), the minimum-norm solution is `x = A^T (A A^T)^{-1} b`, obtained stably from a QR factorization of `A^T`, not of `A`. Conflating the tall (least-squares) and wide (minimum-norm) orientations is a common setup error.
- **TSQR is not "QR but parallel" in a superficial sense.** It builds a valid `R` (up to sign/scaling per block) by recursively combining local `R` factors, but the intermediate `Q` is never formed as one dense matrix — it lives as a tree of small transformations. Getting explicit `Q` (not just `R` or `Q^T b`) means applying that tree in reverse; forgetting this is a common bug when swapping TSQR in for `numpy.linalg.qr`.
- **Tikhonov regularization is not "add a small number to the diagonal" loosely remembered — it acts on the singular values of A, not a condition-number label.** The filter factor for singular value `sigma_i` is `sigma_i^2 / (sigma_i^2 + lambda^2)`: a smooth suppression, not a hard threshold. Confusing it with a truncated-SVD hard cutoff is a persistent slip.

## Common misconceptions

Each item states the misconception, the correct statement, and one concrete numerical check (with real output from the experiments run for this pass).

**1. Misconception: "Normal equations and QR give the same accuracy; QR is just for style/speed."**
Correct statement: forming `A^T A` explicitly squares the condition number, so `kappa(A^T A) = kappa(A)^2` (to leading order, in exact arithmetic; in floating point this is also observed in practice). Since the accuracy of a solved linear system degrades with its condition number, solving `A^T A x = A^T b` directly is much more exposed to rounding error than solving the same least-squares problem via QR of `A`.

Concrete check (run for this pass, `numpy`, double precision, `m=30, n=6`, singular values from 1 down to 1e-4 so `kappa(A) ≈ 1e4`):
```
kappa(A)      = 1.000000e+04
kappa(A^T A)  = 1.000000e+08
kappa(A)^2    = 1.000000e+08
ratio kappa(AtA)/kappa(A)^2 = 1.0000
```
The measured ratio of `kappa(A^T A)` to `kappa(A)^2` is exactly 1.0000, confirming the squaring relationship to four decimal places on this test matrix.

**2. Misconception: "Classical and modified Gram-Schmidt are basically the same algorithm with a reordering that doesn't matter numerically."**
Correct statement: CGS and MGS compute the same result in exact arithmetic, but MGS's departure from orthogonality of the computed `Q` grows roughly in proportion to `kappa(A) * u`, while CGS's grows roughly in proportion to `kappa(A)^2 * u`, where `u` is unit roundoff (`u ≈ 1.11e-16` in double precision). That is a difference of one full power of `kappa(A)`, which becomes dramatic once `kappa(A)` exceeds about `1e8`.

Concrete check (run for this pass, `numpy`, `m=40, n=10`, three matrices with `kappa(A)` roughly `1e3`, `1e6`, `1e10`; measuring `||Q^T Q - I||_2`):
```
kappa(A)~1.00e+03: ||Qc^T Qc - I||=4.138e-12  ||Qm^T Qm - I||=2.685e-14  kappa*u=2.220e-13  kappa^2*u=2.220e-10
kappa(A)~1.00e+06: ||Qc^T Qc - I||=5.447e-07  ||Qm^T Qm - I||=8.963e-12  kappa*u=2.220e-10  kappa^2*u=2.220e-04
kappa(A)~1.00e+10: ||Qc^T Qc - I||=1.048e+00  ||Qm^T Qm - I||=4.100e-07  kappa*u=2.220e-06  kappa^2*u=2.220e+04
```
At `kappa(A) ≈ 1e10`, CGS's orthogonality error is `1.048` — meaning `Q^T Q` is no longer even close to the identity, i.e. the computed columns have essentially lost orthogonality entirely, tracking the predicted `kappa^2 * u ≈ 2.22e4` order-of-magnitude blowup (the actual error saturates near 1 because `||Q^T Q - I||` for unit-norm columns is bounded, but the *trend* across the three condition numbers, roughly 1e-12 to 1e-7 to 1.0, is the telltale `kappa^2` scaling). MGS's error at the same condition number is `4.1e-7`, tracking `kappa * u ≈ 2.22e-6` — four to five orders of magnitude better than CGS, and still usably small.

**3. Misconception: "Reorthogonalizing Gram-Schmidt more than twice keeps improving accuracy, so more passes are always safer."**
Correct statement: the "twice is enough" result (informally attributed to Kahan, discussed in Björck's and Golub & Van Loan's treatments) says one reorthogonalization pass after the initial Gram-Schmidt step is sufficient to bring the loss of orthogonality down to the unit-roundoff level `O(u)`, independent of `kappa(A)`, *provided the first pass did not already fail catastrophically (e.g., near-zero pivot)*. A third or later pass buys essentially nothing beyond the second, because the error is already at the roundoff floor; it just doubles the cost for no benefit. The rule is not "reorthogonalize until it looks good"; it is "one reorthogonalization pass, and check the norm reduction at each step to detect a true rank deficiency."

**4. Misconception: "A well-conditioned A guarantees a well-conditioned least-squares solution."**
Correct statement: the sensitivity of the least-squares solution `x*` to perturbations has a term proportional to `kappa(A)` and a second term proportional to `kappa(A)^2 * tan(theta)`, where `theta` is the angle between `b` and the range of `A` — equivalently, this second term is driven by the residual norm `||r|| = ||b - Ax*||`. When the residual is large relative to `||b||` (a poor fit), the effective sensitivity of `x*` can be governed by `kappa(A)^2`, not `kappa(A)`, even though `A` itself and the QR algorithm used to solve for `x*` are both perfectly well-behaved. "Small residual" is doing real numerical work here, not just describing goodness of fit.

**5. Misconception: "Column-pivoted QR always finds the exact numerical rank of a matrix."**
Correct statement: QRCP is a good heuristic that usually produces a sharp drop in the diagonal of `R` at the true numerical rank, and it is much better than unpivoted QR for this purpose, but it is not guaranteed. The Kahan matrix (an upper-triangular matrix with a specific decaying-cosine structure) is a classical counterexample where QRCP fails to reveal a large gap between "large" and "small" singular values. Strong rank-revealing QR (Gu-Eisenstat) fixes this with a bounded worst-case guarantee, at extra cost; the SVD gives you the exact numerical rank (relative to a chosen tolerance) but at higher cost than either QR variant.

**6. Misconception: "Tikhonov regularization and truncated SVD (hard rank cutoff) are basically interchangeable ways to handle ill-conditioning."**
Correct statement: both suppress the influence of small singular values, but Tikhonov's filter factor `sigma_i^2 / (sigma_i^2 + lambda^2)` transitions smoothly from about 1 (for `sigma_i >> lambda`) to about `(sigma_i/lambda)^2` (for `sigma_i << lambda`), while truncated SVD is a hard 0/1 cutoff at a chosen rank. This matters when singular values decay gradually rather than dropping off a cliff: Tikhonov's smooth filter avoids the discontinuous behavior (and sensitivity to the exact cutoff choice) that truncated SVD can exhibit, but requires choosing `lambda` (e.g., via the L-curve or generalized cross-validation) rather than choosing an integer rank.

## Rat-holes

Things that look essential to master fully but are lower-yield than they first appear, given normal engineering or research use of this material.

- **Deriving the exact backward-error bounds for Householder QR from scratch.** The results (Golub & Van Loan, or Higham's *Accuracy and Stability of Numerical Algorithms*) are dense, with constants that are machine epsilon times low-degree polynomials in `m` and `n`. Knowing the *shape* (backward stable, error independent of `kappa(A)`) and citing it suffices for practical work; re-deriving the proof is a multi-day detour unless you do numerical-analysis research.
- **Memorizing the exact Businger-Golub pivoting update formulas for QRCP.** The idea — pick the column of largest remaining norm, update norms cheaply without full recomputation — is what matters. The precise downdate formula (used to avoid `O(mn)` work per pivot) is an implementation detail to look up in LAPACK's `dgeqp3` docs when needed.
- **Trying to hand-derive the strong RRQR bound.** Gu-Eisenstat's algorithm and its worst-case guarantees are genuinely hard (interchange-based, iterative pivoting refinement). Know it as "QRCP but with a proof" and reach for `scipy`/LAPACK rather than reimplementing it.
- **Over-indexing on TSQR's tree-reduction diagrams before you have a real distributed system to run it on.** Its value — `log(P)` communication rounds instead of `O(P)` — only matters at a scale most single-machine work never reaches. Understanding why it avoids communication (pairwise reduction of local `R` factors) is enough; the tree-shape optimality proofs are a rat-hole outside HPC linear algebra work.
- **Chasing "the" formula for the condition number of a rank-deficient least-squares problem.** Once `A` is rank-deficient, "the" solution is a whole affine subspace, and sensitivity analysis must target the minimum-norm solution via the pseudoinverse. Recognize this qualitatively different regime early instead of forcing full-rank sensitivity formulas onto it.

## High-yield study prompts

Use these to test and deepen understanding; each is answerable in a focused sitting and touches a distinct part of the topic stack.

1. Derive the normal equations from `min ||Ax - b||_2^2` by setting the gradient to zero, then show algebraically why `kappa(A^T A) = kappa(A)^2` follows from the singular values of `A^T A` being the squares of the singular values of `A`.
2. Implement Householder QR from scratch (no library QR call) for a random `10x4` matrix, and verify `||Q^T Q - I||` is at machine-precision level regardless of `kappa(A)` — try `kappa(A)` at `1e2`, `1e8`, and `1e14` and confirm the orthogonality error does not grow with `kappa(A)`.
3. Reproduce the CGS-vs-MGS loss-of-orthogonality experiment above at three condition numbers of your own choosing, and check whether your measured `||Q^T Q - I||` values track `kappa(A) * u` (MGS) and `kappa(A)^2 * u` (CGS) to within an order of magnitude.
4. Take a least-squares problem with `kappa(A) = 100` but construct two versions with different residual norms (one where `b` is nearly in the range of `A`, one where it is far from it), perturb `A` and `b` slightly, and measure how much `x*` moves in each case — confirm the large-residual case is far more sensitive.
5. Construct or look up the Kahan matrix and show that unpivoted QR and QRCP both fail to reveal its rank deficiency, while the SVD reveals it clearly; state what "reveals" means precisely (a large ratio between consecutive diagonal/singular values).
6. For an underdetermined system `Ax = b` with `m < n` and full row rank, derive the minimum-norm solution via the QR factorization of `A^T`, and verify numerically that it matches `A^T (A A^T)^{-1} b` and also matches the pseudoinverse solution `pinv(A) @ b`.
7. Implement Tikhonov regularization via the SVD (`x_lambda = sum_i (sigma_i / (sigma_i^2 + lambda^2)) * (u_i^T b) * v_i`) and plot the filter factors `sigma_i^2/(sigma_i^2+lambda^2)` for a few choices of `lambda`, confirming the smooth transition described in misconception 6 above.
8. Explain, in your own words, why MGS applied to `A` is mathematically equivalent to Householder QR applied to the `(m+n) x n` matrix formed by stacking `A` on top of a zero block conceptually replaced by the identity's action — and what this equivalence does and does not guarantee about the numerical quality of the explicit `Q` that MGS returns.
9. Sketch how TSQR would factor a matrix split into 4 row-blocks across 4 workers: what does each worker compute locally, what gets communicated, and how is the final `R` obtained? State exactly what you would need to do differently to obtain the full explicit `Q` afterward rather than just `R`.
10. Given a weighted least-squares problem `min ||W^{1/2}(Ax - b)||_2` with `W` diagonal and highly non-uniform (some weights near 0, some huge), explain what happens to the effective condition number of the weighted problem and why forming `W^{1/2} A` explicitly before doing QR can reintroduce the same danger that motivated avoiding `A^T A` in the first place.
