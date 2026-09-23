---
theorem: "Theorem 10 — Picard–Lindelöf theorem"
referee: hostile referee pass (P4)
date: 2026-09-22
---

# Verdict: VALID

The proof in `t10-proof.md` proves the statement of item 10 in `theorems.md` exactly as stated. The statement matches: same R, same M, same h (with the M = 0 case), and the same uniqueness class (C¹ solutions on [t₀ − h, t₀ + h] that stay in R). I found no gap, no unjustified step, no missing hypothesis, and no false claim.

## Key steps checked, and why each holds

1. **M and h are well defined (Section 3).** R is a product of a closed bounded interval and a closed ball, so R is compact (Heine–Borel). |f| is continuous, so the maximum M exists (Extreme Value Theorem). The case M = 0 avoids the undefined b/M. In both cases 0 < h ≤ a, so I ⊆ [t₀ − a, t₀ + a]. Holds.

2. **Lemma 0 (vector integral triangle inequality).** The proof uses u = v/|v| and linearity ⟨u, ∫g⟩ = ∫⟨u, g⟩, then Cauchy–Schwarz pointwise and monotonicity. For t < t₀ the proof writes |∫_{t₀}^{t} f| ≤ |∫_{t₀}^{t} |f||, which is correct with the orientation convention. Holds.

3. **Lemma A (ODE ⇔ integral equation).** The hypothesis φ(t) ∈ B̄(x₀, b) plus I ⊆ [t₀ − a, t₀ + a] puts (t, φ(t)) in R, so the integrand is defined and continuous (composition of continuous maps). Direction (i) ⇒ (ii) uses FTC part (b) on [t₀, t] or [t, t₀]; the reversed interval gives the same identity by the stated convention. Direction (ii) ⇒ (i) uses FTC part (a); the derivative equals a continuous function, so φ is C¹. Holds.

4. **Y is a nonempty closed subset of a Banach space (Section 5).** The constant x₀ is in Y. Closedness follows from pointwise limits and continuity of the norm. Closed in complete implies complete. Holds.

5. **T maps Y into Y (Section 5).** |(Tφ)(t) − x₀| ≤ M|t − t₀| ≤ Mh ≤ b when M > 0, because h ≤ b/M. When M = 0, f ≡ 0 on R and Tφ ≡ x₀. This is the step where the choice of h is necessary, and the proof uses it correctly. Holds.

6. **Bielecki norm equivalence (Section 6).** For t ∈ I, e^{−2Lh} ≤ e^{−2L|t−t₀|} ≤ 1, so e^{−2Lh}‖φ‖_∞ ≤ ‖φ‖_w ≤ ‖φ‖_∞. The two norms have the same Cauchy sequences and the same closed sets, so (Y, d_w) is complete. Holds.

7. **Contraction with constant 1/2 (Section 6).** For t > t₀: the integral bound gives L‖φ − ψ‖_w (e^{2L(t−t₀)} − 1)/(2L) ≤ (1/2)‖φ − ψ‖_w e^{2L(t−t₀)}. I checked the case t < t₀ myself: |φ(s) − ψ(s)| ≤ ‖φ − ψ‖_w e^{2L(t₀−s)} on [t, t₀], and ∫_t^{t₀} e^{2L(t₀−s)} ds = (e^{2L(t₀−t)} − 1)/(2L). This gives the same bound, so "symmetric" is correct. The case L = 0 is handled separately (no division by L). The constant 1/2 does not depend on h, so no smallness condition on h beyond Mh ≤ b is needed. Holds.

8. **Existence and uniqueness (Sections 7–8).** Banach's theorem applies: Y is nonempty, (Y, d_w) is complete, T: Y → Y, k = 1/2 < 1. Existence: the fixed point lies in Y, so Lemma A (ii) ⇒ (i) makes it a C¹ solution that stays in R. Uniqueness: a C¹ solution y with (t, y(t)) ∈ R is continuous with values in B̄(x₀, b), so y ∈ Y. Lemma A (i) ⇒ (ii) gives Ty = y, so y = φ*. The uniqueness class in the proof is the same class as in the statement. Holds.

## Minor remarks (not gaps; no change needed for validity)

1. **Section 2, item 3.** The text says completeness of C(I, ℝⁿ) under ‖·‖_∞ follows "consequently" from the Uniform Limit Theorem. The full argument also needs this step: a uniformly Cauchy sequence has a pointwise limit (completeness of ℝⁿ), and the convergence to that limit is uniform. This is a standard textbook fact. The proof cites it by name, so it is not a gap.

2. **Lemma A, endpoints.** At t = t₀ ± h the derivative is one-sided. FTC as stated on [α, β] already covers one-sided derivatives at the endpoints. The proof applies FTC with base point t₀ inside I instead of the left endpoint α. The difference is the constant ∫_α^{t₀}, so the derivative is the same. The proof leaves this step implicit. It is routine.

3. **Uniqueness scope.** The proof shows uniqueness only among solutions whose graph stays in R. This is exactly what the theorem claims. The proof does not claim more, so no issue follows.
