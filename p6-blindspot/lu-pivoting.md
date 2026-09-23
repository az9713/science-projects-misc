# Blind-Spot Pass: Gaussian Elimination, LU, and Pivoting

## Topic Stack

The topic sits on five layers, each depending on the one below it.

1. **Gaussian elimination as matrix factorization.** Eliminating variables row by row is
   the same arithmetic as writing `A = LU`, with `L` unit lower triangular and `U` upper
   triangular, built from the multipliers used in elimination.
2. **Operation count.** Dense LU on an `n x n` matrix costs `(2/3)n^3` flops (leading
   order). This sets the baseline against which every "faster" variant is measured.
3. **Pivoting strategies.** Partial pivoting (swap rows only, pick the largest entry in
   the current column), complete pivoting (swap rows and columns, pick the largest entry
   in the remaining submatrix), and rook pivoting (a cheaper compromise between the two:
   search rows and columns alternately until a local maximum is found).
4. **Stability theory: the growth factor.** `rho_n = max|u_ij| / max|a_ij|` measures how
   much elimination inflates entries. Partial pivoting bounds `rho_n <= 2^(n-1)` in the
   worst case (Wilkinson's example achieves this bound exactly), but `rho_n` stays small,
   typically low tens, on almost all matrices seen in practice.
5. **Structure-exploiting and hardware-aware variants.** Cholesky and `LDL^T` for
   symmetric matrices (with Bunch-Kaufman pivoting for the indefinite case); blocked
   right-looking and left-looking LU that call Level-3 BLAS (matrix-matrix multiply) for
   speed; communication-avoiding LU (CALU) with tournament pivoting for parallel
   machines; iterative refinement to recover accuracy cheaply; and the Hager-Higham
   estimator (used in LAPACK's `xGECON`) that gets a condition-number estimate from the
   LU factors without forming `A^{-1}`.

Each layer answers a question the layer above raises: elimination gives you a
factorization; the flop count tells you it is worth doing once and reusing; pivoting
asks "but is it numerically safe?"; the growth factor answers "how unsafe, exactly, and
how often?"; and the last layer asks "how do we make this fast and useful in the systems
we actually have?" (symmetric problems, multicore/distributed machines, and a need for
error estimates).

## Unknown Unknowns

- **The growth factor bound is not a probability statement.** `rho_n <= 2^(n-1)` is a
  worst-case bound over all matrices, proved by tracking how large an entry can become at
  each elimination step. It says nothing about how likely large growth is. Treating the
  bound as if it described typical behavior is the single largest blind spot in this
  topic (see Misconception 1).
- **Pivoting controls growth, not conditioning.** Partial pivoting keeps the intermediate
  numbers in elimination from blowing up. It does **not** make a badly conditioned matrix
  (large `cond(A) = ||A|| * ||A^{-1}||`) well conditioned. A matrix can be perfectly
  pivoted and still produce a solution with large relative error if `cond(A)` is huge.
  Growth factor and condition number answer different questions and multiply together in
  the standard LU backward-error bound.
- **Complete pivoting is provably safer but essentially unused in practice.** Its
  worst-case growth bound is far smaller than partial pivoting's, yet its `O(n^3)` search
  cost per elimination step (searching the whole trailing submatrix, not just a column)
  makes it too slow for general dense solvers. Rook pivoting exists specifically to
  recover most of the safety at close to partial-pivoting cost.
- **Level-3 BLAS is not an optimization detail bolted onto LU — it reshapes the
  algorithm.** Blocked LU exists because processors can do matrix-matrix multiply
  (`O(n^3)` flops on `O(n^2)` data movement) far faster relative to memory bandwidth than
  matrix-vector operations (`O(n^2)` flops on `O(n^2)` data movement). "Blocked" is not
  "the same algorithm, chunked" — it is a rewrite whose entire motivation is arithmetic
  intensity, not clock speed.
- **Iterative refinement can restore accuracy even when the factorization itself is
  inaccurate**, because refinement only needs residuals computed in extra precision, not
  a better factorization. This is why mixed-precision solvers (compute the factorization
  in low precision, refine in high precision) can match full high-precision accuracy at a
  fraction of the cost. Missing this is missing why anyone still studies iterative
  refinement in 2026-era mixed-precision hardware.
- **`xGECON` never computes `A^{-1}`.** Forming the inverse to get `||A^{-1}||` costs
  another `(2/3)n^3` to `2n^3` flops and can itself be inaccurate. The Hager-Higham
  estimator instead runs a handful of triangular solves against the existing `L` and `U`
  factors (each `O(n^2)`) and returns an estimate that is usually within a small factor
  of the true value. It is an estimator, not an exact computation, and it can (rarely) be
  fooled by adversarially constructed matrices.

## Common Misconceptions

**Misconception 1: "Partial pivoting is unstable because `rho_n` can reach `2^(n-1)`."**
Correct statement: the worst case is `2^(n-1)`, but on random matrices `rho_n` is small,
typically around `n^{2/3}` in growth or smaller in practice, and stays in single or low
double digits for `n` up to several hundred. Wilkinson-type matrices that hit the bound
are rare and structured; they essentially never arise from physical or randomly generated
problems. This is why partial pivoting remains the default in LAPACK's `dgesv` despite
the exponential worst case. Concrete check: the experiment below builds the classic
Wilkinson matrix (subdiagonal `-1`, diagonal `1`, last column `1`) for `n = 10, 20, 40,
60` and compares its growth factor to 200 random Gaussian matrices of the same size.

**Misconception 2: "Pivoting makes the solve accurate no matter what `A` is."**
Correct statement: pivoting bounds the *growth factor*, but the final error bound for
`Ax = b` also scales with `cond(A)`. A well-pivoted factorization of a nearly singular
matrix will still produce a solution with large relative error, because the bound is
roughly `(backward error) * cond(A) * rho_n * n`, and pivoting only controls the `rho_n`
term. Concrete check: solve a Hilbert-matrix system (`cond` in the range of `10^10` or
more for `n` around 12) with partial pivoting and confirm the growth factor stays modest
while the solution error is still large; compare residual `||Ax - b||` (small) against
error `||x - x_true||` (can be large) to see the two failure modes are distinct.

**Misconception 3: "LU and Cholesky are the same algorithm, just named differently for
symmetric matrices."** Correct statement: Cholesky (`A = LL^T`) exploits symmetric
positive definiteness to (a) need no pivoting for stability, and (b) do roughly half the
flops of general LU, `(1/3)n^3` versus `(2/3)n^3`, because it only ever touches half the
matrix. `LDL^T` extends this to general symmetric matrices, but symmetric *indefinite*
matrices need pivoting after all (Bunch-Kaufman pivoting, which permits 1x1 and 2x2
diagonal pivot blocks) because a naive `LDL^T` can divide by a zero or tiny diagonal
entry even when the matrix is well conditioned. Concrete check: time or flop-count
Cholesky versus general LU on the same SPD matrix at increasing `n` and confirm the ratio
approaches 2, and construct a small symmetric indefinite matrix with a zero (1,1) entry
to show plain `LDL^T` fails while Bunch-Kaufman's 2x2 pivot succeeds.

**Misconception 4: "Blocked LU changes the answer or the operation count."** Correct
statement: blocked right-looking and left-looking LU variants compute the *same*
mathematical factorization (up to rounding-order differences from a different order of
floating-point operations) and do the *same* `(2/3)n^3` leading-order flops as
unblocked LU. What changes is data movement: operations are grouped into matrix-matrix
multiplies (Level-3 BLAS) sized to fit in cache, which is a performance change, not an
algorithmic one. Blocking can change the accuracy at the last bit because floating-point
addition is not associative, but this is a second-order effect, not the point of
blocking.

**Misconception 5: "The Hager-Higham estimator in `xGECON` computes the exact condition
number."** Correct statement: it is a norm *estimator* built from a small number
(typically fewer than 5, capped around 5 iterations) of triangular solves using the
already-computed `L` and `U` factors, and it returns an estimate of `||A^{-1}||_1`
that is usually accurate to within a small factor of the truth, not the exact value.
LAPACK's routine name itself says "estimate" (`RCOND` is a reciprocal condition
*estimate*). Concrete check: the experiment below compares the estimator's output to
`||A^{-1}||_1` computed by explicit inversion on two matrices with different target
condition numbers, and reports the ratio.

## Two Numpy Experiments (Run, Real Output)

**Experiment 1 — growth factor: Wilkinson's worst case versus random matrices.**

```
=== Experiment 1: growth factor rho_n ===
n= 10  wilkinson rho=         512  2^(n-1)=512  random rho: mean=1.524 max=3.856
n= 20  wilkinson rho=   5.243e+05  2^(n-1)=5.243e+05  random rho: mean=1.986 max=4.349
n= 40  wilkinson rho=   5.498e+11  2^(n-1)=5.498e+11  random rho: mean=2.997 max=6.362
n= 60  wilkinson rho=   5.765e+17  2^(n-1)=5.765e+17  random rho: mean=3.859 max=8.425
```

The Wilkinson matrix hits `2^(n-1)` exactly at every size tested, confirming the bound is
tight and achieved. The 200 random Gaussian matrices per size never come close: mean
growth factor rises only from about 1.5 (`n=10`) to about 3.9 (`n=60`), and even the
observed maximum over 200 trials stays under 9 at `n=60` — versus a worst case of
`5.8e17`. This is the direct numerical demonstration of Misconception 1: worst case and
typical case differ by roughly 17 orders of magnitude at `n=60`.

**Experiment 2 — Hager-Higham-style 1-norm condition estimate versus the true value.**

```
=== Experiment 2: 1-norm condition number estimate from LU triangular solves ===
target_cond~1e+02  true_cond1=431.2  estimated_cond1=389.3  ratio=0.903
target_cond~1e+06  true_cond1=2.806e+06  estimated_cond1=2.806e+06  ratio=1.000
```

(Target condition numbers are the singular-value spread used to build each test matrix;
the true 1-norm condition number differs from that target because the 1-norm and the
2-norm/singular-value-based condition number are different quantities.) The estimator,
using a Hager-style power-iteration over triangular solves rather than forming `A^{-1}`,
lands within about 10% of the true value at `cond ~ 10^2` and matches to the printed
precision at `cond ~ 10^6`. This supports Misconception 5's correct statement: it is a
close estimate obtained cheaply, not an exact computation, and its relative accuracy can
vary by case (here 0.903 and 1.000, both good, but not identically 1 in general).

## Rat-Holes (Interesting but Off the High-Yield Path)

- **Proving the exact worst-case growth-factor bound for complete pivoting.** The
  known worst case for complete pivoting is much smaller than `2^(n-1)` but the exact
  tight bound is still not fully settled for all `n`; chasing the sharpest known result
  is a research-literature rabbit hole, not needed to use or reason about pivoting.
- **Random matrix theory for the typical growth factor.** Explaining *why* `rho_n` stays
  small on random matrices (heuristic arguments involving average-case behavior of
  Gaussian elimination) is an active and technical area; useful to know it exists, not
  necessary to reproduce.
- **Hand-deriving the Bunch-Kaufman pivoting rules.** The exact threshold constants used
  to decide between a 1x1 and a 2x2 pivot block are fiddly and rarely need to be
  re-derived; knowing what problem they solve (avoiding division by a tiny or zero
  diagonal in a symmetric indefinite matrix without destroying symmetry) is the
  high-yield part.
- **CALU's tournament pivoting tree details.** The full communication-avoiding LU
  algorithm, including the reduction tree used to pick pivot candidates across
  processors, is a systems/parallel-computing topic in its own right; understanding that
  it trades a small amount of stability for a large reduction in inter-processor
  communication is enough for most purposes.
- **Mixed-precision iterative refinement convergence theory.** The conditions under
  which refinement converges (and how many digits it can recover, depending on the
  precision of the residual computation versus the factorization) is a deep numerical
  analysis topic; the practical takeaway (refine when you can, it is nearly free and
  often restores full accuracy) is what most users need.

## High-Yield Study Prompts

1. Derive the `(2/3)n^3` flop count for LU by counting multiply-adds at each of the
   `n-1` elimination steps, and show why Cholesky's exploitation of symmetry halves it
   to `(1/3)n^3`.
2. Explain, in one paragraph, why the growth-factor bound `2^(n-1)` for partial pivoting
   is a worst case and not typical, and name the property of the Wilkinson matrix
   (subdiagonal `-1`, diagonal `1`, last column `1`) that makes it achieve the bound.
3. Write out the backward-error bound for solving `Ax = b` via pivoted LU, and identify
   which factor in that bound is controlled by pivoting (growth factor) and which is not
   (condition number `cond(A)`).
4. Compare partial, complete, and rook pivoting on: (a) worst-case growth factor bound,
   (b) cost per elimination step, and (c) why rook pivoting exists as a middle option.
5. Explain why `LDL^T` needs Bunch-Kaufman pivoting for symmetric indefinite matrices
   even though Cholesky needs no pivoting at all for symmetric positive definite ones.
6. Describe the difference between right-looking and left-looking blocked LU in terms of
   which part of the matrix is updated at each step, and explain why both call Level-3
   BLAS for the same underlying reason.
7. Explain what problem tournament pivoting in CALU solves that partial pivoting does
   not, in a distributed-memory setting, and what it costs in exchange.
8. Walk through why iterative refinement can recover full accuracy from a
   lower-precision factorization, and state the one ingredient that must be computed in
   higher precision for refinement to work.
9. Explain why `xGECON`'s Hager-Higham estimator uses triangular solves against the
   existing `L, U` factors instead of forming `A^{-1}`, and what "estimate" versus
   "exact value" means for `RCOND` in practice.
10. Using the two rerunnable experiments above as a template, construct one additional
    small numpy test that would catch a code review bug: LU implemented without pivoting
    silently used on a matrix where pivoting is required for stability.
