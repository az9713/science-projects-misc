# Theorem (Sylow theorems)

**Statement.** Let $G$ be a finite group, let $p$ be a prime, and write $|G| = p^a m$ with
$a \ge 0$ and $p \nmid m$. A *Sylow $p$-subgroup* of $G$ is a subgroup of order $p^a$. Then:

- **(i)** $G$ has at least one Sylow $p$-subgroup;
- **(ii)** every $p$-subgroup of $G$ (a subgroup whose order is a power of $p$) is contained
  in some Sylow $p$-subgroup, and any two Sylow $p$-subgroups of $G$ are conjugate in $G$;
- **(iii)** the number $n_p$ of Sylow $p$-subgroups of $G$ satisfies $n_p \equiv 1 \pmod p$
  and $n_p \mid m$.

Throughout, "subgroup" means subgroup of the finite group $G$, and all group actions are on
finite sets.

---

## 0. Lemmas used, with standard citations

**Lemma 0 (Lagrange's theorem).** If $H$ is a subgroup of a finite group $G$, then $|H|$
divides $|G|$, and $|G| = [G:H]\,|H|$, where $[G:H]$ is the number of left cosets of $H$ in
$G$. *Citation:* Dummit & Foote, *Abstract Algebra*, 3rd ed., §3.2, Theorem 8; Herstein,
*Topics in Algebra*, 2nd ed., §2.4.

**Lemma 0′ (multiplicativity of index).** If $K \le H \le G$ are finite groups, then
$[G:K] = [G:H]\,[H:K]$. *Proof.* By Lemma 0, $|G| = [G:K]\,|K|$, $|G| = [G:H]\,|H|$, and
$|H| = [H:K]\,|K|$. Substituting the third equation into the second gives
$|G| = [G:H]\,[H:K]\,|K|$. Comparing with $|G| = [G:K]\,|K|$ and cancelling $|K|>0$ gives
$[G:K] = [G:H]\,[H:K]$. $\blacksquare$ *Citation:* Dummit & Foote, §3.2 (Corollary 9 and
surrounding discussion); Lang, *Algebra*, 3rd ed., §I.2.

**Lemma 1 (orbit–stabilizer theorem).** If a finite group $H$ acts on a finite set $X$, then
for any $x \in X$ the map $hH_x \mapsto h\cdot x$ is a well-defined bijection from the set of
left cosets of the stabilizer $H_x = \{h \in H : h\cdot x = x\}$ onto the orbit
$H\cdot x = \{h\cdot x : h \in H\}$. Consequently $|H\cdot x| = [H:H_x]$, and (by Lemma 0)
$|H\cdot x|$ divides $|H|$. *Citation:* Dummit & Foote, §4.1, Proposition 2; Lang, *Algebra*,
§I.5.

**Lemma 2 (fixed-point congruence for $p$-group actions).** Let $H$ be a group of order
$p^k$ (a "$p$-group") acting on a finite set $X$, and let $X^H = \{x \in X : h\cdot x = x \text{ for all } h \in H\}$
be the set of fixed points. Then $|X| \equiv |X^H| \pmod p$.
*Proof.* $X$ is the disjoint union of its $H$-orbits. By Lemma 1, each orbit has size
$[H:H_x]$, which divides $|H| = p^k$ by Lemma 0, so every orbit size is a power of $p$: either
$1$ (exactly when the orbit is $\{x\}$, i.e. $x \in X^H$) or a positive multiple of $p$.
Summing orbit sizes, $|X| = |X^H| + \sum(\text{orbit sizes} \ge p)$, and each term in the sum
is divisible by $p$. Hence $|X| \equiv |X^H| \pmod p$. $\blacksquare$ *Citation:* this
argument is the standard "class equation" style counting argument for $p$-groups; see
Dummit & Foote, §4.3 (the class equation, Theorem 8) and §4.5; Lang, *Algebra*, §I.6.

**Lemma 3 ($p$-adic valuation of $\binom{p^a m}{p^a}$).** If $p \nmid m$, then
$p \nmid \binom{p^a m}{p^a}$.
*Proof.* Write
$$\binom{p^a m}{p^a} = \prod_{i=0}^{p^a-1} \frac{p^a m - i}{p^a - i}.$$
For $i=0$ the factor is $\dfrac{p^a m}{p^a} = m$, and $p \nmid m$ by hypothesis, so this
factor contributes no factor of $p$ to either numerator or denominator.
For $1 \le i \le p^a-1$, write $i = p^k u$ with $p \nmid u$ and, since $i < p^a$, necessarily
$0 \le k \le a-1$ (so $a-k \ge 1$). Then
$$p^a - i = p^k\big(p^{a-k} - u\big), \qquad p^a m - i = p^k\big(p^{a-k} m - u\big).$$
Since $a-k \ge 1$, both $p^{a-k}-u \equiv -u \pmod p$ and $p^{a-k}m - u \equiv -u \pmod p$;
as $p \nmid u$, neither is divisible by $p$. Hence the exponent of $p$ dividing $p^a-i$ is
exactly $k$, and the exponent of $p$ dividing $p^a m - i$ is also exactly $k$. So the factor
$\dfrac{p^a m - i}{p^a - i}$ contributes net $p$-adic valuation $0$.
Every factor in the product (including $i=0$) has $p$-adic valuation $0$, so the whole
product $\binom{p^a m}{p^a}$ has $p$-adic valuation $0$, i.e. $p \nmid \binom{p^a m}{p^a}$.
$\blacksquare$ *Citation:* this is the standard counting lemma used in Wielandt's 1959 proof
of Sylow's existence theorem; see H. Wielandt, "Ein Beweis für die Existenz der
Sylowgruppen," *Arch. Math.* 10 (1959), 401–402, and its exposition in Lang, *Algebra*, 3rd
ed., §I.6 (Sylow's theorems), or Dummit & Foote, §4.5, exercises on Wielandt's proof.

**Lemma 4 (basic conjugation facts).** For $g \in G$ and $H \le G$: (a) the map
$c_g : G \to G$, $c_g(x) = gxg^{-1}$, is an automorphism of $G$, so its restriction to $H$ is
a bijection $H \to gHg^{-1}$; in particular $|gHg^{-1}| = |H|$. (b) The *normalizer*
$N_G(H) = \{g \in G : gHg^{-1} = H\}$ is a subgroup of $G$ containing $H$, and $H$ is a
normal subgroup of $N_G(H)$ (by definition of $N_G(H)$, every element of $N_G(H)$ conjugates
$H$ onto itself). *Citation:* Dummit & Foote, §2.2 (conjugation), §3.1 and §4.3
(normalizers).

---

## 1. Proof of (i): existence of a Sylow $p$-subgroup (Wielandt's counting argument)

Let $n = |G| = p^a m$. Let
$$\Omega = \{\, S \subseteq G : |S| = p^a \,\}$$
be the set of all $p^a$-element subsets of $G$, so $|\Omega| = \binom{n}{p^a} = \binom{p^a m}{p^a}$.

**Step 1 (an action of $G$ on $\Omega$).** Let $G$ act on $\Omega$ by left translation:
$g \cdot S = gS = \{gs : s \in S\}$. Since $x \mapsto gx$ is a bijection $G \to G$,
$|gS| = |S| = p^a$, so $gS \in \Omega$; and $e\cdot S = S$, $g\cdot(h\cdot S) = (gh)\cdot S$, so
this is a genuine group action.

**Step 2 (some orbit has size prime to $p$).** By Lemma 3, $p \nmid |\Omega|$. $\Omega$ is
the disjoint union of its $G$-orbits, so $|\Omega|$ is the sum of the orbit sizes. If every
orbit size were divisible by $p$, the sum $|\Omega|$ would be divisible by $p$, a
contradiction. Hence some orbit $O = G\cdot S_0$ has $|O|$ not divisible by $p$.

**Step 3 (the stabilizer of $S_0$ has order $\le p^a$).** Let
$H = \mathrm{Stab}_G(S_0) = \{g \in G : gS_0 = S_0\}$, a subgroup of $G$. Fix $s_0 \in S_0$
and define $\varphi : H \to S_0$ by $\varphi(h) = h s_0$ (this lands in $S_0$ because
$hS_0 = S_0$ for $h \in H$). If $\varphi(h_1) = \varphi(h_2)$ then $h_1 s_0 = h_2 s_0$, and
left cancellation in $G$ gives $h_1 = h_2$; so $\varphi$ is injective, hence
$|H| \le |S_0| = p^a$.

**Step 4 (the stabilizer has order exactly $p^a$).** By Lemma 1, $|O| = [G:H] = n/|H|$. Since
$p \nmid |O|$, every factor of $p$ in $n = p^a m$ must divide $|H|$; formally, if
$p^{v}$ is the exact power of $p$ dividing $|H|$, then the exact power of $p$ dividing
$n/|H|$ is $p^{a-v}$ (using $p \nmid m$), and this must equal $1$ (i.e. $a-v=0$) since
$p \nmid |O|$. So $v = a$, i.e. $p^a$ divides $|H|$. Combined with Step 3's bound
$|H| \le p^a$, this forces $|H| = p^a$ exactly.

Thus $H$ is a subgroup of $G$ of order $p^a$: a Sylow $p$-subgroup. This proves (i).
$\blacksquare$

---

## 2. Proof of (ii): every $p$-subgroup lies in a Sylow $p$-subgroup, and all Sylow $p$-subgroups are conjugate

Fix, from part (i), one Sylow $p$-subgroup $P \le G$ with $|P| = p^a$, and let $[G:P] = m$
(by Lemma 0, since $|G| = p^a m$).

**Key Lemma (fusion via coset action).** Let $H \le G$ be any $p$-subgroup (so $|H| = p^k$
for some $k \ge 0$; by Lemma 0, $p^k \mid p^a m$ and $p \nmid m$ force $k \le a$). Let $H$ act
on the set of left cosets $G/P = \{gP : g \in G\}$ by $h \cdot (gP) = (hg)P$; this is a valid
group action ($h_1\cdot(h_2\cdot gP) = h_1 h_2 g P = (h_1h_2)\cdot gP$). Then $H$ is contained
in some conjugate of $P$.

*Proof of Key Lemma.* $|G/P| = [G:P] = m$, and $p \nmid m$ by hypothesis. By Lemma 2 applied
to the $p$-group $H$ acting on $X = G/P$,
$$m = |G/P| \equiv |(G/P)^H| \pmod p.$$
Since $p \nmid m$, this forces $|(G/P)^H| \not\equiv 0 \pmod p$; in particular
$(G/P)^H \ne \varnothing$. So there is a coset $gP$ fixed by every $h \in H$: $h(gP) = gP$
for all $h \in H$, i.e. $g^{-1}hg \in P$ for all $h \in H$, i.e.
$$H \subseteq gPg^{-1}.$$
By Lemma 4(a), $gPg^{-1}$ is a subgroup with $|gPg^{-1}| = |P| = p^a$, i.e. a Sylow
$p$-subgroup. This proves the Key Lemma. $\blacksquare$

**Every $p$-subgroup lies in a Sylow $p$-subgroup.** This is exactly the conclusion of the
Key Lemma applied to an arbitrary $p$-subgroup $H$: $H \subseteq gPg^{-1}$, and $gPg^{-1}$ is
a Sylow $p$-subgroup. This proves the first half of (ii).

**Any two Sylow $p$-subgroups are conjugate.** Let $Q$ be any Sylow $p$-subgroup, so
$|Q| = p^a$; in particular $Q$ is a $p$-subgroup, so the Key Lemma (applied with $H = Q$)
gives some $g \in G$ with $Q \subseteq gPg^{-1}$. Since $|Q| = p^a = |gPg^{-1}|$ (Lemma 4(a))
and $Q \subseteq gPg^{-1}$ with both sets finite of the same size, $Q = gPg^{-1}$. Hence every
Sylow $p$-subgroup $Q$ equals $gPg^{-1}$ for some $g \in G$, i.e. every Sylow $p$-subgroup is
conjugate to $P$. Since conjugacy ("$Q$ is conjugate to $P$" iff $Q = gPg^{-1}$ for some $g$)
is an equivalence relation on subgroups of $G$, any two Sylow $p$-subgroups $Q_1 = g_1Pg_1^{-1}$
and $Q_2 = g_2Pg_2^{-1}$ satisfy $Q_2 = (g_2g_1^{-1})Q_1(g_2g_1^{-1})^{-1}$, so $Q_1$ and $Q_2$
are conjugate to each other. This proves the second half of (ii). $\blacksquare$

In particular, the set $\mathrm{Syl}_p(G)$ of all Sylow $p$-subgroups of $G$ is exactly the
conjugacy class of $P$: $\mathrm{Syl}_p(G) = \{gPg^{-1} : g \in G\}$.

---

## 3. Proof of (iii): $n_p \equiv 1 \pmod p$ and $n_p \mid m$

Let $n_p = |\mathrm{Syl}_p(G)|$, and keep $P$ as fixed above.

**$n_p \mid m$.** Let $G$ act on $\mathrm{Syl}_p(G)$ by conjugation: $g \cdot Q = gQg^{-1}$
(this lands in $\mathrm{Syl}_p(G)$ by Lemma 4(a), and $e\cdot Q = Q$,
$g_1\cdot(g_2\cdot Q) = (g_1g_2)\cdot Q$). By Section 2, $\mathrm{Syl}_p(G)$ is exactly the
orbit of $P$ under this action (every Sylow $p$-subgroup is $gPg^{-1}$ for some $g$, and
every $gPg^{-1}$ is a Sylow $p$-subgroup). By Lemma 1,
$$n_p = |\text{orbit of } P| = [G : \mathrm{Stab}_G(P)],$$
where $\mathrm{Stab}_G(P) = \{g \in G : gPg^{-1} = P\} = N_G(P)$, the normalizer of $P$
(Lemma 4(b)). Since $P \le N_G(P) \le G$, Lemma 0′ gives
$$[G:P] = [G:N_G(P)]\,[N_G(P):P], \quad\text{i.e.}\quad m = n_p \cdot [N_G(P):P].$$
Hence $n_p$ divides $m$.

**$n_p \equiv 1 \pmod p$.** Let $P$ (a $p$-group of order $p^a$) act on $X = \mathrm{Syl}_p(G)$
by conjugation, i.e. restrict the action above to $H = P$: $x \cdot Q = xQx^{-1}$ for
$x \in P$. By Lemma 2,
$$n_p = |X| \equiv |X^P| \pmod p,$$
where $X^P = \{Q \in \mathrm{Syl}_p(G) : xQx^{-1} = Q \text{ for all } x \in P\}$, i.e. the set
of Sylow $p$-subgroups $Q$ with $P \subseteq N_G(Q)$.

*Claim: $X^P = \{P\}$.* Certainly $P \in X^P$, since $xPx^{-1} = P$ for all $x \in P \le G$
(any subgroup normalizes itself). Conversely, suppose $Q \in X^P$, i.e. $P \subseteq N_G(Q)$.
Consider the finite group $N = N_G(Q)$. By Lemma 4(b), $Q \trianglelefteq N$ (Q is normal in
its own normalizer). Also $Q \le N$ and $P \le N$ by assumption, and $|P| = |Q| = p^a$, so
both $P$ and $Q$ are Sylow $p$-subgroups of the group $N$ (in the sense of the definition
applied to $N$ in place of $G$: writing $|N| = p^a m'$ with $p \nmid m'$, which holds because
$p^a$ divides $|N|$, as $Q\le N$, while $[G:N] $ divides $[G:P]=m$ by Lemma 0′ applied to
$P\le N\le G$, so $p\nmid [G:N]$, hence $p \nmid |N|/p^a\cdot(\text{consistency with } |G|=p^am)$
more directly: $|N|$ divides $|G|=p^am$ by Lemma 0, and $p^a\mid |N|$ since $Q\le N$, so
$|N|=p^a m'$ with $m' \mid m$ and in particular $p\nmid m'$).
By part (ii) applied inside $N$, $P$ and $Q$ (both Sylow $p$-subgroups of $N$) are conjugate
*in $N$*: there is $x \in N$ with $P = xQx^{-1}$. But $Q \trianglelefteq N$ means
$xQx^{-1} = Q$ for every $x \in N$. Hence $P = xQx^{-1} = Q$.

This proves the claim, so $|X^P| = 1$, and therefore
$$n_p \equiv |X^P| = 1 \pmod p.$$
$\blacksquare$

This completes the proof of (iii), and with it the proof of the Sylow theorems in full.
$\blacksquare$

---

## Summary of the logical structure

1. Lemma 3 (the $p$-adic valuation of $\binom{p^am}{p^a}$ is $0$) drives Wielandt's counting
   argument (Section 1): $G$ acting by left translation on $p^a$-subsets of $G$ must have an
   orbit of size prime to $p$ (else $|\Omega|=\binom{p^am}{p^a}$ would be divisible by $p$),
   and the stabilizer of a representative of that orbit is forced, by Lemma 1 (orbit–stabilizer)
   and an injectivity argument, to have order exactly $p^a$ — proving (i).
2. Lemma 2 (a $p$-group action's fixed points are congruent mod $p$ to the whole set) is the
   single engine behind Section 2 and Section 3. Applied to a $p$-subgroup $H$ acting on the
   coset space $G/P$ (Section 2's Key Lemma), it forces a fixed coset, which translates into
   $H$ lying inside a conjugate of $P$ — giving both halves of (ii) (containment, by applying
   it to any $p$-subgroup; conjugacy of Sylow subgroups, by applying it to another Sylow
   subgroup $Q$ and comparing orders).
3. Applying Lemma 2 again, now to $P$ acting on $\mathrm{Syl}_p(G)$ by conjugation
   (Section 3), the fixed points are shown (via Lemma 4(b) and the conjugacy result of
   Section 2, applied inside $N_G(Q)$) to be exactly $\{P\}$, giving $n_p \equiv 1 \pmod p$.
   Orbit–stabilizer (Lemma 1) identifies $n_p$ with $[G:N_G(P)]$, and the index tower law
   (Lemma 0′) through $P \le N_G(P) \le G$ gives $n_p \mid [G:P] = m$.
