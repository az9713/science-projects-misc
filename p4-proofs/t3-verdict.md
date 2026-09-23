# Referee verdict: Theorem 3 (Urysohn's lemma)

VALID

The proof in `t3-proof.md` is complete and correct for the statement in item 3 of `theorems.md`. It uses only normality as stated (no T1 or Hausdorff axiom). I found no gap. I found three minor defects in wording. None of them breaks a step.

## Key steps checked, and why each holds

1. **Lemma 0 (shrinking), Section 1.** Normality applied to E and X \ O gives disjoint open V ⊇ E, W ⊇ X \ O. Then cl(V) ⊆ X \ W (closed superset of V) ⊆ O. Correct. It uses only the stated definition.
2. **Base case, Section 2.** U_1 := X \ B is open and contains A because A ∩ B = ∅. Lemma 0 on (A, U_1) gives U_0 with A ⊆ U_0 ⊆ cl(U_0) ⊆ U_1. Condition (*) holds on D_0 = {0, 1}.
3. **Inductive step, (2.1).** Each new midpoint m has consecutive level-n neighbours r < s. The hypothesis cl(U_r) ⊆ U_s lets Lemma 0 insert U_m. Each U_m depends only on level-n sets, so the choices at one level are independent. Earlier sets are not changed, so each U_r is well defined on D = ∪ D_n.
4. **Four-case check of (*) on D_{n+1}.** Case 1 is the hypothesis. Cases 2 and 3 use a ≤ r (or b ≥ s), which is true because a and b lie in D_n and m has no D_n point strictly between r and s. Case 4 uses s_1 ≤ r_2, which is true because m_1 < m_2 lie in different level-n intervals. Each chain of inclusions is correct. Thus (P2) holds for all r < s in D, because any two points of D lie in a common D_n.
5. **(P3) and boundary values, Section 3.** (P2) with s = 1 gives U_r ⊆ U_1 = X \ B for all r ∈ D. So a point of B is in no U_r, and f = 1 on B by the convention inf ∅ = 1. A ⊆ U_0 gives f = 0 on A. The range is [0, 1].
6. **Claim A and Claim A′.** Claim A is the definition of infimum. In Claim A′, f(x) < r ≤ 1 excludes the empty-set value 1, so some s < r has x ∈ U_s ⊆ cl(U_s) ⊆ U_r. Correct.
7. **Claim B.** If x ∉ cl(U_r), then x ∉ U_s for all s ≤ r (for s < r, cl(U_s) ⊆ U_r ⊆ cl(U_r)). So every index in the set is > r, and f(x) ≥ r. The empty case gives 1 ≥ r. Correct.
8. **Claim B′.** For r < 1: x ∈ cl(U_r) ⊆ U_s for every dyadic s > r, so f(x) ≤ s. Density gives f(x) ≤ r. Correct (see minor defect 1 for r = 1).
9. **Identity (5.1), 0 < a ≤ 1.** "⊆": density gives r ∈ D with f(x) < r < a, and Claim A′ gives x ∈ U_r. "⊇": Claim A. The right side is a union of open sets.
10. **Identity (5.2), 0 ≤ a < 1.** "⊆": density gives r ∈ D with a < r < f(x) ≤ 1, so r < 1. The contrapositive of Claim B′ gives x ∉ cl(U_r). "⊇": Claim B. The right side is a union of open sets.
11. **Edge values of a.** For a ≤ 0 or a > 1 (first family) and for a ≥ 1 or a < 0 (second family), the preimages are ∅ or X. All real a are covered.
12. **Lemma 2 (subbasis criterion).** The open rays form a subbasis of ℝ; their traces form a subbasis of [0, 1]. Preimages of subbasis sets open implies f is continuous. Correct.

## Minor defects (not gaps)

1. **Claim B′, Section 4, case r = 1.** The text says "the dyadic rationals greater than r have infimum r". For r = 1 this set is empty, and its infimum is not 1 in the usual sense. The conclusion f(x) ≤ 1 is still true, because f ≤ 1 everywhere. Also, (5.2) uses Claim B′ only with r < 1. Fix: add "if r = 1 the claim is trivial since f ≤ 1".
2. **Claim A′, parenthetical, Section 4.** The argument that the index set is not empty is hard to read ("an empty set has infimum 1 ≥ r only if r ≤ 1 ..."). The logic is correct: f(x) < r ≤ 1 ≠ 1 excludes the empty case. Fix: replace it with that one line.
3. **Section 7 summary.** It says Lemma 1 is "used to produce the countable index set D with the order property (P2)". Lemma 1 (density) is not used for (P2). (P2) comes from the induction. Density is used only in Claim B′ and in (5.1) and (5.2). This is a wrong description, not a wrong step.

## Remark on foundations

The construction makes countably many choices in sequence (one open set per dyadic point). This needs the axiom of dependent choice, which is part of ZFC. All standard proofs of Urysohn's lemma make the same choices. This is not a gap relative to the theorem as stated.
