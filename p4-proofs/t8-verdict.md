# Theorem 8 verdict: Uniform Boundedness Principle (Banach–Steinhaus)

VALID

The proof is the standard Baire-category proof. Each step follows from the stated hypotheses. The referee found no gap. The referee found no missing hypothesis and no false claim in the proof chain. Four minor points are listed after the checked steps. None of them changes the verdict.

## Key steps checked

1. **Lemma 1, (a) ⇒ (c) (Section 1).** Continuity at 0 with ε = 1 gives ‖u‖ < δ ⇒ ‖Tu‖ < 1. The proof writes "‖u‖ ≤ δ ⇒ ‖Tu‖ ≤ 1". This form follows if δ is replaced by δ/2, so the bound becomes C = 2/δ. The conclusion "T bounded" holds. Lemma 1 is only used to get "T continuous" from "T bounded", that is (c) ⇒ (b). That direction is a correct Lipschitz argument.
2. **Baire corollary (Section 2).** A closed set with empty interior is nowhere dense, because its closure is itself. So a countable cover of a complete metric space by closed sets with empty interior contradicts the Baire theorem. The citation (Rudin FA Thm 2.2; Folland Thm 5.9) is accurate and acceptable for a cited foundation.
3. **E_n is closed (Step 1).** x ↦ ‖Tx‖ is continuous. It is T (continuous) composed with the norm (1-Lipschitz by the reverse triangle inequality). So each {x : ‖Tx‖ ≤ n} is the preimage of the closed set [0, n] and is closed. An arbitrary intersection of closed sets is closed. The proof correctly states that 𝓕 need not be countable. Only the index n must be countable, and it is.
4. **The E_n cover X (Step 1).** This uses the pointwise hypothesis M_x = sup_T ‖Tx‖ < ∞. The choice n ≥ max(1, ⌈M_x⌉) keeps n in ℕ = {1, 2, …}. The proof handles M_x = 0 explicitly.
5. **Application of Baire (Step 2).** X is complete (Banach), so it is a complete metric space. Some E_N contains an open ball B(x₀, r) with r > 0. This is the only use of completeness. It matches Remark 2.
6. **Local-to-global bound (Step 3).** For ‖x‖ ≤ 1, z = x₀ + (r/2)x satisfies ‖z − x₀‖ ≤ r/2 < r, so z ∈ E_N. Also x₀ ∈ E_N. Linearity gives Tx = (2/r)(Tz − Tx₀). So ‖Tx‖ ≤ (2/r)(N + N) = 4N/r. The sup over the closed unit ball matches the operator norm in the statement. The use of r/2, not r, is correct, because ‖x‖ = 1 is allowed and the ball is open.
7. **Uniformity (Step 4).** N and r are fixed in Step 2, before T is chosen. So the bound 4N/r does not depend on T, and sup_T ‖T‖ ≤ 4N/r < ∞.
8. **Edge cases.** For 𝓕 = ∅, each E_n = X and the conclusion holds with the convention sup ∅ = 0 (Remark 1). For X = {0}, B(x₀, r) = {0} ⊆ E_N and the argument runs unchanged. The scalar field (ℝ or ℂ) is not used.
9. **Hypotheses.** Completeness of Y is not used, which agrees with the statement. Each T ∈ 𝓕 is bounded; this is used for the closedness of E_n. The pointwise bound is used for the cover. No hypothesis is missing.

## Minor points (not gaps)

1. **Section 1, proof of (a) ⇒ (c).** The strict/non-strict inequality mismatch is explained in item 1 above. The repair takes one line: take δ' = δ/2.
2. **Section 1, statement of Lemma 1.** The claim "the least such C equals ‖T‖" is stated but not proved. It is never used: Step 3 bounds ‖T‖ directly from its sup definition. The claim is correct.
3. **Section 0, heading "Open and closed balls".** Only the open ball is defined. This is a cosmetic mismatch with no effect on the proof.
4. **Remark 4, name "resonance theorem".** The remark links the name to the convergence corollary. The name comes from the contrapositive: if sup_T ‖T‖ = ∞, then some x has an unbounded orbit {Tx}. The remark is context only and is not part of the proof. The corollary itself (a pointwise limit T is linear and bounded, with ‖T‖ ≤ liminf ‖T_n‖) is correct.

The counterexample in Remark 2 was checked: X = c₀₀ with the sup norm, T_n(x) = n·x_n. Each ‖T_n‖ = n, and each orbit is finite pointwise because x has finite support. So completeness of X cannot be removed. The counterexample is correct.
