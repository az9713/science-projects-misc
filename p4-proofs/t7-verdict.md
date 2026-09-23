# Theorem 7 (quadratic reciprocity): referee verdict

VALID

The proof is Eisenstein's proof: Fact 0 -> Lemma 1 (Euler) -> Lemma 2 (Gauss) -> Lemma 3 (Eisenstein) -> Lemma 4 (lattice count) -> Theorem. I checked each step. I found no gap, no missing hypothesis, and no false claim on the logical path. I found 3 non-load-bearing defects (list below). They do not change the verdict.

## Key steps checked and why each holds

1. **Fact 0 (primitive roots).** The proof cites it (Gauss, Disquisitiones Art. 55; Ireland-Rosen Prop. 4.1.1) and sketches it. The sketch is correct: x^d - 1 has at most d roots in the field Z/pZ, so the group has at most d elements of order dividing d, for each d; a finite group with this property is cyclic. The group lemma is cited, not proved. The statement of the proof says this at the start, so the citation is declared and standard. Acceptable.
2. **Lemma 1, Step 1.** (g^m)^2 = 1 and x^2 - 1 has only the roots +1, -1 in a field. g^m = 1 would give ord(g) | m < p - 1. So g^m = -1. Holds.
3. **Lemma 1, Step 2.** k even gives a = (g^j)^2. Conversely, a = x^2 with x = g^i gives (p - 1) | (k - 2i); p - 1 is even, so k is even. Both directions hold. Step 3 then gives a^m = (-1)^k = (a/p) mod p. Holds.
4. **Lemma 2, distinctness of r_1..r_m.** r_i = r_j gives p | (i - j), and |i - j| <= m - 1 < p. Holds.
5. **Lemma 2, the Claim {s_i} u {t_j'} = {1..m}.** p/2 is not an integer because p is odd, so r_k > p/2 is the same as r_k >= m + 1. Then t_j' = p - t_j is in [1, m]. A collision s_i = t_j' gives p | (i0 + j0) with 2 <= i0 + j0 <= 2m = p - 1. Contradiction. There are m values in an m-element set, all distinct, so the sets are equal. Holds.
6. **Lemma 2, product step.** The left side of (1) is a^m * m!. From (2), prod t_j' = (-1)^mu prod t_j mod p gives (3). gcd(m!, p) = 1 because every factor is < p, so cancellation is legal. a^m = (-1)^mu mod p, then Lemma 1. The lift from congruence to equality is correct: 1 and -1 differ by 2, and p > 2. Holds.
7. **Lemma 3, identity (4).** ka = p*floor(ka/p) + r_k, with 0 < r_k < p because p does not divide ka. Sum over k. Holds.
8. **Lemma 3, identity (5).** The sum of t_i' is mu*p - sum t_i. So sum r_k = m(m+1)/2 - mu*p + 2*sum t_i. Algebra checked. Holds.
9. **Lemma 3, parity step (6).** (a - 1) m(m+1)/2 = p(T - mu) + 2*sum t_i. m(m+1)/2 is an integer, a - 1 is even (a odd), and p is odd. So T = mu mod 2. With Lemma 2, (a/p) = (-1)^T. Holds. The hypothesis "a odd" is stated in the lemma and is met in the application (a = q, and a = p).
10. **Lemma 4, no point on the line qx = py.** p | qx and gcd(p, q) = 1 give p | x, but 1 <= x <= m < p. Holds. So R splits into R_> and R_< with no remainder.
11. **Lemma 4, count of R_>.** For fixed x, the admissible y are 1..floor(qx/p). The bound qx/p <= q(p - 1)/(2p) < q/2 = n + 1/2 gives floor(qx/p) <= n, so no y exceeds n. The case floor(qx/p) = 0 gives an empty count, which is also correct. The count of R_< follows by the symmetry p <-> q. Holds.
12. **Theorem.** p does not divide q (distinct primes) and q is odd, so Lemma 3 applies with a = q; the same with the roles swapped. Lemma 4 gives A + B = mn. So (p/q)(q/p) = (-1)^{mn}. Holds.
13. **Circularity.** No lemma uses reciprocity or a later lemma. The dependency chain in the table is correct.

## Non-load-bearing defects (do not affect validity)

1. **Remark after Lemma 3 — false claim.** The remark says the oddness of a is "the one place in the whole proof where 'p, q odd primes' is used beyond ensuring (p-1)/2 and (q-1)/2 are integers". This is false. Oddness of p is also used in Lemma 2 (p/2 is not an integer; p > 2 so +1 and -1 stay distinct mod p) and in Lemma 3 (p odd, so p(T - mu) = T - mu mod 2). Also, the oddness of a is the oddness of the *other* prime, which is a different use. Fix: delete the remark, or list all uses.
2. **Lemma 2, wording.** "Since 1 <= m! is a product of integers less than p" is a garbled sentence. The meaning (every factor of m! is in [1, p - 1], so gcd(m!, p) = 1) is correct. Fix: rewrite the sentence.
3. **Notation reuse.** The letters i and j are indices of the distinctness argument, indices of s_i and t_j, and (with i0, j0) indices into k, all in Lemma 2. Lemma 1 also uses i as an exponent. No step is ambiguous in context, but a reader must track the reuse.
