# Theorem 5 — Referee verdict

VALID

The proof in `t5-proof.md` is complete and correct. I found no gap, no unjustified step, no missing hypothesis, and no false claim. I checked each step with the convention of the proof: the inner product is linear in the first slot and conjugate-linear in the second slot.

## Key steps checked

1. **Lemma 0.1 (double adjoint).** The chain ⟨Tu,v⟩ = ⟨u,T*v⟩ = conj⟨T*v,u⟩ = conj⟨v,Su⟩ = ⟨Su,v⟩ is correct. The step "take v = Tu − Su" gives ‖Tu − Su‖² = 0. It holds.
2. **Lemma 0.2 (matrix of T* is A*).** With aᵢⱼ = ⟨Teⱼ,eᵢ⟩ and bᵢⱼ = ⟨T*eⱼ,eᵢ⟩: ⟨Teᵢ,eⱼ⟩ = aⱼᵢ, and ⟨eᵢ,T*eⱼ⟩ = conj(bᵢⱼ). So bᵢⱼ = conj(aⱼᵢ). The indices are correct. It holds.
3. **Lemma A (Schur).** The proof takes an eigenvector u of T* (Fact 0.3, valid because V ≠ {0}). Then W = u⊥ is T-invariant: ⟨Tw,u⟩ = ⟨w,μu⟩ = conj(μ)⟨w,u⟩ = 0. The conjugation is on the correct side. dim W = n − 1 ≥ 1 in the inductive step, so the hypothesis applies. The order e₁,…,eₙ₋₁ from W, then eₙ = u, gives Teₖ ∈ span(e₁,…,eₖ) for k < n, and the condition at k = n is trivial. It holds. The lemma does not use normality, as the proof says.
4. **Lemma B.** ‖Tv‖² = ⟨v,T*Tv⟩ uses the defining identity with the pair (v, Tv). ‖T*v‖² = ⟨v,TT*v⟩ uses the identity for T* and Lemma 0.1. Normality makes the two values equal. It holds.
5. **(⇐), §3.1.** In an orthonormal eigenbasis, T has matrix D = diag(λⱼ). T* has matrix D* by Lemma 0.2. Diagonal matrices commute. The map from an operator to its matrix is injective and keeps composition, so TT* = T*T. It holds.
6. **(⇒), §3.2.** Column m of A* is (conj(a_{m,1}),…,conj(a_{m,n})). So ‖T*eₘ‖² = Σᵢ |a_{m,i}|². Upper-triangularity removes i < m. The induction hypothesis gives a_{j,m} = 0 for j < m, so Teₘ = a_{mm}eₘ and ‖Teₘ‖² = |a_{mm}|². Lemma B then forces a_{m,i} = 0 for i > m. Base case and inductive step are both correct. The result is that A is diagonal.
7. **Matrix form, §4.** With ⟨x,y⟩ = y*x: ⟨Ax,y⟩ = y*Ax = (A*y)*x = ⟨x,A*y⟩. So the adjoint of x ↦ Ax is x ↦ A*x. (⇐): UDU*(UDU*)* = UDD*U* and the reverse product is UD*DU*. These are equal. (⇒): U*U = I follows from orthonormal columns, and UU* = I follows because U is square. AU = UD, column by column, gives A = UDU*. It holds.

## Cited, not proved (acceptable)

- Fact 0 (Riesz representation, existence of T*). The theorem statement grants T*.
- Fact 0.3 (every operator on a nonzero finite-dimensional complex space has an eigenvalue, from the Fundamental Theorem of Algebra).
- dim u⊥ = n − 1, and "the operator-to-matrix map is an injective algebra homomorphism".

These are standard named facts. The proof uses each one correctly.

## Presentation notes (not gaps)

1. §3.2, base case: the text says the sum runs over all i "because a_{1i} … is defined for every column i ≥ 1 by upper-triangularity". This reason is confused. Every entry of A is defined. Upper-triangularity removes no entry from row 1. The formula is correct, so the conclusion does not change.
2. §3.2, inductive step: the phrase "row index m cannot exceed column index i if the term is to be nonzero" is a roundabout statement of a_{m,i} = 0 for i < m. It is correct.
