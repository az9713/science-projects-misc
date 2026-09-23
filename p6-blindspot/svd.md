# Blind-spot pass: The Singular Value Decomposition

## Topic stack

The SVD sits on top of several layers, and gaps low in the stack cause the most confusion higher up.

1. **Linear algebra foundations**: orthogonal/unitary matrices, eigendecomposition of symmetric matrices, the spectral theorem, norms (2-norm, Frobenius norm, operator norm), rank.
2. **Existence and geometry of the SVD**: every real m×n matrix A factors as A = U Σ Vᵀ, with U (m×m) and V (n×n) orthogonal and Σ (m×n) diagonal with nonnegative entries σ₁ ≥ σ₂ ≥ ... ≥ 0. Geometrically, A maps the unit sphere in Rⁿ to an ellipsoid in Rᵍ whose semi-axis lengths are the σᵢ, aligned with the columns of U.
3. **Relation to eigendecomposition**: the σᵢ² are eigenvalues of AᵀA (and of AAᵀ), the vᵢ are eigenvectors of AᵀA, the uᵢ are eigenvectors of AAᵀ. This relation is theoretically correct but numerically dangerous (see misconceptions below).
4. **Low-rank approximation theory**: the Eckart-Young-Mirsky theorem — truncating the SVD to the top k terms gives the best rank-k approximation of A in both the 2-norm and the Frobenius norm.
5. **Generalized inverse**: the Moore-Penrose pseudoinverse A⁺ = V Σ⁺ Uᵀ, used for least-squares problems, especially rank-deficient or ill-conditioned ones.
6. **Numerical rank and thresholds**: in floating point, "rank" is not a yes/no property; it depends on a chosen tolerance applied to the singular value spectrum.
7. **Perturbation theory**: Weyl's inequality bounds how much individual singular values move under a perturbation. Wedin's sin-theta theorem bounds how much singular subspaces (not just values) rotate, and needs a spectral gap.
8. **Algorithms**: Golub-Kahan bidiagonalization, implicit-shift QR on the bidiagonal form, divide-and-conquer (LAPACK's xGESDD), one-sided Jacobi, and their respective cost and accuracy trade-offs.
9. **Applications**: principal component analysis (PCA), total least squares (TLS), and detecting low-rank structure in data.

Each layer depends on the one below it. Someone who knows step 4 (Eckart-Young) but skipped step 3's numerical caveat will confidently form AᵀA "because it's mathematically equivalent" and get garbage for small singular values. That is the single most common blind spot in this topic, and it is demonstrated below with real numbers.

## Unknown unknowns

These are things people who "know the SVD" from a linear algebra course typically do not know they don't know.

- **The SVD of a matrix is not unique** when singular values repeat, or when a σᵢ = 0: the corresponding singular vectors (columns of U, V) can be rotated within their subspace and A = UΣVᵀ still holds. Only the singular *values* are always unique. This matters for reproducibility: two SVD calls (even from the same library on different runs) can return different U, V for degenerate spectra, while Σ stays fixed.
- **Never explicitly form AᵀA to get singular values.** This is covered in depth below because it is the single highest-yield fact in the whole topic.
- **The pseudoinverse of a rank-deficient or nearly rank-deficient matrix amplifies noise.** A⁺ inverts each σᵢ, so 1/σᵢ blows up for small σᵢ. Practitioners often plug A⁺ into a formula (e.g., ordinary least squares) without truncating small singular values first, and get a "solution" dominated by noise.
- **Golub-Kahan bidiagonalization is itself a two-step orthogonal reduction (Householder reflections applied alternately from the left and right)**, and it is the expensive part of a dense SVD; the QR-on-bidiagonal or divide-and-conquer step that follows operates on an n×n (or smaller) bidiagonal matrix and is comparatively cheap. People who only remember "SVD = QR iteration" miss that the bidiagonalization dominates cost for large rectangular matrices.
- **Wedin's sin-theta theorem needs a singular value gap, and the bound is with respect to the smaller of two gaps** (the gap between the k-th and (k+1)-th singular value of the perturbed matrix, or of the original — different formulations use different reference points, and mixing them up silently invalidates a bound someone copies from a paper).
- **One-sided Jacobi SVD is not "the slow method with no upside."** On matrices that are graded (entries spanning many orders of magnitude in a structured way, e.g. weighted least squares design matrices), Jacobi can compute small singular values to full relative accuracy even when the standard bidiagonalization-based algorithms (LAPACK xGESVD/xGESDD) lose that many small singular values to noise near machine epsilon relative to the largest singular value. This is a genuinely different accuracy model (relative vs. absolute/normwise accuracy), not just a speed trade-off. Demmel and Veselić's 1992 analysis is the standard reference.
- **LAPACK's xGESDD (divide-and-conquer) is usually faster than xGESVD (implicit QR) for computing all singular vectors, but can use noticeably more workspace memory**, and for very small matrices or when only singular values are needed, xGESVD or a specialized path can win. "Just use gesdd" is a reasonable default, not a universal one.
- **Total least squares (TLS) uses the *smallest* right singular vector, not the largest.** This is the reverse of what PCA intuition trains people to reach for, and it is easy to grab the wrong end of Σ when adapting PCA code for a TLS problem.
- **The Eckart-Young-Mirsky theorem holds for *unitarily invariant norms in general*, not only the 2-norm and Frobenius norm** — but this session's scope is limited to those two, and even within that scope the *minimizer* is not unique in general (when σ_{k+1} = σ_k, more than one rank-k truncation achieves the minimum), only the minimal *error value* is unique.

## Common misconceptions

Each entry states the false belief, the correct statement, and a concrete numeric check.

### 1. "You can just form AᵀA and eigendecompose it to get the SVD."

**Correct statement:** σᵢ(A) = sqrt(λᵢ(AᵀA)) is true in exact arithmetic, but forming AᵀA squares the condition number and destroys relative accuracy in the small singular values, because floating-point rounding in the matrix product AᵀA is on the order of the machine epsilon times the *largest* entry of AᵀA (≈ σ₁²), not the small ones. Any singular value smaller than about sqrt(machine epsilon) × σ₁ can be corrupted or lost entirely.

**Check (actually run):** built a 6×6 matrix A = Q₁ D Q₂ᵀ with Q₁, Q₂ random orthogonal and D = diag(1, 1e-3, 1e-6, 1e-9, 1e-12, ~1e-15), i.e., singular values spanning 15 orders of magnitude. Computed singular values two ways: (a) `numpy.linalg.svd(A)` directly, and (b) `sqrt(eigvalsh(A.T @ A))`.

```
true singular values (direct SVD): [1.000e+00 1.000e-03 1.000e-06 1.000e-09 1.000e-12 9.587e-16]
via A^T A eigendecomposition:      [1.000e+00 1.000e-03 1.000e-06 4.532e-09 1.170e-09 0.000e+00]
relative error, A^T A route:       [2.220e-16 6.071e-11 4.392e-05 3.532e+00 1.169e+03 1.000e+00]
worst relative error (A^T A route): 1.169e+03  vs. machine epsilon: 2.220e-16
```

The first two singular values survive the AᵀA route to close to machine precision. The third already shows a relative error of about 4.4e-5 — far above machine epsilon. The fourth and fifth are wrong by factors of 3.5 and over 1000 respectively, and the smallest one vanishes to exactly zero. This is not a contrived edge case; any matrix with a wide singular-value spread (common in ill-conditioned least-squares or graded physical measurements) triggers it. LAPACK's SVD routines never form AᵀA internally for this reason — they bidiagonalize A directly.

### 2. "Truncating the SVD at rank k is only optimal in the Frobenius norm; other rank-k approximations can beat it in the spectral (2-) norm."

**Correct statement:** the Eckart-Young-Mirsky theorem says the truncated SVD A_k = Σ_{i=1}^k σᵢ uᵢ vᵢᵀ is the best rank-k approximation of A *simultaneously* in the 2-norm (error = σ_{k+1}) and the Frobenius norm (error = sqrt(Σ_{i>k} σᵢ²)). No other rank-k matrix does better in either norm.

**Check (actually run):** built a random 6×4 matrix A, computed its SVD, and compared the rank-2 truncated SVD against a rank-2 approximation from a *different* orthonormal basis (a random orthogonal projection, representing a "plausible but non-SVD" rank-2 candidate):

```
singular values: [2.5131 1.9507 1.842  1.1038]
SVD rank-2:    Frobenius error = 2.147387   2-norm error = 1.841996
  (theory check: sigma_3 = 1.841996 matches 2-norm error exactly;
   sqrt(sum of sigma_3^2 + sigma_4^2) = 2.147387 matches Frobenius error exactly)
Random-basis rank-2: Frobenius error = 3.251590   2-norm error = 2.388902
SVD error <= random-basis error in both norms? True True
```

The SVD-truncation errors match the closed-form theoretical values exactly (σ₃ for the 2-norm, sqrt(σ₃² + σ₄²) for Frobenius), and both are strictly smaller than the random competitor's errors in both norms — consistent with the theorem, not just in one norm.

### 3. "The pseudoinverse A⁺ is well-behaved as long as A has full rank."

**Correct statement:** full rank guarantees A⁺ exists and the least-squares solution x = A⁺b is unique, but "well-behaved" also requires A to be well-conditioned. As the smallest nonzero singular value σ_min shrinks, A⁺ = VΣ⁺Uᵀ divides by σ_min, so noise in b (or rounding error) is amplified by roughly 1/σ_min. A full-rank matrix with σ_min = 1e-12 has a perfectly well-defined pseudoinverse that is numerically useless for noisy data. The practical fix is truncating or regularizing small singular values before inverting (truncated SVD or Tikhonov regularization), which trades some bias for a large reduction in variance.

### 4. "Numerical rank is a property of the matrix alone."

**Correct statement:** numerical rank is the count of singular values above a chosen threshold, and that threshold is a modeling choice, not something the matrix hands you. A common default is `max(m,n) * eps * σ_max`, but the right threshold depends on the noise level in the data that produced A. The same matrix can have numerical rank 3 under one threshold and rank 5 under a looser one. There is no rank without a stated tolerance.

### 5. "Weyl's inequality and Wedin's sin-theta theorem give you the same kind of guarantee."

**Correct statement:** Weyl's inequality, |σᵢ(A+E) − σᵢ(A)| ≤ ‖E‖₂, bounds how much each singular *value* can move under a perturbation E, and it requires no gap condition — it holds unconditionally for every i. Wedin's sin-theta theorem, by contrast, bounds how much a singular *subspace* (a set of left or right singular vectors) rotates, and it degrades — the bound blows up — as the gap between the relevant singular value and its neighbors shrinks. A matrix can have singular values that move very little under a perturbation (small by Weyl) while its singular vectors rotate wildly, if two singular values are close together (near-degenerate). Conflating "the values are stable" with "the vectors/subspaces are stable" is a common and costly mistake in PCA, where people trust the top principal directions without checking the gap between σ_k and σ_{k+1}.

## Rat-holes

Places that are easy to over-invest in for the level of understanding this topic actually requires:

- **Deriving the full implicit-shift QR algorithm for bidiagonal matrices from scratch**, including the Wilkinson shift strategy and the zero-shift case for graded matrices. This is a specialist numerical-algorithms topic (a chapter of Golub & Van Loan on its own); understanding *what* the bidiagonal QR step does (chases a bulge, converges the trailing singular value) and *why* it's needed after Golub-Kahan bidiagonalization is enough for almost every application.
- **Memorizing the exact flop counts for every SVD variant.** The headline number given for this session — about 4mn² − (4/3)n³ flops for singular values only (m ≥ n), with more for the vectors — is worth keeping as an order-of-magnitude anchor. Re-deriving it operation-by-operation from the Golub-Kahan and QR steps is a multi-hour exercise with little payoff unless you are implementing an SVD routine yourself.
- **Chasing full generality of Wedin's theorem across all its equivalent formulations in different textbooks.** Different sources state it with different norms (2-norm vs. Frobenius) and different gap definitions. Pick one reference (Stewart & Sun's *Matrix Perturbation Theory* is the standard one) and use its version consistently, rather than trying to reconcile every variant you find.
- **Implementing one-sided Jacobi SVD by hand to "really understand" high relative accuracy.** The core insight (it operates via a sequence of 2x2 rotations directly on A, never forming AᵀA, and converges quadratically for well-separated singular values) can be understood and even numerically verified without writing a production-grade implementation with all the pivoting and convergence-acceleration details LAPACK's xGESVJ uses.
- **Debating whether to use the SVD or the eigendecomposition of the covariance matrix for PCA "in general."** For a data matrix that fits comfortably in memory with a moderate number of features, this is often not the actual bottleneck; the accuracy argument in misconception #1 (never form AᵀA, or here, the covariance matrix, for ill-conditioned data) is the one fact worth internalizing, after which the SVD-vs-eigendecomposition choice mostly follows automatically.

## High-yield study prompts

1. Derive, from A = UΣVᵀ, why the columns of V are eigenvectors of AᵀA and the columns of U are eigenvectors of AAᵀ, and identify exactly which step in that derivation is safe in floating point and which is not.
2. Prove the Eckart-Young-Mirsky theorem's Frobenius-norm case for a small (say 3×3) example by direct calculation, then explain in one sentence why "you could probably do better with a non-SVD rank-k choice" is provably false.
3. Write out the definition of A⁺ = VΣ⁺Uᵀ, where Σ⁺ replaces each nonzero σᵢ with 1/σᵢ and leaves zeros as zero, and explain why "replaces each σᵢ with 1/σᵢ" is not equivalent when some σᵢ are only *numerically* nonzero (i.e., tiny but not exactly zero).
4. State Weyl's inequality precisely (with the norm and the direction of the inequality) and construct a 2×2 example where a perturbation E with ‖E‖₂ = 0.01 changes σ₁ by up to 0.01 but rotates the corresponding singular vector by nearly 90 degrees, when σ₁ and σ₂ are nearly equal.
5. Explain, using the two numerical experiments above as your evidence base, why "the SVD is unique" is not quite true, and identify exactly which part of the factorization (singular values vs. singular vectors) the uniqueness claim actually covers.
6. Outline, step by step, how a dense SVD algorithm goes from A to Σ: Golub-Kahan bidiagonalization (A → bidiagonal B), then implicit-shift QR or divide-and-conquer on B → Σ. State which step dominates the flop count for a tall-and-skinny matrix (m ≫ n) and why.
7. Explain why total least squares uses the smallest right singular vector of the augmented data matrix [X | y], not the largest, and contrast this with ordinary PCA's use of the largest singular vectors — what is each method actually minimizing?
8. Given a matrix with singular values [10, 9.9, 0.001], explain what numerical rank you would report at threshold 1e-6 × σ_max versus 0.5 × σ_max, and why the gap between σ₁ and σ₂ (not their absolute size) matters for how much you should trust the top-2 subspace via Wedin's theorem.
9. State the LAPACK routine names for the implicit-QR SVD path (xGESVD) and the divide-and-conquer path (xGESDD), and describe one concrete situation where you would deliberately choose xGESVD over the usually-faster xGESDD.
10. Describe, in your own words, why one-sided Jacobi SVD can achieve high relative accuracy on a graded matrix where bidiagonalization-based methods cannot, tying your answer back to the AᵀA experiment above.

---

*Method note: this pass ran two small numpy experiments (Eckart-Young-Mirsky check against a random competitor rank-2 approximation, and a graded-matrix AᵀA-vs-direct-SVD relative accuracy comparison) with real printed output, both reproduced verbatim above.*
