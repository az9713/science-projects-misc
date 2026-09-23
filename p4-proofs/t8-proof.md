# Theorem 8: Uniform Boundedness Principle (Banach–Steinhaus)

## Statement

Let $X$ be a Banach space, let $Y$ be a normed space, and let $\mathcal{F}$ be a family of
bounded linear operators $T : X \to Y$, with operator norm
$\lVert T \rVert = \sup_{\lVert x \rVert \le 1} \lVert Tx \rVert$. Suppose that for every
$x \in X$,
$$\sup_{T \in \mathcal{F}} \lVert Tx \rVert < \infty.$$
Then
$$\sup_{T \in \mathcal{F}} \lVert T \rVert < \infty.$$

This result is due to Stefan Banach and Hugo Steinhaus (1927); it is also called the
**Uniform Boundedness Principle**, or (rarely) the **resonance theorem**. The proof below is
the standard Baire-category proof.

---

## 0. Preliminaries and definitions

To keep the proof self-contained, we fix the definitions of every object named in the
statement.

**Normed space.** A normed space is a vector space $Z$ (over $\mathbb{R}$ or $\mathbb{C}$)
equipped with a norm $\lVert \cdot \rVert : Z \to [0,\infty)$ satisfying
$\lVert z \rVert = 0 \iff z = 0$, $\lVert \lambda z \rVert = |\lambda| \lVert z \rVert$, and
the triangle inequality $\lVert z_1 + z_2 \rVert \le \lVert z_1 \rVert + \lVert z_2 \rVert$.
A norm induces a metric $d(z_1,z_2) = \lVert z_1 - z_2 \rVert$, hence a topology on $Z$.

**Banach space.** A Banach space is a normed space that is *complete* as a metric space:
every Cauchy sequence in $X$ converges to a point of $X$.

**Bounded linear operator and operator norm.** A linear map $T : X \to Y$ between normed
spaces is *bounded* if
$$\lVert T \rVert := \sup_{\lVert x \rVert \le 1} \lVert Tx \rVert < \infty.$$
Equivalently (proved in Lemma 1 below), $T$ is bounded iff there is a constant $C \ge 0$
with $\lVert Tx \rVert \le C \lVert x \rVert$ for all $x \in X$, and the least such $C$ equals
$\lVert T \rVert$.

**Open and closed balls.** For $x_0 \in X$, $\rho > 0$: the open ball is
$B(x_0,\rho) = \{x \in X : \lVert x - x_0 \rVert < \rho\}$.

**Interior, nowhere dense, meagre.** A set $A \subseteq X$ has *nonempty interior* if it
contains some open ball $B(x_0,\rho)$, $\rho>0$. A set $A$ is *nowhere dense* if its closure
$\overline{A}$ has empty interior. In particular, if $A$ is already closed, "$A$ nowhere
dense" is the same as "$A$ has empty interior."

---

## 1. Lemma 1 (bounded $\iff$ continuous, for linear maps)

**Lemma 1.** Let $T : X \to Y$ be a linear map between normed spaces. The following are
equivalent:

(a) $T$ is continuous at $0$;
(b) $T$ is continuous on all of $X$;
(c) $T$ is bounded, i.e. $\exists\, C \ge 0$ such that $\lVert Tx \rVert \le C \lVert x \rVert$
for every $x \in X$.

*Proof.*

$(c) \Rightarrow (b)$: If $\lVert Tx \rVert \le C\lVert x\rVert$ for all $x$, then for any
$x, x' \in X$, linearity gives
$\lVert Tx - Tx' \rVert = \lVert T(x-x') \rVert \le C \lVert x - x' \rVert$.
So $T$ is Lipschitz with constant $C$, hence uniformly continuous, hence continuous at every
point of $X$.

$(b) \Rightarrow (a)$: Immediate, continuity everywhere implies continuity at the point $0$.

$(a) \Rightarrow (c)$: Since $T(0)=0$ (linearity) and $T$ is continuous at $0$, taking
$\varepsilon = 1$ in the definition of continuity gives a $\delta > 0$ such that
$\lVert u \rVert \le \delta \implies \lVert Tu \rVert \le 1$. Now let $x \in X$, $x \ne 0$
(the case $x=0$ is trivial). Set $u = \delta \, x / \lVert x \rVert$; then
$\lVert u \rVert = \delta$, so $\lVert Tu \rVert \le 1$. By linearity and homogeneity of the
norm,
$$\lVert Tu \rVert = \left\lVert \frac{\delta}{\lVert x \rVert} Tx \right\rVert
= \frac{\delta}{\lVert x \rVert} \lVert Tx \rVert \le 1
\;\Longrightarrow\; \lVert Tx \rVert \le \frac{1}{\delta} \lVert x \rVert.$$
So $(c)$ holds with $C = 1/\delta$. $\blacksquare$

**Consequence used below.** Since every $T \in \mathcal{F}$ is given to be a bounded linear
operator, Lemma 1 gives that every $T \in \mathcal{F}$ is continuous on $X$.

---

## 2. Standard result cited: the Baire Category Theorem

We use the following theorem without reproving it; it is a foundational result of general
topology / metric space theory, entirely prior to and independent of functional analysis.

**Baire Category Theorem (Baire, 1899).** Let $(M,d)$ be a complete metric space. Then $M$
is not the union of countably many nowhere dense subsets of $M$.

*(Reference: e.g. W. Rudin,* Functional Analysis*, 2nd ed., Theorem 2.2; or G. Folland,*
Real Analysis*, Theorem 5.9; or J. B. Conway,* A Course in Functional Analysis*, Ch. III.)*

**Corollary (the form we actually use).** If a complete metric space $M$ is written as a
countable union $M = \bigcup_{n=1}^{\infty} F_n$ of *closed* sets $F_n$, then at least one
$F_n$ has nonempty interior.

*Proof of Corollary from the Baire Category Theorem.* Suppose, for contradiction, that every
$F_n$ has empty interior. Since each $F_n$ is closed, $\overline{F_n} = F_n$ also has empty
interior, so each $F_n$ is nowhere dense by definition. Then $M = \bigcup_n F_n$ exhibits $M$
as a countable union of nowhere dense sets, contradicting the Baire Category Theorem. Hence
some $F_n$ has nonempty interior. $\blacksquare$

---

## 3. Proof of the Uniform Boundedness Principle

**Step 1: Construct a countable family of closed sets covering $X$.**

For each $n \in \mathbb{N} = \{1,2,3,\dots\}$, define
$$E_n := \{\, x \in X : \lVert Tx \rVert \le n \text{ for every } T \in \mathcal{F} \,\}
= \bigcap_{T \in \mathcal{F}} \{\, x \in X : \lVert Tx \rVert \le n \,\}.$$

*Each $E_n$ is closed.* Fix $T \in \mathcal{F}$. By hypothesis $T$ is a bounded linear
operator, so by Lemma 1, $T$ is continuous $X \to Y$. The map $x \mapsto \lVert Tx \rVert$
is then continuous as well (composition of the continuous map $T$ with the continuous norm
function $\lVert \cdot \rVert : Y \to [0,\infty)$, the latter continuous by the reverse
triangle inequality $|\lVert y_1\rVert - \lVert y_2 \rVert| \le \lVert y_1 - y_2 \rVert$).
Hence $\{x \in X : \lVert Tx \rVert \le n\}$ is the preimage of the closed set $[0,n]$ under a
continuous real-valued function, so it is closed in $X$. An arbitrary intersection of closed
sets is closed (this holds for any index set, countable or not, so $\mathcal{F}$ need not be
countable here), so $E_n = \bigcap_{T \in \mathcal{F}} \{x : \lVert Tx \rVert \le n\}$ is
closed.

*The $E_n$ cover $X$.* Let $x \in X$ be arbitrary. By the hypothesis of the theorem,
$\sup_{T \in \mathcal{F}} \lVert Tx \rVert < \infty$; call this finite value $M_x \ge 0$.
Choose any integer $n \ge M_x$ (e.g. $n = \lceil M_x \rceil$, or $n=1$ if $M_x = 0$). Then
$\lVert Tx \rVert \le M_x \le n$ for every $T \in \mathcal{F}$, so $x \in E_n$. Since $x$ was
arbitrary,
$$X = \bigcup_{n=1}^{\infty} E_n.$$

**Step 2: Apply the Baire Category Theorem.**

$X$ is a Banach space, hence a complete metric space under the metric induced by its norm.
We have written $X$ as a countable union of closed sets $E_n$. By the Corollary in Section 2,
some $E_N$ (for a specific integer $N \ge 1$) has nonempty interior: there exist $x_0 \in X$
and $r > 0$ such that
$$B(x_0, r) \subseteq E_N, \qquad \text{i.e.} \qquad
\lVert x - x_0 \rVert < r \implies \lVert Tx \rVert \le N \text{ for all } T \in \mathcal{F}.
\tag{$\ast$}$$

**Step 3: Turn the local bound $(\ast)$ into a bound on the operator norms.**

Fix $T \in \mathcal{F}$ arbitrarily; we bound $\lVert T \rVert$ uniformly in $T$. Let
$x \in X$ with $\lVert x \rVert \le 1$. Define
$$z := x_0 + \frac{r}{2} x.$$
Then $\lVert z - x_0 \rVert = \frac{r}{2}\lVert x \rVert \le \frac{r}{2} < r$, so $z \in
B(x_0,r) \subseteq E_N$ by $(\ast)$, giving
$$\lVert T z \rVert \le N. \tag{1}$$
Also $x_0$ itself lies in $B(x_0,r)$ (it is the center of the ball), so $x_0 \in E_N$,
giving
$$\lVert T x_0 \rVert \le N. \tag{2}$$
Since $T$ is linear,
$$T z = T x_0 + \frac{r}{2} T x
\;\Longrightarrow\;
T x = \frac{2}{r}\bigl( T z - T x_0 \bigr).$$
Taking norms and using the triangle inequality together with (1) and (2):
$$\lVert T x \rVert = \frac{2}{r} \lVert T z - T x_0 \rVert
\le \frac{2}{r}\bigl( \lVert T z \rVert + \lVert T x_0 \rVert \bigr)
\le \frac{2}{r}(N + N) = \frac{4N}{r}.$$

This bound $\lVert Tx \rVert \le 4N/r$ holds for every $x$ with $\lVert x \rVert \le 1$.
Taking the supremum over such $x$,
$$\lVert T \rVert = \sup_{\lVert x \rVert \le 1} \lVert T x \rVert \le \frac{4N}{r}.$$

**Step 4: Conclude.**

The bound $\lVert T \rVert \le 4N/r$ was derived for an arbitrary $T \in \mathcal{F}$, and
the right-hand side $4N/r$ does not depend on $T$ (it depends only on $N$ and $r$, which were
fixed once in Step 2, from the covering $\{E_n\}$ and the hypothesis — not on which $T \in
\mathcal{F}$ we later chose in Step 3). Hence
$$\sup_{T \in \mathcal{F}} \lVert T \rVert \le \frac{4N}{r} < \infty,$$
which is the assertion of the theorem. $\blacksquare$

---

## 4. Remarks

**Remark 1 (degenerate case $\mathcal{F} = \varnothing$).** If $\mathcal{F}$ is empty, the
hypothesis holds vacuously for every $x$ ($\sup_{T \in \varnothing} \lVert Tx \rVert$ is the
supremum of the empty set of nonnegative reals, taken to be $0$ by convention, certainly
finite), and the conclusion $\sup_{T \in \varnothing}\lVert T \rVert < \infty$ also holds
vacuously (the empty supremum is $0$). The proof above still runs correctly in this case: each
$E_n$ is then all of $X$ (an empty intersection of subsets of $X$ equals $X$), so the covering
and Baire-category steps are trivial, and Step 3–4 are vacuous statements about no operators.
No case split is actually needed.

**Remark 2 (role of completeness of $X$).** Completeness of $X$ is used in exactly one place:
Step 2, to invoke the Baire Category Theorem. The theorem is false without it — the standard
counterexample takes $X = c_{00}$, the space of finitely-supported real sequences with the
sup norm (a normed but *incomplete* space), and $\mathcal{F} = \{T_n\}_{n\ge1}$ where $T_n$ is
the $n$-th coordinate functional multiplied by $n$, i.e. $T_n(x) = n\,x_n$: each $T_n$ is
bounded on $c_{00}$, for each fixed $x \in c_{00}$ only finitely many coordinates are nonzero
so $\sup_n |T_n(x)| < \infty$ pointwise, yet $\lVert T_n \rVert = n \to \infty$, so
$\sup_n \lVert T_n \rVert = \infty$. Completeness of $Y$ is *not* needed anywhere in the
proof, matching the hypothesis of the theorem, which only requires $Y$ to be a normed space.

**Remark 3 (sharpness of the method, not of the constant).** The constant $4N/r$ produced in
Step 3 is an artifact of the proof (the choice of radius $r/2$ inside the ball); the theorem
only asserts finiteness of $\sup_T \lVert T \rVert$, not a specific value, so no attempt is
made here to optimize the constant.

**Remark 4 (typical corollary, stated for context only, not used above).** A frequent
application: if $(T_n)$ is a sequence of bounded linear operators $X \to Y$ ($X$ Banach) such
that $T_n x \to T x$ (in $Y$) for every $x \in X$, then $\sup_n \lVert T_n \rVert < \infty$ by
this theorem (each orbit $\{T_n x\}$ converges, hence is bounded, giving the pointwise
hypothesis), and one further shows $T$ itself is linear and bounded with
$\lVert T \rVert \le \liminf_n \lVert T_n \rVert$. This corollary is not required to prove
Theorem 8 and is recorded only as context for why the theorem is also called the resonance
theorem.
