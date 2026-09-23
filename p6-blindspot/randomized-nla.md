# Blind-spot pass: Randomized numerical linear algebra

## Scope

This pass covers random sketching and subspace embeddings (Gaussian, subsampled
randomized Hadamard transform (SRHT), CountSketch, sparse sign embeddings), the
Johnson-Lindenstrauss (JL) lemma, the randomized range finder and randomized SVD with
oversampling and power iteration (Halko-Martinsson-Tropp 2011, "HMT"), error bounds in
expectation and with high probability, the Nystrom approximation for positive
semidefinite (PSD) matrices, sketch-and-solve and sketch-and-precondition least squares
(Blendenpik, LSRN), randomized column selection (leverage scores, CUR, interpolative
decomposition), randomized trace and diagonal estimation (Hutchinson, Hutch++),
single-pass streaming algorithms, and randomized preconditioners (randomly pivoted
Cholesky).

## Topic stack

Randomized numerical linear algebra (RandNLA) sits on top of classical numerical
linear algebra and needs these layers built first, in order:

1. **Deterministic factorizations.** QR (Householder, Gram-Schmidt), the SVD, and how
   they give optimal low-rank approximation (Eckart-Young). Without this you cannot
   judge what a randomized method is approximating or what "optimal" means.
2. **Concentration of measure and probability tail bounds.** Markov, Chebyshev,
   sub-Gaussian and sub-exponential tail bounds, and the matrix Bernstein / matrix
   Chernoff inequalities. These are what turn "a random sketch works on average" into
   "a random sketch works with probability at least 1 - delta."
3. **The Johnson-Lindenstrauss lemma.** Says n points in high dimension can be mapped
   into O(log n / epsilon^2) dimensions while preserving all pairwise distances up to a
   factor (1 +/- epsilon). This is the seed idea behind nearly every sketching method
   below.
4. **Subspace embeddings.** A stronger, structured version of JL: a random matrix S
   that preserves the norm of every vector in a fixed k-dimensional subspace
   simultaneously (not just a finite point set), with high probability. This is the
   object that makes sketch-and-solve legitimate.
5. **Sketch constructions**, layered by cost and structure:
   - Dense Gaussian sketches (simplest to analyze, expensive to apply: O(nd) per
     sketch of an n x d matrix).
   - SRHT / subsampled randomized Fourier/Hadamard transforms (apply in O(nd log n)
     via a fast transform, then subsample rows).
   - CountSketch (apply in time proportional to the number of nonzeros, O(nnz(A)),
     one nonzero per row).
   - Sparse sign / OSNAP embeddings (a few nonzeros per column, a middle ground
     between CountSketch and Gaussian in accuracy per row).
6. **The randomized range finder and randomized SVD (HMT 2011).** Uses a sketch to
   find an approximate orthonormal basis for the range of a matrix, then projects onto
   it and does a cheap deterministic SVD on the small projected matrix. Oversampling
   (drawing more sketch columns than the target rank) and power iteration (repeated
   multiplication by A and A^T) control the two error terms.
7. **Error bounds.** In-expectation bounds (average-case guarantees, easy to prove)
   versus high-probability bounds (worst-case-over-randomness guarantees, needed for a
   result you can rely on for one run). Both appear in HMT 2011 and its follow-ups.
8. **Applications built on top of the range finder**: Nystrom approximation for PSD
   matrices (uses symmetry to halve the work relative to general randomized SVD),
   randomized column selection (leverage-score sampling, CUR decomposition,
   interpolative decomposition (ID)), sketch-and-solve and sketch-and-precondition
   least squares (Blendenpik, LSRN), randomized trace and diagonal estimation
   (Hutchinson, Hutch++), streaming (single-pass) variants, and randomized
   preconditioners such as randomly pivoted Cholesky (RPC).

Each layer above depends on the one before it. Skipping the concentration-inequality
layer is the single most common shortcut, and it is why so many misconceptions below
exist: people memorize the algorithms without the probabilistic machinery that bounds
their failure probability.

## Unknown unknowns

These are the things a learner typically does not know they need to know, because
introductory treatments (blog posts, single lecture slides) usually skip them.

1. **The sketch size k depends on the failure probability delta, not just on the
   accuracy epsilon.** Most informal explanations say "JL needs k = O(log n /
   epsilon^2) dimensions" and stop there. The constant hides a log(1/delta) term. If
   you want a guarantee that holds with probability 1 - 10^-9 (needed when you sketch
   millions of times in a pipeline), k grows with log(1/delta), and ignoring this is a
   real source of surprise failures in production sketching code.

2. **A subspace embedding needs a working failure probability tied to the dimension
   of the subspace, not the number of points.** JL bounds a finite point set. When you
   need "preserve norms for every vector in a k-dimensional subspace" (an infinite
   set), you get there through a covering-number / net argument, and the sketch size
   for a subspace embedding scales like O(k / epsilon^2) (up to log factors), not
   O(log(number of points)/epsilon^2). Conflating the two size formulas is common and
   leads people to undersize a sketch used for least squares.

3. **Randomized range finder error has two separate terms, and oversampling and power
   iteration fix different ones.** The Halko-Martinsson-Tropp bound (Theorem 1.1 in
   their 2011 SIAM Review paper) is roughly:
   E[||A - QQ^T A||] <= (1 + sqrt(k/(p-1))) * sigma_{k+1} + (e*sqrt(k+p)/p) * sqrt(sum
   of squared tail singular values).
   The first term is controlled mainly by oversampling p; the second (the tail-energy
   term) is what power iteration crushes, because power iteration replaces A with
   (A A^T)^q A, which raises the singular value ratio (sigma_{k+1}/sigma_i) to the
   power (2q+1) and makes the spectral gap look much sharper. Not knowing that these
   are two independent knobs solving two independent failure modes leads people to
   "fix" a bad randomized SVD by cranking oversampling when what they actually need is
   power iteration, or vice versa.

4. **Power iteration must be reorthogonalized between multiplications in finite-precision
   arithmetic**, or the sketch loses rank numerically (the vectors align onto the
   dominant direction and the smaller singular directions underflow into rounding
   noise) after only a few iterations. HMT's algorithm explicitly QR-orthonormalizes
   Y after every application of A or A^T for exactly this reason; skipping it because
   "it's just a couple of matrix-vector products" silently degrades accuracy for any q
   greater than about 2-3.

5. **Leverage scores are themselves expensive to compute exactly** (they require the
   SVD or QR of A, which is what you were trying to avoid). Practical algorithms use a
   sketch to *estimate* leverage scores cheaply, and this adds another layer of
   approximation error on top of the sampling error that most short explanations of
   "sample rows by leverage score" do not mention.

6. **CUR and interpolative decomposition are not automatically as good as the
   truncated SVD.** They select actual columns/rows of A (interpretable, sparsity/
   nonnegativity-preserving), but a rank-k CUR approximation error is provably worse
   than the optimal rank-k SVD error by a problem-dependent factor (often stated as
   within a constant factor of (k+1) times optimal for the best known deterministic
   selection schemes, and randomized leverage-score CUR gives comparable but
   probabilistic guarantees). Assuming CUR = SVD accuracy is a common error.

7. **Hutchinson's trace estimator has variance that depends on the matrix**, not just
   on the number of probes. For a matrix with a few dominant eigenvalues and a long
   flat tail, plain Hutchinson needs very many probes to converge; Hutch++ fixes this
   by first removing a low-rank randomized-SVD estimate of the dominant directions and
   only using Hutchinson on the residual, converging in O(1/epsilon) probes versus
   Hutchinson's O(1/epsilon^2). The variance-versus-spectrum dependency is rarely
   spelled out.

8. **Sketch-and-solve and sketch-and-precondition are different algorithms with
   different accuracy ceilings.** Sketch-and-solve (solve the sketched least-squares
   problem directly) gives only a constant-factor-accurate solution — good enough for
   many machine-learning uses but not for a numerically exact linear solve.
   Sketch-and-precondition (Blendenpik, LSRN: use the sketch to build a preconditioner,
   then run iterative refinement such as LSQR on the *original* system) converges to
   full machine precision in a handful of iterations. Treating them as interchangeable
   ("sketching solves least squares") is a real error.

9. **Randomly pivoted Cholesky (RPC) is a 2023-era method** (Chen, Epperly, Tropp,
   Webber) specifically for PSD low-rank approximation and preconditioning, distinct
   from and generally more accurate per unit of matrix access than uniform or ridge
   leverage-score Nystrom sampling; it adaptively re-weights pivot probabilities after
   each column is picked, which is why it beats one-shot leverage-score sampling.
   Learners often lump it in with "just another Nystrom variant" and miss that its
   adaptivity is the entire point.

## Common misconceptions

Each item: the wrong belief, the correct statement, and one concrete check.

**1. Wrong belief:** "A random Gaussian sketch distorts vectors by an amount that
depends on the ambient dimension d — sketching a 10,000-dimensional vector down to 100
dimensions is much less accurate than sketching a 100-dimensional vector down to 100
dimensions."
**Correct statement:** For a Gaussian (or SRHT/CountSketch-type) sketch S of size
k x d applied to a fixed vector, the distortion |‖Sx‖^2 - ‖x‖^2| concentrates at a rate
governed by k alone (with the target subspace dimension entering for subspace
embeddings) — not by the ambient dimension d. This is exactly the JL/Johnson–
Lindenstrauss point: dimension reduction cost is paid in k and epsilon, and d drops
out.
**Concrete check (numpy, output shown, seed 0):**
```
d=  200 k=  50  mean|distortion|=0.1686  max=0.6377
d=  200 k= 200  mean|distortion|=0.0812  max=0.2773
d= 2000 k=  50  mean|distortion|=0.1575  max=0.8194
d= 2000 k= 200  mean|distortion|=0.0815  max=0.3090
```
Doubling k (50 -> 200) roughly halves the mean distortion at both d=200 and d=2000;
increasing d by 10x (200 -> 2000) at fixed k leaves the distortion essentially
unchanged. This directly falsifies "bigger ambient dimension needs a bigger sketch to
hit the same accuracy" for this construction.

**2. Wrong belief:** "Randomized SVD gives you an approximation about as good as the
plain truncated SVD, as long as you oversample a bit (say p=5 to 10 extra columns)."
**Correct statement:** Oversampling alone is not enough when the singular value
spectrum decays slowly (a long, flat tail) — the HMT error bound's tail-energy term
stays large regardless of p in that regime, and only power iteration (q >= 1) sharpens
the effective spectral gap and shrinks the error. Whether you need power iteration is
a property of the spectrum, not a general truth about randomized SVD.
**Concrete check (numpy, output shown, seed 1, n=500, target rank k=20, oversampling
p=10, slowly decaying singular values s_i = i^-0.5):**
```
power iterations q=0: max abs error in top-20 singular values = 0.09649
power iterations q=1: max abs error in top-20 singular values = 0.02059
power iterations q=4: max abs error in top-20 singular values = 0.00101
```
With oversampling fixed at p=10, going from q=0 to q=4 power iterations cuts the
worst-case singular-value error by about 95x (0.09649 -> 0.00101), while oversampling
was already present and constant across all three rows. This shows oversampling and
power iteration are separate knobs and that oversampling by itself does not rescue a
slow-decay spectrum.

**3. Wrong belief:** "Sketch-and-solve for least squares gives you the same answer
you would get from solving the original normal equations, just faster."
**Correct statement:** Sketch-and-solve gives a solution whose residual is only
within a constant factor (1 + epsilon) of the optimal residual, and whose coefficient
vector can differ from the true least-squares solution by an amount that does not go
to zero as you add more sketch rows past a fixed working precision — it is a
constant-factor approximation, not a convergent one. To get a solution accurate to
machine precision you need sketch-and-precondition (Blendenpik/LSRN): build the
preconditioner from the sketch, then run LSQR/CG on the original A, which converges
to full precision in a small, spectrum-independent number of iterations because the
preconditioned system has a condition number close to (1+epsilon)/(1-epsilon).

**4. Wrong belief:** "CountSketch and other sparse sketches are strictly worse than
dense Gaussian sketches — you use them only when you cannot afford the O(nd) cost of a
dense sketch."
**Correct statement:** CountSketch needs a somewhat larger row count k for the same
epsilon and delta compared to a dense Gaussian sketch (the constant in its JL-type
bound is worse), but it applies in time proportional to the number of nonzero entries
of A, O(nnz(A)), rather than O(nd). For sparse input matrices (common in text,
graphs, genomics) this makes it not just cheaper but often the only feasible choice,
and combining it with a dense sketch on the (already-reduced) output ("sketch of a
sketch") recovers most of the accuracy while keeping the speed.

**5. Wrong belief:** "CUR decomposition and randomized SVD solve the same problem, so
you can always substitute one for the other."
**Correct statement:** Randomized SVD gives an orthonormal basis approximation with
error close to the unconstrained optimum (Eckart-Young), but its factors are dense
linear combinations of the original rows/columns and are not directly interpretable.
CUR selects actual rows and columns of A (interpretable, preserves sparsity/
nonnegativity/structure) but pays an accuracy price relative to the optimal rank-k
approximation — the best known CUR error bounds are worse than the SVD's optimal
error by a problem-dependent factor. The two are not interchangeable; choose CUR when
interpretability of the selected rows/columns matters more than hitting the smallest
possible residual.

**6. Wrong belief:** "Hutchinson's trace estimator with matrix-vector products needs
roughly the same number of probes to reach a given accuracy regardless of the
matrix's spectrum."
**Correct statement:** Hutchinson's variance is governed by the sum of squared
off-diagonal-ish structure and, in practice, by how concentrated the spectrum is:
matrices with a few large eigenvalues and a long flat tail need many more probes
(the number of probes for a fixed relative error scales like O(1/epsilon^2) in the
worst case, driven by the ratio between the Frobenius norm and the trace). Hutch++
addresses exactly this by deflating the top eigenspace (found via a cheap randomized
range finder) before applying Hutchinson to the residual, cutting the probe count to
O(1/epsilon).

## Rat-holes (time sinks that do not pay off proportionally at this level)

- **Re-deriving the matrix Bernstein inequality from scratch.** Useful once for
  intuition, but the proof techniques (Lieb's concavity theorem, matrix exponential
  tricks) are a specialist detour; treat the inequality as a black box and use it.
- **Chasing the tightest known constant in JL-type embedding dimension bounds.**
  Knowing the O(.) form and that delta enters logarithmically is enough for applied
  work; optimizing constants rarely changes an implementation decision.
- **Implementing SRHT/Hadamard-transform sketches by hand for a one-off analysis.**
  The fast transform (bit-reversal, padding to a power of 2, sign randomization) is
  easy to get subtly wrong; use a library routine unless the goal is specifically to
  learn the implementation.
- **Trying to make CUR match SVD accuracy exactly by tuning the sampling
  distribution.** There is a provable gap; closing it below the known theoretical
  limit is fighting a theorem, not a bug.
- **Deep-diving randomly pivoted Cholesky's 2023 convergence proof before using it.**
  For a first pass, the practical takeaway (adaptive re-weighting beats one-shot
  leverage sampling for PSD low-rank approximation) is enough to use it correctly.

## High-yield study prompts

1. State the Johnson-Lindenstrauss lemma precisely, including how the embedding
   dimension k depends on the number of points n, the distortion epsilon, and the
   failure probability delta. Then explain why a *subspace* embedding (needed for
   sketched least squares) requires a different sizing argument than the finite-point
   JL lemma.
2. Derive, or look up and explain in your own words, the two-term HMT error bound for
   the randomized range finder. Identify which physical algorithmic choice
   (oversampling p, or power iteration count q) controls each term, and why.
3. Implement the randomized SVD algorithm (range finder + small deterministic SVD) for
   a matrix with (a) fast singular value decay and (b) slow singular value decay.
   Measure the approximation error as a function of q for both, and explain the
   difference you observe using the HMT bound.
4. Explain the difference between sketch-and-solve and sketch-and-precondition for
   least squares. Name Blendenpik and LSRN and state which category each belongs to,
   and why sketch-and-precondition can reach machine precision while sketch-and-solve
   cannot.
5. Compare leverage-score sampling, CUR decomposition, and the interpolative
   decomposition. State what each one selects (rows, columns, or both), and what
   accuracy guarantee each one has relative to the optimal rank-k SVD approximation.
6. Explain why Hutch++ has better sample complexity than plain Hutchinson for trace
   estimation. Identify the role of the randomized range finder inside Hutch++.
7. Describe the Nystrom approximation for a PSD matrix and explain why exploiting
   symmetry (compared to general randomized SVD) roughly halves the number of matrix
   accesses needed.
8. Explain what "single-pass" means for a streaming randomized SVD/range-finder
   algorithm, and identify which quantities must be sketched simultaneously (row
   space and column space) to avoid a second pass over the data.
9. Explain how randomly pivoted Cholesky picks pivots adaptively, and contrast this
   with one-shot (non-adaptive) leverage-score or ridge-leverage-score sampling for
   Nystrom approximation. State why adaptivity improves accuracy per matrix access.
10. Reproduce the two numerical experiments in this document (JL distortion versus k
    and d; power iteration versus oversampling for slow spectral decay) with your own
    seeds and matrix sizes, and confirm the qualitative conclusions still hold.
