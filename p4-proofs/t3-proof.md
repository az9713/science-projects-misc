# Theorem (Urysohn's Lemma)

**Statement.** Let $X$ be a normal topological space: for every pair of disjoint closed
sets $C,D\subseteq X$ there are disjoint open sets $U\supseteq C$ and $V\supseteq D$ (no
separation axiom beyond this is assumed). Let $A$ and $B$ be disjoint closed subsets of
$X$. Then there exists a continuous function $f:X\to[0,1]$ with $f(x)=0$ for all $x\in A$
and $f(x)=1$ for all $x\in B$.

Throughout, "closed"/"open" refer to the topology of $X$; $\operatorname{cl}(S)$ denotes
the closure of $S\subseteq X$ in $X$. No $T_1$ or Hausdorff assumption is used anywhere in
the proof — only normality as stated.

---

## 0. Lemmas used, with standard citations

**Lemma 0 (Shrinking Lemma).** Let $X$ be normal. If $E\subseteq X$ is closed, $O\subseteq
X$ is open, and $E\subseteq O$, then there is an open set $V$ with
$$E\subseteq V\subseteq \operatorname{cl}(V)\subseteq O.$$

*Citation:* This is the standard "shrinking" reformulation of normality; see Munkres,
*Topology*, 2nd ed., Lemma 31.1, or Willard, *General Topology*, Theorem 15.4. It is proved
directly from the definition of normal below (Section 1), so the proof is self-contained.

**Lemma 1 (Density of dyadic rationals).** The set $D=\{k/2^n : n\ge 0,\ 0\le k\le 2^n\}$ of
dyadic rationals in $[0,1]$ is dense in $[0,1]$ with its usual order and topology: for any
real $a<b$ in $[0,1]$ there is $r\in D$ with $a<r<b$ whenever $b-a>0$, and for any real
$a\in[0,1)$ there is $r\in D$ with $r>a$, and for any $a\in(0,1]$ there is $r\in D$ with
$r<a$.

*Citation:* Elementary fact about the reals; follows from the Archimedean property (choose
$n$ with $2^{-n}<b-a$, then some multiple of $2^{-n}$ lies strictly between $a$ and $b$).
See Rudin, *Principles of Mathematical Analysis*, 3rd ed., Theorem 1.20, applied to the
dyadic subgroup $\mathbb{Z}[1/2]$ of $\mathbb{R}$.

**Lemma 2 (Subbasis criterion for continuity into a subspace of $\mathbb{R}$).** Let
$Y\subseteq\mathbb{R}$ carry the subspace topology and let $g:X\to Y$ be any function. Then
$g$ is continuous if and only if for every $a\in\mathbb{R}$ the two sets
$$g^{-1}\big(Y\cap(-\infty,a)\big)\qquad\text{and}\qquad g^{-1}\big(Y\cap(a,\infty)\big)$$
are open in $X$.

*Citation:* The rays $(-\infty,a)$ and $(a,\infty)$, $a\in\mathbb{R}$, form a subbasis for
the order topology on $\mathbb{R}$, which coincides with the usual metric topology; a
subspace's topology has as subbasis the traces of a subbasis of the ambient space. A map
into a space with a given subbasis is continuous iff preimages of subbasis elements are
open: Munkres, *Topology*, 2nd ed., Theorem 18.1 and the remark following it (subbasis
version), or Willard, *General Topology*, Theorem 8.5. We apply this with $Y=[0,1]$.

No other results are used; in particular no metrizability, countability, or $T_1$
assumption on $X$ is invoked.

---

## 1. Proof of Lemma 0 (Shrinking Lemma)

Let $E$ be closed, $O$ open, $E\subseteq O$. Then $X\setminus O$ is closed, and
$E\cap(X\setminus O)=\varnothing$ because $E\subseteq O$. Since $E$ and $X\setminus O$ are
disjoint closed sets, normality of $X$ gives disjoint open sets $V\supseteq E$ and
$W\supseteq X\setminus O$.

Because $V\cap W=\varnothing$, we have $V\subseteq X\setminus W$. Since $W$ is open,
$X\setminus W$ is closed; since $V\subseteq X\setminus W$ and $X\setminus W$ is closed and
closure is the smallest closed set containing $V$,
$$\operatorname{cl}(V)\subseteq X\setminus W.$$
Also, $W\supseteq X\setminus O$ gives, on taking complements (which reverses inclusions),
$X\setminus W\subseteq X\setminus(X\setminus O)=O$. Combining,
$$E\subseteq V\subseteq \operatorname{cl}(V)\subseteq X\setminus W\subseteq O,$$
which is exactly the claim. $\blacksquare$

---

## 2. Construction of the Urysohn family $\{U_r\}_{r\in D}$

Let $D=\bigcup_{n\ge 0}D_n$ with $D_n=\{k/2^n:0\le k\le 2^n\}$, the dyadic rationals in
$[0,1]$ (Lemma 1). We construct, by induction on $n$, open sets $U_r\subseteq X$ for every
$r\in D_n$ such that:

$$(\ast)\qquad \text{for all } r,s\in D_n \text{ with } r<s:\quad \operatorname{cl}(U_r)\subseteq U_s,$$

and such that once $U_r$ is defined at some stage it is never redefined at a later stage.
We also arrange $U_0\supseteq A$ and $U_1=X\setminus B$ from the base case onward.

**Base case ($n=0$).** $D_0=\{0,1\}$. Since $A,B$ are closed and disjoint, put
$U_1:=X\setminus B$; this is open, and $A\subseteq U_1$ because $A\cap B=\varnothing$.
Apply Lemma 0 to the closed set $A$ and the open set $U_1\supseteq A$: obtain an open $U_0$
with
$$A\subseteq U_0\subseteq \operatorname{cl}(U_0)\subseteq U_1.$$
This gives $(\ast)$ for $D_0$ (the single pair $0<1$), and fixes $U_0,U_1$ once and for all.

**Inductive step ($n\to n+1$).** Assume $U_r$ has been constructed for every $r\in D_n$,
satisfying $(\ast)$ on $D_n$. The new points of $D_{n+1}$ are the midpoints
$$m=\frac{2k+1}{2^{n+1}},\qquad 0\le k\le 2^n-1,$$
each lying strictly between the consecutive level-$n$ points $r=k/2^n$ and $s=(k+1)/2^n$.
By the inductive hypothesis $(\ast)$ applied to this $r<s$ in $D_n$, we have
$\operatorname{cl}(U_r)\subseteq U_s$. Apply Lemma 0 to the closed set $\operatorname{cl}(U_r)$
and the open set $U_s\supseteq \operatorname{cl}(U_r)$: obtain an open $U_m$ with
$$\operatorname{cl}(U_r)\subseteq U_m\subseteq \operatorname{cl}(U_m)\subseteq U_s. \tag{2.1}$$
Do this independently for every new midpoint $m$ (each uses only the already-fixed
level-$n$ sets, so there is no circularity). All previously defined $U_r$, $r\in D_n$, are
left unchanged.

*Verification that $(\ast)$ extends to $D_{n+1}$.* Let $a<b$ be any two points of
$D_{n+1}=D_n\cup\{\text{new midpoints}\}$. There are four cases.

1. **Both $a,b\in D_n$.** Then $\operatorname{cl}(U_a)\subseteq U_b$ holds by the inductive
   hypothesis directly.

2. **$a\in D_n$, $b=m$ a new midpoint with $D_n$-neighbors $r<s$ (so $r=$ the level-$n$
   point below $m$, $s=$ the one above).** Since $a<m$ and $a\in D_n$, we have $a\le r$.
   - If $a=r$: $(2.1)$ gives $\operatorname{cl}(U_a)=\operatorname{cl}(U_r)\subseteq U_m$
     directly.
   - If $a<r$: the inductive hypothesis gives $\operatorname{cl}(U_a)\subseteq U_r$, and
     $(2.1)$ gives $U_r\subseteq \operatorname{cl}(U_r)\subseteq U_m$. Chaining,
     $\operatorname{cl}(U_a)\subseteq U_r\subseteq\operatorname{cl}(U_r)\subseteq U_m$.

3. **$a=m$ a new midpoint with neighbors $r<s$, $b\in D_n$.** Symmetrically $b\ge s$.
   - If $b=s$: $(2.1)$ gives $\operatorname{cl}(U_m)\subseteq U_s=U_b$ directly.
   - If $b>s$: the inductive hypothesis gives $\operatorname{cl}(U_s)\subseteq U_b$, and
     $(2.1)$ gives $\operatorname{cl}(U_m)\subseteq U_s$. Chaining,
     $\operatorname{cl}(U_m)\subseteq U_s\subseteq\operatorname{cl}(U_s)\subseteq U_b$.

4. **$a=m_1<m_2=b$, both new midpoints**, with respective $D_n$-neighbor pairs
   $r_1<s_1$ and $r_2<s_2$. Since $m_1<m_2$ lie in disjoint or adjacent level-$n$
   intervals, $s_1\le r_2$.
   - If $s_1=r_2$: by $(2.1)$ for $m_1$, $\operatorname{cl}(U_{m_1})\subseteq U_{s_1}$; by
     $(2.1)$ for $m_2$ (using $r_2=s_1$), $\operatorname{cl}(U_{r_2})\subseteq U_{m_2}$, i.e.
     $\operatorname{cl}(U_{s_1})\subseteq U_{m_2}$. Chaining through $U_{s_1}\subseteq
     \operatorname{cl}(U_{s_1})$ gives $\operatorname{cl}(U_{m_1})\subseteq U_{m_2}$.
   - If $s_1<r_2$ (both in $D_n$): the inductive hypothesis gives
     $\operatorname{cl}(U_{s_1})\subseteq U_{r_2}$. Combined with $(2.1)$ for $m_1$
     ($\operatorname{cl}(U_{m_1})\subseteq U_{s_1}$) and $(2.1)$ for $m_2$
     ($\operatorname{cl}(U_{r_2})\subseteq U_{m_2}$), we chain
     $$\operatorname{cl}(U_{m_1})\subseteq U_{s_1}\subseteq\operatorname{cl}(U_{s_1})
     \subseteq U_{r_2}\subseteq\operatorname{cl}(U_{r_2})\subseteq U_{m_2}.$$

In every case $\operatorname{cl}(U_a)\subseteq U_b$, so $(\ast)$ holds on $D_{n+1}$. This
completes the induction.

**Conclusion.** Since $D=\bigcup_n D_n$ and any two elements $r<s$ of $D$ lie together in
some $D_n$ (namely $n=$ the larger of their two dyadic levels, since $D_n\subseteq
D_{n+1}\subseteq\cdots$), we obtain a family $\{U_r\}_{r\in D}$ of open subsets of $X$ with

$$\textbf{(P1)}\quad A\subseteq U_0,\qquad U_1=X\setminus B,$$
$$\textbf{(P2)}\quad \operatorname{cl}(U_r)\subseteq U_s \text{ for all } r<s \text{ in } D.$$

In particular, since $0$ is the minimum and $1$ the maximum of $D$, (P2) gives $U_r\subseteq
U_1=X\setminus B$ for every $r\in D$ (take $s=1$ if $r<1$; trivial if $r=1$), i.e.

$$\textbf{(P3)}\quad U_r\cap B=\varnothing \text{ for every } r\in D.$$

---

## 3. Definition of $f$ and its basic properties

For $x\in X$, define
$$f(x)\;=\;\inf\{\,r\in D : x\in U_r\,\},$$
with the convention $\inf\varnothing = 1$.

Since $\{r\in D: x\in U_r\}\subseteq D\subseteq[0,1]$, this infimum (when the set is
nonempty) lies in $[0,1]$; together with the convention for the empty case, $f(x)\in[0,1]$
for every $x\in X$. Thus $f:X\to[0,1]$.

**$f=0$ on $A$.** If $x\in A$, then by (P1) $x\in U_0$, so $0\in\{r:x\in U_r\}$ and hence
$f(x)\le 0$; since $f(x)\ge 0$ always (it is an infimum of a subset of $[0,1]$, or $1$),
$f(x)=0$.

**$f=1$ on $B$.** If $x\in B$, then by (P3) $x\notin U_r$ for every $r\in D$, so
$\{r:x\in U_r\}=\varnothing$ and $f(x)=1$ by the convention.

It remains to prove $f$ is continuous.

---

## 4. Two key claims

**Claim A.** For $r\in D$: $\quad x\in U_r\ \Longrightarrow\ f(x)\le r.$

*Proof.* $r\in\{s\in D:x\in U_s\}$, a nonempty set, so its infimum $f(x)$ is $\le r$.
$\blacksquare$

**Claim A$'$.** For $r\in D$: $\quad f(x)<r\ \Longrightarrow\ x\in U_r.$

*Proof.* If $f(x)<r$, then since $f(x)=\inf\{s\in D:x\in U_s\}$ and this infimum is $<r$,
the set $\{s\in D:x\in U_s\}$ is nonempty (an empty set has infimum $1\ge r$ only if
$r\le1$, but strictly $f(x)<r\le 1$ forces the set nonempty since the convention value $1$
would not be $<r$ unless $r>1$, impossible as $r\in D\subseteq[0,1]$) and there exists
$s\in D$, $x\in U_s$, with $s<r$ (a basic property of infimum: if $\inf S<r$ then some
element of $S$ is $<r$). By (P2), $\operatorname{cl}(U_s)\subseteq U_r$, so
$x\in U_s\subseteq U_r$. $\blacksquare$

**Claim B.** For $r\in D$: $\quad x\notin\operatorname{cl}(U_r)\ \Longrightarrow\ f(x)\ge r.$

*Proof.* Suppose $x\notin\operatorname{cl}(U_r)$. We show $x\notin U_s$ for every $s\in D$
with $s\le r$; this forces $\{s\in D:x\in U_s\}\subseteq(r,1]\cap D$, so its infimum (or the
convention value $1$, if the set is empty) is $\ge r$, i.e. $f(x)\ge r$.

Let $s\le r$, $s\in D$. If $s=r$: $x\notin\operatorname{cl}(U_r)\supseteq U_r$ gives
$x\notin U_r=U_s$. If $s<r$: by (P2), $\operatorname{cl}(U_s)\subseteq U_r\subseteq
\operatorname{cl}(U_r)$; if $x$ were in $U_s$ it would be in $\operatorname{cl}(U_r)$,
contradiction. So $x\notin U_s$. $\blacksquare$

**Claim B$'$.** For $r\in D$: $\quad x\in\operatorname{cl}(U_r)\ \Longrightarrow\ f(x)\le r.$

*Proof.* Let $s\in D$ with $s>r$. By (P2), $\operatorname{cl}(U_r)\subseteq U_s$, so
$x\in\operatorname{cl}(U_r)$ gives $x\in U_s$; by Claim A, $f(x)\le s$. This holds for every
dyadic $s>r$, and by Lemma 1 the dyadic rationals greater than $r$ have infimum $r$
(density), so $f(x)\le\inf\{s\in D:s>r\}=r$. $\blacksquare$

(Claim B$'$ is the contrapositive-strengthening of Claim A, and Claim B is used in its
contrapositive form below; both directions will be needed.)

---

## 5. Continuity of $f$

We use Lemma 2 with $Y=[0,1]$. Fix $a\in\mathbb{R}$; we show
$f^{-1}\big([0,1]\cap(-\infty,a)\big)=\{x:f(x)<a\}$ and
$f^{-1}\big([0,1]\cap(a,\infty)\big)=\{x:f(x)>a\}$ are both open in $X$.

**The set $\{x:f(x)<a\}$.**

- If $a\le 0$: since $f(x)\ge 0$ always, the set is $\varnothing$, which is open.
- If $a>1$: since $f(x)\le 1<a$ always, the set is $X$, which is open.
- If $0<a\le 1$: we claim
$$\{x: f(x)<a\} = \bigcup_{r\in D,\ r<a} U_r. \tag{5.1}$$
  ($\subseteq$) If $f(x)<a$, by Lemma 1 there is $r\in D$ with $f(x)<r<a$ (density of $D$ in
  $[0,1]$; such $r$ exists in $(f(x),a)\cap D\subseteq[0,1]$ since $f(x)<a\le1$). By Claim
  A$'$, $f(x)<r$ implies $x\in U_r$, and $r<a$, so $x$ is in the right-hand union.
  ($\supseteq$) If $x\in U_r$ for some $r\in D$ with $r<a$, Claim A gives $f(x)\le r<a$.

  The right-hand side of (5.1) is a union of open sets $U_r$, hence open. So
  $\{x:f(x)<a\}$ is open.

**The set $\{x:f(x)>a\}$.**

- If $a\ge 1$: since $f(x)\le1$ always, the set is $\varnothing$, open.
- If $a<0$: since $f(x)\ge0>a$ always, the set is $X$, open.
- If $0\le a<1$: we claim
$$\{x: f(x)>a\} = \bigcup_{r\in D,\ r>a} \big(X\setminus \operatorname{cl}(U_r)\big). \tag{5.2}$$
  ($\subseteq$) If $f(x)>a$, by Lemma 1 there is $r\in D$ with $a<r<f(x)$ (density, using
  $a<f(x)\le1$). By the contrapositive of Claim B$'$ ($f(x)>r\Rightarrow x\notin
  \operatorname{cl}(U_r)$), $x\notin\operatorname{cl}(U_r)$, and $r>a$, so $x$ lies in the
  right-hand union.
  ($\supseteq$) If $x\notin\operatorname{cl}(U_r)$ for some $r\in D$ with $r>a$, Claim B
  gives $f(x)\ge r>a$.

  Each $X\setminus\operatorname{cl}(U_r)$ is open (complement of a closed set), so the
  right-hand side of (5.2) is open, hence $\{x:f(x)>a\}$ is open.

Since $a\in\mathbb{R}$ was arbitrary, both families of preimages required by Lemma 2 are
open, so $f:X\to[0,1]$ is continuous. $\blacksquare$

---

## 6. Conclusion

The function $f:X\to[0,1]$ constructed in Section 3 satisfies $f\equiv 0$ on $A$ and
$f\equiv 1$ on $B$ (Section 3), and is continuous (Section 5). This proves Urysohn's Lemma:
for a normal space $X$ and disjoint closed sets $A,B\subseteq X$, there exists a continuous
$f:X\to[0,1]$ with $f|_A=0$ and $f|_B=1$. $\blacksquare$

---

## 7. Summary of what was used

- **Definition of normal** (as given in the statement): applied twice per construction step
  — once in the base case, once per new dyadic midpoint at each induction level — via the
  Shrinking Lemma (Lemma 0, proved in Section 1 directly from the definition; no other form
  of normality is used).
- **Lemma 1** (density of dyadic rationals in $[0,1]$, elementary real analysis, Rudin
  Thm. 1.20) — used to produce the countable index set $D$ with the order property (P2),
  and again in Section 5 to produce the strict intermediate dyadic points needed for both
  set identities (5.1) and (5.2).
- **Lemma 2** (subbasis criterion for continuity into a subspace of $\mathbb{R}$, Munkres
  Thm. 18.1 / Willard Thm. 8.5) — used once, to reduce continuity of $f$ to the two families
  of preimages computed in Section 5.
- No separation axiom beyond normality (in particular, no $T_1$/Hausdorff hypothesis) was
  used at any point, consistent with the theorem statement's parenthetical remark.
