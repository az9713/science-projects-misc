# Referee verdict: Theorem 6 (Hall's marriage theorem)

VALID

The proof is complete and correct. It is the Halmos–Vaughan induction on |X|, with a split into a "strict surplus" case and a "tight proper subset" case. I found no gap, no missing hypothesis, and no false claim. The minor remarks below are about wording and edge cases. None of them breaks a step.

## Key steps checked, and why each holds

1. **Necessity (Part 1).** A matching M that saturates X gives each x in S exactly one M-edge x m(x), because two M-edges at x would share the endpoint x. The map m is injective, because m(x) = m(x') for x ≠ x' gives two M-edges that share m(x). Each m(x) is in N(S). So |S| = |m(S)| ≤ |N(S)|. Correct.
2. **Base case n = 0.** The empty matching saturates the empty set. Correct. The induction hypothesis is strong induction over all finite bipartite graphs with a smaller X-class, which is what Cases 1 and 2 use.
3. **Case 1, choice of edge.** n ≥ 1, so some x exists. Hall's condition on {x} gives a neighbour y. Correct. This also covers n = 1, where the Case 1 hypothesis is vacuous (X has no nonempty proper subset).
4. **Case 1, Hall's condition in G' = G − x − y.** For T ⊆ X', deleting x does not change the Y-neighbours of T, and deleting y removes at most one of them, so N_{G'}(T) = N_G(T) \ {y}. For T ≠ ∅, T is a nonempty proper subset of X, so |N_G(T)| ≥ |T| + 1 and |N_{G'}(T)| ≥ |T|. For T = ∅ the claim is trivial. Correct.
5. **Case 1, combining.** M' uses no vertex x or y, so M' ∪ {xy} is a matching that saturates X. Correct.
6. **Case 2, sub-step (a).** Every G-neighbour of T ⊆ S_0 is in N(S_0), and G_1 is the induced subgraph on S_0 ∪ N(S_0), so N_{G_1}(T) = N_G(T). Hall's condition passes to G_1. |S_0| = k ≤ n − 1, so the induction hypothesis applies. Correct.
7. **Case 2, sub-step (b).** For T ⊆ X \ S_0: N_G(T ∪ S_0) = N_G(T) ∪ N(S_0), and Hall in G gives |N_G(T) ∪ N(S_0)| ≥ |T| + k. The identity |A ∪ B| = |A \ B| + |B| gives |N_G(T) ∪ N(S_0)| = |N_{G_2}(T)| + k, where N_{G_2}(T) = N_G(T) \ N(S_0) holds because G_2 is induced on (X \ S_0) ∪ (Y \ N(S_0)). So |N_{G_2}(T)| ≥ |T|. |X_2| = n − k ≤ n − 1, so the induction hypothesis applies. This is the step where the tightness |N(S_0)| = |S_0| is used, and it is used correctly.
8. **Case 2, combining.** The X-endpoints of M_1 and M_2 are in the disjoint sets S_0 and X \ S_0. The Y-endpoints are in the disjoint sets N(S_0) and Y \ N(S_0). So M_1 ∪ M_2 is a matching that saturates X. Correct.
9. **Exhaustiveness of the cases.** Hall's condition gives |N(S)| ≥ |S| for each nonempty proper S. So either every such S has |N(S)| ≥ |S| + 1 (Case 1), or some S_0 has |N(S_0)| = |S_0| (Case 2). The two cases cover all possibilities. Correct.

## Minor remarks (not gaps)

1. **Preliminaries, identity for N.** The proof states N(S_1 ∪ S_2) = N(S_1) ∪ N(S_2) only for disjoint S_1, S_2. The identity holds for all subsets of X. The restriction is unnecessary but harmless, because the proof uses it only for the disjoint sets T and S_0.
2. **Wording of the n = 1 note.** "Subsumed by the base case argument below in spirit" is imprecise: n = 1 is handled by Case 1 of the inductive step, not by the base case. The note is labelled as extra, so the proof does not depend on it.
3. **Part 1, "since S is finite".** Injectivity of m gives |S| ≤ |N(S)| for any set S. Finiteness is not needed here. This is not an error.
4. **Inequality in sub-step (b).** The proof writes |N_G(T) ∪ N(S_0)| ≤ |N_G(T) \ N(S_0)| + |N(S_0)|. This is in fact an equality, since the two sets on the right are disjoint. Only the ≤ direction is needed, so the step holds.
5. **Remarks section.** The deficiency form (a maximum matching saturates all but max over S ⊆ X of (|S| − |N(S)|) vertices of X, with S = ∅ giving a maximum of at least 0) is the König–Ore formula and is correctly stated. The routes through König's theorem and max-flow/min-cut are correctly named. The citations (Halmos and Vaughan, Amer. J. Math., 1950; P. Hall, J. London Math. Soc., 1935) match the standard references. None of these remarks is used in the proof.
