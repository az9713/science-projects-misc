# P6 blind-spot sweep: numerical linear algebra — twelve subtopics

Field: numerical linear algebra. Reader: a graduate student. The twelve subtopics below together cover the field. Each entry gives a slug, a title, and a one-paragraph scope.

## 1. floating-point-conditioning
**Title:** Floating point, conditioning, and backward stability

**Scope:** IEEE 754 binary formats (binary16, bfloat16, binary32, binary64), unit roundoff u = 2^-53 for binary64, the standard model fl(x op y) = (x op y)(1 + delta) with |delta| <= u, rounding modes, subnormals, and catastrophic cancellation. Condition numbers of problems (kappa(A) = ||A|| ||A^-1|| for linear systems, and the conditioning of least squares, eigenvalue, and singular value problems). Forward error, backward error, and the rule of thumb forward error <= condition number x backward error. Backward stability as the central standard for an algorithm, the difference between an ill-conditioned problem and an unstable algorithm, a priori and a posteriori error bounds, and running error analysis (Higham, Accuracy and Stability of Numerical Algorithms).

## 2. lu-pivoting
**Title:** Gaussian elimination, LU, and pivoting

**Scope:** LU factorization as Gaussian elimination, operation count (2/3)n^3 flops, partial, complete, and rook pivoting, the growth factor rho_n and its worst case 2^(n-1) under partial pivoting (Wilkinson's example) against its small typical size on random matrices. Cholesky for symmetric positive definite matrices and LDL^T with Bunch-Kaufman pivoting for symmetric indefinite matrices. Blocked, right-looking and left-looking variants that use Level-3 BLAS, communication-avoiding and tournament pivoting (CALU), iterative refinement, and the use of LU to estimate condition numbers cheaply (Hager-Higham estimator in LAPACK xGECON).

## 3. qr-least-squares
**Title:** QR factorization and least squares

**Scope:** The linear least-squares problem min ||Ax - b||_2, the normal equations and why they square the condition number, Householder reflections, Givens rotations, classical and modified Gram-Schmidt and their loss of orthogonality (MGS loses orthogonality in proportion to kappa(A) u; CGS in proportion to kappa(A)^2 u; reorthogonalization "twice is enough"). Column-pivoted QR (QRCP) and rank-revealing QR, the sensitivity of least squares (dependence on kappa(A)^2 through the residual), rank-deficient and underdetermined problems, minimum-norm solutions, weighted and constrained least squares, Tikhonov regularization, and tall-skinny QR (TSQR) for communication-avoiding computation.

## 4. svd
**Title:** The singular value decomposition

**Scope:** Existence and geometry of the SVD A = U Sigma V^T, the Eckart-Young-Mirsky theorem for best rank-k approximation in the 2-norm and Frobenius norm, the pseudoinverse, numerical rank and truncation thresholds, and perturbation theory (Weyl's inequality for singular values, Wedin's sin-theta theorem for singular subspaces). Algorithms: Golub-Kahan bidiagonalization, implicit-shift QR on the bidiagonal, divide and conquer (LAPACK xGESDD), one-sided Jacobi SVD and its high relative accuracy on graded matrices, and the cost of full SVD (about 4m n^2 - 4n^3/3 flops for singular values only, more with vectors). Applications to principal component analysis, total least squares, and low-rank structure detection.

## 5. eigenvalue-algorithms
**Title:** Dense eigenvalue algorithms

**Scope:** Power iteration, inverse iteration, and Rayleigh quotient iteration (cubic convergence for symmetric matrices), reduction to Hessenberg or tridiagonal form, the QR algorithm with Wilkinson and Francis double shifts, deflation, aggressive early deflation, and bulge chasing. Symmetric tridiagonal methods: implicit QR, divide and conquer, bisection with Sturm sequences, and MRRR (LAPACK xSTEMR). Schur form, non-normal matrices, the conditioning of eigenvalues (reciprocal of |y^* x|), Bauer-Fike, pseudospectra, the Jacobi method, and the generalized eigenproblem Ax = lambda Bx via the QZ algorithm.

## 6. krylov-methods
**Title:** Krylov subspace methods

**Scope:** Krylov subspaces K_k(A, b), the Arnoldi and Lanczos processes, and the solvers built on them: conjugate gradient (CG) for symmetric positive definite systems with the convergence bound 2((sqrt(kappa) - 1)/(sqrt(kappa) + 1))^k in the A-norm, MINRES and SYMMLQ for symmetric indefinite systems, GMRES and restarted GMRES(m) for nonsymmetric systems, BiCG, BiCGSTAB, QMR, and IDR(s). Polynomial approximation as the view of convergence, the effect of eigenvalue clustering and non-normality, finite-precision behavior (loss of orthogonality in Lanczos, delay of convergence in CG, Paige's analysis, Greenbaum's results), LSQR and LSMR for least squares, and Krylov eigensolvers (implicitly restarted Arnoldi in ARPACK, Krylov-Schur, Lanczos with selective reorthogonalization, LOBPCG, Jacobi-Davidson).

## 7. preconditioning
**Title:** Preconditioning

**Scope:** Left, right, and split preconditioning and their effect on the residual that a Krylov method minimizes. Classical stationary iterations (Jacobi, Gauss-Seidel, SOR, SSOR) as preconditioners, incomplete factorizations (ILU(0), ILU(k), ILUT, incomplete Cholesky) and their breakdown modes, sparse approximate inverses (SPAI, FSAI), algebraic and geometric multigrid, domain decomposition (additive and multiplicative Schwarz, FETI, BDDC), block and Schur-complement preconditioners for saddle-point systems, and physics-based preconditioning. Mesh-independent convergence as the design target, the trade-off between setup cost, cost per application, and iteration count, and the parallel scalability limits of each family.

## 8. sparse-direct-methods
**Title:** Sparse direct methods

**Scope:** Sparse storage formats (CSR, CSC, COO), fill-in and its graph model (elimination graphs, elimination trees), fill-reducing orderings (approximate minimum degree AMD, nested dissection via METIS, reverse Cuthill-McKee for bandwidth), symbolic and numeric factorization, supernodal and multifrontal methods, threshold and static pivoting for unsymmetric matrices, and parallel solvers (SuperLU, MUMPS, PARDISO, CHOLMOD, UMFPACK). The complexity of nested dissection on 2D grids (O(n^1.5) flops, O(n log n) fill) against 3D grids (O(n^2) flops, O(n^(4/3)) fill), memory as the limiting resource, and the choice between direct and iterative solvers.

## 9. randomized-nla
**Title:** Randomized numerical linear algebra

**Scope:** Random sketching and subspace embeddings (Gaussian, subsampled randomized Hadamard transform SRHT, CountSketch, sparse sign embeddings), the Johnson-Lindenstrauss lemma, the randomized range finder and randomized SVD with oversampling and power iteration (Halko-Martinsson-Tropp 2011), error bounds in expectation and with high probability, the Nystrom approximation for positive semidefinite matrices, sketch-and-solve and sketch-and-precondition least squares (Blendenpik, LSRN), randomized column selection (leverage scores, CUR, interpolative decomposition), randomized trace and diagonal estimation (Hutchinson, Hutch++), single-pass streaming algorithms, and randomized preconditioners (randomly pivoted Cholesky).

## 10. structured-matrices
**Title:** Structured and data-sparse matrices

**Scope:** Matrices with exploitable structure: banded, Toeplitz, Hankel, circulant (diagonalized by the FFT in O(n log n)), Cauchy, and Vandermonde matrices and their displacement rank, fast and superfast Toeplitz solvers (Levinson-Durbin O(n^2), superfast O(n log^2 n)) and their stability limits. Kronecker products and the Sylvester and Lyapunov equations (Bartels-Stewart), semiseparable and quasiseparable matrices, and hierarchical low-rank formats (H-matrices, H^2-matrices, HSS, HODLR) with near-linear-complexity arithmetic, as used for integral equations and the fast multipole method. Low-rank tensor formats (Tucker, tensor train) as the higher-order extension.

## 11. mixed-precision
**Title:** Mixed-precision and hardware-aware algorithms

**Scope:** Low-precision formats (fp16 with u = 2^-11, bfloat16 with u = 2^-8, fp8 variants, TF32) and their range limits, mixed-precision iterative refinement in two and three precisions (Carson-Higham GMRES-IR) with its convergence conditions on kappa(A), low-precision factorizations as preconditioners, tensor-core matrix multiply and its error analysis, probabilistic rounding-error analysis with bounds that grow as sqrt(n) u rather than n u, stochastic rounding, and error-free transformations and compensated summation (Kahan, TwoSum). Communication-avoiding algorithms and lower bounds on data movement, the roofline model, BLAS levels and blocking, GPU dense linear algebra (MAGMA, cuSOLVER), and reproducibility across parallel reductions.

## 12. matrix-functions
**Title:** Matrix functions and matrix equations

**Scope:** Definitions of f(A) through Jordan form, Cauchy integral, and polynomial interpolation, conditioning via the Frechet derivative, the matrix exponential by scaling and squaring with Pade approximants (expm in MATLAB and SciPy) and the "nineteen dubious ways" survey (Moler-Van Loan), the Schur-Parlett algorithm, matrix square root, logarithm, and sign function (Newton iterations and their stability), and the polar decomposition. Action of a matrix function on a vector f(A)b by Krylov and rational Krylov methods for large sparse A, exponential integrators, and the algebraic Riccati equation. Applications to network centrality, differential equations, and control.
