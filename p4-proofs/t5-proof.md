# Theorem 5 — Spectral Theorem for Normal Operators

## Statement

Let V be a finite-dimensional complex inner product space with dim V = n ≥ 1.
Let T: V → V be linear, and let T* be its **adjoint**, the unique linear map
satisfying

  ⟨Tu, v⟩ = ⟨u, T*v⟩   for all u, v ∈ V.

Then T is **normal**, i.e. T T* = T* T, if and only if V has an orthonormal
basis consisting of eigenvectors of T.

**Matrix form.** A ∈ ℂⁿˣⁿ satisfies A A* = A* A if and only if A = U D U*
for some unitary U ∈ ℂⁿˣⁿ and some diagonal D ∈ ℂⁿˣⁿ.

Throughout, ⟨·,·⟩ is linear in the first argument and conjugate-linear in the
second, and ‖v‖² = ⟨v,v⟩. All vector spaces are over ℂ and all bases have
n = dim V vectors.

---

## 0. Preliminaries (cited standard results)

**Fact 0 (Existence and uniqueness of the adjoint).** For a finite-dimensional
complex inner product space V and a linear map T: V → V, there is a unique
linear map T*: V → V with ⟨Tu,v⟩ = ⟨u,T*v⟩ for all u, v ∈ V. This is a
standard consequence of the **Riesz Representation Theorem** (for each fixed
v, the map u ↦ ⟨Tu,v⟩ is a linear functional on V, hence equals ⟨u,w⟩ for a
unique w = T*v; linearity of T* in v follows from linearity of the inner
product and uniqueness of Riesz representatives). The problem statement
already grants T* this defining property, so we take Fact 0 as given.

**Lemma 0.1 (Double adjoint).** (T*)* = T.

*Proof.* Write S = (T*)*, so ⟨T*u,v⟩ = ⟨u,Sv⟩ for all u,v. We show
⟨Tu,v⟩ = ⟨Su,v⟩ for all u,v, which forces T = S. For all u,v:
  ⟨Tu,v⟩ = ⟨u,T*v⟩ (definition of T*)
  ⟨u,T*v⟩ = conj⟨T*v,u⟩ (conjugate symmetry)
  ⟨T*v,u⟩ = ⟨v,Su⟩ (definition of S = (T*)*, applied to the pair (v,u))
  ⟨v,Su⟩ = conj⟨Su,v⟩ (conjugate symmetry).
Chaining, ⟨Tu,v⟩ = conj(conj⟨Su,v⟩) = ⟨Su,v⟩ for all u,v. Fix u; then
⟨Tu − Su, v⟩ = 0 for every v ∈ V, and taking v = Tu − Su gives
‖Tu − Su‖² = 0, so Tu = Su. Since u was arbitrary, T = S = (T*)*. ∎

**Lemma 0.2 (Matrix of the adjoint in an orthonormal basis).** Let
e₁,…,eₙ be an orthonormal basis of V and let A = [aᵢⱼ] be the matrix of T in
this basis, defined by T eⱼ = Σᵢ aᵢⱼ eᵢ, so that aᵢⱼ = ⟨Teⱼ,eᵢ⟩. Then the
matrix B = [bᵢⱼ] of T* in the same basis satisfies bᵢⱼ = conj(aⱼᵢ); that is,
B = A* (conjugate transpose).

*Proof.* Because the basis is orthonormal, the coefficient of eᵢ in the
expansion of any vector w is ⟨w,eᵢ⟩. Hence bᵢⱼ = ⟨T*eⱼ,eᵢ⟩. By the defining
property of the adjoint applied to u = eᵢ, v = eⱼ:
  ⟨Teᵢ,eⱼ⟩ = ⟨eᵢ,T*eⱼ⟩.
The right side equals conj⟨T*eⱼ,eᵢ⟩ = conj(bᵢⱼ) by conjugate symmetry, and
the left side is aⱼᵢ by definition of A. So aⱼᵢ = conj(bᵢⱼ), i.e.
bᵢⱼ = conj(aⱼᵢ). ∎

**Fact 0.3 (Existence of an eigenvalue, via the Fundamental Theorem of
Algebra).** Every linear operator S on a nonzero finite-dimensional complex
vector space W has an eigenvalue. *Sketch:* the characteristic polynomial
det(S − λI) is a polynomial in λ of degree dim W ≥ 1 with complex
coefficients; by the **Fundamental Theorem of Algebra**, ℂ is algebraically
closed, so this polynomial has a root λ₀ ∈ ℂ, and S − λ₀I is then singular,
giving a nonzero v with Sv = λ₀v. (Equivalently one may run Axler's
determinant-free argument using the minimal polynomial, which also only
needs that ℂ is algebraically closed.) This is a standard fact from
introductory linear algebra and is cited here by name.

---

## 1. Lemma A — Schur (unitary) triangularization

**Lemma A.** For every linear operator T on a finite-dimensional complex
inner product space V with dim V = n ≥ 1, there is an orthonormal basis
e₁,…,eₙ of V such that the matrix of T in this basis is upper triangular,
i.e. T eₖ ∈ span(e₁,…,eₖ) for every k = 1,…,n.

*Proof.* Induction on n.

*Base case n = 1.* Any unit vector e₁ (obtained from any nonzero vector by
normalizing) is an orthonormal basis, and the 1×1 matrix of T is trivially
upper triangular.

*Inductive step.* Assume the lemma holds in every complex inner product
space of dimension n − 1, and let dim V = n ≥ 2. By Fact 0.3 applied to
T* (a nonzero, finite-dimensional operator, here on V itself), T* has an
eigenvalue μ with eigenvector u ≠ 0; normalize so ‖u‖ = 1.

Let W = u⊥ = { w ∈ V : ⟨w,u⟩ = 0 }, an (n−1)-dimensional subspace of V (it
is the orthogonal complement of the 1-dimensional span(u), by the standard
dimension formula dim W + dim span(u) = dim V for an orthogonal complement).

*Claim: W is T-invariant.* For w ∈ W,
  ⟨Tw,u⟩ = ⟨w,T*u⟩ = ⟨w,μu⟩ = conj(μ)⟨w,u⟩ = conj(μ)·0 = 0,
using the defining property of T* and conjugate-linearity of ⟨·,·⟩ in the
second slot. Hence Tw ∈ u⊥ = W, proving the claim.

W, with the inner product inherited from V, is an (n−1)-dimensional complex
inner product space, and T|_W : W → W is a well-defined linear operator (by
the invariance just shown). By the inductive hypothesis, W has an
orthonormal basis e₁,…,e_{n−1} such that T eₖ = T|_W eₖ ∈ span(e₁,…,eₖ) for
each k = 1,…,n−1.

Set eₙ = u. Since u is a unit vector orthogonal to W = span(e₁,…,e_{n−1})
(by construction of W and orthonormality of e₁,…,e_{n−1} inside W), the list
e₁,…,e_{n−1},eₙ is an orthonormal basis of V (it is orthonormal by
construction, and has n = dim V vectors, hence is a basis).

Finally check T is upper triangular in this basis: for k = 1,…,n−1,
T eₖ ∈ span(e₁,…,eₖ) as shown; for k = n, the condition T eₙ ∈
span(e₁,…,eₙ) = V holds trivially. This completes the induction. ∎

(Lemma A is the standard **Schur triangularization theorem**; it is proved
here in full because it is the engine of the harder direction of Theorem 5,
and it does not itself assume normality of T.)

---

## 2. Lemma B — normal operators preserve norms under T and T*

**Lemma B.** If T is normal (T*T = TT*), then ‖Tv‖ = ‖T*v‖ for every v ∈ V.

*Proof.* For any v ∈ V, using the defining property of the adjoint twice:
  ‖Tv‖² = ⟨Tv,Tv⟩ = ⟨v,T*Tv⟩,
and, applying the defining property to the operator T* (using
(T*)* = T from Lemma 0.1),
  ‖T*v‖² = ⟨T*v,T*v⟩ = ⟨v,(T*)*T*v⟩ = ⟨v,TT*v⟩.
Since T is normal, T*T = TT*, so ⟨v,T*Tv⟩ = ⟨v,TT*v⟩, i.e. ‖Tv‖² = ‖T*v‖²,
and since norms are nonnegative real numbers, ‖Tv‖ = ‖T*v‖. ∎

---

## 3. Proof of Theorem 5

### 3.1 (⇐) Orthonormal eigenbasis implies normal

Suppose e₁,…,eₙ is an orthonormal basis of V with T eⱼ = λⱼ eⱼ for scalars
λⱼ ∈ ℂ, j = 1,…,n. In this basis the matrix of T is the diagonal matrix
D = diag(λ₁,…,λₙ) (since T eⱼ = λⱼ eⱼ + 0·(other basis vectors)).

By Lemma 0.2, the matrix of T* in this same orthonormal basis is D* =
conjugate-transpose of D, and the conjugate transpose of a diagonal matrix
is again diagonal, namely D* = diag(conj(λ₁),…,conj(λₙ)).

Two diagonal matrices always commute: D D* = diag(λⱼ conj(λⱼ)) =
diag(|λⱼ|²) = diag(conj(λⱼ) λⱼ) = D* D. Since the map "operator ↦ its matrix
in a fixed basis" is an algebra isomorphism (in particular it preserves
composition/multiplication and is injective), D D* = D* D as matrices
implies T T* = T* T as operators. Hence T is normal.

### 3.2 (⇒) Normal implies orthonormal eigenbasis

Suppose T is normal. By Lemma A, choose an orthonormal basis e₁,…,eₙ of V
such that the matrix A = [aⱼₖ] of T in this basis is upper triangular:

  T eₖ = Σ_{j=1}^{k} aⱼₖ eⱼ  for k = 1,…,n  (aⱼₖ = 0 whenever j > k).

We prove by induction on m = 1,…,n that row m of A has no entries strictly
to the right of the diagonal, i.e. a_{m,k} = 0 for every k > m. Once this is
established for all m, A is diagonal, so T eₘ = a_{mm} eₘ for every m, i.e.
e₁,…,eₙ is an orthonormal basis of eigenvectors, proving the theorem.

**Base case m = 1.** Since the basis is orthonormal, ‖T e₁‖² = |a₁₁|²
(from T e₁ = a₁₁e₁, the only term with k = 1 in the triangular expansion).

By Lemma 0.2, T* has matrix A* in this basis, with (A*)ᵢⱼ = conj(aⱼᵢ).
Hence, expanding T* e₁ in the orthonormal basis,
  T* e₁ = Σ_{i=1}^{n} (A*)_{i1} e_i = Σ_{i=1}^{n} conj(a_{1i}) e_i,
where the sum runs over **all** i = 1,…,n because a_{1i} (row 1) is defined
for every column i ≥ 1 by upper-triangularity (row index 1 never exceeds any
column index). By orthonormality,
  ‖T* e₁‖² = Σ_{i=1}^{n} |a_{1i}|².

By Lemma B (normality), ‖T e₁‖ = ‖T* e₁‖, so
  |a₁₁|² = Σ_{i=1}^{n} |a_{1i}|²  ⟹  Σ_{i=2}^{n} |a_{1i}|² = 0
  ⟹  a_{1i} = 0 for i = 2,…,n.
This is exactly the claim for m = 1: row 1 has zero entries to the right of
the diagonal.

**Inductive step.** Fix m with 2 ≤ m ≤ n and assume the claim holds for all
rows 1,…,m−1, i.e. a_{j,k} = 0 whenever j < m and k > j. In particular,
taking k = m > j for each j = 1,…,m−1 gives a_{j,m} = 0 for every
j = 1,…,m−1.

Consequently, in the triangular expansion T eₘ = Σ_{j=1}^{m} a_{jm} eⱼ, all
terms with j < m vanish by the previous paragraph, leaving
  T eₘ = a_{mm} eₘ,
so by orthonormality ‖T eₘ‖² = |a_{mm}|².

As before, T* eₘ = Σ_i (A*)_{i,m} e_i = Σ_i conj(a_{m,i}) e_i, and by
upper-triangularity a_{m,i} = 0 automatically for i < m (row index m cannot
exceed column index i if the term is to be nonzero), so the sum runs over
i = m,…,n:
  T* eₘ = Σ_{i=m}^{n} conj(a_{m,i}) e_i,
  ‖T* eₘ‖² = Σ_{i=m}^{n} |a_{m,i}|².

By Lemma B, ‖T eₘ‖ = ‖T* eₘ‖, so
  |a_{mm}|² = Σ_{i=m}^{n} |a_{m,i}|²  ⟹  Σ_{i=m+1}^{n} |a_{m,i}|² = 0
  ⟹  a_{m,i} = 0 for i = m+1,…,n,
which is the claim for row m.

By induction, a_{j,k} = 0 for every pair j < k, so A is diagonal:
T eⱼ = a_{jj} eⱼ for every j = 1,…,n. Thus e₁,…,eₙ is an orthonormal basis
of V consisting of eigenvectors of T. ∎

This completes the proof of the operator form of Theorem 5: T is normal if
and only if V has an orthonormal basis of eigenvectors of T.

---

## 4. Matrix form

**Claim.** A ∈ ℂⁿˣⁿ satisfies A A* = A* A if and only if A = U D U* for some
unitary U ∈ ℂⁿˣⁿ and diagonal D ∈ ℂⁿˣⁿ.

*Proof.* Let V = ℂⁿ with the standard inner product ⟨x,y⟩ = y* x (so that
the adjoint of the operator "multiply by A" is exactly "multiply by A*",
the conjugate transpose — this is the standard fact that, in the standard
basis, which is orthonormal for the standard inner product, the matrix of
an operator's adjoint is the conjugate transpose of the operator's matrix;
this is precisely Lemma 0.2 specialized to the standard orthonormal basis).
Let T: V → V be the operator T(x) = Ax; then T* is multiplication by A*, and
T is normal iff A A* = A* A.

(⇐) If A = U D U* with U unitary (U*U = UU* = I) and D diagonal, then
  A A* = U D U* (U D U*)* = U D U* U D* U* = U D D* U*  (using U*U = I),
  A* A = U D* U* U D U* = U D* D U*  (using U*U = I).
Since D is diagonal, D and D* are both diagonal and diagonal matrices
commute (as in §3.1), so D D* = D* D, hence A A* = A* A. So A is normal.

(⇒) Suppose A A* = A* A, i.e. T (multiplication by A) is normal on
V = ℂⁿ with the standard inner product. By the operator form of Theorem 5
(§3), ℂⁿ has an orthonormal basis u₁,…,uₙ of eigenvectors of T, i.e.
A uⱼ = λⱼ uⱼ for scalars λⱼ ∈ ℂ. Let U be the n×n matrix whose j-th column
is uⱼ, and let D = diag(λ₁,…,λₙ). Since u₁,…,uₙ are orthonormal with
respect to the standard inner product, U is **unitary**: (U*U)ᵢⱼ =
uᵢ*uⱼ = ⟨uⱼ,uᵢ⟩ = δᵢⱼ (Kronecker delta), i.e. U*U = I, and for a square
matrix this also gives UU* = I.

Comparing columns, A U = U D, because the j-th column of A U is A uⱼ = λⱼ uⱼ,
which is exactly λⱼ times the j-th column of U, i.e. the j-th column of U D.
Since U is invertible (U* = U⁻¹), right-multiplying A U = U D by U* gives
  A = U D U*.
This is the required unitary diagonalization. ∎

---

## 5. Summary of results used

- **Riesz Representation Theorem** — existence/uniqueness of the adjoint
  (Fact 0).
- **Fundamental Theorem of Algebra** — every nonconstant complex polynomial
  has a root; used to guarantee every operator on a nonzero finite-dimensional
  complex vector space has an eigenvalue (Fact 0.3).
- **Schur triangularization theorem** — every operator on a finite-dimensional
  complex inner product space is upper-triangular in some orthonormal basis
  (Lemma A, proved in full above by induction using Fact 0.3 applied to T*
  and the orthogonal-complement invariant-subspace construction).
- Elementary facts about inner products (conjugate symmetry, orthonormal
  expansion coefficients ⟨w,eᵢ⟩, orthogonal complements and dimension
  counting) and about diagonal matrices commuting.

No result beyond these standard, named facts is assumed. Every lemma used in
the main argument (Lemma 0.1, Lemma 0.2, Lemma A, Lemma B) is proved in full
above from these standard facts, and both directions of the operator
statement and the matrix-form corollary are proved in full. No part of
Theorem 5 was skipped.
