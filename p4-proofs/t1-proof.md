# Theorem (Arzelà–Ascoli)

**Statement.** Let $(K,d)$ be a compact metric space, and let $C(K)$ be the space of
continuous functions $f:K\to\mathbb{R}$ with the sup norm $\|f\|_\infty = \max_{x\in K}|f(x)|$.
A subset $F\subseteq C(K)$ is relatively compact (its closure in $C(K)$ is compact) if and
only if:

- **(a) Uniform boundedness:** $\sup_{f\in F}\|f\|_\infty < \infty$;
- **(b) Equicontinuity:** for every $\varepsilon>0$ there is $\delta>0$ such that
  $|f(x)-f(y)|<\varepsilon$ for all $f\in F$ and all $x,y\in K$ with $d(x,y)<\delta$.

Equivalently, (a) and (b) hold if and only if every sequence in $F$ has a subsequence that
converges uniformly on $K$.

Throughout, "compact" for a metric space means: every open cover has a finite subcover.
"Relatively compact" means the closure is compact.

---

## 0. Lemmas used, with standard citations

**Lemma 0 (metric-space compactness characterization).** For a metric space $X$, the
following are equivalent:
1. $X$ is compact.
2. $X$ is sequentially compact (every sequence has a subsequence converging in $X$).
3. $X$ is complete and totally bounded (for every $\varepsilon>0$, $X$ is covered by
   finitely many balls of radius $\varepsilon$).

*Citation:* this is a standard theorem of general topology / metric-space theory; see
Rudin, *Principles of Mathematical Analysis*, 3rd ed., Theorem 3.11 (compact $\Rightarrow$
sequentially compact, in the setting of metric spaces) together with Theorem 2.35 and the
surrounding discussion of total boundedness, or Munkres, *Topology*, 2nd ed., §45
("Compactness in Metric Spaces", Theorem 45.1). We use it three times below: once for $K$
itself, once for boxes in $\mathbb{R}^n$ (this is the Heine–Borel theorem, the
$\mathbb{R}^n$ special case), and once for $C(K)$.

**Lemma 1 (total boundedness passes to closures and subsets).** If $F$ is totally bounded
in a metric space $X$, then (i) $\overline{F}$ is totally bounded, and (ii) every subset of
$F$ is totally bounded. *Proof.* (ii) is immediate from the definition. For (i): given
$\varepsilon>0$, an $(\varepsilon/2)$-net $\{p_1,\dots,p_k\}\subseteq F$ for $F$ is an
$\varepsilon$-net for $\overline{F}$, since every point of $\overline F$ lies within
$\varepsilon/2$ of a point of $F$, which lies within $\varepsilon/2$ of some $p_i$. $\blacksquare$

**Lemma 2 (relative compactness $\Leftrightarrow$ total boundedness, in a complete ambient
space).** Let $X$ be a complete metric space and $F\subseteq X$. Then $F$ is relatively
compact if and only if $F$ is totally bounded.
*Proof.* ($\Leftarrow$) By Lemma 1(i), $\overline F$ is totally bounded. $\overline F$ is a
closed subset of the complete space $X$, hence complete. By Lemma 0 (3 $\Rightarrow$ 1),
$\overline F$ is compact. ($\Rightarrow$) If $\overline F$ is compact, then by Lemma 0
(1 $\Rightarrow$ 3), $\overline F$ is totally bounded, and $F\subseteq\overline F$ is totally
bounded by Lemma 1(ii). $\blacksquare$

**Lemma 3 (Heine–Cantor theorem).** A continuous function from a compact metric space to a
metric space is uniformly continuous. *Citation:* Rudin, *Principles of Mathematical
Analysis*, Theorem 4.19; Munkres, *Topology*, Theorem 27.6.

**Lemma 4 (Extreme Value Theorem).** A continuous real-valued function on a nonempty
compact metric space attains a maximum. *Citation:* Rudin, *Principles of Mathematical
Analysis*, Theorem 4.16. (This is what makes $\|f\|_\infty=\max_{x\in K}|f(x)|$ a genuine
maximum rather than merely a supremum, since $K$ is compact and $|f|$ is continuous.)

**Lemma 5 (Uniform Limit Theorem).** If $(g_n)$ is a sequence of continuous functions
$K\to\mathbb{R}$ converging uniformly on $K$ to $g$, then $g$ is continuous. *Citation:*
Rudin, *Principles of Mathematical Analysis*, Theorem 7.12.

**Lemma 6 ($C(K)$ is complete).** $(C(K),\|\cdot\|_\infty)$ is a complete metric space.
*Proof.* Let $(f_n)$ be Cauchy in $\|\cdot\|_\infty$. For each fixed $x\in K$,
$|f_n(x)-f_m(x)|\le\|f_n-f_m\|_\infty$, so $(f_n(x))_n$ is a Cauchy sequence of real
numbers; by completeness of $\mathbb R$ it converges to some limit, which we call $f(x)$.
This defines $f:K\to\mathbb R$, and $f_n\to f$ pointwise. To see the convergence is
uniform: given $\varepsilon>0$, choose $N$ so that $\|f_n-f_m\|_\infty<\varepsilon/2$ for
all $n,m\ge N$. Fix $n\ge N$ and any $x\in K$; letting $m\to\infty$ in
$|f_n(x)-f_m(x)|<\varepsilon/2$ gives $|f_n(x)-f(x)|\le\varepsilon/2<\varepsilon$. As $x$ was
arbitrary, $\|f_n-f\|_\infty\le\varepsilon/2$ for all $n\ge N$, i.e. $f_n\to f$ uniformly.
By Lemma 5, $f$ is continuous, so $f\in C(K)$, and $f_n\to f$ in $C(K)$. $\blacksquare$

Combining Lemma 2 and Lemma 6: **for $F\subseteq C(K)$, $F$ is relatively compact if and
only if $F$ is totally bounded in the sup norm.** This reduces the theorem to showing:

$$\text{(a) and (b) hold} \iff F \text{ is totally bounded in } (C(K),\|\cdot\|_\infty).$$

---

## 1. Direction 1: (a) and (b) $\implies$ $F$ is totally bounded (hence relatively compact)

Assume (a): $M:=\sup_{f\in F}\|f\|_\infty<\infty$, and (b): equicontinuity of $F$.

Fix $\varepsilon>0$.

**Step 1 (use equicontinuity to get a modulus $\delta$).** By (b) applied to $\varepsilon/4$,
there is $\delta>0$ such that for all $f\in F$ and all $x,y\in K$ with $d(x,y)<\delta$,
$$|f(x)-f(y)|<\varepsilon/4. \tag{1}$$

**Step 2 (cover $K$ using compactness of $K$).** Since $K$ is compact, by Lemma 0
(1 $\Rightarrow$ 3) $K$ is totally bounded, so $K$ can be covered by finitely many balls of
radius $\delta/2$: there exist $x_1,\dots,x_n\in K$ with
$$K=\bigcup_{i=1}^n B(x_i,\delta/2). \tag{2}$$

**Step 3 (discretize the values at $x_1,\dots,x_n$ using compactness of $\mathbb R^n$).**
By (a), for every $f\in F$ and every $i$, $|f(x_i)|\le M$, so the map
$$\Phi:F\to\mathbb R^n,\qquad \Phi(f)=(f(x_1),\dots,f(x_n))$$
has image contained in the box $[-M,M]^n$. By the Heine–Borel theorem (the
$\mathbb R^n$ case of Lemma 0), $[-M,M]^n$ is compact, hence (Lemma 0 again) totally
bounded with respect to the max-coordinate metric $\rho(a,b)=\max_i|a_i-b_i|$. So there is a
finite set of points $a^{(1)},\dots,a^{(m)}\in[-M,M]^n$ such that every point of $[-M,M]^n$
is within $\varepsilon/4$ (in $\rho$) of some $a^{(j)}$.

For each $f\in F$, pick (any) index $j(f)\in\{1,\dots,m\}$ with $\rho(\Phi(f),a^{(j(f))})<\varepsilon/4$,
i.e.
$$|f(x_i)-a^{(j(f))}_i|<\varepsilon/4 \quad\text{for } i=1,\dots,n. \tag{3}$$
This partitions $F$ into (at most) $m$ nonempty groups $F_1,\dots,F_m$, where
$F_j=\{f\in F: j(f)=j\}$.

**Step 4 (functions in the same group are uniformly $\varepsilon$-close).** Let $f,g\in F_j$
for the same $j$. Take any $x\in K$. By (2), $x\in B(x_i,\delta/2)$ for some $i$, so
$d(x,x_i)<\delta/2<\delta$. Then by the triangle inequality, (1) (applied twice, to $f$ and
to $g$, each with the pair $x,x_i$), and (3) (applied to $f$ and to $g$ at index $i$):
$$
|f(x)-g(x)| \le |f(x)-f(x_i)| + |f(x_i)-a^{(j)}_i| + |a^{(j)}_i-g(x_i)| + |g(x_i)-g(x)|
< \frac{\varepsilon}{4}+\frac{\varepsilon}{4}+\frac{\varepsilon}{4}+\frac{\varepsilon}{4}=\varepsilon.
$$
This strict inequality holds for **every** $x\in K$. The function $x\mapsto|f(x)-g(x)|$ is
continuous ($f,g$ are continuous) on the compact set $K$, so by Lemma 4 it attains its
maximum at some point $x_0\in K$. Applying the displayed bound at $x=x_0$ gives
$$\|f-g\|_\infty = |f(x_0)-g(x_0)| < \varepsilon.$$
So every group $F_j$ has diameter $<\varepsilon$ in $\|\cdot\|_\infty$.

**Step 5 (conclude total boundedness).** Choosing one representative $f_j\in F_j$ from each
nonempty group ($m$ groups, so finitely many representatives), every $f\in F$ lies in
$F_{j(f)}$ and satisfies $\|f-f_{j(f)}\|_\infty<\varepsilon$ by Step 4. Hence
$\{f_1,\dots,f_m\}$ is a finite $\varepsilon$-net for $F$. Since $\varepsilon>0$ was
arbitrary, $F$ is totally bounded in $(C(K),\|\cdot\|_\infty)$.

By Lemma 2 (using completeness of $C(K)$, Lemma 6), $F$ is relatively compact. $\blacksquare$

---

## 2. Direction 2: $F$ relatively compact $\implies$ (a) and (b)

Assume $\overline F$ is compact in $C(K)$. By Lemma 0 (1 $\Rightarrow$ 3), $\overline F$ is
totally bounded, hence by Lemma 1(ii) so is its subset $F$.

**Proof of (a).** Total boundedness with $\varepsilon=1$ gives finitely many
$f_1,\dots,f_k\in C(K)$ with $F\subseteq\bigcup_{i=1}^k B(f_i,1)$. Let
$M:=\max_{1\le i\le k}\|f_i\|_\infty<\infty$. For any $f\in F$, $f\in B(f_i,1)$ for some
$i$, so $\|f\|_\infty\le\|f_i\|_\infty+\|f-f_i\|_\infty< M+1$. Hence
$\sup_{f\in F}\|f\|_\infty\le M+1<\infty$, which is (a).

**Proof of (b).** Fix $\varepsilon>0$. By total boundedness of $F$, choose a finite
$(\varepsilon/3)$-net $g_1,\dots,g_k\in C(K)$ for $F$: for every $f\in F$ there is $i$ with
$$\|f-g_i\|_\infty<\varepsilon/3. \tag{4}$$
Each $g_i$ is continuous on the compact metric space $K$, so by Lemma 3 (Heine–Cantor) it
is uniformly continuous: there is $\delta_i>0$ such that
$$d(x,y)<\delta_i \implies |g_i(x)-g_i(y)|<\varepsilon/3.$$
Let $\delta:=\min\{\delta_1,\dots,\delta_k\}>0$ (a minimum of finitely many positive
numbers, hence still positive).

Now let $f\in F$ be arbitrary and let $x,y\in K$ with $d(x,y)<\delta$. Choose $i$ satisfying
(4) for this $f$. Since $\delta\le\delta_i$, $d(x,y)<\delta_i$, so $|g_i(x)-g_i(y)|<\varepsilon/3$.
By the triangle inequality,
$$
|f(x)-f(y)| \le |f(x)-g_i(x)| + |g_i(x)-g_i(y)| + |g_i(y)-f(y)|
< \frac{\varepsilon}{3}+\frac{\varepsilon}{3}+\frac{\varepsilon}{3}=\varepsilon,
$$
using $|f(x)-g_i(x)|\le\|f-g_i\|_\infty<\varepsilon/3$ and likewise for $y$. The index $i$
depended on $f$, but $\delta$ did not, so: for every $\varepsilon>0$ there is $\delta>0$
(independent of $f$) such that $d(x,y)<\delta$ implies $|f(x)-f(y)|<\varepsilon$ for **all**
$f\in F$. This is exactly (b). $\blacksquare$

This completes the proof of the biconditional: $F$ relatively compact $\iff$ (a) and (b). $\blacksquare$

---

## 3. Equivalence with the sequential formulation

**Claim.** (a) and (b) hold if and only if every sequence in $F$ has a subsequence that
converges uniformly on $K$ (i.e., converges in the norm $\|\cdot\|_\infty$ to some function
in $C(K)$; that the limit of a uniformly convergent sequence of continuous functions is
itself continuous is Lemma 5, so "converges uniformly on $K$" and "converges in $C(K)$" mean
the same thing here).

**($\Rightarrow$)** Assume (a) and (b). By Sections 1–2 (or directly Lemma 2), $\overline F$
is compact, so by Lemma 0 (1 $\Rightarrow$ 2), $\overline F$ is sequentially compact. Given
any sequence $(f_n)$ in $F\subseteq\overline F$, sequential compactness of $\overline F$
gives a subsequence $(f_{n_k})$ converging, in $\|\cdot\|_\infty$, to some
$g\in\overline F\subseteq C(K)$. That is exactly "converges uniformly on $K$."

**($\Leftarrow$)** Assume every sequence in $F$ has a subsequence converging uniformly on
$K$ (to a limit in $C(K)$). We show $\overline F$ is sequentially compact, which by Lemma 0
(2 $\Rightarrow$ 1) gives $\overline F$ compact, i.e. $F$ relatively compact, which by
Section 2 gives (a) and (b).

Let $(h_n)$ be any sequence in $\overline F$. By definition of closure in a metric space,
for each $n$ choose $f_n\in F$ with $\|h_n-f_n\|_\infty<1/n$. By hypothesis, $(f_n)$ has a
subsequence $(f_{n_k})$ with $f_{n_k}\to g$ uniformly for some $g\in C(K)$. Then
$$
\|h_{n_k}-g\|_\infty \le \|h_{n_k}-f_{n_k}\|_\infty+\|f_{n_k}-g\|_\infty
< \frac{1}{n_k}+\|f_{n_k}-g\|_\infty \xrightarrow[k\to\infty]{} 0,
$$
so $h_{n_k}\to g$ as well. Moreover $g=\lim_k f_{n_k}$ with each $f_{n_k}\in F$, so $g$ is a
limit of a sequence of points of $F$, hence $g\in\overline F$ (this is the standard
sequential characterization of closure in a metric space: $\overline F$ consists exactly of
the limits of convergent sequences from $F$). Thus $(h_n)$ has a subsequence converging in
$\overline F$, and since $(h_n)$ was an arbitrary sequence in $\overline F$, $\overline F$ is
sequentially compact. $\blacksquare$

This establishes the "Equivalently" clause of the theorem, and completes the proof of the
Arzelà–Ascoli theorem in full. $\blacksquare$

---

## Summary of the logical structure

1. Lemma 6 (completeness of $C(K)$) + Lemma 2 (relative compactness $\equiv$ total
   boundedness in a complete space) reduce the theorem to: (a)+(b) $\iff$ $F$ totally
   bounded.
2. Section 1 proves (a)+(b) $\Rightarrow$ totally bounded, by combining an
   equicontinuity-driven $\delta$, a finite cover of $K$ by $\delta/2$-balls (compactness of
   $K$), and a finite discretization of the values at the cover's centers (compactness of a
   box in $\mathbb R^n$, i.e. Heine–Borel) into a single finite $\varepsilon$-net for $F$.
3. Section 2 proves the converse using total boundedness of $F$ directly: boundedness gives
   (a); a finite $\varepsilon/3$-net of continuous (hence, by Heine–Cantor, uniformly
   continuous) functions gives a single $\delta$ that works for every $f\in F$, giving (b).
4. Section 3 upgrades the "relatively compact" formulation to the sequential one, using
   only the general metric-space fact that compact $\iff$ sequentially compact (Lemma 0)
   and the sequential characterization of closure.
