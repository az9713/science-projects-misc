# P4 Theorem 9 — The Radon–Nikodym Theorem

## Statement

Let $(\Omega,\mathcal F)$ be a measurable space and let $\mu,\nu$ be $\sigma$-finite
positive measures on $\mathcal F$ with $\nu \ll \mu$ (i.e. $\mu(E)=0 \Rightarrow \nu(E)=0$
for $E\in\mathcal F$). Then there exists an $\mathcal F$-measurable function
$f:\Omega\to[0,\infty)$ such that
$$\nu(E)=\int_E f\,d\mu \qquad \text{for every } E\in\mathcal F .$$
The function $f$ is unique up to $\mu$-almost-everywhere equality.

The proof below is von Neumann's 1940 Hilbert-space proof (existence, via $L^2$ and the
Riesz representation theorem) together with the standard $\sigma$-finite exhaustion
argument and a direct uniqueness argument. Every non-elementary fact used is stated as a
named lemma before it is used.

---

## 0. Preliminary lemmas

All lemmas are standard results of measure and integration theory (Halmos, *Measure
Theory*, 1950; Rudin, *Real and Complex Analysis*, 1987; Folland, *Real Analysis*, 1999).
They are quoted, not reproved, except where the proof is one line.

**Lemma A (monotonicity of the measure comparison).** If $\lambda_1,\lambda_2$ are
positive measures on $(\Omega,\mathcal F)$ and $\lambda_1(E)\le\lambda_2(E)$ for every
$E\in\mathcal F$, then for every $\mathcal F$-measurable $\varphi\ge0$,
$\int\varphi\,d\lambda_1\le\int\varphi\,d\lambda_2$.
*(Proof sketch: true for indicators by hypothesis, extends to nonnegative simple
functions by linearity, and to nonnegative measurable functions by the Monotone
Convergence Theorem, Lemma F below, applied to an increasing sequence of simple functions
converging to $\varphi$.)*

**Lemma B (positivity of the integral).** If $\lambda$ is a positive measure,
$E\in\mathcal F$ with $\lambda(E)>0$, and $\varphi>0$ pointwise on $E$, then
$\int_E\varphi\,d\lambda>0$.
*(Proof: $E=\bigcup_{k=1}^\infty E_k$ with $E_k=E\cap\{\varphi\ge 1/k\}$, an increasing
union, so by continuity from below (Lemma D) $\lambda(E_k)\to\lambda(E)>0$; hence
$\lambda(E_k)>0$ for some $k$, and $\int_E\varphi\,d\lambda\ge\int_{E_k}\varphi\,d\lambda
\ge \lambda(E_k)/k>0$.)*

**Lemma C (finite integral $\Rightarrow$ a.e. finite).** If $\varphi\ge0$ is
$\mathcal F$-measurable and $\int\varphi\,d\lambda<\infty$, then $\varphi<\infty$
$\lambda$-a.e.
*(Proof: if $\lambda(\{\varphi=\infty\})>0$ then by Lemma B, applied on
$\{\varphi=\infty\}$ with the constant value $+\infty$, $\int\varphi\,d\lambda=\infty$,
a contradiction.)*

**Lemma D (continuity from below/above of measures).** If $\lambda$ is a positive measure
and $E_1\subseteq E_2\subseteq\cdots$ (resp. $E_1\supseteq E_2\supseteq\cdots$ with
$\lambda(E_1)<\infty$) are in $\mathcal F$, then $\lambda\!\left(\bigcup_n E_n\right)
=\lim_n\lambda(E_n)$ (resp. $\lambda\!\left(\bigcap_n E_n\right)=\lim_n\lambda(E_n)$).
This is a direct consequence of countable additivity.

**Lemma E (Cauchy–Schwarz inequality).** For a positive measure $\lambda$ and
$g,\phi\in L^2(\lambda)$, $\left|\int g\phi\,d\lambda\right|\le\|g\|_2\,\|\phi\|_2$, where
$\|g\|_2=\left(\int g^2\,d\lambda\right)^{1/2}$.

**Lemma F (Monotone Convergence Theorem, MCT).** If $0\le\varphi_1\le\varphi_2\le\cdots$
are $\mathcal F$-measurable and $\varphi_n\uparrow\varphi$ pointwise, then
$\int\varphi_n\,d\lambda\uparrow\int\varphi\,d\lambda$.

**Lemma G (Dominated Convergence Theorem, DCT).** If $\varphi_n\to\varphi$ pointwise
$\lambda$-a.e. and $|\varphi_n|\le\Phi$ for all $n$ with $\Phi\in L^1(\lambda)$, then
$\int\varphi_n\,d\lambda\to\int\varphi\,d\lambda$.

**Lemma H (Riesz–Fischer theorem).** For a positive measure $\lambda$, $L^2(\lambda)$
(real-valued, square-$\lambda$-integrable functions modulo $\lambda$-a.e. equality),
equipped with $\langle g,\phi\rangle=\int g\phi\,d\lambda$, is a complete inner-product
space, i.e. a (real) Hilbert space.

**Lemma I (Riesz Representation Theorem for Hilbert spaces).** If $H$ is a Hilbert space
and $T:H\to\mathbb R$ is a bounded linear functional, then there is a unique $h\in H$ with
$T(g)=\langle g,h\rangle$ for all $g\in H$.

These are the only external results used. Everything else below is proved from them.

---

## 1. Reduction to the case of two finite measures

Because $\mu$ is $\sigma$-finite, write $\Omega=\bigcup_{i=1}^\infty A_i$ with
$A_i\in\mathcal F$ pairwise disjoint and $\mu(A_i)<\infty$. Because $\nu$ is
$\sigma$-finite, write $\Omega=\bigcup_{j=1}^\infty B_j$ with $B_j\in\mathcal F$ pairwise
disjoint and $\nu(B_j)<\infty$. The countable family $\{A_i\cap B_j\}_{i,j\ge1}$ is a
countable, pairwise-disjoint partition of $\Omega$ into sets on which *both* $\mu$ and
$\nu$ are finite (since $\mu(A_i\cap B_j)\le\mu(A_i)<\infty$ and
$\nu(A_i\cap B_j)\le\nu(B_j)<\infty$). Re-index this partition as $\{\Omega_n\}_{n\ge1}$.

For each $n$, let $\mathcal F_n=\{E\cap\Omega_n : E\in\mathcal F\}$ (the trace
$\sigma$-algebra on $\Omega_n$), and let $\mu_n,\nu_n$ be the restrictions of $\mu,\nu$ to
$(\Omega_n,\mathcal F_n)$; these are **finite** positive measures. If $\mu_n(E)=0$ for
$E\in\mathcal F_n$, i.e. $\mu(E)=0$ (viewing $E\subseteq\Omega_n\subseteq\Omega$), then
$\nu(E)=0$ since $\nu\ll\mu$, i.e. $\nu_n(E)=0$. So $\nu_n\ll\mu_n$.

**Claim.** If the theorem holds for every pair of finite measures, then it holds for
$\mu,\nu$.

*Proof of claim.* By that case, for each $n$ there is $\mathcal F_n$-measurable
$f_n:\Omega_n\to[0,\infty)$ with $\nu(E)=\int_E f_n\,d\mu$ for every $\mathcal
F$-measurable $E\subseteq\Omega_n$. Extend $f_n$ to all of $\Omega$ by setting $f_n=0$ on
$\Omega\setminus\Omega_n$; this extension is $\mathcal F$-measurable. Define
$$f=\sum_{n=1}^\infty f_n .$$
This is $\mathcal F$-measurable (a pointwise-convergent, in fact pointwise-exact-at-one-
term, series of nonnegative measurable functions) and $f\ge0$. For any $E\in\mathcal F$,
since the $\Omega_n$ partition $\Omega$,
$$\nu(E)=\sum_{n=1}^\infty \nu(E\cap\Omega_n)=\sum_{n=1}^\infty\int_{E\cap\Omega_n} f_n\,d\mu
=\sum_{n=1}^\infty\int_E f_n\,d\mu \stackrel{\text{Lemma F}}{=} \int_E\Big(\sum_n f_n\Big)d\mu
=\int_E f\,d\mu,$$
where the first equality is countable additivity of $\nu$, the third uses $f_n=0$ off
$\Omega_n$, and the interchange of sum and integral is Lemma F (MCT) applied to the
partial sums $\sum_{n=1}^N f_n \uparrow f$. This proves the existence part of the claim.
$\blacksquare$

It remains to prove the theorem when $\mu,\nu$ are both **finite** positive measures on
$(\Omega,\mathcal F)$ with $\nu\ll\mu$, and separately to prove uniqueness in full
$\sigma$-finite generality (Section 4).

---

## 2. Existence for finite measures (von Neumann's $L^2$ argument)

Assume now $\mu(\Omega)<\infty$, $\nu(\Omega)<\infty$, $\nu\ll\mu$.

### 2.1 A bounded functional on $L^2(\lambda)$

Let $\lambda=\mu+\nu$. Then $\lambda$ is a finite positive measure, and $\nu(E)\le\lambda(E)$
for every $E\in\mathcal F$ (since $\mu\ge0$).

Define $T:L^2(\lambda)\to\mathbb R$ by
$$T(g)=\int g\,d\nu .$$
$T$ is well defined and bounded: since $\lambda(\Omega)<\infty$, every bounded
measurable function lies in $L^2(\lambda)$, and for general $g\in L^2(\lambda)$,
$$|T(g)|\le\int|g|\,d\nu \stackrel{\text{Lemma A}}{\le}\int|g|\,d\lambda
\stackrel{\text{Lemma E}}{\le}\lambda(\Omega)^{1/2}\Big(\int g^2\,d\lambda\Big)^{1/2}
=\lambda(\Omega)^{1/2}\|g\|_2 ,$$
(Lemma E applied with the pair $|g|,\mathbf 1$). $T$ is clearly linear. So $T$ is a
bounded linear functional on the Hilbert space $L^2(\lambda)$ (Lemma H), with operator
norm at most $\lambda(\Omega)^{1/2}<\infty$.

By the Riesz Representation Theorem (Lemma I), there is a unique $h\in L^2(\lambda)$ with
$$\int g\,d\nu = \int g\,h\,d\lambda \qquad\text{for every } g\in L^2(\lambda). \tag{2.1}$$
Since $\lambda$ is finite, (2.1) in particular holds for every bounded
$\mathcal F$-measurable $g$.

### 2.2 $h$ takes values in $[0,1]$ $\lambda$-a.e.

Suppose $\lambda(\{h<0\})>0$; put $E=\{h<0\}$. Take $g=\mathbf 1_E$ in (2.1):
$$\nu(E)=\int_E h\,d\lambda .$$
On $E$, $-h>0$, so by Lemma B, $\int_E(-h)\,d\lambda>0$, i.e. $\int_E h\,d\lambda<0$. But
$\nu(E)\ge0$ since $\nu$ is a positive measure. Contradiction. Hence $h\ge0$
$\lambda$-a.e.

Suppose $\lambda(\{h>1\})>0$; put $F=\{h>1\}$, so $\lambda(F)>0$. Take $g=\mathbf 1_F$ in
(2.1):
$$\nu(F)=\int_F h\,d\lambda .$$
On $F$, $h-1>0$, so by Lemma B, $\int_F(h-1)\,d\lambda>0$, i.e.
$\int_F h\,d\lambda>\lambda(F)$. Thus $\nu(F)>\lambda(F)$. But
$\nu(F)\le\lambda(F)$ (Section 2.1). Contradiction. Hence $h\le1$ $\lambda$-a.e.

Redefine $h$ on the $\lambda$-null set where $0\le h\le1$ fails (setting it, say, to $0$
there); this does not change any integral against $\lambda$, so (2.1) still holds, and now
$h:\Omega\to[0,1]$ everywhere.

### 2.3 The key identity

Substituting $h=1-(1-h)$ is not needed; instead rewrite (2.1), for bounded measurable
$g$, as
$$\int g(1-h)\,d\nu = \int g\,d\nu-\int gh\,d\nu
\stackrel{(2.1)}{=}\int gh\,d\lambda-\int gh\,d\nu
=\int gh\,d\mu+\int gh\,d\nu-\int gh\,d\nu=\int gh\,d\mu,$$
using $\lambda=\mu+\nu$. Hence for every bounded $\mathcal F$-measurable $g$,
$$\int g(1-h)\,d\nu=\int g\,h\,d\mu. \tag{2.2}$$

### 2.4 The set $A=\{h=1\}$ is $\mu$-null

Take $g=\mathbf 1_A$ in (2.2), $A=\{h=1\}$: the left side is $\int_A(1-h)\,d\nu=0$ since
$1-h=0$ on $A$; the right side is $\int_A h\,d\mu=\mu(A)$ since $h=1$ on $A$. Hence
$$\mu(A)=0. \tag{2.3}$$
Since $\nu\ll\mu$, (2.3) gives $\nu(A)=0$ as well.

### 2.5 Constructing $f$ on $A^c$

Fix bounded $\mathcal F$-measurable $g\ge0$. For $n=0,1,2,\dots$ let
$$g_n=g\,\mathbf 1_{A^c}\sum_{k=0}^n h^k .$$
Each $g_n$ is bounded and measurable (a finite sum of products of bounded measurable
functions), so (2.2) applies to $g_n$:
$$\int g_n(1-h)\,d\nu=\int g_n h\,d\mu .$$
Since $(1-h)\sum_{k=0}^n h^k=1-h^{n+1}$, the left side is
$\int g\,\mathbf 1_{A^c}(1-h^{n+1})\,d\nu$, and the right side is
$\int g\,\mathbf 1_{A^c}\sum_{k=1}^{n+1}h^k\,d\mu$. So
$$\int_{A^c} g\,(1-h^{n+1})\,d\nu=\int_{A^c} g\Big(\sum_{k=1}^{n+1}h^k\Big)\,d\mu. \tag{2.4}$$

*Left side as $n\to\infty$:* on $A^c$, $0\le h<1$, so $h^{n+1}\to0$ pointwise on $A^c$;
$g(1-h^{n+1})\mathbf1_{A^c}$ is bounded uniformly in $n$ by $\sup|g|$, and $\nu$ is a
finite measure, so the constant function $\sup|g|$ is $\nu$-integrable. By the Dominated
Convergence Theorem (Lemma G),
$$\int_{A^c} g(1-h^{n+1})\,d\nu \;\longrightarrow\; \int_{A^c} g\,d\nu .$$

*Right side as $n\to\infty$:* $g\ge0$ and the partial sums
$\sum_{k=1}^{n+1}h^k\,\mathbf1_{A^c}$ increase pointwise on $A^c$ (since $h\ge0$) to
$\dfrac{h}{1-h}\mathbf 1_{A^c}\in[0,\infty]$ (a geometric series, convergent pointwise
since $0\le h<1$ on $A^c$). By the Monotone Convergence Theorem (Lemma F),
$$\int_{A^c} g\Big(\sum_{k=1}^{n+1}h^k\Big)\,d\mu \;\longrightarrow\; \int_{A^c} g\,\frac{h}{1-h}\,d\mu \;\in[0,\infty].$$

Passing to the limit in (2.4):
$$\int_{A^c} g\,d\nu = \int_{A^c} g\,\frac{h}{1-h}\,d\mu \qquad\text{for every bounded measurable } g\ge0. \tag{2.5}$$
The left side is finite (bounded by $\sup|g|\cdot\nu(\Omega)<\infty$), so the right side
is finite too, for every such $g$.

Define
$$f=\frac{h}{1-h}\,\mathbf 1_{A^c} \quad(\text{with } f=0 \text{ on } A). $$
$f$ is $\mathcal F$-measurable (a measurable function of $h$ times an indicator), and
$f\ge0$, $f:\Omega\to[0,\infty)$ since $f$ is finite everywhere by construction (a
genuine real number at every point of $A^c$, and $0$ on $A$).

### 2.6 $f$ is the Radon–Nikodym derivative

Fix $E\in\mathcal F$ and apply (2.5) with $g=\mathbf 1_E$ (bounded, measurable, $\ge0$):
$$\nu(E\cap A^c) = \int_{E\cap A^c} f\,d\mu = \int_E f\,d\mu$$
(the last equality because $f=0$ on $A$). Since $\nu(A)=0$ (Section 2.4),
$\nu(E\cap A^c)=\nu(E)-\nu(E\cap A)=\nu(E)$. Hence
$$\nu(E)=\int_E f\,d\mu \qquad\text{for every } E\in\mathcal F,$$
which is the claimed identity for the finite-measure case. This completes Section 1's
reduction (via 2.1–2.6, existence is proved for finite measures, hence, by Section 1, for
$\sigma$-finite $\mu,\nu$).

---

## 3. $f<\infty$ everywhere and integrability remark

By construction in Section 2.5, $f$ is real-valued everywhere ($[0,\infty)$-valued, not
merely finite a.e.), matching the theorem's statement exactly. In the general
$\sigma$-finite construction of Section 1, $f=\sum_n f_n$ with each $f_n\ge0$
real-valued; since $\int f_n\,d\mu=\nu(\Omega_n)<\infty$ (finite, by the choice of the
partition in Section 1), Lemma C gives $f_n<\infty$ $\mu$-a.e., and since a countable
union of $\mu$-null sets is $\mu$-null, $f=\sum_n f_n<\infty$ $\mu$-a.e. On the
$\mu$-null exceptional set (if any) redefine $f:=0$; this changes $f$ only on a
$\mu$-null set, so $\int_E f\,d\mu$ is unaffected for every $E$ (integrals over a
$\mu$-null set's contribution vanish), and now $f:\Omega\to[0,\infty)$ everywhere, as the
theorem states.

---

## 4. Uniqueness

**Claim.** If $f,f':\Omega\to[0,\infty)$ are $\mathcal F$-measurable and
$\int_E f\,d\mu=\int_E f'\,d\mu\;(=\nu(E))$ for every $E\in\mathcal F$, then $f=f'$
$\mu$-a.e.

*Proof.* It suffices to show $\mu(\{f>f'\})=0$; the symmetric argument (exchanging the
roles of $f$ and $f'$) then gives $\mu(\{f'>f\})=0$, and
$\{f\ne f'\}=\{f>f'\}\cup\{f'>f\}$, so $\mu(\{f\ne f'\})=0$.

Since $\mu$ is $\sigma$-finite, write $\Omega=\bigcup_n\Omega_n$, $\Omega_n\in\mathcal F$
pairwise disjoint, $\mu(\Omega_n)<\infty$. Since $\{f>f'\}=\bigcup_n(\{f>f'\}\cap\Omega_n)$,
it suffices (countable subadditivity) to show $\mu(\{f>f'\}\cap\Omega_n)=0$ for each $n$.
Fix $n$.

Since $\nu$ is $\sigma$-finite, write $\Omega=\bigcup_m C_m$ with $C_m\in\mathcal F$
increasing and $\nu(C_m)<\infty$. Fix $k\ge1$ and $m\ge1$, and set
$$A_{k,m}=\{f\ge f'+1/k\}\cap\Omega_n\cap C_m .$$
This is well defined for all $\omega$ (using extended-real arithmetic $f'+1/k$, finite
since $f'(\omega)\in[0,\infty)$), and $A_{k,m}\in\mathcal F$.

On $A_{k,m}$: since $f'\ge0$ is finite-valued everywhere (theorem's conclusion) and
$f\ge f'+1/k$ forces $f$ finite too (as $f'+1/k<\infty$), both $f,f'$ are real numbers on
$A_{k,m}$, so $f-f'$ is a well-defined, $\mathcal F$-measurable, real-valued function on
$A_{k,m}$, and $f-f'\ge 1/k>0$ there.

By hypothesis, $\int_{A_{k,m}} f\,d\mu=\nu(A_{k,m})=\int_{A_{k,m}} f'\,d\mu$. Both sides
equal $\nu(A_{k,m})\le\nu(C_m)<\infty$, so both integrals are finite real numbers
(nonnegative integrands with finite integral). Because both are finite, the subtraction
is legitimate:
$$\int_{A_{k,m}}(f-f')\,d\mu=\int_{A_{k,m}}f\,d\mu-\int_{A_{k,m}}f'\,d\mu=0 .$$
But $f-f'\ge1/k>0$ on $A_{k,m}$, so by Lemma B, if $\mu(A_{k,m})>0$ then
$\int_{A_{k,m}}(f-f')\,d\mu>0$, a contradiction. Hence
$$\mu(A_{k,m})=0 \qquad\text{for all } k,m. \tag{4.1}$$

Fix $k$. The sets $C_m$ increase to $\Omega$, so $A_{k,m}=\{f\ge f'+1/k\}\cap\Omega_n\cap
C_m$ increases (in $m$) to $\{f\ge f'+1/k\}\cap\Omega_n$. By continuity from below (Lemma
D) and (4.1),
$$\mu\big(\{f\ge f'+1/k\}\cap\Omega_n\big)=\lim_{m\to\infty}\mu(A_{k,m})=0 .$$
Now let $k\to\infty$: the sets $\{f\ge f'+1/k\}\cap\Omega_n$ increase (as $1/k$
decreases) to $\{f>f'\}\cap\Omega_n$ (since $f,f'$ are finite everywhere,
$f(\omega)>f'(\omega)$ iff $f(\omega)\ge f'(\omega)+1/k$ for some $k$). By Lemma D again,
$$\mu\big(\{f>f'\}\cap\Omega_n\big)=\lim_{k\to\infty}\mu\big(\{f\ge f'+1/k\}\cap\Omega_n\big)=0 .$$
This holds for every $n$, so, as noted above,
$$\mu(\{f>f'\})\le\sum_n\mu\big(\{f>f'\}\cap\Omega_n\big)=0 .$$
By the symmetric argument, $\mu(\{f'>f\})=0$, and therefore $\mu(\{f\ne f'\})=0$, i.e.
$f=f'$ $\mu$-a.e. $\blacksquare$

---

## 5. Conclusion

Section 1 reduces the $\sigma$-finite case to the finite-measure case. Sections 2–3
construct, for finite $\mu,\nu$ with $\nu\ll\mu$, an $\mathcal F$-measurable
$f:\Omega\to[0,\infty)$ with $\nu(E)=\int_E f\,d\mu$ for all $E\in\mathcal F$, using only
the Cauchy–Schwarz inequality (Lemma E), the Riesz–Fischer completeness of $L^2$ (Lemma
H), the Riesz Representation Theorem for Hilbert spaces (Lemma I), and the Monotone and
Dominated Convergence Theorems (Lemmas F, G). Section 1's reassembly argument (via MCT)
extends this to $\sigma$-finite $\mu,\nu$. Section 4 proves that any two functions
satisfying the conclusion agree $\mu$-almost everywhere, using only $\sigma$-finiteness of
$\mu$ and $\nu$, continuity from below of measures (Lemma D), and positivity of the
integral over sets of positive measure (Lemma B).

This establishes both the existence and the $\mu$-a.e. uniqueness of $f$, as stated in
Theorem 9. $\blacksquare$

---

### Named results used (for reference)

- Cauchy–Schwarz inequality (Lemma E)
- Monotone Convergence Theorem (Lemma F)
- Dominated Convergence Theorem (Lemma G)
- Riesz–Fischer theorem: completeness of $L^2(\lambda)$ (Lemma H)
- Riesz Representation Theorem for Hilbert spaces (Lemma I)
- Countable additivity / continuity from below and above of measures (Lemma D)
- von Neumann's 1940 $L^2$ proof strategy (Sections 2.1–2.6), as presented in, e.g.,
  Rudin, *Real and Complex Analysis*, 3rd ed., Theorem 6.10, and Folland, *Real
  Analysis*, 2nd ed., Theorem 3.8.
