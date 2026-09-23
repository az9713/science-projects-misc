# Theorem 7 — The Law of Quadratic Reciprocity

## Statement

Let $p$ be an odd prime and $a$ an integer with $p \nmid a$. The **Legendre symbol** is
defined by
$$
\left(\frac{a}{p}\right) =
\begin{cases}
+1 & \text{if } a \equiv x^2 \pmod p \text{ for some integer } x, \\
-1 & \text{otherwise.}
\end{cases}
$$

**Theorem (Quadratic Reciprocity).** Let $p$ and $q$ be distinct odd primes. Then
$$
\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2}\cdot\frac{q-1}{2}}.
$$

The proof below is the classical proof of Eisenstein (1844), which replaces Gauss's
original geometric/induction argument with a lattice-point count. It is self-contained
except for one standard structural fact about finite fields, cited by name. Throughout,
$p, q$ denote distinct odd primes, and we write
$$
m = \frac{p-1}{2}, \qquad n = \frac{q-1}{2}.
$$

---

## Fact 0 (Cyclicity of $(\mathbb Z/p\mathbb Z)^\times$)

*For every prime $p$, the multiplicative group $(\mathbb Z/p\mathbb Z)^\times$ of nonzero
residues modulo $p$ is cyclic of order $p-1$.*

This is the classical **existence of primitive roots modulo a prime**, first proved by
Gauss (*Disquisitiones Arithmeticae*, 1801, Art. 55). We record the one-line reason it
holds, since it is short: $\mathbb Z/p\mathbb Z$ is a field, so for every divisor $d$ of
$p-1$ the polynomial $x^d-1$ has at most $d$ roots in it; a finite abelian group with this
property (at most $d$ elements of order dividing $d$, for every $d$) is necessarily
cyclic (a standard group-theory lemma, sometimes attributed to the same argument used for
finite subgroups of the multiplicative group of any field). We use Fact 0 only through
Lemma 1 below and do not re-derive the group-theory lemma; it is standard and appears,
e.g., in Ireland–Rosen, *A Classical Introduction to Modern Number Theory*, Prop. 4.1.1,
or Serre, *A Course in Arithmetic*, Ch. I.

---

## Lemma 1 (Euler's Criterion)

*Let $p$ be an odd prime and $a$ an integer with $p \nmid a$. Then*
$$
\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod p.
$$

**Proof.** By Fact 0, choose a generator $g$ of $(\mathbb Z/p\mathbb Z)^\times$, so every
residue class prime to $p$ is $g^k$ for a unique $k \in \{0,1,\dots,p-2\}$. Write
$a \equiv g^k \pmod p$.

*Step 1: $g^{(p-1)/2} \equiv -1 \pmod p$.* Since $g$ has order $p-1$, $\left(g^{(p-1)/2}\right)^2
= g^{p-1} \equiv 1 \pmod p$. In the field $\mathbb Z/p\mathbb Z$ the polynomial $x^2-1 =
(x-1)(x+1)$ has exactly the two roots $1,-1$ (a field has no zero divisors, so a
polynomial of degree $d$ has at most $d$ roots). Hence $g^{(p-1)/2} \equiv 1$ or $-1
\pmod p$. It cannot be $1$: that would mean the order of $g$ divides $(p-1)/2 < p-1$,
contradicting that $g$ has order exactly $p-1$. So $g^{(p-1)/2} \equiv -1 \pmod p$.

*Step 2: $a$ is a quadratic residue iff $k$ is even.* If $k=2j$ is even, then
$a \equiv (g^j)^2 \pmod p$, so $a$ is a QR. Conversely, if $a \equiv x^2 \pmod p$ for
some $x$ with $p \nmid x$ (note $p\nmid a$ forces $p \nmid x$), write $x \equiv g^i
\pmod p$; then $g^k \equiv g^{2i} \pmod p$, so $g^{k-2i}\equiv 1$, so $(p-1) \mid (k-2i)$,
so $k \equiv 2i \pmod{p-1}$; since $p-1$ is even this forces $k$ even. Thus $a$ is a QR
$\iff k$ is even, i.e. $\left(\frac ap\right) = (-1)^k$.

*Step 3: conclude.* $a^{(p-1)/2} \equiv g^{k(p-1)/2} \equiv \left(g^{(p-1)/2}\right)^k
\equiv (-1)^k \pmod p$ by Step 1. Combined with Step 2, $a^{(p-1)/2} \equiv
\left(\frac ap\right) \pmod p$. $\blacksquare$

---

## Lemma 2 (Gauss's Lemma)

*Let $p$ be an odd prime, $a$ an integer with $p\nmid a$, and $m=(p-1)/2$. For
$k=1,\dots,m$ let $r_k \in \{1,\dots,p-1\}$ be the least positive residue of $ka$ modulo
$p$. Let $\mu$ be the number of indices $k$ for which $r_k > p/2$. Then*
$$
\left(\frac ap\right) = (-1)^\mu.
$$

**Proof.** The residues $r_1,\dots,r_m$ are pairwise distinct: if $r_i = r_j$ then
$p \mid (i-j)a$, and since $p\nmid a$ this gives $p \mid (i-j)$; but $|i-j| < m < p$, so
$i=j$.

Split the indices $1,\dots,m$ into those with $r_k \le m$ (call these values
$s_1,\dots,s_{m-\mu}$) and those with $r_k > m$ (call these values $t_1,\dots,t_\mu$; note
$p/2$ is not an integer, so "$r_k>p/2$" is the same as "$r_k \ge m+1$", i.e. $r_k>m$).
For each $t_i$ set $t_i' = p - t_i$, so $1 \le t_i' \le m$ as well (since $m+1\le t_i\le
p-1$ gives $1 \le t_i' \le m$).

*Claim: $\{s_1,\dots,s_{m-\mu}\}\cup\{t_1',\dots,t_\mu'\}=\{1,2,\dots,m\}$ (as a set of
$m$ distinct integers).* There are exactly $m$ values listed, all lying in
$\{1,\dots,m\}$, so it suffices to show no two coincide. The $s_i$ are pairwise distinct
(they are a subset of the pairwise-distinct $r_k$), and likewise the $t_i'$ are pairwise
distinct (since the $t_i$ are). Suppose $s_i = t_j'$ for some $i,j$, i.e.
$s_i + t_j = p$. Write $s_i \equiv i_0 a \pmod p$ and $t_j \equiv j_0 a \pmod p$ for the
corresponding indices $i_0,j_0 \in \{1,\dots,m\}$; then $p \mid (i_0+j_0)a$, and since
$p\nmid a$, $p \mid (i_0+j_0)$. But $2 \le i_0+j_0 \le 2m = p-1$, so $p\nmid(i_0+j_0)$ —
contradiction. Hence the two lists are disjoint, proving the claim.

*Product computation.* Multiplying the definitions of the $r_k$,
$$
a \cdot 2a \cdots ma \equiv r_1 r_2 \cdots r_m = \Big(\prod_i s_i\Big)\Big(\prod_j t_j\Big)
\pmod p. \tag{1}
$$
By the Claim,
$$
\Big(\prod_i s_i\Big)\Big(\prod_j t_j'\Big) = m!. \tag{2}
$$
Since $t_j' = p - t_j \equiv -t_j \pmod p$, we have $\prod_j t_j' \equiv (-1)^\mu
\prod_j t_j \pmod p$. Substituting into (2) and reducing mod $p$:
$$
\Big(\prod_i s_i\Big)(-1)^\mu\Big(\prod_j t_j\Big) \equiv m! \pmod p,
$$
so
$$
\Big(\prod_i s_i\Big)\Big(\prod_j t_j\Big) \equiv (-1)^\mu m! \pmod p \tag{3}
$$
(using $(-1)^{-\mu}=(-1)^\mu$). Combining (1) and (3):
$$
a^m \, m! \equiv (-1)^\mu m! \pmod p.
$$
Since $1\le m! $ is a product of integers less than $p$, $\gcd(m!,p)=1$, so we may
cancel $m!$:
$$
a^m \equiv (-1)^\mu \pmod p.
$$
By Lemma 1 (Euler's Criterion), $a^m \equiv \left(\frac ap\right) \pmod p$. Hence
$\left(\frac ap\right) \equiv (-1)^\mu \pmod p$. Both sides lie in $\{1,-1\}$ and $p>2$,
so distinct elements of $\{1,-1\}$ remain distinct mod $p$; therefore
$\left(\frac ap\right) = (-1)^\mu$ exactly (not just modulo $p$). $\blacksquare$

---

## Lemma 3 (Eisenstein's Lemma)

*Let $p$ be an odd prime and $a$ an **odd** integer with $p \nmid a$. Let $m=(p-1)/2$.
Then*
$$
\left(\frac ap\right) = (-1)^{\,T(a,p)}, \qquad
T(a,p) := \sum_{k=1}^{m} \left\lfloor \frac{ka}{p} \right\rfloor .
$$

**Proof.** Reuse the notation of Lemma 2's proof: for $k=1,\dots,m$, write the division
$$
ka = p\left\lfloor \frac{ka}{p}\right\rfloor + r_k, \qquad 0 < r_k < p
$$
(the remainder is nonzero because $p \nmid k$ and $p\nmid a$). Summing over
$k=1,\dots,m$ and using $\sum_{k=1}^m k = \frac{m(m+1)}{2}$:
$$
a\cdot\frac{m(m+1)}{2} = p\sum_{k=1}^m \left\lfloor\frac{ka}{p}\right\rfloor + \sum_{k=1}^m r_k
= p\,T(a,p) + \sum_{k=1}^m r_k. \tag{4}
$$

As in Lemma 2, split $\{r_k\}$ into the "small" values $s_1,\dots,s_{m-\mu}$ (those
$\le m$) and "large" values $t_1,\dots,t_\mu$ (those $>m$), with $t_i' = p-t_i \in
\{1,\dots,m\}$, and $\{s_i\}\cup\{t_i'\} = \{1,\dots,m\}$ exactly. Summing that set
identity:
$$
\sum_i s_i + \sum_i t_i' = \frac{m(m+1)}{2}, \qquad \text{i.e.} \qquad
\sum_i s_i + \Big(\mu p - \sum_i t_i\Big) = \frac{m(m+1)}{2}.
$$
Hence $\sum_i s_i - \sum_i t_i = \frac{m(m+1)}{2} - \mu p$. Adding $2\sum_i t_i$ to both
sides,
$$
\sum_{k=1}^m r_k = \sum_i s_i + \sum_i t_i = \frac{m(m+1)}{2} - \mu p + 2\sum_i t_i. \tag{5}
$$

Substitute (5) into (4):
$$
a\cdot\frac{m(m+1)}{2} = p\,T(a,p) + \frac{m(m+1)}{2} - \mu p + 2\sum_i t_i,
$$
which rearranges to
$$
(a-1)\cdot\frac{m(m+1)}{2} = p\big(T(a,p) - \mu\big) + 2\sum_i t_i. \tag{6}
$$

Now reduce (6) modulo $2$. On the right: $2\sum_i t_i \equiv 0 \pmod 2$, and $p$ is odd
so $p\big(T(a,p)-\mu\big) \equiv T(a,p) - \mu \equiv T(a,p)+\mu \pmod 2$. On the left:
$a$ is odd by hypothesis, so $a-1$ is even, and $\frac{m(m+1)}{2}$ is an integer; an even
integer times an integer is even, so the left side is $\equiv 0 \pmod 2$. Thus
$$
0 \equiv T(a,p) + \mu \pmod 2, \qquad \text{i.e.} \qquad T(a,p) \equiv \mu \pmod 2.
$$

By Lemma 2, $\left(\frac ap\right) = (-1)^\mu = (-1)^{T(a,p)}$, since $\mu$ and $T(a,p)$
have the same parity. $\blacksquare$

*(Remark: the oddness of $a$ is exactly what is needed to kill the term
$(a-1)\cdot\frac{m(m+1)}{2}$ modulo $2$; this is the one place in the whole proof where
"$p,q$ odd primes" is used beyond ensuring $(p-1)/2$ and $(q-1)/2$ are integers.)*

---

## Lemma 4 (Lattice-point count)

*Let $p,q$ be distinct odd primes, $m=(p-1)/2$, $n=(q-1)/2$. Then*
$$
\sum_{k=1}^{m}\left\lfloor\frac{kq}{p}\right\rfloor \;+\; \sum_{k=1}^{n}\left\lfloor\frac{kp}{q}\right\rfloor \;=\; mn.
$$

**Proof.** Consider the set $R$ of lattice points $(x,y)$ with integers $1\le x\le m$,
$1\le y\le n$; $|R| = mn$.

*No point of $R$ lies on the line $qx=py$.* If $qx=py$ for integers $x,y$ with $1\le
x\le m$, then $p\mid qx$; since $p,q$ are distinct primes, $\gcd(p,q)=1$, so $p \mid x$.
But $1 \le x \le m = \frac{p-1}{2} < p$, so no positive multiple of $p$ lies in this
range — contradiction. Hence every point of $R$ satisfies $qx \ne py$, i.e. $qx>py$ or
$qx<py$, and $R$ splits into two disjoint sets accordingly:
$$
R = R_> \sqcup R_<, \qquad R_> = \{(x,y)\in R : qx>py\}, \quad R_< = \{(x,y)\in R: qx<py\}.
$$

*Counting $R_>$.* Fix $x\in\{1,\dots,m\}$. The condition $qx>py$ (with $p>0$) is
$y < qx/p$. Since $p\nmid x$ (shown above) and $p \nmid q$, $qx/p$ is never an integer,
so the integers $y$ with $1\le y$ and $y<qx/p$ are exactly $y=1,\dots,\left\lfloor
\frac{qx}{p}\right\rfloor$. We must check these all satisfy $y\le n$: for $x\le m$,
$$
\frac{qx}{p} \le \frac{qm}{p} = \frac{q(p-1)}{2p} < \frac q2 = n+\tfrac12,
$$
and since $qx/p$ is not an integer, $\left\lfloor\frac{qx}{p}\right\rfloor \le n$.
Hence, for each $x$, the count of valid $y$ is exactly $\left\lfloor\frac{qx}{p}
\right\rfloor$, and
$$
|R_>| = \sum_{x=1}^m \left\lfloor\frac{qx}{p}\right\rfloor.
$$

*Counting $R_<$.* By the identical argument with the roles of $(p,x,m)$ and $(q,y,n)$
exchanged (the hypotheses are symmetric in $p\leftrightarrow q$),
$$
|R_<| = \sum_{y=1}^n \left\lfloor\frac{py}{q}\right\rfloor.
$$

Since $R = R_>\sqcup R_<$ and $|R|=mn$,
$$
\sum_{k=1}^m\left\lfloor\frac{qk}{p}\right\rfloor + \sum_{k=1}^n\left\lfloor\frac{pk}{q}\right\rfloor = mn. \qquad\blacksquare
$$

---

## Proof of the Theorem

Let $p,q$ be distinct odd primes, $m=(p-1)/2$, $n=(q-1)/2$.

$q$ is an odd integer with $p\nmid q$ (as $p\ne q$ are both prime), so Lemma 3
(Eisenstein's Lemma), applied with $a=q$, gives
$$
\left(\frac qp\right) = (-1)^{A}, \qquad A := \sum_{k=1}^{m}\left\lfloor\frac{kq}{p}\right\rfloor.
$$
Symmetrically, $p$ is an odd integer with $q\nmid p$, so Lemma 3 applied with the roles
of $p,q$ swapped gives
$$
\left(\frac pq\right) = (-1)^{B}, \qquad B := \sum_{k=1}^{n}\left\lfloor\frac{kp}{q}\right\rfloor.
$$

Multiplying,
$$
\left(\frac pq\right)\left(\frac qp\right) = (-1)^{A+B}.
$$

By Lemma 4, $A+B = mn = \dfrac{p-1}{2}\cdot\dfrac{q-1}{2}$. Therefore
$$
\left(\frac pq\right)\left(\frac qp\right) = (-1)^{\frac{p-1}{2}\cdot\frac{q-1}{2}}. \qquad\blacksquare
$$

---

## Dependency summary

| Result | Depends on | What it supplies |
|---|---|---|
| Fact 0 (primitive roots exist mod $p$) | Standard field/group theory (cited: Gauss 1801; Ireland–Rosen Prop. 4.1.1) | Structure of $(\mathbb Z/p\mathbb Z)^\times$ |
| Lemma 1 (Euler's Criterion) | Fact 0 | $\left(\frac ap\right)\equiv a^{(p-1)/2}\pmod p$ |
| Lemma 2 (Gauss's Lemma) | Lemma 1 | $\left(\frac ap\right)=(-1)^\mu$, sign-count form |
| Lemma 3 (Eisenstein's Lemma) | Lemma 2 | Replaces $\mu$ by a floor-sum $T(a,p)$, valid for odd $a$ |
| Lemma 4 (lattice count) | Elementary (uses $\gcd(p,q)=1$) | $A+B = mn$ |
| **Theorem** | Lemmas 3 and 4 | Full reciprocity law |

No step assumes the result being proved; the chain is strictly Fact 0 → Lemma 1 →
Lemma 2 → Lemma 3 → (independently) Lemma 4 → Theorem. Every numeric identity used
($\sum_{k=1}^m k = m(m+1)/2$, the parity argument in Lemma 3, and the strict inequalities
in Lemma 4) is derived in place rather than asserted.
