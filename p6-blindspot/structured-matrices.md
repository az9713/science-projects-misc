# Blind-spot pass: Structured and data-sparse matrices

## Topic stack

Structured-matrix numerical linear algebra sits on general dense/sparse solvers but replaces "store and factor everything" with "exploit the pattern that generates the entries." Each layer below assumes the one before it.

1. **Explicit-structure classes**: banded (nonzero only near the diagonal), Toeplitz (constant along diagonals, T[i,j] = t[i-j]), Hankel (constant along anti-diagonals, H[i,j] = h[i+j]), circulant (Toeplitz with wraparound, C[i,j] = c[(j-i) mod n]), Cauchy (C[i,j] = 1/(x_i - y_j)), and Vandermonde (V[i,j] = x_i^j). Each stores O(n) or O(n²) generators instead of the full O(n²) or O(n³) matrix.
2. **Displacement rank**: the unifying idea (Kailath, Kung, Morf, 1979) that Toeplitz, Hankel, Cauchy, and Vandermonde matrices are all "close to" a shift-invariant operator: for ∇(M) = A M - M B with suitable shift matrices A, B, the rank of ∇(M) is small (often 1 or 2) even though M itself is full rank. This displacement rank, not the matrix's literal shape, is what fast algorithms exploit, and it is why Cauchy and Vandermonde belong in the same chapter as Toeplitz even though they look nothing alike.
3. **FFT diagonalization of circulant matrices**: every circulant matrix C is diagonalized by the DFT matrix F: C = F⁻¹ diag(Fc) F, c the first column. This gives an O(n log n) matrix-vector product and solve, and is the engine under most fast Toeplitz methods (a Toeplitz matrix embeds inside a larger circulant matrix).
4. **Toeplitz solvers**: Levinson-Durbin, O(n²), extends the problem size by one at each step, reusing the previous step's reflection coefficients. Superfast solvers, O(n log² n), use displacement rank plus FFT-based polynomial multiplication. Both are less numerically stable than a generic O(n³) solve, in different ways (see misconceptions below).
5. **Kronecker products and matrix equations**: A ⊗ B applies B on one axis and A on another; vec(AXB) = (Bᵀ ⊗ A) vec(X) turns the Sylvester equation AX + XB = C and the Lyapunov special case AX + XAᵀ = C into a Kronecker-structured linear system. Bartels-Stewart avoids forming the O(n²)×O(n²) Kronecker system by reducing A and B to real Schur form, then back-substituting in O(n³), instead of the naive O(n⁶).
6. **Semiseparable and quasiseparable matrices**: matrices whose off-diagonal blocks are all low rank, generalizing "banded" to "low-rank away from the diagonal." These arise as inverses of banded matrices and support O(n) or O(n log n) solves via generator representations.
7. **Hierarchical low-rank formats**: H-matrices and H²-matrices (Hackbusch) partition a matrix into a tree of blocks; admissible (far-field) blocks compress to low rank, near-field blocks stay dense or recurse. HSS and HODLR are simpler special cases used in fast direct solvers, giving near-linear matrix-vector products (and, for some formats, near-linear direct solves). These are the standard tool for dense matrices from integral equations (boundary element methods), and are the algebraic counterpart of the fast multipole method (FMM), which reaches the same near-linear complexity via physical multipole expansions instead of purely algebraic compression.
8. **Low-rank tensor formats**: Tucker (a core tensor contracted with a factor matrix per mode) and tensor train / matrix product states (a chain of 3-way core tensors) extend low-rank ideas from matrices to higher-order arrays, trading exponential-in-order storage for storage linear in order (given bounded rank).

The load-bearing connection is step 2: displacement rank is why "one theory" covers Toeplitz, Hankel, Cauchy, and Vandermonde, and it is the layer most courses skip in favor of teaching each class as an unrelated special case.

## Unknown unknowns

- **A Toeplitz matrix is not automatically well-conditioned just because it looks "smooth."** Some (e.g., ones from a moment problem or a badly spaced Cauchy-like kernel) are exponentially ill-conditioned in n; fast means fewer operations, not more accuracy.
- **The O(n log n) circulant solve requires the matrix to be circulant, not merely Toeplitz.** A Toeplitz solve via FFT works by *embedding* the matrix in a larger circulant matrix (typically size 2n or the next highly composite size ≥ 2n-1); getting the embedding size or zero-padding wrong silently corrupts the result.
- **Levinson-Durbin can divide by a near-zero pivot even when the full Toeplitz matrix is well-conditioned**, because it implicitly requires every *leading principal submatrix* to be nonsingular, not just the full matrix. A well-conditioned matrix with an ill-conditioned leading minor breaks the recursion partway through — a generic LU-with-pivoting solve handles this by pivoting, but Levinson-Durbin structurally cannot pivot without losing its O(n²) speed.
- **Superfast O(n log² n) Toeplitz solvers are considerably less numerically robust than the already-fragile O(n²) Levinson-Durbin**, and many "fast Toeplitz solver" libraries quietly fall back to a slower, stable method (or refuse ill-conditioned input); treat "superfast" as research-grade unless the library documents a stabilized variant.
- **The Sylvester equation AX + XB = C does not always have a unique solution**, and Bartels-Stewart's Schur-form reduction only works cleanly when A and B share no eigenvalues (λᵢ(A) + λⱼ(B) ≠ 0 for all i, j); near-shared eigenvalues ill-condition the equation even when a unique solution exists, independent of A's or B's own conditioning.
- **"Semiseparable" is not one standard definition across papers.** Some mean off-diagonal blocks of rank exactly bounded by r; others mean a specific generator recursion (Givens-vector, quasiseparable generators); these are not always equivalent, and code ported between conventions can silently assume the wrong format.
- **H-matrices, H²-matrices, HSS, and HODLR are not "the same idea, different name."** HODLR uses one non-nested low-rank basis per level; HSS and H² use *nested* bases (a child's basis is expressed via its parent's), which is what gives H²/HSS a true O(n) matrix-vector product instead of HODLR's O(n log n); a "linear time" claim true for HSS is not automatically true for HODLR.
- **FMM and hierarchical matrix compression are two independent derivations reaching the same near-linear complexity** for the same physical problems (N-body potentials, boundary integral equations) — one via multipole/local expansions of the kernel, one via algebraic low-rank compression of well-separated blocks. They generally do not give numerically identical answers, since their compression errors come from different sources.
- **Tensor train and Tucker are not just "matrix low-rank generalized in the obvious way."** CP rank (canonical polyadic), the most direct analogue of matrix rank, is NP-hard to compute and its best-rank-r approximation problem can fail to have a minimizer at all; Tucker and tensor train sidestep this with rank *tuples* on unfoldings/bonds rather than a single CP rank, which is why they are preferred in practice despite CP looking like the more natural analogy to SVD.

## Common misconceptions

### 1. "A circulant matrix's eigenvalues have to be computed with a general eigenvalue solver; FFT is only for speeding up matrix-vector products."

**Correct statement:** the eigenvalues of an n×n circulant matrix C (first column c) are exactly the discrete Fourier transform of c, and the eigenvectors are exactly the columns of the (fixed, matrix-independent) DFT matrix. No numerical eigenvalue iteration is needed at all — the eigendecomposition is known in closed form for every circulant matrix, and computing it costs one O(n log n) FFT rather than the O(n³) of a general eigensolver.

**Check (actually run):** built a 6×6 circulant matrix from the first column c = [4, 1, 0, 0, 0, 2], computed its eigenvalues with `numpy.linalg.eigvals` (a general dense eigensolver) and separately with `numpy.fft.fft(c)`.

```
general eigvals (sorted):  [1.+0.j       2.5-0.866025j 2.5+0.866025j 5.5-0.866025j 5.5+0.866025j 7.+0.j]
FFT(first col) (sorted):   [1.-0.j       2.5-0.866025j 2.5+0.866025j 5.5-0.866025j 5.5+0.866025j 7.+0.j]
max abs difference: 6.22e-15
```

The two match to machine precision (6.22e-15, versus the general eigensolver's own roundoff floor near 1e-15 for entries of this size). For circulant matrices, "diagonalize with FFT" is not an approximation or a speed trick applied to an eigenvalue problem — it is the exact closed-form eigendecomposition, and it generalizes directly to the O(n log n) solve C x = b via x = F⁻¹( (Fb) / (Fc) ), elementwise division in the Fourier domain.

### 2. "Levinson-Durbin is just a faster way to solve any Toeplitz system, so replace a general solver with it whenever the matrix is Toeplitz."

**Correct statement:** Levinson-Durbin computes the correct answer only when every leading principal submatrix of the (symmetric) Toeplitz matrix is nonsingular, and even when it completes, it can be markedly less numerically stable than a pivoted general solver on an ill-conditioned Toeplitz system, because it has no mechanism for pivoting. Whether the instability actually shows up depends on where the ill-conditioning comes from: if it comes from the whole matrix being close to singular (large condition number) while every leading minor stays reasonably scaled, Levinson-Durbin can track a generic solver closely; the classic failure mode is specifically a leading principal minor being near-singular even while the full matrix is fine, or vice versa.

**Check (actually run):** built an 8×8 symmetric Toeplitz matrix from r = [1, 0.999999, 0.999998, ..., 0.999993] (a matrix that is close to singular overall — condition number about 1.54e7), generated a random true solution x_true, formed b = T @ x_true, and solved for x two ways: with a from-scratch implementation of the classical Levinson-Durbin recursion, and with `numpy.linalg.solve` (LAPACK's general LU with partial pivoting).

```
condition number of T: 1.539e+07
Levinson-Durbin relative error:  5.018e-10
Direct solve relative error:     6.355e-10
```

The two methods land within a factor of ~0.8 of each other, both tracking the matrix's condition number as expected — this matrix's leading minors happen to stay well-scaled, so this run does not expose Levinson-Durbin's structural weak point. The corrected takeaway is narrower than the claim it tests: overall ill-conditioning alone does not reliably separate the two methods; the textbook instability case is a leading principal minor near-singular independent of the full matrix's conditioning, which this construction does not force. Do not conclude from one passing comparison that Levinson-Durbin is safe in general — construct a leading-minor-targeted test before trusting it on a production ill-conditioned system.

### 3. "Bartels-Stewart is an approximate or iterative method for the Sylvester equation, like an eigenvalue iteration."

**Correct statement:** Bartels-Stewart is a direct method: it reduces A and B to real Schur form (a black-box O(n³) subroutine), then solves the resulting triangular Sylvester equation by back-substitution in closed form — no iteration or tolerance in the Sylvester-solving step itself. Cost is O(n³) for square n×n A, B (O(n³ + m³) for A: n×n, B: m×m), a large improvement over the O(n⁶) of vectorizing directly.

**Check (concrete, not re-run numerically to keep scope to two experiments):** vec(AX + XB) = (Iₙ ⊗ A + Bᵀ ⊗ Iₙ) vec(X); solving this Kronecker system directly costs O((n²)³) = O(n⁶) time and O(n⁴) memory for the dense (n²)×(n²) coefficient matrix, versus O(n³) time and O(n²) memory for Bartels-Stewart — at n = 200 that is roughly 6.4×10¹² versus 8×10⁶ floating-point operations, a factor of about 800,000. The two agree in exact arithmetic; Bartels-Stewart is a reformulation for cost, not an approximation.

### 4. "H-matrices, HSS, and HODLR are basically the same technique with different names, so a complexity result for one applies to the others."

**Correct statement:** all four hierarchical formats share low-rank compression on well-separated (admissible) blocks, but HODLR uses one non-nested low-rank factorization per block, giving matrix-vector products around O(n log n); HSS and H² require *nested* bases (a node's basis expressed via its children's), which removes the extra log factor and gives a true O(n) matrix-vector product and, with the right recursion, a near-O(n) direct solve. A "linear time" claim true for HSS is not automatically true for HODLR.

## Rat-holes

- **Chasing a "fully general" fast direct solver for HSS/H²-matrices.** Construction, compression-tolerance selection, and update-under-perturbation algorithms are an active, fragmented research area (papers use incompatible generator conventions); building an HSS solver from scratch as a first exposure burns far more time than using an existing library (e.g., STRUMPACK, HODLRlib) to get intuition first.
- **Proving displacement-rank identities from scratch for every matrix class separately**, instead of learning the one general displacement-operator framework (Kailath-Sayed) once and specializing it; treating each class as independent triples the algebra for no new insight.
- **Deriving FMM's error bounds from the multipole-expansion side when the goal is to understand hierarchical-matrix compression.** FMM's classical error analysis is a physics/approximation-theory argument (truncated spherical harmonics or Taylor expansions) largely orthogonal to the linear-algebra low-rank argument used for H-matrices; conflating the two obscures what each bound actually depends on.
- **Assuming Levinson-type recursions generalize trivially to block-Toeplitz or non-symmetric Toeplitz systems.** The block case needs a separate, more delicate recursion (block Levinson, or Schur-type algorithms) with genuinely different pivoting/breakdown conditions.
- **Optimizing tensor-train or Tucker rank truncation as if it were a single scalar-rank SVD problem.** Because both use per-mode or per-bond ranks, the Eckart-Young analogue (e.g., TT-SVD's quasi-optimality) gives a bound with an extra factor (often √(d-1) for a d-way train), not exact optimality — expecting tensor-train truncation to be as sharp as matrix SVD truncation causes confusing "why isn't this the best rank-r tensor" debugging.

## High-yield study prompts

1. Derive ∇(T) = Z T - T Zᵀ (Z the down-shift matrix) for a Toeplitz matrix T, and show its rank is at most 2; repeat for a Cauchy matrix with the diagonal-shift operator, and compare the two derivations.
2. Implement Levinson-Durbin from scratch, then construct a symmetric Toeplitz matrix with small full condition number but a near-singular middle leading minor; confirm the recursion loses far more accuracy than a pivoted general solver there, and contrast with a matrix whose ill-conditioning does not concentrate in one leading minor.
3. Embed a non-symmetric n×n Toeplitz matrix in a 2n×2n circulant matrix, verify the embedding reproduces the Toeplitz matrix-vector product via FFT alone, and time it against a direct O(n²) product for several n to find where FFT actually wins.
4. Solve a small Lyapunov equation AX + XAᵀ = C two ways — Kronecker vectorization and direct solve, versus Schur-form reduction and back-substitution (Bartels-Stewart by hand) — confirm matching X, and record the operation-count and memory ratio at n = 50 and n = 200.
5. Assemble a dense interaction matrix from a small 1-D boundary integral equation or N-body problem, compress its off-diagonal blocks into HODLR at a fixed tolerance, and compare matrix-vector time and accuracy against a direct dense product as n grows; note which complexity class (O(n log n) vs O(n)) your implementation lands in and why.
6. Take a 4-way tensor of known low tensor-train rank, compute its Tucker and tensor-train decompositions, and compare stored parameter counts as tensor order rises from 3 to 6, to see why tensor train (linear-in-order storage) beats Tucker (exponential-in-order core) at high order.
