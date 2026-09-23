# Referee verdict: Theorem 4 (Strong law of large numbers, Etemadi's form)

**Verdict: VALID**

The proof in `t4-proof.md` proves the statement in item 4 of `theorems.md`. It uses only the stated hypotheses: pairwise independence, identical distribution, and E|X_1| < ∞. I found no gap in the logic. I found 5 minor defects in wording and in the remark. None of them changes a step of the argument. They are listed after the checked steps.

## Key steps checked, and why each step holds

1. **Lemma 1 (functions of independent variables).** σ(g(X)) ⊆ σ(X) and σ(h(Y)) ⊆ σ(Y). Independence of σ-algebras passes to sub-σ-algebras. The pairwise version applies the lemma to each pair i ≠ j. Correct.
2. **Lemma 7 (tail-sum bound).** EX = ∫_0^∞ P(X>t) dt follows from Tonelli on 1{t < X}. For t ≤ k, P(X>t) ≥ P(X>k), so P(X>k) ≤ ∫_{k-1}^k P(X>t) dt. The sum of these integrals is ∫_0^∞. Correct.
3. **Lemma 8 (truncated second moment).** The bound (*) Σ_{k≥m} 1/k² ≤ 1/m² + 1/m ≤ 2/m is correct by the telescoping bound 1/k² ≤ 1/(k−1) − 1/k for k ≥ 2. For integer k ≥ 1, the condition x ≤ k is equivalent to k ≥ ⌈x⌉. Thus Σ_k 1{x≤k}/k² = g(x). For x > 0, m = ⌈x⌉ ≥ x gives g(x) ≤ 2/m ≤ 2/x. This also covers 0 < x < 1 (m = 1, g ≤ 2 ≤ 2/x). Thus x²g(x) ≤ 2x. Tonelli moves the sum inside E. Correct.
4. **Lemma 9 (geometric subsequence).** For x ≥ 2, ⌊x⌋ > x − 1 ≥ x/2, so n_k ≥ α^k/2 for k ≥ k_0. The small-k part is a finite sum and gives C_1/j² with C_1 = A_α J_0². For the large-k part, the set {k ≥ k_0 : n_k ≥ j} is a subset of {k ≥ k_1} by minimality of k_1. This inclusion holds without a monotonicity argument. The geometric tail is 4α^{−2k_1}/(1 − α^{−2}). The inequality α^{k_1} ≥ n_{k_1} ≥ j gives α^{−2k_1} ≤ 1/j². Correct. The lemma counts repeated values of n_k (for α near 1, ⌊α^k⌋ repeats for small k) once per index k. Step 3 also sums once per index k. The two counts agree.
5. **Step 1 (reduction to X_i ≥ 0).** X_i^± are Borel functions of X_i. Lemma 1 gives pairwise independence. Identical distribution passes to X_i^±. Both means are finite. The intersection of two probability-1 events has probability 1. E[X_1] = E[X_1^+] − E[X_1^−]. Correct.
6. **Step 2a (variance of T_n).** Y_k = X_k 1{X_k ≤ k} is bounded by k. Thus all second moments are finite, covariances exist, and independence gives Cov(Y_i, Y_j) = 0 for i ≠ j. This is the only step that needs independence (see defect 4). Correct.
7. **Step 2b.** Var(Y_k) ≤ E[Y_k²] = E[X_1² 1{X_1 ≤ k}] by identical distribution. Lemma 8 gives (2.2) with bound 2μ. Correct.
8. **Step 3 (subsequence convergence of T).** T_{n_k} ≤ n_k², so Chebyshev (Lemma 2) applies. The interchange of the double sum Σ_k Σ_{j ≤ n_k} = Σ_j Σ_{k: n_k ≥ j} is valid because all terms are ≥ 0 (Lemma 5). Lemma 9 and (2.2) give a finite sum, bounded by 2μC_α/ε². Borel–Cantelli I needs no independence. The countable union over ε = 1/m gives (3.1). For (3.2), MCT gives EY_k → μ, and Cesàro gives ET_n/n → μ, thus also along n_k → ∞. Correct.
9. **Step 4 (removal of the truncation).** Σ P(X_k ≠ Y_k) = Σ P(X_1 > k) ≤ μ by Lemma 7. Borel–Cantelli gives X_k = Y_k eventually, a.s. Thus S_n − T_n is eventually constant and (S_n − T_n)/n → 0. The subsequence n_k → ∞ inherits the limit, which gives (4.1). Correct.
10. **Step 5 (sandwich).** S_n is nondecreasing because X_i ≥ 0. The inequality α^k − 1 < n_k ≤ α^k gives n_k/α^k → 1, thus n_{k+1}/n_k → α. The bounds μ/α ≤ liminf ≤ limsup ≤ μα follow. The case μ = 0 also holds. The countable intersection over α = 1 + 1/m and the limit m → ∞ give S_n/n → μ a.s. Correct.

## Minor defects (none is a gap in the logic)

1. **Step 5, missing sentence on the index k(n).** The proof does not state that each n ≥ 1 is in some interval [n_k, n_{k+1}), with k = k(n) → ∞ as n → ∞. This fact is necessary to pass from the bounds on the subsequence to liminf and limsup over all n. It is true because n_0 = 1 and n_k → ∞. The proof uses it implicitly. It is a presentation omission and not an error.
2. **Step 1, wrong term "i.i.d.".** Step 1 says "each sequence is i.i.d." The sequences (X_i^±) are pairwise independent and identically distributed, not fully independent. The reduction then applies the theorem in the correct pairwise form. Thus the defect is only in the term. Replace "i.i.d." with "pairwise independent and identically distributed".
3. **Lemma 8, unclear phrase.** "let m = ⌈x⌉ ≥ 1 ≥ x/m, i.e. m ≥ x" puts two facts in one chain in an unclear order. The fact that the proof needs is m = ⌈x⌉ ≥ x. That fact is true. Write "let m = ⌈x⌉; then m ≥ 1 and m ≥ x".
4. **Final remark, incorrect count.** The remark says "Pairwise independence is used exactly twice". Then it says that the second use (Borel–Cantelli in Section 4) "needs no independence at all". These two statements contradict each other. The correct count: the proof uses pairwise independence in (2.1), and also in Step 1, where Lemma 1 transfers pairwise independence to X_i^+ and X_i^−. Section 4 does not use independence. The remark is commentary, not a step of the proof. Thus the verdict is VALID. Correct the remark before publication.
5. **Citation numbers not checked.** The referee did not check the theorem numbers against the cited editions. Examples: Billingsley Theorem 20.4 for Lemma 1, and Durrett Theorem 1.5.1 for MCT. Each cited lemma is standard and correct as stated. Thus a wrong number does not change validity. Check the numbers before publication.

## Hypotheses check

- Only pairwise independence is used. No maximal inequality and no full independence occur. This agrees with the statement.
- Identical distribution is used in 2b, in Step 4 (P(X_k > k) = P(X_1 > k)), and in Step 1.
- E|X_1| < ∞ is used in Step 1 and through μ < ∞ in Lemmas 7 and 8.
- No second moment of X_1 is assumed. Truncation makes every second moment in the proof finite.
