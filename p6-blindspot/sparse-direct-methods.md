# Blind-Spot Pass: Sparse Direct Methods

## Topic Stack

The topic sits on six layers, each depending on the one below it.

1. **Sparse storage formats.** COO (coordinate: three parallel arrays of row, column,
   value) is the easy-to-build, hard-to-compute-with format. CSR (compressed sparse row)
   and CSC (compressed sparse column) compress one dimension into a pointer array so
   row-wise or column-wise access is O(1) amortized. The choice between CSR and CSC is
   not cosmetic: CSC is the natural layout for column-oriented left-looking LU and for
   Cholesky, while CSR suits row-oriented sparse matrix-vector products. Converting
   between them costs a sort, so codes pick one and stick with it.
2. **Fill-in and its graph model.** Eliminating a variable in Gaussian elimination or
   Cholesky can turn a zero entry into a nonzero (fill-in). This is exactly graph
   elimination: represent the matrix's nonzero pattern as a graph (an edge for each
   off-diagonal nonzero), and eliminating a node connects all of its still-uneliminated
   neighbors to each other, adding fill edges. The elimination graph is the same object
   after each step, one node smaller. The elimination tree records, for each node, the
   first later-eliminated node it becomes connected to — it is the dependency structure
   of the whole factorization, and every later concept (supernodes, multifrontal
   fronts, parallelism) is a computation organized on top of this tree.
3. **Fill-reducing orderings.** Because fill-in depends entirely on the order variables
   are eliminated in, and finding the fill-minimizing order is NP-hard, practical solvers
   use three heuristic families: approximate minimum degree (AMD, a greedy "eliminate
   the cheapest node next" heuristic), nested dissection (recursively split the graph
   with a small separator, order the two halves before the separator — this is the one
   with provable asymptotic bounds on 2D and 3D grids, usually computed by METIS), and
   reverse Cuthill-McKee (RCM, a bandwidth-reducing ordering from breadth-first search,
   good for banded solvers but not a fill-minimizer in the same sense as AMD or nested
   dissection).
4. **Symbolic and numeric factorization.** Because the fill pattern depends only on the
   graph, not on the numeric values (true for Cholesky and, with caveats, for LU with a
   fixed pivot sequence), solvers split the work: a symbolic factorization pass computes
   where the nonzeros will land and allocates storage once, then a numeric factorization
   pass fills in the actual numbers. This split is why sparse solvers can reuse the
   symbolic phase across multiple matrices that share a sparsity pattern (repeated
   time-steps, Newton iterations) at close to zero extra cost.
5. **Supernodal and multifrontal organization.** Both are ways to turn the elimination
   tree into blocks of dense arithmetic so the factorization can call fast dense kernels
   (Level-3 BLAS) instead of scalar sparse operations. A supernode is a group of
   consecutive columns with an (almost) identical nonzero pattern, factored together as
   one dense block. The multifrontal method goes further: it associates a small dense
   "frontal matrix" with each node of the elimination tree, factors it, and passes an
   "update matrix" (the Schur complement contribution) up to the parent — turning the
   whole sparse factorization into a tree of independent dense updates, which is also
   the natural unit of parallel work.
6. **Pivoting and parallel solvers for the general (unsymmetric, indefinite, or
   ill-conditioned) case.** Symmetric positive-definite problems can fix the pivot order
   from the graph alone (Cholesky never needs numerical pivoting for stability). General
   unsymmetric or indefinite matrices cannot: threshold pivoting relaxes partial pivoting
   to allow choices that preserve sparsity, and static pivoting fixes the pivot order
   from the graph up front and repairs any resulting instability afterward with
   iterative refinement, so the ordering and the parallel structure decided in layers 3–5
   survive unchanged. The named production solvers (SuperLU, MUMPS, PARDISO, CHOLMOD,
   UMFPACK) are specific engineering choices along these axes: symmetric vs. unsymmetric
   input, multifrontal vs. supernodal, and shared- vs. distributed-memory parallelism.

Each layer answers the question the one above raises: storage formats make "store only
the nonzeros" concrete; the elimination graph explains why sparsity does not survive
factorization for free; fill-reducing orderings ask which elimination order hurts
least; the symbolic/numeric split asks how much of that answer can be computed once
and reused; supernodes and multifrontal fronts ask how to get dense-matrix speed out of
a sparse computation; and pivoting plus parallel engineering asks what to do when the
matrix is not symmetric positive definite, and how to use many cores.

## Unknown Unknowns

- **Fill-in is a property of the graph and the order, not of "how sparse" the matrix
  is.** Two matrices with the same nonzero count can factor into a nearly-sparse factor
  or a nearly-dense one, purely from which variable graph and elimination order is
  used. See Misconception 1 and the arrowhead experiment below, where reordering the
  identical matrix changes fill-in from 21 new edges to 0.
- **The elimination tree, not the matrix, is what multifrontal and supernodal methods
  parallelize over.** Independent subtrees factor concurrently; the critical path
  through parallel sparse Cholesky is the tree's height, not its node count. A wide,
  shallow tree (nested dissection tends to produce this) parallelizes far better than a
  tall, thin one (poorly-ordered elimination), for the same matrix.
- **Symbolic factorization for LU is not exact the way it is for Cholesky.** For
  symmetric positive-definite matrices, the graph-only symbolic phase predicts the
  exact nonzero pattern. For unsymmetric matrices with numerical pivoting, the pivot
  sequence can change at runtime, so the symbolic prediction is only an upper bound
  (conservative allocation). Static pivoting trades a little numerical freedom to get
  exactness back.
- **Memory, not flops, is usually the binding constraint in practice.** Fill-in
  determines memory; memory determines whether the factor fits in cache/RAM; once it
  does not, memory bandwidth (not FLOP count) sets wall-clock time. This is why nested
  dissection's fill-in bound, not just its flop bound, is often the number that
  matters, and why "the matrix fits in RAM but the factor does not" is a common
  failure with no accuracy symptom — it just runs out of memory or thrashes.
- **The 2D-vs-3D nested dissection gap compounds, it does not just shift.** On a 2D
  grid of n nodes, nested dissection gives O(n log n) fill and O(n^1.5) flops. On a 3D
  grid, separators are 2D surfaces instead of 1D curves, changing the bounds to
  O(n^(4/3)) fill and O(n^2) flops. Practitioners who have only worked in 2D (image-grid
  Poisson solves, 2D FEM) routinely underestimate how much worse 3D factorization is.
- **The choice between a direct and an iterative solver is not "sparse matrix therefore
  iterative."** Direct methods give an exact (to round-off) factorization reusable
  across many right-hand sides for the cost of one triangular solve each. Iterative
  methods (CG, GMRES with a preconditioner) avoid the fill-in memory blowup but must be
  re-run for every new right-hand side and may not converge without a good
  preconditioner. The deciding factor is whether fill-in is affordable, not whether the
  matrix "looks sparse."
- **A solver name is not a single algorithm.** SuperLU, MUMPS, PARDISO, CHOLMOD, and
  UMFPACK differ beyond branding: CHOLMOD is symmetric-positive-definite only
  (Cholesky); the others handle general unsymmetric matrices but differ in whether they
  are multifrontal (MUMPS) or supernodal (SuperLU, UMFPACK, PARDISO), and in memory
  model (MUMPS and PARDISO support distributed-memory parallelism; SuperLU and UMFPACK
  are primarily shared-memory or serial, though SuperLU_DIST is the distributed
  variant). Picking one by reputation instead of by problem shape is a common mistake.

## Common Misconceptions

**Misconception 1: "A sparse matrix stays roughly sparse after direct factorization."**
Correct statement: fill-in during elimination can make the factor dense enough that
storing or computing it becomes infeasible, and how much fill-in occurs depends almost
entirely on the elimination order, not on the original nonzero count. Concrete check:
the numpy/scipy experiment below builds a graph with one central "hub" node connected to
seven leaves (the classic worst case, an arrowhead sparsity pattern) and symbolically
eliminates it two ways. Eliminating the hub first connects all seven leaves to each
other, adding 21 fill edges out of a possible 21 (total fill, the leaf block becomes
fully dense). Eliminating the hub last adds zero fill edges, because each leaf is
eliminated while only ever touching the hub. Same matrix, same number of original
nonzeros, 21 versus 0 fill edges — order is the entire story.

**Misconception 2: "Fill-reducing orderings like AMD or nested dissection find the
absolute best order."** Correct statement: minimizing fill-in exactly is NP-hard, so
AMD and nested dissection are heuristics with no exactness guarantee on a general
graph; nested dissection has provable asymptotic bounds specifically for graphs with
good separators (such as regular 2D/3D grids and other planar-like structures), not a
proof of optimality on arbitrary sparse graphs. Concrete check: the numpy/scipy
experiment below builds a 5x5 2D grid graph (25 nodes, the nonzero pattern of a 2D
5-point finite-difference stencil) and symbolically eliminates it under two orders.
Natural row-major order produces 64 fill edges; reverse Cuthill-McKee order produces 50
— an improvement, but RCM is a bandwidth-reducer, not a dedicated fill minimizer like
AMD or nested dissection, so this comparison itself is evidence that "an ordering
heuristic" is not one interchangeable thing.

**Misconception 3: "CSR/CSC are just compressed COO — pick whichever, then convert
freely."** Correct statement: the format must match the access pattern (column-oriented
elimination wants CSC; row-oriented products want CSR), and repeated conversion between
them costs a sort each time, easy to hide inside a slow inner loop. Concrete check:
build a matrix in `scipy.sparse.coo_matrix`, then time `.tocsc()` called once versus
called inside a per-iteration loop (a common beginner mistake porting a dense algorithm
to sparse) — the loop reintroduces an O(nnz log nnz) cost every iteration.

**Misconception 4: "Symbolic factorization always tells you the exact numeric factor's
pattern."** Correct statement: this holds only when the pivot order is fixed
independent of the numeric values (Cholesky on symmetric positive-definite matrices),
not for general LU with partial pivoting, where runtime pivot choices can differ from
the graph-predicted pattern. Concrete check: factor the same unsymmetric sparse matrix
with `scipy.sparse.linalg.splu` under different `permc_spec` values and compare `nnz`
of the resulting `L` and `U` — they will not always match the graph-only prediction
when pivoting reorders rows at runtime.

**Misconception 5: "Nested dissection scales the same way in 3D as in 2D, just with a
bigger constant."** Correct statement: the exponents change, not just the constant: 2D
gives O(n^1.5) flops and O(n log n) fill; 3D gives O(n^2) flops and O(n^(4/3)) fill,
because separators become 2D surfaces instead of 1D curves. Concrete check: compare
fill counts from a small 2D grid (as above) against a same-node-count 3D grid (a 3x3x3
cube versus a 5x5 square, both n approximately 25) under the same ordering — fill-in
per added node grows faster in the 3D case, the qualitative signature of the exponent
change even at small n.

**Misconception 6: "A 'sparse' solver is automatically memory-efficient versus an
iterative one."** Correct statement: a sparse direct solver's memory use is set by
fill-in, which for a poorly-conditioned ordering or a hard-to-separate graph (long thin
3D domains) can approach dense-matrix memory use, while an iterative method's memory
stays close to the original nonzero count regardless of separator quality. "Sparse"
describes the input's storage, not a guarantee about the factor's storage.

## Rat-Holes

- **Chasing the exact minimum-fill ordering.** Minimum fill-in is NP-hard, so time spent
  seeking a provably optimal order for one matrix rarely pays off; AMD, nested
  dissection, or a hybrid, then moving on, is already close to as good as it gets.
- **Hand-implementing a multifrontal or supernodal solver from scratch.** Elimination-tree
  bookkeeping, dynamic supernode amalgamation, and numerical pivoting take production
  solvers (SuperLU, MUMPS) years to get right; a hand-rolled version teaches the graph
  concepts at small scale (as in the experiments here) but will not scale to real sizes.
- **Re-deriving nested dissection's complexity bounds from separator theorems
  (Lipton-Tarjan and successors).** The proofs are real graph theory and their own
  multi-week rat-hole; the bounds themselves (O(n^1.5)/O(n log n) in 2D,
  O(n^2)/O(n^(4/3)) in 3D) are what engineering decisions need, and can be taken as given.
- **Tuning threshold-pivoting parameters by trial and error on one matrix.** The
  sparsity-versus-stability tradeoff is problem-dependent; hand-tuning it for a single
  test matrix teaches little that transfers, versus trusting the solver's default.
- **Benchmarking direct-vs-iterative on one toy problem and generalizing the verdict.**
  The answer depends on size, pattern, conditioning, number of right-hand sides, and
  available memory; a small benchmark generalizes poorly to a million-node 3D mesh.

## High-Yield Study Prompts

1. Draw the elimination graph and elimination tree by hand for a 4x4 2D grid (16
   nodes), under natural row-major order, then under a nested-dissection-style order
   (split the grid with a separator, order each half, then the separator last). Count
   fill edges added at each step under both orders.
2. Using `scipy.sparse.csgraph.reverse_cuthill_mckee` and a symbolic elimination
   simulator (as in the experiments above), compare fill-in on a 5x5, a 9x9, and a
   13x13 grid under natural order versus RCM order. Connect the growth trend to the
   O(n log n) 2D nested-dissection fill bound.
3. Explain what changes and what stays the same between the supernodal and
   multifrontal organizations of the same elimination tree. Name one production solver
   of each kind (CHOLMOD is supernodal; MUMPS is multifrontal) and one design
   consequence of the choice.
4. Factor a small hand-built unsymmetric 8x8 sparse matrix with `scipy.sparse.linalg.splu`
   under `permc_spec='NATURAL'` versus `'COLAMD'`. Compare `nnz` of `L` and `U` in
   both cases and connect the difference to Misconception 4.
5. For a 3D 5x5x5 grid graph (125 nodes, 6-point stencil), estimate the expected fill
   using the O(n^(4/3)) 3D bound and compare it to actual fill-in from a symbolic
   elimination simulator. State in one sentence why the 3D exponent, not a bigger
   constant, explains the gap relative to a same-n 2D grid.
6. Write, without looking it up, the one-sentence job of each solver: SuperLU, MUMPS,
   PARDISO, CHOLMOD, UMFPACK. Check each against Unknown Unknown 7 above and correct
   any that conflated "unsymmetric" with "multifrontal" or "distributed-memory."
7. For a problem you know (or a synthetic 3D Poisson matrix, n=50,000+), estimate
   memory for a sparse direct factorization using the nested-dissection fill bound for
   that dimensionality, and compare it to available RAM. State whether a direct solver
   is affordable, and if not, name the iterative method and preconditioner instead.

## Experiment Log (real output)

Two small numpy/scipy experiments were run to check Misconceptions 1 and 2 directly, using
a hand-written symbolic elimination simulator (elimination = for each eliminated node,
connect all its still-remaining neighbors to each other, counting new edges as fill-in).

```
Experiment 1: 5x5 grid graph (n=25 nodes, 2D 5-point stencil pattern)
  Fill-in edges, natural row-major order : 64
  Fill-in edges, reverse Cuthill-McKee    : 50

Experiment 2: arrowhead graph (1 hub + 7 leaves, star pattern)
  Fill-in edges, eliminate hub FIRST : 21
  Fill-in edges, eliminate hub LAST  : 0
```

Experiment 1 shows that even a "smarter" ordering (RCM, a bandwidth reducer, not a
dedicated fill minimizer) only partly reduces fill-in (64 to 50 edges) on a small 2D
grid — consistent with Misconception 2's point that ordering heuristics are not
interchangeable or provably optimal. Experiment 2 shows the extreme case behind
Misconception 1: on the identical 8-node graph, elimination order alone is the
difference between 21 fill edges (complete fill of the leaf block) and 0 fill edges.
