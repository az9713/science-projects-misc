# Referee verdict: Theorem 2 (Sylow theorems)

**Verdict: VALID**

The proof in `t2-proof.md` proves (i), (ii), and (iii) exactly as stated in item 2 of
`theorems.md`, with the same hypotheses (G finite, p prime, |G| = p^a·m, a ≥ 0, p ∤ m).
I found no logical gap. I found one exposition defect (item E1 below). It does not affect
validity, because the same passage contains a correct, self-contained argument.

## Key steps checked, and why each holds

1. **Lemma 0′ (index tower), lines 24-29.** Derived from Lagrange by substitution and
   cancellation of |K| > 0. Correct.
2. **Lemma 2 (fixed-point congruence), lines 38-47.** Each orbit size is [H:H_x], a divisor
   of p^k, so it is 1 (exactly for fixed points) or a multiple of p. Summing over the orbit
   partition gives |X| ≡ |X^H| (mod p). Correct, including k = 0.
3. **Lemma 3 (p ∤ C(p^a·m, p^a)), lines 49-67.** The i = 0 factor is m, valuation 0. For
   1 ≤ i ≤ p^a − 1, i = p^k·u with k ≤ a − 1, and both p^{a−k} − u and p^{a−k}·m − u are
   ≡ −u (mod p), so numerator and denominator each have valuation exactly k. The p-adic
   valuation on ℚ is additive over the product, so the integer C(p^a·m, p^a) has valuation 0.
   Correct. For a = 0 the product is the single factor m. Correct.
4. **(i) Step 2, lines 90-93.** Orbit partition plus p ∤ |Ω| gives an orbit O of size prime
   to p. Correct.
5. **(i) Step 3, lines 95-100.** h ↦ h·s₀ maps the stabilizer H injectively into S₀ by left
   cancellation, so |H| ≤ p^a. Correct.
6. **(i) Step 4, lines 102-107.** |O| = n/|H| with p ∤ |O| and p ∤ m forces v_p(|H|) = a, so
   p^a divides |H|. With |H| ≤ p^a this gives |H| = p^a. Correct.
7. **(ii) Key Lemma, lines 119-133.** |G/P| = m ≢ 0 (mod p), so Lemma 2 gives a fixed coset
   gP. The equivalence h·gP = gP ⇔ g⁻¹hg ∈ P holds for all h ∈ H, so H ⊆ gPg⁻¹, and
   |gPg⁻¹| = p^a by Lemma 4(a). Correct. The bound k ≤ a (line 120) is correct but not needed.
8. **(ii) conjugacy, lines 139-147.** Q ⊆ gPg⁻¹ with equal finite orders gives equality.
   Transitivity through P gives conjugacy of any two Sylow subgroups. Correct.
9. **(iii) n_p | m, lines 158-167.** Syl_p(G) is one conjugation orbit (from Section 2), its
   stabilizer is N_G(P), and Lemma 0′ on P ≤ N_G(P) ≤ G gives m = n_p·[N_G(P):P]. Correct.
10. **(iii) n_p ≡ 1 (mod p), lines 169-191.** Lemma 2 for P acting on Syl_p(G) by
    conjugation gives n_p ≡ |X^P|. For Q ∈ X^P, both P and Q lie in N = N_G(Q) and have
    order p^a. |N| divides p^a·m and p^a divides |N|, so |N| = p^a·m′ with m′ | m and p ∤ m′.
    So P and Q are Sylow p-subgroups of N. Part (ii) is proved for an arbitrary finite group,
    so it applies to N. It gives x ∈ N with P = xQx⁻¹ = Q, because Q ⊴ N. So X^P = {P} and
    n_p ≡ 1 (mod p). Correct. There is no circularity: (ii) for N uses only (i) and Lemma 2,
    not (iii).
11. **Edge case a = 0.** P = {e}, n_p = 1. Every step above stays valid (the trivial group is
    a p-group of order p^0). Correct.

## Exposition defects (not gaps)

- **E1, lines 181-185.** The parenthetical that shows |N| = p^a·m′ with p ∤ m′ contains a
  broken sentence: "hence p ∤ |N|/p^a·(consistency with |G|=p^am)". That fragment is not a
  well-formed claim. The text then gives a correct complete argument ("more directly: |N|
  divides |G| = p^a·m by Lemma 0, and p^a | |N| since Q ≤ N, so |N| = p^a·m′ with m′ | m").
  Fix: delete everything from "writing |N| = p^a m′" up to "more directly:" and keep only the
  direct argument.
- **E2 (minor).** Lemma 1 (well-definedness of hH_x ↦ h·x) and Lemma 4(b) (N_G(H) is a
  subgroup) are cited, not proved. Both are standard textbook facts with correct citations,
  so this is acceptable for a proof at this level.
