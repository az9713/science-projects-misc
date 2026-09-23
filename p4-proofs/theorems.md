# P4 proof arena: ten theorems

Each entry gives the area, the name, and the precise statement with all hypotheses.
Each full proof fits in 1 to 3 pages.

## 1. Arzelà–Ascoli theorem (analysis)

Let (K, d) be a compact metric space. Let C(K) be the space of continuous functions f: K → ℝ with the sup norm ‖f‖∞ = max_{x∈K} |f(x)|. A subset F ⊆ C(K) is relatively compact (its closure in C(K) is compact) if and only if F satisfies both conditions:
(a) F is uniformly bounded: sup_{f∈F} ‖f‖∞ < ∞;
(b) F is equicontinuous: for every ε > 0 there is δ > 0 such that |f(x) − f(y)| < ε for all f ∈ F and all x, y ∈ K with d(x, y) < δ.
Equivalently, (a) and (b) hold if and only if every sequence in F has a subsequence that converges uniformly on K.

## 2. Sylow theorems (algebra)

Let G be a finite group, let p be a prime, and write |G| = p^a·m with a ≥ 0 and p ∤ m. A Sylow p-subgroup of G is a subgroup of order p^a. Then:
(i) G has at least one Sylow p-subgroup;
(ii) every p-subgroup of G (a subgroup of order a power of p) is contained in some Sylow p-subgroup, and any two Sylow p-subgroups of G are conjugate in G;
(iii) the number n_p of Sylow p-subgroups of G satisfies n_p ≡ 1 (mod p) and n_p divides m.

## 3. Urysohn's lemma (topology)

Let X be a normal topological space: for every pair of disjoint closed sets C, D ⊆ X there are disjoint open sets U ⊇ C and V ⊇ D (no separation axiom beyond this is assumed). Let A and B be disjoint closed subsets of X. Then there exists a continuous function f: X → [0, 1] with f(x) = 0 for all x ∈ A and f(x) = 1 for all x ∈ B.

## 4. Strong law of large numbers, Etemadi's form (probability)

Let X₁, X₂, … be real random variables on a probability space (Ω, 𝓕, P) that are pairwise independent and identically distributed, with E|X₁| < ∞. Let S_n = X₁ + ⋯ + X_n. Then S_n / n → E[X₁] almost surely as n → ∞.

## 5. Spectral theorem for normal operators (linear algebra)

Let V be a finite-dimensional complex inner product space with dim V = n ≥ 1, let T: V → V be linear, and let T* be its adjoint, defined by ⟨Tu, v⟩ = ⟨u, T*v⟩ for all u, v ∈ V. Then T T* = T* T (T is normal) if and only if V has an orthonormal basis that consists of eigenvectors of T. Matrix form: A ∈ ℂ^{n×n} satisfies A A* = A* A if and only if A = U D U* for some unitary U and some diagonal D.

## 6. Hall's marriage theorem (combinatorics)

Let G be a finite bipartite graph with vertex classes X and Y. For S ⊆ X let N(S) ⊆ Y be the set of vertices adjacent to at least one vertex of S. Then G has a matching that covers every vertex of X if and only if |N(S)| ≥ |S| for every subset S ⊆ X.

## 7. Law of quadratic reciprocity (number theory)

For an odd prime p and an integer a with p ∤ a, the Legendre symbol (a/p) equals 1 if a ≡ x² (mod p) for some integer x, and −1 otherwise. Let p and q be distinct odd primes. Then
(p/q)·(q/p) = (−1)^{((p−1)/2)·((q−1)/2)}.

## 8. Uniform boundedness principle, Banach–Steinhaus (functional analysis)

Let X be a Banach space, let Y be a normed space, and let 𝓕 be a family of bounded linear operators T: X → Y, with operator norm ‖T‖ = sup_{‖x‖≤1} ‖Tx‖. Suppose that for every x ∈ X, sup_{T∈𝓕} ‖Tx‖ < ∞. Then sup_{T∈𝓕} ‖T‖ < ∞.

## 9. Radon–Nikodym theorem (measure theory)

Let (Ω, 𝓕) be a measurable space and let μ and ν be σ-finite positive measures on 𝓕 with ν ≪ μ (that is, μ(E) = 0 implies ν(E) = 0 for E ∈ 𝓕). Then there exists an 𝓕-measurable function f: Ω → [0, ∞) such that ν(E) = ∫_E f dμ for every E ∈ 𝓕. The function f is unique up to μ-almost-everywhere equality.

## 10. Picard–Lindelöf theorem (ODE / dynamics)

Let t₀ ∈ ℝ, x₀ ∈ ℝⁿ, a > 0, b > 0, and R = [t₀ − a, t₀ + a] × B̄(x₀, b), where B̄(x₀, b) is the closed Euclidean ball. Let f: R → ℝⁿ be continuous and Lipschitz in x uniformly in t: there is L ≥ 0 with |f(t, x) − f(t, y)| ≤ L|x − y| for all (t, x), (t, y) ∈ R. Let M = max_R |f|, and let h = min(a, b/M) if M > 0 and h = a if M = 0. Then the initial value problem x′(t) = f(t, x(t)), x(t₀) = x₀ has exactly one solution x: [t₀ − h, t₀ + h] → ℝⁿ that is C¹ and satisfies (t, x(t)) ∈ R for all t in that interval.
