# Theorem 6 (Hall's Marriage Theorem)

## Statement

Let $G$ be a finite bipartite graph with vertex classes $X$ and $Y$. For $S \subseteq X$, let
$$N(S) = \{y \in Y : y \text{ is adjacent to some } x \in S\} \subseteq Y.$$
Then $G$ has a matching that covers (saturates) every vertex of $X$ if and only if
$$|N(S)| \ge |S| \quad \text{for every } S \subseteq X. \tag{Hall's condition}$$

## Preliminaries and definitions

- A **matching** in a graph is a set $M$ of edges, no two of which share an endpoint.
- A matching $M$ **saturates** (or **covers**) a vertex $v$ if some edge of $M$ is incident to $v$. $M$ saturates a set $S$ of vertices if it saturates every vertex of $S$.
- A graph $G$ is **bipartite with classes $X, Y$** if $V(G) = X \cup Y$, $X \cap Y = \varnothing$, and every edge has one endpoint in $X$ and one in $Y$.
- For disjoint $S_1, S_2 \subseteq X$ (regarded as sets of vertices with edges into $Y$), $N(S_1 \cup S_2) = N(S_1) \cup N(S_2)$, directly from the definition of $N$; this elementary set identity is used repeatedly below and is not restated as a separate lemma.

We prove the two directions separately. Throughout, $G$, $X$, $Y$ are as in the statement, and $X$, $Y$, $E(G)$ are all finite, as required by the hypothesis that $G$ is a finite graph.

## Part 1: Necessity

**Claim.** If $G$ has a matching $M$ that saturates $X$, then $|N(S)| \ge |S|$ for every $S \subseteq X$.

**Proof.** Fix $S \subseteq X$. Since $M$ saturates $X$, it saturates $S$; hence for each $x \in S$ there is a unique edge $x\,m(x) \in M$ with $m(x) \in Y$, and $x \mapsto m(x)$ is injective because $M$ is a matching (an edge of $M$ cannot be reused for two different vertices of $S$, as that would give two edges of $M$ sharing the endpoint $m(x)$). Each $m(x)$ is a neighbour of $x$, so $m(x) \in N(S)$ for all $x \in S$. Thus $m : S \to N(S)$ is an injective map, and since $S$ is finite,
$$|S| = |m(S)| \le |N(S)|.$$
This holds for every $S \subseteq X$, proving necessity. $\blacksquare$

## Part 2: Sufficiency

**Claim.** If $|N(S)| \ge |S|$ for every $S \subseteq X$, then $G$ has a matching saturating $X$.

We give the classical inductive proof, due to Halmos and Vaughan (P. R. Halmos and H. E. Vaughan, "The marriage problem," *American Journal of Mathematics*, 1950), which reduces the general case to two subcases by induction on $|X|$. (P. Hall's original argument, in "On representatives of subsets," *Journal of the London Mathematical Society*, 1935, establishes the same result by a different route.)

**Proof.** We induct on $n = |X|$.

**Base case ($n = 0$).** $X = \varnothing$, and the empty matching $M = \varnothing$ trivially saturates $X$.

(We also record $n=1$ directly for clarity, though it is subsumed by the base case argument below in spirit: if $X = \{x\}$, Hall's condition applied to $S = \{x\}$ gives $|N(\{x\})| \ge 1$, so $x$ has at least one neighbour $y \in Y$, and $M = \{xy\}$ saturates $X$.)

**Inductive step.** Let $n \ge 1$ and suppose the theorem holds for every finite bipartite graph whose $X$-class has fewer than $n$ vertices. Let $G$ have $|X| = n$ and suppose Hall's condition holds for $G$. We distinguish two cases.

---

**Case 1: Strict Hall condition off the top.** Suppose that for every $S$ with $\varnothing \ne S \subsetneq X$ (so $1 \le |S| \le n-1$),
$$|N(S)| \ge |S| + 1.$$

Since $|X| = n \ge 1$, apply Hall's condition to the singleton $S = \{x\}$ for some $x \in X$: $|N(\{x\})| \ge 1$, so $x$ has a neighbour $y \in Y$. Fix one such edge $xy$.

Form the graph $G' = G - x - y$, i.e. delete the vertices $x$ and $y$ (and all edges incident to either) from $G$, leaving bipartite classes $X' = X \setminus \{x\}$ and $Y' = Y \setminus \{y\}$, with $|X'| = n - 1$.

We check Hall's condition holds for $G'$. Let $T \subseteq X'$. Since $T \subseteq X$ as well and $T \subsetneq X$ (as $x \notin T$), $T$ falls under the case hypothesis if $T \ne \varnothing$, giving $|N_G(T)| \ge |T| + 1$ in $G$. Deleting the single vertex $y$ from $Y$ can remove at most one element from $N_G(T)$ when passing to $N_{G'}(T) = N_G(T) \setminus \{y\}$, so
$$|N_{G'}(T)| \ge |N_G(T)| - 1 \ge (|T|+1) - 1 = |T|.$$
If $T = \varnothing$ the inequality $|N_{G'}(T)| \ge |T| = 0$ is immediate. Hence Hall's condition holds for $G'$, which has $|X'| = n-1 < n$ vertices in its first class. By the induction hypothesis, $G'$ has a matching $M'$ saturating $X'$.

Let $M = M' \cup \{xy\}$. Since $M'$ uses only vertices of $X' \cup Y'$, none of which is $x$ or $y$, $M$ is again a matching (no two edges share an endpoint), and $M$ saturates $X' \cup \{x\} = X$. This proves the inductive step in Case 1.

---

**Case 2: A tight (critical) proper subset exists.** Suppose there exists $S_0$ with $\varnothing \ne S_0 \subsetneq X$ and
$$|N(S_0)| = |S_0|.$$
Let $k = |S_0|$, so $1 \le k \le n-1$.

*Sub-step (a): matching $S_0$ into $N(S_0)$.* Let $G_1$ be the induced bipartite subgraph of $G$ on the classes $S_0$ and $N(S_0)$ (keep exactly the edges of $G$ with both endpoints in $S_0 \cup N(S_0)$). For any $T \subseteq S_0$, the neighbourhood of $T$ computed inside $G_1$ equals the neighbourhood of $T$ computed inside $G$, because every $G$-neighbour of a vertex of $T \subseteq S_0$ already lies in $N(S_0)$ by definition of $N(S_0)$, and no edges are lost by restricting to $S_0 \cup N(S_0)$. Hence $N_{G_1}(T) = N_G(T)$, and Hall's condition for $G$ gives $|N_{G_1}(T)| = |N_G(T)| \ge |T|$. So Hall's condition holds for $G_1$, and $|S_0| = k < n$ (since $S_0 \subsetneq X$ and $X$ is finite with $|X|=n$). By the induction hypothesis, $G_1$ has a matching $M_1$ saturating $S_0$. Note every edge of $M_1$ has its $Y$-endpoint in $N(S_0)$.

*Sub-step (b): matching $X \setminus S_0$ into $Y \setminus N(S_0)$.* Let $G_2$ be the induced bipartite subgraph of $G$ on the classes $X_2 = X \setminus S_0$ and $Y_2 = Y \setminus N(S_0)$. We check Hall's condition for $G_2$. Let $T \subseteq X_2$. Since $T$ and $S_0$ are disjoint subsets of $X$, the identity noted in the Preliminaries gives
$$N_G(T \cup S_0) = N_G(T) \cup N(S_0).$$
Applying Hall's condition in $G$ to the set $T \cup S_0 \subseteq X$:
$$|N_G(T) \cup N(S_0)| = |N_G(T \cup S_0)| \ge |T \cup S_0| = |T| + |S_0| = |T| + k,$$
using disjointness of $T$ and $S_0$ for the last equality. By inclusion–exclusion (or directly, since $|A \cup B| \le |A \setminus B| + |B|$),
$$|N_G(T) \cup N(S_0)| \le |N_G(T) \setminus N(S_0)| + |N(S_0)| = |N_{G_2}(T)| + k,$$
where $N_{G_2}(T) = N_G(T) \setminus N(S_0)$ because $G_2$ is obtained from $G$ by deleting exactly the vertices of $N(S_0)$ from the $Y$-side (together with $S_0$ from the $X$-side, which is irrelevant to neighbours of $T \subseteq X_2$). Combining the two displayed inequalities,
$$|N_{G_2}(T)| + k \ge |N_G(T) \cup N(S_0)| \ge |T| + k \implies |N_{G_2}(T)| \ge |T|.$$
Hence Hall's condition holds for $G_2$, and $|X_2| = n - k < n$ since $k \ge 1$. By the induction hypothesis, $G_2$ has a matching $M_2$ saturating $X_2$. Every edge of $M_2$ has its $Y$-endpoint in $Y \setminus N(S_0)$.

*Combining.* Let $M = M_1 \cup M_2$. The $X$-endpoints of $M_1$ lie in $S_0$ and those of $M_2$ lie in $X \setminus S_0$; these are disjoint, so $M$ saturates $S_0 \cup (X\setminus S_0) = X$. The $Y$-endpoints of $M_1$ lie in $N(S_0)$ and those of $M_2$ lie in $Y \setminus N(S_0)$; these too are disjoint, so no vertex of $Y$ is used twice, and no two edges of $M_1 \cup M_2$ share an endpoint (endpoints in $X$ are separated as shown, endpoints in $Y$ are separated as shown). Hence $M$ is a matching saturating $X$.

---

Cases 1 and 2 are exhaustive: either every nonempty proper subset $S$ of $X$ satisfies the strict inequality $|N(S)| \ge |S|+1$ (Case 1), or some nonempty proper subset attains equality $|N(S_0)| = |S_0|$ (Case 2) — recall equality cannot fall below $|S_0|$ by the hypothesis $|N(S)|\ge|S|$ applied to $S_0$ itself, so the only alternative to strict inequality for a particular $S$ is exact equality. In both cases we produced a matching of $G$ saturating $X$, completing the induction. $\blacksquare$

## Conclusion

Both directions are established: a matching saturating $X$ exists if and only if Hall's condition $|N(S)| \ge |S|$ holds for every $S \subseteq X$. This proves Theorem 6 (Hall's Marriage Theorem). $\blacksquare$

## Remarks (not required for the proof, recorded for context)

- **Alternative proofs.** Hall's theorem can also be derived as a corollary of **König's theorem** (in a bipartite graph, the maximum matching size equals the minimum vertex cover size) together with a counting argument, or as a special case of the **max-flow/min-cut theorem** applied to the bipartite graph with a source joined to all of $X$ and a sink joined to all of $Y$, all capacities $1$ (the max-flow min-cut argument is the standard modern route and is equivalent to Menger's theorem for this bipartite setting). These are cited here by name only as alternative routes; the induction above is a complete, self-contained proof and does not rely on them.
- **Deficiency version.** A quantitative strengthening, sometimes called the **Defect (or Deficiency) form of Hall's theorem**, states that the maximum matching in $G$ saturates all but $\max_{S \subseteq X} (|S| - |N(S)|)$ vertices of $X$; Theorem 6 is the special case where this deficiency is $0$.
