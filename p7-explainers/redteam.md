# Red team — P7 explainer series (Lessons 1–8)

Method: steelman-redteam. For each lesson, the strongest attack a skilled, skeptical
reader could make is built as strongly as possible, then checked against the lesson's
own text. All eight lessons already carry a "model limits" section and, in most cases,
have been through a prior science-editor pass (`lessonN-edit.md`), so most surface
errors (wrong equations, wrong figures, sign errors) are already fixed. The attacks
below are the ones that survive that pass: places where a claim, a demonstrated code
result, or a worked numeric answer could still mislead a reader who does not follow
every cross-reference, even though the lesson's authors were aware of the underlying
issue somewhere in the page.

---

## Lesson 1 — Frequency Is Shared State

**Attack.** The opening problem's headline answer — frequency takes 6.40 s to reach
49.2 Hz and 9.60 s to reach 48.8 Hz after a 1000 MW loss — is framed as *the* answer to
"how many seconds pass," and the lesson spends its RoCoF derivation making that number
feel load-bearing. The "What this model captures, and what it misses" list does say "no
governor, no primary response," but gives no sense of scale for how wrong the 9.60 s
figure is as an estimate of usable response time on a real grid. A reader who takes the
disclosed limitation seriously but has no numbers to weigh it against can still walk
away treating 6.40–9.60 s as an operational planning figure — "I have about six
seconds" — rather than an upper bound that a real interconnection's governors are
already eating into within the first one to two seconds after the trip, before the
9.2 Hz threshold is even close.

**Evidence.** Lines 387–404 of `lesson1.html` ("What this model captures, and what it
misses") name the missing governor response as a bullet point but attach no time
constant or fraction to it, unlike every other quantitative claim in the lesson (which
gives H = 2–8 s, RoCoF = 0.125 Hz/s, etc., to several digits). The opening problem itself
(lines 12–35) states the 6.40/9.60 s pair as "the answer," full stop, before the
limitations are reached 350 lines later.

**Fix.** Add one sentence, next to the opening-problem answer or in the limits list,
giving an order-of-magnitude bound on primary response delay (governors on a
well-tuned interconnection begin moving power within roughly 1–2 s of a frequency
deviation this size) and state explicitly that 6.40/9.60 s is a *ceiling* on available
time, not an estimate of it, for any system with governors in service.

---

## Lesson 2 — One Machine on a Stiff Grid

**Attack.** Section 6 ("Model limits") lists five things the classical model omits
(flux decay, AVR, saliency, stator resistance, the infinite-bus idealisation) and then
asserts: "None of these five omissions changes the shape of the answer this lesson
gives — a spring-and-dashpot second-order system." That claim is too strong for one of
the five. Adding excitation control (AVR) is the textbook example of an omission that
*does* change the shape of the answer: a fast, high-gain AVR is well known to inject
*negative* damping into exactly this electromechanical mode under some loading and
network conditions, turning a decaying oscillation into a growing one — not merely
shifting K_s or K_D by some amount. The lesson's own Exercise 5 gestures at this
without naming it: it says a power system stabiliser "raises the effective damping
torque," which only makes sense as a fix if something in the excitation loop can lower
it below what this lesson computes, including below zero.

**Evidence.** Lines 376–398 ("Model limits"): "None of these five omissions changes the
shape of the answer." Exercise 5's answer target (lines 485–498) describes a PSS
raising K_D without saying why K_D would ever need raising if AVR/excitation dynamics
were shape-preserving.

**Fix.** Narrow the claim: state that four of the five omissions only rescale K_s or
K_D, but excitation control is the exception — a high-gain AVR can drive the
*computed* damping ratio negative in some operating regions, which is precisely the
mechanism power system stabilisers exist to counteract (cited in Exercise 5). This
also gives Exercise 5's PSS remark a stated cause instead of an implied one.

---

## Lesson 3 — When the Integrator Lies

**Attack.** Section 3.4 presents the stability margins of semi-implicit Euler (about
62× forward Euler's step limit) and RK4 (about 90×, at four function evaluations per
step) as an unqualified win for the pricier methods, with the takeaway reading as
"these methods tolerate much bigger steps." The accuracy caveat that would stop a
reader from acting on that headline — that a method can be *stable* far past where it
is *accurate* — is stated for forward Euler in §3.2, but for RK4 it appears only inside
Exercise 3's answer key: at h = 0.2 s and 0.3 s, both comfortably inside RK4's 0.319 s
stability limit, RK4 reports late amplitudes of 0.0000°, which the answer key itself
attributes to "strong RK4 numerical damping (|R| well below e^(σh))," concluding
"'decaying' there means stable, not accurate." A reader who reads §3.4's "90 times"
comparison and stops there — the natural place to stop, since it is presented as the
lesson's conclusion about RK4 — will not see that warning, because it lives three
subsections later, attached to an exercise rather than to the claim it qualifies.

**Evidence.** §3.4 (lines 159–185): "RK4's stability boundary... about 90 times forward
Euler's limit... at four function evaluations per step," no accuracy caveat attached.
Exercise 3 answer target (lines 460–476): "include strong RK4 numerical damping...
'decaying' there means stable, not accurate" — the only place this appears.

**Fix.** Move one sentence of Exercise 3's caveat up into §3.4, next to the "90 times"
and "62 times" figures: stability margin is not accuracy margin, and RK4 itself starts
over-damping this mode well inside its own stability boundary (demonstrated in
Exercise 3).

---

## Lesson 4 — Big Faults: the Equal-Area Criterion

**Attack.** The lesson teaches a first-swing criterion — does δ stay below δ_max on the
way out after the fault clears — and calls a clearing time that satisfies this
criterion "stable." The Model Limits section (§7) discloses that with K_D = 0 the
post-fault machine "keeps oscillating rather than settling" (line 444–445) and that
AVR/governor effects "change the picture" only "on a longer time horizon than the first
swing" (lines 470–473). Nowhere does the lesson name the specific, well-documented
failure mode this gap points at: multi-swing instability, where a system passes the
first-swing (equal-area) test but loses synchronism on a later swing because of
governor reallocation or AVR-driven negative damping (the same mechanism flagged as
missing in Lesson 2). A reader who takes "the equal-area criterion says this clearing
time is stable" as the operational answer, rather than as "stable on the first swing
only," is repeating the single most common real-world misuse of this method.

**Evidence.** §7 (lines 455–530): the five listed limits cover damping, machine model,
network reduction, and fault severity, but never name multi-swing instability as a
named failure mode distinct from "does not extend to K_D ≠ 0."

**Fix.** Add one bullet to §7 naming multi-swing instability explicitly: passing the
equal-area (first-swing) test is necessary but not sufficient for transient stability;
a real assessment must also check later swings, where governor and AVR dynamics this
lesson excludes (and Lesson 2 flags for the same reason) can still cause loss of
synchronism.

---

## Lesson 5 — Rotating frames: the Park transform and the PLL

**Attack.** Exercise 3 shows that a 10% negative-sequence component produces a 100 Hz
ripple directly on v_q (measured 0.10044 pu, matching the 10% injection). Exercise 4,
three exercises later, retunes the same PLL for a 20 Hz bandwidth and reports the
result entirely as a win: "settling time about halves... as expected." Because the
lesson's own glossary states that an "f Hz bandwidth" design (ω_n = 2πf) yields a
closed-loop −3 dB bandwidth well above f (20.6 Hz measured for a 10 Hz design, §2.1
footnote), a 20 Hz design pushes the actual −3 dB bandwidth toward roughly 40 Hz — only
about 2.4× below the 100 Hz negative-sequence ripple frequency Exercise 3 introduces.
The two exercises are never cross-referenced: Exercise 4 frames "faster tracking" as an
unqualified improvement, without noting that the same retuning narrows the separation
from the unbalance ripple that Exercise 3 spent its own paragraph establishing.

**Evidence.** Exercise 3 target (lines 428–438): "A 100 Hz ripple... v_q ripple
amplitude = 0.10044 pu." Exercise 4 target (lines 440–460): "doubling the bandwidth
halves the settling time, as expected," with no mention of negative-sequence rejection.
Glossary entry on "bandwidth" (lines 305–311): 10 Hz design → 20.6 Hz −3 dB bandwidth.

**Fix.** Add a line to Exercise 4's answer noting the trade-off it does not mention:
raising PLL bandwidth to speed up tracking narrows the separation from any
negative-sequence ripple at twice grid frequency (Exercise 3), which is why real PLL
tuning is a compromise between tracking speed and unbalance rejection, not a
free choice of "faster is better."

---

## Lesson 6 — Following on a Weak Grid

**Attack.** The lesson's headline result is a static stability bound: the PLL loses
lock as θ_0 → 90° (K_pll → 0), and Section 5's root locus is offered as confirmation,
staying in the left half-plane "all the way to K_pll = 0.1." Section 6 then states,
almost as an aside, that "the observed instability before the static bound is
reached is a cited result, not one derived in this lesson" and that the mechanism (PLL
and current-loop interaction) is "left for a later lesson to derive" [S08 — verify].
This means the lesson's own linear model — the one used to answer the opening problem's
"can the plant export its full rating" question — is conceded, in its own text, to be
optimistic relative to documented real-world behaviour: real weak-grid PLL
instabilities are commonly observed at SCRs above (i.e., grids stronger than) where
this lesson's static bound would predict trouble. A reader who uses only this lesson's
SCR/θ_0 criterion for a real siting decision is using a bound the lesson itself says is
not tight.

**Evidence.** §6 (lines ~490–496): "The observed instability before the static bound is
reached is a cited result, not one derived in this lesson... left for a later lesson to
derive." §5's root locus stays stable "all the way to K_pll = 0.1" (i.e., very close to
the θ_0 → 90° edge), which is the evidence the lesson uses to support its own bound
even while flagging that bound as not matching observed practice.

**Fix.** State directly, next to the opening-problem answer, that the SCR/θ_0 bound
computed here is a necessary condition, not a sufficient one: real converters have been
observed to lose lock at higher SCR than this static bound predicts, because of
current-loop/PLL interaction this single-loop model excludes — so a design should
treat this lesson's number as an optimistic floor, not a target.

---

## Lesson 7 — Forming Instead of Following: Droop Is a Swing Equation

**Attack.** The lesson's central payload is the equivalence H_eq = 1/(2 m_p ω_c),
K_D,eq = 1/m_p — droop control behaves exactly like a synchronous machine with this
inertia and damping. The model-limits section discloses, correctly, that "every result
above assumes the converter can source or sink whatever current the voltage-behind-
reactance model demands," and that once the converter saturates at I_max, "it has
silently become a current source... and the entire grid-forming analysis of this
lesson stops applying at that moment." The problem is where this equivalence is most
useful: it is invoked to argue that grid-forming converters can substitute for
synchronous inertia during large events — exactly the kind of event (a large,
sudden ΔP, the same shape as Lesson 1's 1000 MW trip) most likely to push a
current-limited converter into saturation almost immediately. The lesson never
connects its own caveat back to its own headline claim: the H_eq equivalence is least
trustworthy precisely during the large disturbances it is most often cited to help
with.

**Evidence.** "What this model captures, and what it misses" (lines ~505–512):
"Current limit I_max ignored... the entire grid-forming analysis of this lesson stops
applying at that moment." The H_eq/K_D,eq derivation itself (Exercise 1 target, lines
~537–543) states the match is "exact under the assumption that makes it exact,"
without a corresponding warning at the point the equivalence is first presented.

**Fix.** Add one sentence where H_eq and K_D,eq are first presented (not only in the
limits section at the end): this inertia-like behaviour holds only below I_max, and
because I_max is reached fastest during the large events this equivalence is usually
invoked for, a claimed H_eq contribution should be checked against the converter's
current headroom for the specific disturbance size being analysed, not assumed.

---

## Lesson 8 — From One Machine to a System

**Attack.** The sizing example (Fig. 8.3, §"Energy... Power... Current") concludes that
a 1120 MVA grid-forming fleet meets the power and current constraints "exactly... no
margin" — its added current (0.20 pu) "lands exactly on I_max = 1.2 pu stacked on
1.0 pu dispatch... with nothing left over." The model-limits section separately states
that "converter stability while saturated at I_max is not proved here, and is an open
problem (National Grid ESO GC0137; IEEE Std 2800-2022 — verify)," and that "sizing a
fleet to sit exactly at I_max says nothing about whether it stays stable once actually
saturated there." These two passages describe the same fleet: the worked sizing answer
that the lesson presents as the solution to its sizing problem is, by the lesson's own
later admission, sized to sit exactly at the boundary condition whose stability is an
unresolved open question. The sizing section does not carry that warning forward or
recommend a margin; a reader who stops at the sizing answer gets a specific number
(1120 MVA) with an implied "problem solved" that the limits section quietly retracts.

**Evidence.** Sizing section (Fig. 8.3 caption and surrounding text): "lands exactly on
I_max = 1.2 pu... with nothing left over." Model limits section: "sizing a fleet to sit
exactly at I_max says nothing about whether it stays stable once actually saturated
there" — same 1120 MVA fleet, same I_max = 1.2 pu, no cross-reference between the two.

**Fix.** Add a line at the sizing conclusion itself (not only in the limits section)
recommending a current margin below I_max, and note explicitly that the "exactly at
I_max, no margin" result this exercise produces is the specific case the model-limits
section later flags as stability-unproven — so the sizing answer should be read as a
lower bound on fleet size, not a design target.

---

## Series-level issues

**S1 — The current-limit gap is the load-bearing risk of the whole grid-forming half
of the series, and it is never closed.** Lesson 7 states that its entire
inertia-equivalence result stops applying once a converter saturates at I_max. Lesson 8
independently states that converter stability while saturated at I_max is an open
problem, then produces a worked sizing answer that sits exactly at that boundary with
no margin. No lesson in the series checks whether the numbers Lesson 8 computes
(1120 MVA, 0.20 pu added current) would keep the fleet inside I_max during the actual
disturbance dynamics (not just the steady final state) that a 1000 MW-class loss (the
series' own recurring example, from Lesson 1) would produce. The two disclosures
reinforce each other but are never cross-referenced, so a reader who reads only Lesson
8 does not learn that Lesson 7 already named this as the point where "the entire
grid-forming analysis... stops applying."

**S2 — Grid-forming control is never analysed on a weak grid.** Lesson 6 builds the
weak-grid/SCR framework (current bound, vanishing PLL gain) exclusively for a
grid-following converter. Lesson 7 builds the droop-as-swing-equation equivalence for
a grid-forming converter, but explicitly reuses Lesson 2's infinite-bus (stiff-grid)
setup ("Lesson 2 showed that a synchronous machine against an infinite bus..."). The
series therefore never models the case most often cited in industry as the motivation
for grid-forming control in the first place — a grid-forming converter on a weak grid
(low SCR) — despite having built exactly the two pieces (Lesson 6's SCR machinery,
Lesson 7's droop-as-swing-equation machinery) that a combined treatment would need.

**S3 — AVR/excitation-driven negative damping is flagged twice, named nowhere.**
Lesson 2's model-limits section claims that omitting AVR/excitation control "does not
change the shape" of the classical model's answer, then Exercise 5 describes a power
system stabiliser as needed to raise damping torque — implying something can lower it.
Lesson 4's model-limits section separately notes that AVR/governor effects "change the
picture" on a longer time horizon than the first swing, without saying how. Both
lessons gesture at the same real mechanism (excitation-control-induced negative
damping, the reason power system stabilisers exist and the reason equal-area's
first-swing pass can be followed by a later-swing failure) without ever naming it as
one mechanism or cross-referencing each other. A reader who reads both lessons still
has no single place that tells them these two disclosed gaps are the same phenomenon.
