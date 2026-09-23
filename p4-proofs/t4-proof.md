# Theorem (Strong Law of Large Numbers, Etemadi's form)

**Statement.** Let $X_1, X_2, \dots$ be real random variables on a probability space
$(\Omega, \mathcal F, P)$ that are **pairwise independent** and **identically distributed**,
with $E|X_1| < \infty$. Let $S_n = X_1 + \cdots + X_n$. Then
$$\frac{S_n}{n} \to E[X_1] \quad \text{almost surely as } n \to \infty.$$

The point of Etemadi's proof (1981) is that it needs only **pairwise** independence, not
full independence. The classical proof of the SLLN uses Kolmogorov's maximal inequality,
which is proved from full independence. Etemadi's proof instead applies Chebyshev's
inequality only along a sparse geometric subsequence $n_k = \lfloor \alpha^k \rfloor$, and
Chebyshev's inequality needs only that $\operatorname{Var}(\sum Y_k) = \sum \operatorname{Var}(Y_k)$,
which holds already under pairwise uncorrelatedness. A monotonicity argument (valid because
we reduce to $X_i \ge 0$) then fills in the values of $n$ between subsequence points.

---

## 0. Lemmas used, with citations

**Lemma 1 (functions of independent variables are independent).** If $X$ and $Y$ are
independent random variables and $g, h$ are Borel measurable functions, then $g(X)$ and
$h(Y)$ are independent. *Citation:* this is immediate from the definition of independence
via $\sigma$-algebras — $\sigma(g(X)) \subseteq \sigma(X)$ and $\sigma(h(Y)) \subseteq
\sigma(Y)$, and independent $\sigma$-algebras contain only independent random variables
measurable with respect to them. See Billingsley, *Probability and Measure*, 3rd ed.,
Theorem 20.4, or Durrett, *Probability: Theory and Examples*, 5th ed., §2.1. Applied
componentwise, if $X_1, X_2, \dots$ are pairwise independent, then $g(X_1), g(X_2), \dots$
are pairwise independent for any fixed measurable $g$ (apply the lemma to each pair $i \ne j$).

**Lemma 2 (Chebyshev's inequality).** For a random variable $Z$ with $E[Z^2] < \infty$ and
$t > 0$, $P(|Z - E Z| > t) \le \operatorname{Var}(Z)/t^2$. *Citation:* Durrett, §1.6, or any
standard probability text (Markov's inequality applied to $(Z - EZ)^2$).

**Lemma 3 (Borel–Cantelli I).** If $A_1, A_2, \dots$ are events with $\sum_n P(A_n) <
\infty$, then $P(A_n \text{ infinitely often}) = 0$. *Citation:* Durrett, Theorem 2.3.1;
Billingsley, Theorem 4.3.

**Lemma 4 (Monotone Convergence Theorem).** If $0 \le Z_k \uparrow Z$ pointwise, then
$E[Z_k] \to E[Z]$ (both possibly $+\infty$). *Citation:* Durrett, Theorem 1.5.1;
Rudin, *Real and Complex Analysis*, Theorem 1.26.

**Lemma 5 (Tonelli's theorem).** For a nonnegative measurable function of two variables,
the integral (or sum) may be computed in either order, and any rearrangement of a
nonnegative double series has the same sum. *Citation:* Rudin, *Real and Complex Analysis*,
Theorem 8.8 (Tonelli); the discrete case (Fubini–Tonelli for series) is the statement that
a double series with nonnegative terms may be summed in any order.

**Lemma 6 (Cesàro's theorem).** If $a_1, a_2, \dots \in \mathbb R$ and $a_k \to L$, then
$\frac{1}{n}\sum_{k=1}^n a_k \to L$. *Proof.* Fix $\varepsilon > 0$ and choose $N$ with
$|a_k - L| < \varepsilon$ for all $k > N$. For $n > N$,
$$\left|\frac{1}{n}\sum_{k=1}^n a_k - L\right| \le \frac{1}{n}\sum_{k=1}^N |a_k - L| +
\frac{1}{n}\sum_{k=N+1}^n |a_k - L| \le \frac{1}{n}\sum_{k=1}^N|a_k-L| + \varepsilon.$$
The first term $\to 0$ as $n \to \infty$ ($N$ fixed), so $\limsup_n \left|\frac1n\sum a_k -
L\right| \le \varepsilon$. Let $\varepsilon \downarrow 0$. $\blacksquare$ *Citation:*
standard classical analysis; e.g. Rudin, *Principles of Mathematical Analysis*, Theorem 3.4
(Cesàro means of a convergent sequence converge to the same limit).

**Lemma 7 (tail-sum bound).** If $X \ge 0$ and $E X < \infty$, then $\sum_{k=1}^\infty P(X >
k) \le E X$. *Proof.* By Tonelli (Lemma 5), for $X \ge 0$,
$$E X = E\left[\int_0^\infty \mathbf 1\{t < X\}\,dt\right] = \int_0^\infty P(X>t)\,dt.$$
Since $t \mapsto P(X>t)$ is nonincreasing, $P(X>k) \le \int_{k-1}^k P(X>t)\,dt$ for each
integer $k \ge 1$. Summing,
$$\sum_{k=1}^\infty P(X>k) \le \sum_{k=1}^\infty \int_{k-1}^k P(X>t)\,dt \le \int_0^\infty
P(X>t)\,dt = EX. \qquad\blacksquare$$

**Lemma 8 (truncated second-moment bound).** If $X \ge 0$ and $EX < \infty$, then
$$\sum_{k=1}^\infty \frac{E[X^2 \mathbf 1\{X \le k\}]}{k^2} \le 2\,EX < \infty.$$
*Proof.* First, an elementary sum estimate: for every integer $m \ge 1$,
$$\sum_{k=m}^\infty \frac{1}{k^2} \le \frac 2m. \tag{$*$}$$
Indeed, for $k \ge 2$, $\frac{1}{k^2} \le \frac{1}{k(k-1)} = \frac{1}{k-1}-\frac1k$, so
$$\sum_{k=m}^\infty \frac1{k^2} = \frac1{m^2} + \sum_{k=m+1}^\infty \frac1{k^2} \le
\frac1{m^2} + \sum_{k=m+1}^\infty\left(\frac1{k-1}-\frac1k\right) = \frac1{m^2}+\frac1m \le
\frac2m,$$
the last step because $m \ge 1 \Rightarrow 1/m^2 \le 1/m$.

Now define, for $x \ge 0$, $g(x) = \sum_{k \ge \max(1,\lceil x\rceil)} 1/k^2$. If $x>0$, let
$m = \lceil x \rceil \ge 1 \ge x/m$, i.e. $m \ge x$, so by $(*)$, $g(x) \le 2/m \le 2/x$.
Hence $x^2 g(x) \le 2x$ for $x > 0$; and at $x=0$, $x^2g(x) = 0 = 2\cdot 0$. So
$$x^2 g(x) \le 2x \quad \text{for all } x \ge 0. \tag{$**$}$$
Finally, by Tonelli (Lemma 5, all terms nonnegative),
$$\sum_{k=1}^\infty \frac{E[X^2\mathbf1\{X\le k\}]}{k^2} = E\left[X^2\sum_{k=1}^\infty
\frac{\mathbf1\{X\le k\}}{k^2}\right] = E[X^2 g(X)] \overset{(**)}{\le} E[2X] = 2EX.
\qquad\blacksquare$$

**Lemma 9 (geometric-subsequence sum bound).** Fix $\alpha > 1$ and let $n_k = \lfloor
\alpha^k \rfloor$ for $k = 0, 1, 2, \dots$ (so $n_k \ge 1$). There is a constant $C_\alpha <
\infty$, depending only on $\alpha$, such that for every integer $j \ge 1$,
$$\sum_{k\,:\,n_k \ge j} \frac{1}{n_k^2} \le \frac{C_\alpha}{j^2}.$$
*Proof.* Since $\lfloor x \rfloor > x - 1 \ge x/2$ whenever $x \ge 2$, let $k_0 = k_0(\alpha)
= \min\{k \ge 0 : \alpha^k \ge 2\}$ (finite since $\alpha>1$); then for $k \ge k_0$, $n_k \ge
\alpha^k/2$.

*Small $k$ (namely $k < k_0$).* There are only $k_0$ such indices, and each $n_k$ is a
fixed positive integer, so $A_\alpha := \sum_{k<k_0} 1/n_k^2$ is a finite constant. Let
$J_0 = \max_{k<k_0} n_k$. For $j \le J_0$: $\sum_{k<k_0,\,n_k\ge j} 1/n_k^2 \le A_\alpha \le
A_\alpha J_0^2/j^2$ (using $j \le J_0 \Rightarrow J_0^2/j^2 \ge 1$). For $j > J_0$: no $k <
k_0$ satisfies $n_k \ge j$, so this part contributes $0$. Either way it is $\le C_1/j^2$
with $C_1 := A_\alpha J_0^2$.

*Large $k$ (namely $k \ge k_0$).* Here $1/n_k^2 \le 4\alpha^{-2k}$. Let $k_1 = k_1(j) =
\min\{k \ge k_0 : n_k \ge j\}$ (exists once $j$ is fixed, since $n_k \to \infty$). Then
$$\sum_{k \ge k_1} \frac{1}{n_k^2} \le \sum_{k\ge k_1} 4\alpha^{-2k} =
\frac{4\alpha^{-2k_1}}{1-\alpha^{-2}} = C_2\, \alpha^{-2k_1}, \qquad C_2 :=
\frac{4}{1-\alpha^{-2}}.$$
By minimality, $n_{k_1} \ge j$, and $n_{k_1} \le \alpha^{k_1}$ always (flooring only
decreases), so $\alpha^{k_1} \ge j$, i.e. $\alpha^{-2k_1} \le 1/j^2$. Hence this part is $\le
C_2/j^2$.

Adding the two parts, the claim holds with $C_\alpha = C_1 + C_2$. $\blacksquare$

---

## 1. Reduction to nonnegative $X_i$

Write $X_i = X_i^+ - X_i^-$ with $X_i^+ = \max(X_i,0) \ge 0$, $X_i^- = \max(-X_i,0) \ge 0$.
By Lemma 1 applied with $g(x)=\max(x,0)$ and $h(x)=\max(-x,0)$, the sequences $(X_i^+)_{i\ge1}$
and $(X_i^-)_{i\ge1}$ are each pairwise independent; since $X_i \overset{d}{=} X_1$ for all
$i$, also $X_i^+ \overset{d}{=} X_1^+$ and $X_i^- \overset{d}{=} X_1^-$ for all $i$, i.e.
each sequence is i.i.d. Since $E|X_1|<\infty$, both $E[X_1^+]<\infty$ and $E[X_1^-]<\infty$.

If the theorem is established for nonnegative pairwise-independent i.i.d. sequences with
finite mean, apply it to $(X_i^+)$ and to $(X_i^-)$: there are events $\Omega_+, \Omega_-$
of probability $1$ on which $\frac1n\sum_{i=1}^n X_i^+ \to E[X_1^+]$ and $\frac1n\sum_{i=1}^n
X_i^- \to E[X_1^-]$ respectively. On $\Omega_+ \cap \Omega_-$, which still has probability
$1$ (intersection of two full-measure events),
$$\frac{S_n}{n} = \frac1n\sum_{i=1}^n X_i^+ - \frac1n\sum_{i=1}^n X_i^- \to E[X_1^+] -
E[X_1^-] = E[X_1].$$
So it suffices to prove the theorem when $X_i \ge 0$ for all $i$. **Assume this from now
on**, and write $\mu = E[X_1] \in [0,\infty)$.

## 2. Truncation

For $k = 1, 2, \dots$ define $Y_k = X_k \mathbf 1\{X_k \le k\}$, and let
$$T_n = \sum_{k=1}^n Y_k, \qquad S_n = \sum_{k=1}^n X_k.$$
Both $T_n, S_n \ge 0$ and $T_n \le S_n$.

**(2a) Variance of the truncated sum.** For $i \ne j$, $Y_i$ is a measurable function of
$X_i$ alone and $Y_j$ of $X_j$ alone, so by Lemma 1, $Y_i, Y_j$ are independent, hence
uncorrelated: $\operatorname{Cov}(Y_i,Y_j) = 0$. Therefore
$$\operatorname{Var}(T_n) = \sum_{k=1}^n \operatorname{Var}(Y_k). \tag{2.1}$$

**(2b) The key series bound.** Since $\operatorname{Var}(Y_k) \le E[Y_k^2]$ always (because
$\operatorname{Var}(Y_k) = E[Y_k^2] - (EY_k)^2 \le E[Y_k^2]$), and since $X_k
\overset{d}{=}X_1$,
$$E[Y_k^2] = E[X_k^2\mathbf1\{X_k\le k\}] = E[X_1^2 \mathbf1\{X_1\le k\}].$$
By Lemma 8 (applied to $X=X_1 \ge 0$, $E X_1 = \mu <\infty$),
$$\sum_{k=1}^\infty \frac{\operatorname{Var}(Y_k)}{k^2} \le \sum_{k=1}^\infty
\frac{E[X_1^2\mathbf1\{X_1\le k\}]}{k^2} \le 2\mu < \infty. \tag{2.2}$$

## 3. Almost-sure convergence of $T_n/n$ along a geometric subsequence

Fix $\alpha > 1$ and let $n_k = \lfloor \alpha^k \rfloor$, $k=0,1,2,\dots$. Fix $\varepsilon >
0$. By Chebyshev's inequality (Lemma 2) applied to $Z = T_{n_k}$, using $(2.1)$,
$$P\big(|T_{n_k} - E T_{n_k}| > \varepsilon n_k\big) \le \frac{\operatorname{Var}(T_{n_k})}
{\varepsilon^2 n_k^2} = \frac1{\varepsilon^2 n_k^2}\sum_{j=1}^{n_k}\operatorname{Var}(Y_j).$$
Summing over $k$ and swapping the order of summation (Lemma 5; all terms $\ge 0$),
$$\sum_{k=0}^\infty P\big(|T_{n_k}-ET_{n_k}|>\varepsilon n_k\big) \le \frac1{\varepsilon^2}
\sum_{k=0}^\infty \frac1{n_k^2}\sum_{j=1}^{n_k}\operatorname{Var}(Y_j) = \frac1{\varepsilon^2}
\sum_{j=1}^\infty \operatorname{Var}(Y_j) \sum_{k\,:\,n_k \ge j} \frac1{n_k^2}.$$
By Lemma 9, the inner sum is $\le C_\alpha/j^2$, so, using $(2.2)$,
$$\sum_{k=0}^\infty P\big(|T_{n_k}-ET_{n_k}|>\varepsilon n_k\big) \le \frac{C_\alpha}
{\varepsilon^2}\sum_{j=1}^\infty \frac{\operatorname{Var}(Y_j)}{j^2} \le \frac{2\mu
C_\alpha}{\varepsilon^2} < \infty.$$
By Borel–Cantelli (Lemma 3), $P\big(|T_{n_k}-ET_{n_k}|>\varepsilon n_k \text{ i.o.}\big)=0$.
This holds for every $\varepsilon>0$; taking $\varepsilon = 1/m$, $m=1,2,\dots$, and a
countable union of the (probability-zero) exceptional events, we get, almost surely,
$$\frac{T_{n_k}-ET_{n_k}}{n_k} \to 0 \quad \text{as } k\to\infty. \tag{3.1}$$

**Deterministic part.** Since $0 \le X_1\mathbf1\{X_1\le k\} \uparrow X_1$ pointwise as
$k\to\infty$, Lemma 4 (MCT) gives $E Y_k = E[X_1\mathbf1\{X_1\le k\}] \to E X_1 = \mu$. By
Cesàro's theorem (Lemma 6),
$$\frac{ET_n}{n} = \frac1n\sum_{k=1}^n EY_k \to \mu, \qquad \text{so in particular }
\frac{ET_{n_k}}{n_k}\to\mu. \tag{3.2}$$
Combining $(3.1)$ and $(3.2)$: almost surely,
$$\frac{T_{n_k}}{n_k} \to \mu \quad \text{as } k \to \infty. \tag{3.3}$$

## 4. Removing the truncation

Since $X_k \overset{d}{=} X_1$, $P(X_k \ne Y_k) = P(X_k > k) = P(X_1>k)$, so by Lemma 7
(applied to $X = X_1$, $EX_1 = \mu <\infty$),
$$\sum_{k=1}^\infty P(X_k \ne Y_k) = \sum_{k=1}^\infty P(X_1>k) \le \mu <\infty.$$
By Borel–Cantelli (Lemma 3), almost surely there is a (random) $K(\omega)$ such that $X_k =
Y_k$ for all $k > K(\omega)$. Hence $S_n - T_n = \sum_{k=1}^n (X_k-Y_k)$ is, for $n >
K(\omega)$, equal to the fixed finite quantity $\sum_{k=1}^{K(\omega)}(X_k-Y_k)$, so
$(S_n-T_n)/n \to 0$ almost surely. Combining with $(3.3)$: almost surely,
$$\frac{S_{n_k}}{n_k} \to \mu \quad \text{as } k \to \infty. \tag{4.1}$$

## 5. From the subsequence to the full sequence

Since $X_i \ge 0$, $n \mapsto S_n$ is nondecreasing. For $n_k \le n \le n_{k+1}$,
$$S_{n_k} \le S_n \le S_{n_{k+1}} \quad\Longrightarrow\quad \frac{S_{n_k}}{n_{k+1}} \le
\frac{S_n}{n} \le \frac{S_{n_{k+1}}}{n_k}$$
(using $1/n_{k+1}\le 1/n \le 1/n_k$ on the two sides respectively). Because $n_k =
\lfloor\alpha^k\rfloor$, $n_k/\alpha^k \to 1$ as $k\to\infty$, so $n_k/n_{k+1} \to 1/\alpha$
and $n_{k+1}/n_k \to \alpha$. Hence, using $(4.1)$, almost surely
$$\frac{S_{n_k}}{n_{k+1}} = \frac{S_{n_k}}{n_k}\cdot\frac{n_k}{n_{k+1}} \to \frac{\mu}
{\alpha}, \qquad \frac{S_{n_{k+1}}}{n_k} = \frac{S_{n_{k+1}}}{n_{k+1}}\cdot\frac{n_{k+1}}{n_k}
\to \mu\alpha.$$
Therefore, almost surely,
$$\frac{\mu}{\alpha} \le \liminf_{n\to\infty}\frac{S_n}{n} \le \limsup_{n\to\infty}
\frac{S_n}{n} \le \mu\alpha. \tag{5.1}$$

This was derived for one fixed $\alpha>1$; the exceptional null event depends on $\alpha$.
Now let $\alpha$ range over the countable set $\{1+1/m : m=1,2,3,\dots\}$ and intersect the
countably many resulting probability-$1$ events (still probability $1$). On that
intersection, $(5.1)$ holds simultaneously for every $\alpha = 1+1/m$. Letting $m\to\infty$
(so $\alpha \downarrow 1$) in $(5.1)$:
$$\mu \le \liminf_{n\to\infty}\frac{S_n}{n} \le \limsup_{n\to\infty}\frac{S_n}{n} \le \mu.$$
Hence, almost surely, $S_n/n \to \mu = E[X_1]$.

## 6. Conclusion

This proves the theorem when $X_i \ge 0$. By Step 1, the general case ($E|X_1|<\infty$,
$X_i$ real-valued) follows by writing $X_i = X_i^+ - X_i^-$. $\blacksquare$

---

### Remark on where pairwise independence is used, and where it is not

Pairwise independence is used exactly twice, and both times only to justify that a
covariance vanishes: in $(2.1)$, to get $\operatorname{Var}(T_n) = \sum
\operatorname{Var}(Y_k)$ (via Lemma 1, applied to each pair $Y_i, Y_j$), and in the
tail-event Borel–Cantelli step of Section 4, which needs no independence at all (Lemma 3
requires no independence among the events, only summability of probabilities). No step
invokes a maximal inequality over an interval of $n$'s — that is precisely what the
subsequence-plus-sandwich argument of Sections 3 and 5 replaces, and it is why full
independence is never needed.
