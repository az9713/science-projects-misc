# Blind-Spot Pass: Matrix Functions and Matrix Equations

## Topic stack

1. **What f(A) means.** Three equivalent definitions: (a) Jordan form, A = X J X^{-1}, f(A) = X f(J) X^{-1}, with f(J) built block-by-block from f and its derivatives at each block's eigenvalue; (b) the Cauchy integral, f(A) = (1/2*pi*i) * contour_integral( f(z)(zI-A)^{-1} dz ); (c) Hermite interpolation, f(A) = p(A) for the unique polynomial p (degree bounded by the total Jordan structure) matching f and its derivatives at each eigenvalue. Jordan explains why defective A needs derivatives of f; Cauchy underlies contour-based algorithms and perturbation theory; Hermite interpolation explains why f(A) is always a bounded-degree polynomial in A, even for transcendental f.
2. **Conditioning via the Fréchet derivative.** L_f(A,E), defined by f(A+E) - f(A) - L_f(A,E) = o(||E||), is the matrix-function analogue of a Jacobian; its operator norm gives the condition number of evaluating f(A). This, not eigenvalue conditioning of A alone, is the right tool for asking whether a computed f(A) is trustworthy.
3. **The matrix exponential.** expm(A) by scaling-and-squaring with a Padé approximant: scale A by 2^-s so ||A/2^s|| is small, apply a diagonal Padé approximant there, then square s times, using exp(A) = exp(A/2^s)^{2^s}. This is the algorithm behind MATLAB's and SciPy's `expm`. Moler and Van Loan's "Nineteen Dubious Ways to Compute the Exponential of a Matrix" (1978, revisited 2003) rates roughly nineteen candidate methods (Taylor series, eigendecomposition, ODE integration, Padé, contour integrals, ...) and explains why most fail in some regime.
4. **Schur-Parlett** is the general-purpose algorithm for arbitrary f: Schur-factor A = QTQ*, reorder/block T so eigenvalues within a block are close, evaluate f directly on each small clustered block, then reconstruct via the block Parlett recurrence (a matrix generalization of divided differences). It never forms an eigenvector matrix, which is exactly what avoids the trap demonstrated numerically below.
5. **Named special functions.** sqrtm(A) (principal square root, positive-real-part branch), logm(A) (principal branch, needs no eigenvalue on the negative real axis), sign(A) (eigenvalues map to +-1 by sign of real part). Each has a Newton-type iteration: sqrtm's naive Newton form is numerically unstable and is replaced by the coupled/product (Denman-Beavers) form; sign(A)'s iteration X_{k+1} = (X_k + X_k^{-1})/2 converges quadratically once close, but needs scaling (e.g., determinantal scaling) far from convergence.
6. **Polar decomposition.** A = UH, U unitary, H Hermitian positive semidefinite, computed via A(A*A)^{-1/2} or, more robustly, via the same Newton-iteration family as sign(A) — tying polar decomposition, sign(A), and sqrtm's Newton iterations into one algorithm family.
7. **f(A)b via Krylov methods.** For large sparse A, forming dense f(A) is infeasible: project onto K_m(A,b) via Arnoldi, get the small Hessenberg H_m, and approximate f(A)b ~ ||b|| V_m f(H_m) e_1. Rational Krylov subspaces (using (A-sigma*I)^{-1} b instead of powers of A) converge far faster for a well-chosen shift sigma, at the cost of one sparse solve per step.
8. **Exponential integrators** (exponential Euler, exponential time differencing, EXPOKIT-style Krylov methods) use expm(A)b or phi-functions (phi_1(z) = (exp(z)-1)/z, etc.) to integrate the stiff linear part of y' = Ay + g(y) exactly.
9. **Algebraic Riccati equation (ARE).** A^T X + X A - X B R^{-1} B^T X + Q = 0, central to LQR control and Kalman filtering; solved via the Hamiltonian matrix's stable invariant subspace or Newton's method on the ARE, where each Newton step solves a Lyapunov equation.
10. **Applications.** Network centrality (Katz, subgraph, communicability all reduce to entries/traces of exp(beta*Adjacency) or (I-alpha*Adjacency)^{-1}); linear ODEs (y(t) = exp(At)y(0)); control theory (the ARE, sign(A) methods for stable/unstable subspace separation).

## Unknown unknowns

- **f(A) is always a bounded-degree polynomial in A**, even for f = exp or log. For an n x n matrix needing d Hermite-matching conditions, f(A) = p(A) for a specific polynomial p of degree at most d-1. Easy to miss from the Cauchy-integral or eigendecomposition views alone.
- **Eigendecomposition is the classic wrong tool for f(A), even for exactly diagonalizable A.** Diagonalizability guarantees the formula V f(D) V^{-1} is exact only in infinite precision. Its numerical accuracy depends on cond(V), which can be huge for A close to defective, even though every eigenvalue stays simple. Verified below.
- **A "safe-looking" Taylor truncation for exp(A) is not automatically safe.** The number of terms needed for machine precision grows with ||A||; truncating at a small fixed count without first scaling A is one of Moler-Van Loan's dubious ways. Verified below.
- **Scaling-and-squaring is not just "square the Taylor sum at the end."** Halving A repeatedly forces the Padé approximant to work only near the origin, where it is most accurate; squaring then exactly recovers exp(A). That is why it needs far fewer terms than a global approximation of exp on the original, possibly large-norm A.
- **The sign-function Newton iteration can lose accuracy or stall far from convergence**, despite quadratic convergence near the fixed point; production code uses scaling (e.g., determinantal scaling c_k = |det(X_k)|^{-1/n}) to shorten the pre-asymptotic phase.
- **Krylov convergence for f(A)b depends heavily on f.** Entire functions like exp converge fast because low-degree polynomials approximate them well over A's field of values; a resolvent (A-sigma*I)^{-1} with sigma near an eigenvalue converges slowly under plain polynomial Krylov, since no low-degree polynomial approximates a nearby pole — exactly the gap rational Krylov closes.
- **The ARE is not a generic nonlinear equation.** Its quadratic term X B R^{-1} B^T X makes Newton's method the natural solver, and each Newton step reduces to a Lyapunov equation, so ARE-solving reuses Lyapunov-equation machinery rather than starting from scratch.
- **"exp of the adjacency matrix" centrality scores are a Katz-family construction, not a physical simulation.** beta in exp(beta*Adjacency) must be below 1/(largest eigenvalue of Adjacency) for the walk-counting series to converge with its intended meaning; too-large beta produces overflow or a result dominated purely by the top eigenvector.

## Common misconceptions

**1. "If A is diagonalizable, computing f(A) = V f(D) V^{-1} is a numerically fine way to evaluate any matrix function."**
Correct statement: diagonalizability guarantees only exactness in infinite precision. Numerical accuracy is controlled by cond(V) = ||V|| * ||V^{-1}||, which can be enormous for A close to a defective matrix even though every eigenvalue is simple. This is exactly why Schur-Parlett, which needs only a numerically stable unitary Schur factorization and never an eigenvector matrix, is the recommended general-purpose algorithm.
Check performed (NumPy, double precision): A = V D V^{-1} with D = diag(1.0, 1.2, 1.4, 1.6, 1.8) and V built so two columns are forced closer to parallel by a parameter eps, pushing A toward defective without ever making it exactly so. Computed exp(A) via V exp(D) V^{-1} and via `scipy.linalg.expm` (reference):
```
eps=1e-01  cond(V)=3.2773e+02  rel_err_eigendecomp_vs_expm=2.840484e-15
eps=1e-02  cond(V)=3.6333e+03  rel_err_eigendecomp_vs_expm=9.861398e-13
eps=1e-03  cond(V)=3.6708e+04  rel_err_eigendecomp_vs_expm=1.616540e-09
eps=1e-04  cond(V)=3.6746e+05  rel_err_eigendecomp_vs_expm=3.137074e-07
eps=1e-06  cond(V)=3.6519e+07  rel_err_eigendecomp_vs_expm=3.542667e+00
eps=1e-08  cond(V)=1.6348e+08  rel_err_eigendecomp_vs_expm=1.000000e+00
```
As cond(V) rises from 3.3e2 to 1.6e8, relative error rises from machine precision (2.8e-15) to an O(1) error (worse than useless at eps=1e-8; off by more than 3.5x in relative norm at eps=1e-6). A stayed diagonalizable at every eps — only the eigenvector conditioning degraded.

**2. "A Taylor series for exp(A) is fine with 20 or 30 terms — that's surely plenty."**
Correct statement: the term count needed scales with ||A||; a fixed "generous" count can be far too few once ||A|| is not small. This is exactly why scaling-and-squaring shrinks ||A|| first rather than adding more raw terms.
Check performed: a random 6x6 A with ||A||_2 = 14.2201, naive truncated Taylor sum vs. `scipy.linalg.expm`:
```
||A||_2 = 14.2201
terms=  5  rel_err_vs_expm = 9.663876e-01
terms= 10  rel_err_vs_expm = 5.544843e-01
terms= 20  rel_err_vs_expm = 5.187035e-03
terms= 30  rel_err_vs_expm = 7.156804e-07
terms= 60  rel_err_vs_expm = 1.201834e-13
```
At 20 terms the result is still off by half a percent; at 5-10 terms it has barely started converging. Only 60 terms reach machine precision. A larger ||A|| would push these counts higher still — precisely the failure mode Moler-Van Loan catalog.

**3. "Newton's method for sign(A) or sqrtm converges quadratically, so it's always fast and safe."**
Correct statement: quadratic convergence is asymptotic, guaranteed only once the iterate is already close to the fixed point. Far from convergence, the plain sign(A) iteration (X_{k+1} = (X_k + X_k^{-1})/2) or the naive (non-coupled) sqrtm iteration can converge slowly, lose accuracy from ill-conditioned inversions, or become unstable — which is why sqrtm uses the coupled Denman-Beavers form and sign(A) uses scaling (e.g., determinantal scaling) to shorten the pre-asymptotic phase.
Check to run (needs a deliberately ill-scaled matrix, not executed here): take A with eigenvalue real parts spanning 1e-3 to 1e3, run unscaled Newton for sign(A) a fixed number of steps, compare residual decay against the same iteration with determinantal scaling; confirm the unscaled version needs visibly more iterations, especially early on.

**4. "logm and sqrtm are single-valued the way scalar log and sqrt are, once you pick a branch."**
Correct statement: even on the principal branch (no eigenvalue on the negative real axis for logm, right half-plane for sqrtm), the function's condition number (the Fréchet derivative's norm) grows large near the branch cut, so two numerically close matrices can have principal logs or square roots differing far more than the input difference suggests — even though each individual value is well defined.
Check to run (needs an eigenvalue swept across the branch cut, not executed here): build matrices with one eigenvalue moving from angle 170 to 190 degrees around the origin, compute logm at each point, and observe ||logm(A)|| jump discontinuously as the eigenvalue crosses the negative real axis while A itself changes only slightly.

**5. "Krylov subspaces converge at the same rate for f(A)b regardless of which f is used."**
Correct statement: convergence depends on how well low-degree polynomials approximate f over A's field of values. An entire function like exp typically converges fast; a resolvent (A-sigma*I)^{-1} with sigma near an eigenvalue converges slowly under plain polynomial Krylov, since no low-degree polynomial approximates a nearby pole well — which is why rational Krylov subspaces (built-in shift-and-invert) are used instead of just enlarging the polynomial subspace.
Check to run (needs a sparse test matrix and comparison harness, not executed here): place a shift sigma close to one eigenvalue of a sparse A, approximate (A-sigma*I)^{-1}b via plain Arnoldi at increasing dimension m and via a rational Krylov subspace with one good shift; compare the m each needs to reach a fixed residual tolerance.

## Rat-holes (interesting but low-yield for a first pass)

- Deriving the full block Parlett recurrence by hand — know it exists and generalizes scalar divided differences; do not re-derive its combinatorics before using it.
- Chasing all nineteen Moler-Van Loan methods equally — a handful (unscaled Taylor, eigendecomposition, unscaled Padé, ODE integration) cover the recurring failure modes; the rest are variations on the same lessons.
- Proving optimal shift-selection theory for rational Krylov before building intuition with one well-chosen shift on a small example.
- Deriving the Hamiltonian-matrix invariant-subspace approach to the ARE from scratch before first solving a small ARE by Newton's method and checking the residual.
- Substituting general eigenvalue perturbation theory (Bauer-Fike) for the Fréchet derivative condition number — related, but they answer different questions.

## High-yield study prompts

1. State the Hermite-interpolation definition of f(A) for a Jordan block of size k, and use it to explain why f(A) is always a bounded-degree polynomial in A even when f = exp.
2. Using L_f(A,E), explain what it means for evaluating f(A) to be ill-conditioned, and contrast this with A's own eigenvalue conditioning.
3. Reproduce the eigendecomposition-vs-expm experiment at one eps between 1e-4 and 1e-6, find where relative error crosses 1e-2, and relate that threshold to cond(V) and machine epsilon (~2.2e-16).
4. Explain why scaling-and-squaring needs far fewer terms than a direct large-norm Taylor sum, using exp(A) = exp(A/2^s)^{2^s}.
5. Describe Schur-Parlett's three stages and explain why it avoids ever forming an eigenvector matrix.
6. Contrast the naive sign(A) Newton iteration with a determinantally scaled variant, and state where scaling matters most.
7. Explain how sign(A), the polar decomposition, and sqrtm connect through related Newton fixed-point iterations, and state the polar decomposition's defining property A = UH.
8. Explain why forming f(A) explicitly is infeasible for large sparse A, and describe f(A)b ~ ||b|| V_m f(H_m) e_1 in terms of the Arnoldi factorization AV_m = V_m H_m + h_{m+1,m} v_{m+1} e_m^T.
9. State why a near-spectrum resolvent converges slowly under plain polynomial Krylov and what a rational Krylov subspace changes.
10. Write the continuous-time ARE, name the term that makes it nonlinear, and explain why one Newton step reduces to a Lyapunov equation.

## Notes on the two numerical checks

Both were run in NumPy/SciPy (double precision; `numpy` 2.2.6, `scipy` 1.16.0) as small self-contained scripts, with real output reproduced verbatim above: (1) a naive truncated Taylor series for exp(A) on a random 6x6 matrix, ||A||_2 = 14.2201, at term counts 5, 10, 20, 30, 60 against `scipy.linalg.expm`; (2) the eigendecomposition formula V exp(D) V^{-1} on A = V D V^{-1} with fixed eigenvalues diag(1.0, 1.2, 1.4, 1.6, 1.8) and V engineered toward singularity (two columns forced closer to parallel) as eps shrinks from 1e-1 to 1e-8, against `scipy.linalg.expm`, with cond(V) measured at each eps via `np.linalg.cond`.
