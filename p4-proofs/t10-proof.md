---
theorem: "Theorem 10 — Picard–Lindelöf theorem"
status: complete
---

# Theorem 10 — Picard–Lindelöf theorem

## 1. Statement

Let t₀ ∈ ℝ, x₀ ∈ ℝⁿ, a > 0, b > 0. Let R = [t₀ − a, t₀ + a] × B̄(x₀, b), where B̄(x₀, b) is the closed Euclidean ball of radius b around x₀ in ℝⁿ.

Let f : R → ℝⁿ be continuous. Assume f is Lipschitz in x, uniformly in t: there is L ≥ 0 with

|f(t, x) − f(t, y)| ≤ L|x − y| for all (t, x), (t, y) ∈ R.

Let M = max_R |f|. Let h = min(a, b/M) if M > 0, and h = a if M = 0.

Claim: the initial value problem

x′(t) = f(t, x(t)),  x(t₀) = x₀

has exactly one solution x : [t₀ − h, t₀ + h] → ℝⁿ. This solution is C¹, and (t, x(t)) ∈ R for every t in the interval.

Throughout, |·| is the Euclidean norm on ℝⁿ (or on ℝ, where it is the absolute value). Write I = [t₀ − h, t₀ + h].

## 2. Named results used

The proof cites four standard results by name. It states each one so the proof is self-contained.

1. **Extreme Value Theorem (Weierstrass).** A continuous real-valued function on a nonempty compact set attains a maximum on that set.
2. **Fundamental Theorem of Calculus**, both parts, applied componentwise to ℝⁿ-valued functions of one real variable:
   (a) If g : [α, β] → ℝⁿ is continuous, then G(t) = ∫_α^t g(s) ds is differentiable on [α, β], with G′(t) = g(t).
   (b) If G : [α, β] → ℝⁿ is C¹, then G(t) − G(α) = ∫_α^t G′(s) ds.
3. **Uniform Limit Theorem.** A uniform limit of continuous functions is continuous. Consequently, C(I, ℝⁿ), equipped with the sup norm ‖φ‖_∞ = sup_{t∈I} |φ(t)|, is a Banach space (a complete normed vector space).
4. **Banach Fixed-Point Theorem (contraction mapping principle).** Let (X, d) be a nonempty complete metric space, and let T : X → X satisfy d(Tφ, Tψ) ≤ k · d(φ, ψ) for all φ, ψ ∈ X, for some fixed k with 0 ≤ k < 1. Then T has exactly one fixed point in X.

The proof also uses one elementary integral inequality, proved below for completeness:

**Lemma 0 (triangle inequality for integrals).** For continuous g : [α, β] → ℝⁿ, |∫_α^β g(s) ds| ≤ ∫_α^β |g(s)| ds.

*Proof.* Let v = ∫_α^β g(s) ds. If v = 0 the claim is trivial. Otherwise let u = v/|v|, a unit vector. Then |v| = ⟨u, v⟩ = ∫_α^β ⟨u, g(s)⟩ ds ≤ ∫_α^β |u| |g(s)| ds = ∫_α^β |g(s)| ds, using the Cauchy–Schwarz inequality ⟨u, g(s)⟩ ≤ |u||g(s)| pointwise, and monotonicity of the integral. ∎

## 3. R is compact, M and h are well defined and positive

R = [t₀ − a, t₀ + a] × B̄(x₀, b) is a product of a closed bounded interval and a closed bounded ball in ℝⁿ, hence closed and bounded in ℝ^{n+1}, hence compact (Heine–Borel). f is continuous on R, so |f| is continuous on R, so by the Extreme Value Theorem M = max_R |f| exists and is a finite nonnegative number. This justifies the definition of M in the statement.

For h: if M = 0, h = a > 0 by hypothesis. If M > 0, h = min(a, b/M); both a and b/M are strictly positive, so h > 0. In either case h > 0 and h ≤ a, so I = [t₀ − h, t₀ + h] ⊆ [t₀ − a, t₀ + a].

## 4. Lemma A — equivalence with an integral equation

**Lemma A.** Let φ : I → ℝⁿ be continuous with φ(t) ∈ B̄(x₀, b) for every t ∈ I. Then the following are equivalent:

(i) φ is C¹ on I, φ(t₀) = x₀, φ′(t) = f(t, φ(t)) for every t ∈ I.

(ii) φ(t) = x₀ + ∫_{t₀}^{t} f(s, φ(s)) ds for every t ∈ I.

(Here ∫_{t₀}^{t} for t < t₀ means −∫_{t}^{t₀}, as usual.)

*Proof.* Since φ(t) ∈ B̄(x₀, b) for all t ∈ I and I ⊆ [t₀ − a, t₀ + a] (Section 3), the point (t, φ(t)) lies in R for every t ∈ I, so f(t, φ(t)) is defined for every t ∈ I. The map t ↦ (t, φ(t)) is continuous (φ is continuous), and f is continuous on R, so the composite map t ↦ f(t, φ(t)) is continuous on I.

(i) ⇒ (ii): φ is C¹ with φ′(t) = f(t, φ(t)). By Fundamental Theorem of Calculus, part (b), applied on [t₀, t] or [t, t₀]: φ(t) − φ(t₀) = ∫_{t₀}^{t} φ′(s) ds = ∫_{t₀}^{t} f(s, φ(s)) ds. Since φ(t₀) = x₀, this is (ii).

(ii) ⇒ (i): The integrand s ↦ f(s, φ(s)) is continuous on I, as shown above. By Fundamental Theorem of Calculus, part (a), the function t ↦ ∫_{t₀}^{t} f(s, φ(s)) ds is differentiable on I with derivative f(t, φ(t)), and this derivative is continuous (it equals the continuous map t ↦ f(t, φ(t))). Hence φ, which by (ii) equals x₀ plus this function, is differentiable with φ′(t) = f(t, φ(t)), and φ′ is continuous, so φ is C¹. Setting t = t₀ in (ii) gives φ(t₀) = x₀ + 0 = x₀. ∎

Lemma A shows: a C¹ solution x of the IVP on I with (t, x(t)) ∈ R for all t ∈ I is exactly the same object as a continuous function φ : I → B̄(x₀, b) satisfying the integral equation (ii). The rest of the proof finds exactly one such φ.

## 5. The space Y and the Picard operator T

Define

Y = { φ ∈ C(I, ℝⁿ) : φ(t) ∈ B̄(x₀, b) for every t ∈ I }.

**Y is nonempty.** The constant function φ ≡ x₀ belongs to Y.

**Y is closed in (C(I, ℝⁿ), ‖·‖_∞).** Suppose φ_k ∈ Y and φ_k → φ uniformly on I. For each fixed t ∈ I, φ_k(t) → φ(t) and |φ_k(t) − x₀| ≤ b for every k, so |φ(t) − x₀| ≤ b by continuity of the norm. Hence φ ∈ Y.

By the Uniform Limit Theorem, (C(I, ℝⁿ), ‖·‖_∞) is complete. A closed subset of a complete metric space is itself complete in the induced metric. Hence **(Y, ‖·‖_∞) is a complete metric space.**

Define the Picard operator T on Y by

(Tφ)(t) = x₀ + ∫_{t₀}^{t} f(s, φ(s)) ds, t ∈ I.

**T is well defined on Y and Tφ ∈ C(I, ℝⁿ).** For φ ∈ Y, the integrand s ↦ f(s, φ(s)) is continuous on I, by the same composition argument as in the proof of Lemma A ((t, φ(t)) ∈ R for all t ∈ I since φ ∈ Y). Hence (Tφ)(t) is a well-defined integral of a continuous function, and t ↦ (Tφ)(t) is continuous (indeed C¹, by Fundamental Theorem of Calculus part (a), but continuity is all that is needed here).

**T maps Y into Y.** Fix φ ∈ Y and t ∈ I. By Lemma 0 and |f| ≤ M on R,

|(Tφ)(t) − x₀| = |∫_{t₀}^{t} f(s, φ(s)) ds| ≤ |∫_{t₀}^{t} |f(s, φ(s))| ds| ≤ M |t − t₀| ≤ M h.

If M = 0, then f ≡ 0 on R (the maximum of the nonnegative function |f| is 0), so (Tφ)(t) = x₀ for every t, and x₀ ∈ B̄(x₀, b) since b > 0. If M > 0, then h ≤ b/M, so M h ≤ b. In both cases |(Tφ)(t) − x₀| ≤ b, so Tφ(t) ∈ B̄(x₀, b) for every t ∈ I, i.e. Tφ ∈ Y.

By Lemma A, a fixed point of T in Y is exactly a solution of the IVP on I staying in R, and conversely. It remains to show T has exactly one fixed point in Y.

## 6. T is a contraction (Bielecki weighted norm)

Define, for φ ∈ C(I, ℝⁿ), the weighted norm

‖φ‖_w = sup_{t∈I} |φ(t)| e^{−2L|t−t₀|}.

**‖·‖_w is a norm on C(I, ℝⁿ), equivalent to ‖·‖_∞.** For every t ∈ I, |t − t₀| ≤ h, so 1 ≥ e^{−2L|t−t₀|} ≥ e^{−2Lh} > 0. Hence for every φ,

e^{−2Lh} ‖φ‖_∞ ≤ ‖φ‖_w ≤ ‖φ‖_∞.

This two-sided bound shows ‖·‖_w and ‖·‖_∞ induce the same topology on C(I, ℝⁿ) (the same convergent sequences, the same closed sets, the same Cauchy sequences). In particular (C(I, ℝⁿ), ‖·‖_w) is complete, and Y — already shown closed under ‖·‖_∞ — is also closed under ‖·‖_w. So **(Y, ‖·‖_w) is a complete metric space**, with metric d_w(φ, ψ) = ‖φ − ψ‖_w.

**Claim: ‖Tφ − Tψ‖_w ≤ (1/2) ‖φ − ψ‖_w for all φ, ψ ∈ Y.**

Fix φ, ψ ∈ Y and t ∈ I. If t = t₀, (Tφ)(t) − (Tψ)(t) = 0, and the desired pointwise bound holds trivially. Take t > t₀ (the case t < t₀ is symmetric, with the roles of t₀ and t exchanged and |s − t₀| = t₀ − s). Using the Lipschitz hypothesis on f and Lemma 0:

|(Tφ)(t) − (Tψ)(t)| = |∫_{t₀}^{t} [f(s, φ(s)) − f(s, ψ(s))] ds| ≤ ∫_{t₀}^{t} L |φ(s) − ψ(s)| ds.

For s ∈ [t₀, t], |s − t₀| = s − t₀, so |φ(s) − ψ(s)| = |φ(s) − ψ(s)| e^{−2L(s−t₀)} · e^{2L(s−t₀)} ≤ ‖φ − ψ‖_w e^{2L(s−t₀)}, directly from the definition of ‖·‖_w. Hence

∫_{t₀}^{t} L |φ(s) − ψ(s)| ds ≤ L ‖φ − ψ‖_w ∫_{t₀}^{t} e^{2L(s−t₀)} ds.

If L = 0, the right side is 0, and the claimed pointwise bound |(Tφ)(t) − (Tψ)(t)| ≤ (1/2)‖φ − ψ‖_w e^{2L(t−t₀)} holds trivially (0 ≤ anything nonnegative). If L > 0, evaluate the integral:

∫_{t₀}^{t} e^{2L(s−t₀)} ds = [e^{2L(s−t₀)}/(2L)]_{t₀}^{t} = (e^{2L(t−t₀)} − 1)/(2L) ≤ e^{2L(t−t₀)}/(2L),

so

L ‖φ − ψ‖_w ∫_{t₀}^{t} e^{2L(s−t₀)} ds ≤ L ‖φ − ψ‖_w · e^{2L(t−t₀)}/(2L) = (1/2) ‖φ − ψ‖_w e^{2L(t−t₀)}.

In either case (L = 0 or L > 0),

|(Tφ)(t) − (Tψ)(t)| ≤ (1/2) ‖φ − ψ‖_w e^{2L(t−t₀)} = (1/2) ‖φ − ψ‖_w e^{2L|t−t₀|}.

Multiplying both sides by e^{−2L|t−t₀|} gives

|(Tφ)(t) − (Tψ)(t)| e^{−2L|t−t₀|} ≤ (1/2) ‖φ − ψ‖_w.

The symmetric argument gives the same bound for t < t₀, and t = t₀ was already trivial. Taking the supremum over t ∈ I:

‖Tφ − Tψ‖_w = sup_{t∈I} |(Tφ)(t) − (Tψ)(t)| e^{−2L|t−t₀|} ≤ (1/2) ‖φ − ψ‖_w.

This proves the claim: T : Y → Y is a contraction with constant k = 1/2 < 1 on the complete metric space (Y, d_w).

## 7. Existence and uniqueness of the fixed point

By the Banach Fixed-Point Theorem, applied to T : Y → Y on the complete metric space (Y, d_w) with contraction constant k = 1/2, T has exactly one fixed point φ* ∈ Y:

φ*(t) = x₀ + ∫_{t₀}^{t} f(s, φ*(s)) ds for every t ∈ I,

and no other φ ∈ Y satisfies Tφ = φ.

## 8. Conclusion: exactly one C¹ solution of the IVP

Set x = φ*. Since φ* ∈ Y, x is continuous on I and x(t) ∈ B̄(x₀, b) for every t ∈ I, so (t, x(t)) ∈ R for every t ∈ I (Section 3 gives I ⊆ [t₀ − a, t₀ + a]). Since x satisfies the integral equation (ii) of Lemma A, that lemma's (ii) ⇒ (i) direction gives: x is C¹ on I, x(t₀) = x₀, and x′(t) = f(t, x(t)) for every t ∈ I. So x is a solution of the stated form.

**Uniqueness.** Suppose y : I → ℝⁿ is any C¹ solution of the IVP with (t, y(t)) ∈ R for every t ∈ I. Since (t, y(t)) ∈ R and R = [t₀ − a, t₀ + a] × B̄(x₀, b), this means y(t) ∈ B̄(x₀, b) for every t ∈ I; together with y being continuous (C¹ implies continuous), this gives y ∈ Y. By Lemma A, (i) ⇒ (ii) applied to y: y(t) = x₀ + ∫_{t₀}^{t} f(s, y(s)) ds for every t ∈ I, i.e. Ty = y. So y is a fixed point of T in Y. By Section 7, T has exactly one fixed point in Y, namely φ* = x. Hence y = x.

This shows the IVP has exactly one solution x : [t₀ − h, t₀ + h] → ℝⁿ with the stated properties: x is C¹, x(t₀) = x₀, x′(t) = f(t, x(t)) for all t ∈ [t₀ − h, t₀ + h], and (t, x(t)) ∈ R for all t in that interval. ∎

## 9. Summary of external results cited

- Extreme Value Theorem (Weierstrass) — Section 3, to obtain M.
- Heine–Borel theorem — Section 3, to obtain compactness of R.
- Fundamental Theorem of Calculus, parts (a) and (b) — Lemma A and the definition/well-definedness of T.
- Uniform Limit Theorem — Section 5, to get completeness of C(I, ℝⁿ) under the sup norm.
- Banach Fixed-Point Theorem (contraction mapping principle) — Section 7, to produce the unique fixed point φ*.
- Cauchy–Schwarz inequality — used inside the proof of Lemma 0 (triangle inequality for vector-valued integrals), stated and proved in Section 2.

No other named results are used. Every step from Section 3 onward is a direct computation from the theorem's hypotheses.
