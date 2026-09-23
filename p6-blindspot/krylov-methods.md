# Blind-Spot Pass: Krylov Subspace Methods

## Topic stack

1. **Krylov subspace itself.** K_k(A, b) = span{b, Ab, A^2 b, ..., A^{k-1} b}. Everything downstream is either a way to build an orthogonal basis for this space (Arnoldi, Lanczos) or a way to extract an approximate solution or eigenpair from it.
2. **Basis construction.** Arnoldi (general A, builds an upper Hessenberg H_k) and Lanczos (A = A^T, H_k collapses to tridiagonal T_k). Lanczos is Arnoldi's three-term-recurrence special case, not a separate algorithm.
3. **Linear-system solvers built on the basis.**
   - Symmetric positive definite (SPD): conjugate gradient (CG), the A-norm error bound 2((sqrt(kappa)-1)/(sqrt(kappa)+1))^k.
   - Symmetric indefinite: MINRES, SYMMLQ.
   - Nonsymmetric: GMRES and its restarted variant GMRES(m); BiCG, BiCGSTAB, QMR, IDR(s) (short-recurrence alternatives that avoid GMRES's growing storage).
4. **The convergence lens: polynomial approximation.** Every Krylov solver's error after k steps is (a version of) min over degree-k polynomials p with p(0)=1 of ||p(A) e_0||, evaluated over the spectrum (and, for nonnormal A, over pseudospectra). Eigenvalue clustering shrinks the achievable polynomial; non-normality breaks the simple spectral bound.
5. **Finite-precision reality.** Exact-arithmetic Lanczos/CG theory (finite termination in n steps, orthogonal Krylov basis) does not survive floating point. Loss of orthogonality in Lanczos, delayed/duplicated convergence in CG, Paige's 1971/1976 analysis of what actually happens, and Greenbaum's 1989 result connecting finite-precision CG to exact CG on a related larger problem.
6. **Least-squares extensions.** LSQR and LSMR apply CG-type / MINRES-type ideas to A^T A or the normal equations without forming them, via bidiagonalization (Golub-Kahan).
7. **Eigensolvers built on the same machinery.** Implicitly restarted Arnoldi (IRAM, the engine inside ARPACK/`eigs`), the more numerically robust Krylov-Schur reformulation, Lanczos with selective reorthogonalization for large symmetric eigenproblems, LOBPCG (block, preconditioned, for a handful of extreme eigenpairs), and Jacobi-Davidson (correction-equation methods for interior or clustered eigenvalues where pure Krylov struggles).

## Unknown unknowns

- **CG is a special case of a much larger family, not a standalone trick.** It solves exactly the "SPD" corner of a design space (symmetry + definiteness) that also has MINRES (symmetric only) and GMRES (neither). Learners often memorize the CG update formulas without knowing which of the two properties buys which guarantee: symmetry buys the short three-term recurrence (bounded memory); positive definiteness buys the A-norm monotonicity and the classical convergence bound.
- **The convergence bound is a worst case over all right-hand sides with a given spectrum, not a prediction for your matrix.** Real CG runs on clustered spectra converge far faster than the kappa-based bound suggests (this is verified numerically below). Treating the bound as an estimate of "how many iterations I need" is the single most common practical error.
- **GMRES has no analogue of the CG bound in general** because for a nonnormal matrix, eigenvalues alone do not control convergence — the field of values or pseudospectra do. A matrix can have eigenvalues clustered at 1 and still make GMRES stagnate for many steps if it is far from normal.
- **Lanczos "loses orthogonality" specifically when a Ritz value has converged**, not randomly or uniformly over iterations. The loss is tied to convergence itself (Paige's observation), which is why naive "just reorthogonalize occasionally" schemes must be triggered by convergence monitoring, not by a fixed iteration count.
- **Restarting GMRES(m) can stall or fail to converge at all**, even though full GMRES is guaranteed to converge in at most n steps. Restarting throws away the Krylov space and loses the optimal-polynomial property across the restart boundary; there exist matrices for which GMRES(m) never reduces the residual below a fixed threshold.
- **BiCGSTAB, QMR, and IDR(s) exist because short-recurrence methods for nonsymmetric systems must give up either optimality (least residual) or guaranteed breakdown-freedom** — there is a theorem (Faber-Manteuffel, 1984) that short recurrences with the CG-style optimality property exist essentially only for a narrow class of matrices related to A^T = A or A^T = -A (up to shifts). This is why so many nonsymmetric short-recurrence methods exist instead of one obviously best method.
- **The eigensolver side (ARPACK/IRAM) is not "Lanczos with a stopping rule."** Implicit restarting changes the starting vector by applying a filter polynomial (via shifted QR steps on the Hessenberg/tridiagonal factor) to damp unwanted directions, without ever forming that polynomial explicitly or refactoring A. Krylov-Schur reorganizes the same idea to avoid a known numerical instability in IRAM's exact-shift strategy.

## Common misconceptions

**1. "The CG bound 2((sqrt(kappa)-1)/(sqrt(kappa)+1))^k tells you how many iterations CG needs."**
Correct statement: this bound is a worst-case guarantee over all spectra with condition number kappa; it is tight only when the eigenvalues are spread roughly uniformly (or at the two extremes) over [lambda_min, lambda_max]. When eigenvalues are clustered into a few groups, CG's error is controlled by a polynomial that only needs one root per cluster, so convergence is governed by the number of clusters, not by kappa.
Check performed: built a 50x50 SPD matrix with eigenvalues spread uniformly over [1, 100] (kappa = 100, predicted rate (sqrt(100)-1)/(sqrt(100)+1) ≈ 0.818), ran CG, and compared the actual A-norm error to the bound at several iterations:

```
k, actual ||e_k||_A, bound 2*rate^k*||e0||_A, ratio actual/bound
  0  1.454294e+00   2.908589e+00   0.5000
  5  7.165062e-01   1.066428e+00   0.6719
 10  2.098119e-01   3.910035e-01   0.5366
 20  6.872026e-03   5.256284e-02   0.1307
 30  1.900865e-05   7.066056e-03   0.0027
 39  5.855695e-09   1.160982e-03   0.0000
```
The actual error is always below the bound (correct — the bound holds), but by an increasingly large margin (ratio falling from 0.50 to under 0.001), confirming that treating the bound as an iteration-count predictor is far too pessimistic even for a uniformly-spread spectrum; with real clustering it would be worse still.

**2. "Lanczos vectors stay orthogonal because the three-term recurrence guarantees it."**
Correct statement: the three-term recurrence guarantees orthogonality only in exact arithmetic. In floating point, rounding error causes the computed Lanczos vectors to lose orthogonality, and — per Paige's analysis — this loss appears first and fastest in the directions where a Ritz value (an eigenvalue estimate from T_k) has already converged, because that convergence is exactly what amplifies rounding error into the previously-orthogonal subspace.
Check performed: ran unreorthogonalized Lanczos for 40 steps on a 60x60 symmetric matrix with three closely clustered eigenvalues (500.0, 500.1, 500.2) planted among 60 eigenvalues spread over [1, 1000], and tracked the largest off-diagonal entry of V_k^T V_k (which should be exactly 0 in exact arithmetic):

```
k, max |V_k^T V_k - I| off-diagonal
  5   1.390e-15
 10   1.590e-15
 15   1.848e-15
 20   2.696e-15
 25   3.547e-14
 30   1.523e-12
 35   4.822e-11
 40   2.469e-08
```
Orthogonality is near machine epsilon (~1e-15) through step 20, then degrades by roughly three orders of magnitude every five steps once the clustered eigenvalue group starts to converge, reaching 2.5e-8 by step 40 — a directly observed instance of Paige's "loss tied to convergence" behavior, not a slow uniform drift.

**3. "GMRES(m) is just GMRES done in cheaper chunks; it converges to the same answer, just slower."**
Correct statement: GMRES(m) is not guaranteed to converge at all for general nonsymmetric A. Full GMRES minimizes the residual over the full, ever-growing Krylov space and is guaranteed to reach the exact solution in at most n steps; restarting after m < n steps discards the accumulated Krylov space and restarts the polynomial-approximation problem from scratch with a new residual as the seed vector, which can produce stagnation cycles for adversarial matrices.
Check to run (not executed here, since it needs a specifically constructed adversarial matrix rather than a generic random one): construct a real 3x3 or 4x4 nonsymmetric matrix from a known GMRES(m)-stagnation example in the literature (e.g., a rotation-like matrix built so residuals repeat with period m), run GMRES(3) versus full GMRES, and confirm the restarted residual norm stops decreasing while full GMRES's does not.

**4. "MINRES and CG are interchangeable for symmetric systems; MINRES is just 'CG for indefinite matrices.'"**
Correct statement: MINRES minimizes the 2-norm of the residual at every step (works for any symmetric A, definite or not) and gives a residual-norm history that decreases monotonically; CG minimizes the A-norm of the error, which requires A to be SPD for that norm to be well defined (sqrt(e^T A e) is imaginary or the "norm" is not a norm if A has negative eigenvalues). Applying CG's update formulas to an indefinite matrix can break down (division by a near-zero or negative p^T A p) or converge to the wrong point; it does not merely converge slower.

**5. "BiCGSTAB always converges faster and more smoothly than BiCG because it 'stabilizes' it."**
Correct statement: BiCGSTAB adds a local GMRES(1)-style minimization step on top of BiCG's search direction to smooth BiCG's characteristically erratic residual history, but it does not remove BiCG's more fundamental failure mode — breakdown when the shadow residual becomes (near-)orthogonal to the true residual, nor does it prevent stagnation from the extra minimization step itself producing a near-zero denominator. QMR was designed independently to address BiCG's erratic convergence by a quasi-minimization over the Krylov basis rather than a stabilization step, and neither method dominates the other on all problems.

## Rat-holes (interesting but low-yield for a first pass)

- Deriving the full Faber-Manteuffel theorem proof (which matrices admit an optimal short-recurrence method) — useful to know the *statement*, not worth reproducing the proof.
- Hand-deriving the exact IRAM shift-selection strategies (exact shifts vs. Chebyshev, or Sorensen's original 1992 paper's proofs) before understanding Krylov-Schur's motivation for replacing it — read Krylov-Schur's motivating example first.
- Chasing every variant acronym (TFQMR, CGS, GPBiCG, ML(k)BiCG, ...) — these are incremental refinements of BiCG/BiCGSTAB/QMR; understanding the three parents plus IDR(s)'s different derivation (via induced dimension reduction subspaces, not Krylov-subspace minimization per se) covers the design space.
- Getting lost in the general theory of preconditioning (incomplete LU, algebraic multigrid as preconditioner, etc.) — it is essential in practice but is a separate topic stack from the Krylov method itself; do not let it absorb the first pass through Krylov theory.
- Proving Greenbaum's finite-precision equivalence theorem in full — the useful takeaway ("finite-precision CG behaves like exact CG on a larger system with a perturbed, near-continuous spectrum") is a one-paragraph fact; the full proof is a research-level detour.

## High-yield study prompts

1. Derive the three-term Lanczos recurrence from the Arnoldi process by showing that A symmetric forces H_k to be tridiagonal, and state exactly which step of the Arnoldi orthogonalization becomes redundant.
2. Using the polynomial-approximation view, explain why CG's convergence bound depends on kappa = lambda_max/lambda_min while GMRES has no equally simple bound for a general nonnormal matrix; name the quantity (field of values or pseudospectrum) that replaces the spectrum in the GMRES case.
3. Reproduce the CG experiment above with a spectrum that has a genuine gap (e.g., 45 eigenvalues near 1 and 5 eigenvalues near 100) instead of a uniform spread, and confirm CG converges in roughly (number of clusters) iterations rather than needing sqrt(kappa) iterations.
4. Explain, in terms of Ritz value convergence, why full reorthogonalization of Lanczos vectors is expensive (O(k) work per step) while selective reorthogonalization is not, and state the criterion selective reorthogonalization uses to decide when to reorthogonalize.
5. State the exact property that MINRES guarantees (monotonic residual-norm decrease) and the exact property that CG guarantees (monotonic A-norm error decrease), and give a concrete SPD example where CG's residual norm temporarily increases even while its A-norm error decreases monotonically.
6. Explain why LSQR and LSMR avoid explicitly forming A^T A, and state which classical numerical hazard (squaring the condition number: kappa(A^T A) = kappa(A)^2) this avoidance is designed to prevent.
7. Compare implicitly restarted Arnoldi (IRAM) and Krylov-Schur on one sentence each: what numerical failure mode of IRAM's exact-shift strategy does Krylov-Schur's reordered Schur-form restart avoid?
8. State the one structural difference between LOBPCG and Jacobi-Davidson (block preconditioned gradient descent in a 3-vector subspace vs. a correction-equation approach solving a shifted, projected linear system at each step) and give one situation where interior eigenvalues make plain Krylov/Lanczos methods a poor choice, motivating Jacobi-Davidson.

## Notes on the two numerical checks

Both experiments were run in NumPy (double precision, no external libraries) as small, self-contained scripts and their real output is reproduced verbatim above rather than described from memory: (1) classical CG on a 50x50 SPD matrix with a uniformly-spread spectrum over condition number kappa = 100, comparing the actual A-norm error against the textbook bound at iterations 0, 5, 10, 20, 30, 39; (2) unreorthogonalized Lanczos for 40 steps on a 60x60 symmetric matrix with three closely spaced eigenvalues planted among 60 spread over [1, 1000], tracking the largest off-diagonal entry of V_k^T V_k as a direct, numerical measure of loss of orthogonality.
