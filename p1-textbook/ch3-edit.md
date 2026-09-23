# Chapter 3 edit — `ch3.html`

**Verdict: ACCEPT WITH CHANGES.** A graduate reader can learn this chapter after nine blocking fixes; the largest is a dVOC reduction that drops a coupling term with no stated assumption.

No derivation fails. No number is invented. One HTML tag is malformed. One cross-reference and one percentage are wrong. Two physical assertions, in §3.1 and Example 3.1, have no argument and point the wrong way. Four symbols are used before the prose defines them. One citation is attributed to a source that cannot carry it.

Editor method: `science-editor` skill, five-part standard. Brief assembled from `book-plan.md` (§2 result graph, §3 notation table, §4 Chapter 3 spec, §5 rules), `HANDOFF.md`, and the chapter 3 entry of `draft-results.json`. Check scripts in the session scratchpad: `edit_ch3_check.py` (127 numbers recomputed, `html.parser` pass, prose scans) and `edit_ch3_lines.py` (line lookup). No project file was edited. The draft agent's claims were tested, not accepted; two of them are confirmed in Part E (items 49 and 50).

Notes for the fix stage:

1. Line numbers refer to `ch3.html` as on disk (13:38 PDT, 1827 lines). Apply items from the bottom of the file upward, so that the line numbers above each edit stay valid.
2. Each replacement is complete HTML for the quoted span. Paste it in place of the quoted text. Keep `<var>`, `<sub>`, `<sup>` markup; add no MathML and no heading below `<h3>`.
3. "Part N" names the part of the five-part standard that is missing: 1 precise statement, 2 every term defined, 3 proof in the smallest setting, 4 rescue or limit case, 5 tie to something concrete.
4. Items are numbered 1 to 60 across all five parts. Report by item number.

---

## A. Blocking defects

### 1. `ch3.html:923` — malformed tag `<sub>D</var>`. HTML rule (f).

Quote (lines 922–924):

```html
<p>Substituting (3.17), dividing by <var>S</var><sub>base</sub>, and matching
against the <var>K</var><sub>D</var><var>&delta;&omega;</var> term of (3.3)
gives</p>
```

Defect: `<sub>` is closed by `</var>`. `html.parser` reports two errors at this point (mismatched `</var>` at 923:30, mismatched `</p>` at 924:5). This is the only parse error in the file. Rule (f) requires a clean parse.

Replacement (lines 922–924):

```html
<p>Substitute (3.17), divide by <var>S</var><sub>base</sub>, and match the
result against the <var>K</var><sub>D</sub> <var>&delta;&omega;</var> term of
(3.3). This gives</p>
```

### 2. `ch3.html:1148–1157` — the dVOC reduction drops a coupling term and states no assumption. Part 4 missing; part 3 incomplete.

Quote (lines 1148–1157):

```html
<p>At the operating point the amplitude regulator has done its work, so
<var>E</var> = <var>V</var><sub>ref</sub> and (3.24) reads
d<var>&theta;</var>/d<var>t</var> = <var>&omega;</var><sub>0</sub> +
(<var>&eta;</var>/<var>V</var><sub>ref</sub><sup>2</sup>)
(<var>P</var><sub>ref</sub> &minus; <var>P</var>). That is a droop line, written
in rad/s. Convert it to per unit by dividing by
<var>&omega;</var><sub>0</sub>, which is what (3.2) requires:</p>
<p class="eq">&Delta;<var>&omega;</var> = &minus; [<var>&eta;</var> /
(<var>&omega;</var><sub>0</sub> <var>V</var><sub>ref</sub><sup>2</sup>)]
&Delta;<var>P</var><span class="n">(3.25)</span></p>
```

Defect: at κ = π/2, equation (3.24) is dθ/dt = ω<sub>0</sub> + η(P<sub>ref</sub>/V<sub>ref</sub>² − P/E²). Its derivative with respect to E at the operating point is 2ηP<sub>ref</sub>/V<sub>ref</sub>³. That term is zero only when P<sub>ref</sub> = 0. The passage sets E = V<sub>ref</sub> before it takes deviations, so it sets ΔE = 0 without saying so. The chapter labels (3.24) to (3.27) "proved here" and Theorem 3.7 and Table 3.1 rest on them. Write the assumption down. Items 27, 28 and 29 carry it into the two places that inherit it.

Replacement (lines 1148–1157):

```html
<p>At the operating point the amplitude regulator has done its work, so
<var>E</var> = <var>V</var><sub>ref</sub>. Take deviations of (3.24) about that
point. Two terms appear, because <var>E</var> stands in the denominator of the
power error:</p>
<p class="eq">&Delta;(d<var>&theta;</var>/d<var>t</var>) = &minus;
(<var>&eta;</var>/<var>V</var><sub>ref</sub><sup>2</sup>) &Delta;<var>P</var>
+ (2<var>&eta;</var><var>P</var><sub>ref</sub>/<var>V</var><sub>ref</sub><sup>3</sup>)
&Delta;<var>E</var></p>
<p><strong>Assumption for the reduction.</strong> Hold the magnitude at its set
point: &Delta;<var>E</var> = 0. This selects the power-to-frequency channel
alone, and it is the same decoupling that assumption (iv) of Model 3.2 makes
for droop control. It holds when the amplitude regulator in (3.23) is fast
compared with the angle dynamics, or when the reactive-power error is zero.
With &Delta;<var>E</var> = 0 the second term vanishes, and what remains is a
droop line written in rad/s. Convert it to per unit by dividing by
<var>&omega;</var><sub>0</sub>, which is what (3.2) requires:</p>
<p class="eq">&Delta;<var>&omega;</var> = &minus; [<var>&eta;</var> /
(<var>&omega;</var><sub>0</sub> <var>V</var><sub>ref</sub><sup>2</sup>)]
&Delta;<var>P</var><span class="n">(3.25)</span></p>
```

### 3. `ch3.html:932` — "(3.22) gives" points at the dVOC angle equation. Part 1.

Quote (lines 930–933):

```html
term is not a correction to be dropped. Set <var>k</var><sub>dc</sub> = 0, that is
a stiff current source, and (3.22) gives
<var>K</var><sub>D,eq</sub> = &minus;<var>P</var><sub>0</sub>: a source that holds
```

Defect: the damping result is (3.21). Equation (3.22) is the dVOC angle law of Model 3.6. The draft's own notes call the matching damping "(3.22)", so the equation numbers shifted after the note was written and this reference was not updated. A reader who follows the reference lands in the wrong family.

Replacement (line 932):

```html
a stiff current source, and (3.21) gives
```

### 4. `ch3.html:670–671` — "11 %" is the inverse of the printed ratio. Part 5, wrong number.

Quote (lines 669–671):

```html
tracks power quickly, gives almost no inertia: 0.3183 s at 5 Hz, which is 11 % of
a 3.5 s machine.
```

Recomputed: 0.3183 / 3.5 = 0.0909, that is 9.1 %. The text printed 3.5 / 0.3183 = 11.0 and called it a percentage.

Replacement (lines 670–671):

```html
tracks power quickly, gives almost no inertia: 0.3183 s at 5 Hz, which is 9.1 %
of a 3.5 s machine (0.3183 / 3.5 = 0.0909; the machine's constant is 11.0 times
the converter's).
```

### 5. `ch3.html:660–665` — "slow enough to interact with the current loop of R14" is asserted, not argued, and the direction is reversed. Parts 3 and 5 missing.

Quote (lines 660–665):

```html
<p><strong>The design consequence, in one sentence.</strong> To match the
<var>H</var> = 3.5 s of the machine in Example 1.1, invert (3.7):
<var>&omega;</var><sub>c</sub> = 1 / (2 &times; 0.05 &times; 3.5) = 1/0.35 =
2.8571 rad/s, that is 0.4547 Hz, a power measurement filter with a time constant
of 0.3500 s &mdash; slow enough to interact with the current loop of R14 and with
protection timing.</p>
```

Defect: Chapter 2 sets α<sub>c</sub> = 2π(500) = 3141.59 rad/s in its worked tuning (`ch2.html:269`). The filter pole at 2.8571 rad/s lies three decades below it. A slower filter widens the timescale separation that assumption (iii) of Model 3.2 needs; it does not "interact" with the current loop. The filter pole does lie within one decade of the swing mode that Theorem 3.3 creates: with K<sub>s</sub> = 1.491 pu/rad from Example 1.1 (R08) and H<sub>eq</sub> = 3.5 s, R07 gives ω<sub>n</sub> = √(1.491 × 376.99 / 7) = 8.96 rad/s. It also sits on the protection timescale: 4 to 6 cycles is 0.067 s to 0.100 s at 60 Hz (Example 1.2, `ch1.html:880`), and a 0.35 s filter has registered only 17 % to 25 % of a step in power by then (1 − e<sup>−t/0.35</sup> at those two times). The phrase comes from the plan's Example 3.1 spec (`book-plan.md`, Chapter 3, worked examples). This edit overrules the plan on the physics. Item 41 records the plan correction. The replacement uses only Chapter 1 and Chapter 2 results, so no forward dependency is created.

Replacement (lines 660–665):

```html
<p><strong>The design consequence, in one sentence.</strong> To match the
<var>H</var> = 3.5 s of the machine in Example 1.1, invert (3.7):
<var>&omega;</var><sub>c</sub> = 1 / (2 &times; 0.05 &times; 3.5) = 1/0.35 =
2.8571 rad/s, that is 0.4547 Hz, a power measurement filter with a time constant
of 0.3500 s.</p>
<p><strong>What that slowness touches, and what it does not.</strong> It does not
touch the current loop. The worked tuning of &sect;2.3 sets
<var>&alpha;</var><sub>c</sub> = 2&pi;(500) = 3141.59 rad/s (R14), three
decades above 2.8571 rad/s, so a slower power filter widens the timescale
separation that assumption (iii) of Model 3.2 needs. The filter pole sits next
to two other things. First, the swing mode that Theorem 3.3 creates. Take
<var>K</var><sub>s</sub> = 1.491 pu/rad from Example 1.1 (R08) as the network's
spring constant. The swing equation (3.3) with <var>H</var><sub>eq</sub> = 3.5 s
then has, by R07, <var>&omega;</var><sub>n</sub> =
&radic;(<var>K</var><sub>s</sub> <var>&omega;</var><sub>0</sub> /
(2<var>H</var><sub>eq</sub>)) = &radic;(1.491 &times; 376.99 / 7) = 8.96 rad/s
at 60 Hz, the same mode frequency as the machine, and
<var>&zeta;</var> = <var>K</var><sub>D,eq</sub>/(4<var>H</var><sub>eq</sub><var>&omega;</var><sub>n</sub>)
= 20/(4 &times; 3.5 &times; 8.96) = 0.159 against the machine's 0.016. The filter
pole at <var>&omega;</var><sub>c</sub> = 2.8571 rad/s is the open-loop pole of
the frequency channel (3.10), <var>K</var><sub>D,eq</sub>/(2<var>H</var><sub>eq</sub>)
= 20/7 = 2.8571 rad/s; closing it through the network spring is what places the
converter's swing mode in the machine's band. Section 3.7.2 shows that the
converter does contribute this <var>K</var><sub>s</sub>. Second, protection
timing. A breaker clears a fault in about 4 to 6 cycles, that is 0.067 s to
0.100 s at 60 Hz (Example 1.2). A filter with a 0.35 s time constant has
registered only 17 % to 25 % of a step change in power by then
(1 &minus; e<sup>&minus;<var>t</var>/0.35 s</sup> at those two times), so the
controller acts on a power change after the fault that caused it has cleared.</p>
```

### 6. `ch3.html:283–291` — "better conditioned as the external impedance rises" is asserted, and the natural reading is false. Parts 1 and 3 missing.

Quote (lines 283–291):

```html
<li><strong>What happens as grid strength falls.</strong> R18 showed that a
grid-following converter's loop gain is
<var>K</var><sub>pll</sub> = <var>V</var><sub>g</sub> cos
<var>&theta;</var><sub>0</sub>, which goes to zero at the current existence
bound. Equation (3.1) has no such gain. A voltage source behind an impedance is
better conditioned as the external impedance rises, not worse. The limiting case
&mdash; an islanded network with no external source at all &mdash; is the case a
grid-forming converter is built for and a grid-following converter cannot
serve.</li>
```

Defect: the spring constant K<sub>s</sub> = (E V<sub>g</sub>/X) cos δ<sub>0</sub> (R06; equation (3.29) later) falls as 1/X. At a fixed export P, δ<sub>0</sub> = arcsin(PX/(E V<sub>g</sub>)) reaches 90° at a finite X, so K<sub>s</sub> reaches zero at a finite X too. "Better conditioned" cannot be checked, and read as a statement about the synchronizing loop it is wrong. What is true and checkable: the voltage source holds its terminal magnitude at E, so the network's power limit is E V<sub>g</sub>/X, that is SCR × E × V<sub>g</sub> in per unit, against the R18 model's SCR × V<sub>g</sub>²/2. At SCR = 1.2, E = 1.1 pu, V<sub>g</sub> = 1.0 pu that is 1.32 pu against the 0.600 pu of Example 2.1, a factor 2.2. And the angle θ needs no grid voltage to advance. The replacement uses R06, R18 and Example 2.1 only.

Replacement (lines 283–291):

```html
<li><strong>What happens as grid strength falls.</strong> R18 showed that a
grid-following converter's loop gain is
<var>K</var><sub>pll</sub> = <var>V</var><sub>g</sub> cos
<var>&theta;</var><sub>0</sub>, which goes to zero at the current existence
bound. Equation (3.1) has no such gain. Its angle <var>&theta;</var> advances
whether or not a grid voltage exists, so no state of the controller loses its
input when <var>X</var><sub>g</sub> rises. What the voltage source does hold is
its own terminal magnitude <var>E</var>. Across a reactance <var>X</var> to a
source <var>V</var><sub>g</sub>, the power it can export is bounded by the
network's own limit <var>E</var> <var>V</var><sub>g</sub> / <var>X</var>, which
is SCR &times; <var>E</var> &times; <var>V</var><sub>g</sub> in per unit when
<var>X</var> = <var>X</var><sub>g</sub>, subject to the current limit
<var>I</var><sub>max</sub> that &sect;3.7 treats. The R18 model, with no
voltage support, peaks at SCR &times; <var>V</var><sub>g</sub><sup>2</sup>/2.
At SCR = 1.2, <var>E</var> = 1.1 pu and <var>V</var><sub>g</sub> = 1.0 pu that
is 1.32 pu against the 0.600 pu of Example 2.1, a factor 2.2. The spring
constant that goes with the voltage source has the machine's form
(<var>E</var> <var>V</var><sub>g</sub> / <var>X</var>) cos
<var>&delta;</var><sub>0</sub> (R06); &sect;3.7 proves it for a converter. It
falls as <var>X</var> rises, as a machine's does. The limiting case &mdash; an
islanded network with no external source at all &mdash; is the case a
grid-forming converter is built for and a grid-following converter cannot
serve, because the converter's voltage and frequency are its own states.</li>
```

### 7. `ch3.html:1415–1420` — E<sub>res</sub> is used in Corollary 3.8(b) with no prose definition. Part 2 missing.

Quote (lines 1415–1420):

```html
<p><strong>(b) Inertia, bounded by energy.</strong> The inertial response over a
frequency excursion &Delta;<var>f</var> requires the DC side to deliver</p>
<p class="eq"><var>E</var><sub>res</sub> &ge; 2 <var>H</var><sub>eq</sub>
<var>S</var><sub>base</sub> &Delta;<var>f</var> /
<var>f</var><sub>0</sub><span class="n">(3.30)</span></p>
```

Defect: E<sub>res</sub> appears in the central-result card (line 118) and in the notation list (line 202). No prose sentence defines it before (3.30). The plan's acceptance check requires every symbol "defined in the prose before its first use, not only in the table". The plan lists "usable energy reserve" among the definitions this chapter introduces.

Replacement (lines 1415–1420):

```html
<p><strong>(b) Inertia, bounded by energy.</strong> Write
<var>E</var><sub>res</sub> for the <strong>usable energy reserve</strong> of the
converter: the energy, in joules, that the source behind the DC link can deliver
at the instant of the disturbance, after state of charge, temperature and every
other commitment are taken off. Write &Delta;<var>f</var> for the magnitude of
the frequency excursion, in hertz. The inertial response over that excursion
requires</p>
<p class="eq"><var>E</var><sub>res</sub> &ge; 2 <var>H</var><sub>eq</sub>
<var>S</var><sub>base</sub> &Delta;<var>f</var> /
<var>f</var><sub>0</sub><span class="n">(3.30)</span></p>
```

### 8. `ch3.html:232–235` and `ch3.html:1421–1428` — RoCoF, δ, Q<sub>f</sub> and "headroom" are used without a definition in this chapter; (3.31) adds currents as scalars with no stated condition. Parts 2 and 4 missing.

Defect, four symbols:

- RoCoF first appears at line 1422. The book table defines it in Chapter 4 §4.3, so Chapter 3 uses a symbol the book has not yet defined. The text also uses it as a positive magnitude without saying so; for a falling frequency d<var>f</var>/d<var>t</var> is negative.
- δ (not δ<sub>0</sub>) is differentiated at line 1409, d<var>P</var>/d<var>δ</var>. The book defines δ only as a rotor angle (§3.2 of the plan). For a converter it must be defined.
- Q<sub>f</sub> appears in (3.6) at line 446 and is explained at line 452, but the local list at lines 209–235 omits it.
- "headroom" appears at line 1496 with no definition. The plan lists it among the definitions this chapter introduces.
- (3.31) adds the dispatch current i<sub>0</sub> and the inertial current as scalars. That holds when both are active currents. With a reactive part in i<sub>0</sub> the currents add as vectors and the true headroom is larger (checked numerically at I<sub>max</sub> = 1.2 pu, |i<sub>0</sub>| = 1.0 pu over 0° to 90°: the vector headroom rises from 0.200 pu to 0.663 pu; the scalar form is never larger). State the condition and the direction.

Replacement (a) — insert after line 234 (the `<var>P</var><sub>0</sub>` entry ending `(pu).`) and before line 235 (`Two book-wide symbols are reused`):

```html
<var>Q</var><sub>f</sub> &mdash; the output of the reactive-power measurement
filter (pu), the companion of <var>P</var><sub>f</sub> in equation (3.6).
<var>&delta;</var> &mdash; for a converter, the angle by which the internal
voltage <var>E</var> &ang; <var>&theta;</var> leads the grid source voltage
(rad); it is <var>&theta;</var> minus the source angle. It takes the place of
the rotor angle of Chapter 1, and <var>&delta;</var><sub>0</sub> is its
equilibrium value.
RoCoF &mdash; rate of change of frequency, |d<var>f</var>/d<var>t</var>|, in
Hz/s, used in this chapter as a positive magnitude. The book-wide definition is
in Chapter 4; this chapter needs only the symbol.
headroom &mdash; the current a converter can add above its dispatch before it
reaches its limit, <var>I</var><sub>max</sub> &minus; <var>i</var><sub>0</sub>
(pu).
```

Replacement (b) — lines 1421–1428, quoted:

```html
<p><strong>(c) Inertia, bounded by current.</strong> At a rate of change of
frequency RoCoF, the inertial power is
2<var>H</var><sub>eq</sub>RoCoF/<var>f</var><sub>0</sub> in per unit. At a
terminal voltage near 1 pu that is also the extra current, so with the converter
dispatched at <var>i</var><sub>0</sub> per unit,</p>
<p class="eq">2 <var>H</var><sub>eq</sub> RoCoF / <var>f</var><sub>0</sub> &le;
<var>I</var><sub>max</sub> &minus; <var>i</var><sub>0</sub><span class="n">(3.31)</span></p>
```

becomes:

```html
<p><strong>(c) Inertia, bounded by current.</strong> Write RoCoF for the
magnitude of the rate of change of frequency, |d<var>f</var>/d<var>t</var>|, in
Hz/s. At that rate the inertial power is
2<var>H</var><sub>eq</sub> RoCoF / <var>f</var><sub>0</sub> in per unit. Assume
a terminal voltage of 1 pu, and assume that the dispatch current
<var>i</var><sub>0</sub> and the inertial current are both active currents, in
phase with the terminal voltage, so that they add as scalars. Then the inertial
power is also the extra current, and the <strong>headroom</strong>
<var>I</var><sub>max</sub> &minus; <var>i</var><sub>0</sub> must hold it:</p>
<p class="eq">2 <var>H</var><sub>eq</sub> RoCoF / <var>f</var><sub>0</sub> &le;
<var>I</var><sub>max</sub> &minus; <var>i</var><sub>0</sub><span class="n">(3.31)</span></p>
<p>If part of <var>i</var><sub>0</sub> is reactive, the two currents add as
vectors, the true headroom is larger than this difference, and (3.31) is
conservative.</p>
```

### 9. `ch3.html:1526–1530` — the Great Britain loss-of-mains setting is attributed to S16, an EirGrid/SONI document. Misattributed citation, check (d).

Quote (lines 1526–1530):

```html
<li><strong>1 Hz/s</strong> is the figure used in Ireland's DS3 programme and in
Great Britain's loss-of-mains protection policy
<span class="cite">[S16, EirGrid and SONI, DS3 programme documentation, the
rate-of-change-of-frequency figure &mdash; document and year not yet checked
&mdash; verify]</span>. It is a system-operation and protection setting.</li>
```

Defect: S16 is Irish DS3 documentation. It cannot be the source for a Great Britain protection policy. The plan's standing warning (`book-plan.md` §5.2) and `HANDOFF.md` both assign Great Britain to S16, so the chapter inherited the error. The source list is fixed at S01 to S20 and holds no Great Britain loss-of-mains document. Rule §5.2: no bare claim without a source identifier. The chapter fix is to drop the Great Britain clause and say why. Item 42 records the plan correction.

Replacement (lines 1526–1530):

```html
<li><strong>1 Hz/s</strong> is the figure used in Ireland's DS3 programme
<span class="cite">[S16, EirGrid and SONI, DS3 programme documentation, the
rate-of-change-of-frequency figure &mdash; document and year not yet checked
&mdash; verify]</span>. It is a system-operation and protection setting. The
book's source list holds no document for the Great Britain loss-of-mains
setting, so this chapter makes no claim about it.</li>
```

---

## B. Line-level rewrites

Each item: location, quote, defect, replacement. Group 1 (items 10–15) is cross-references and unsourced claims. Group 2 (items 16–26) is sentences a reader cannot follow or evaluative phrases with no measurement. Group 3 (items 27–38) is the assumptions that items 2 and 8 make explicit, carried into the places that inherit them, plus the exercises and the closing link.

### 10. `ch3.html:597` — SVG label cites (3.8) twice.

Quote: `<text class="m2" x="220" y="104">eliminate &#916;P<tspan font-size="9">f</tspan>; equations (3.8) and (3.8)</text>`

Replacement: `<text class="m2" x="220" y="104">eliminate &#916;P<tspan font-size="9">f</tspan>; equations (3.8) and (3.9)</text>`

### 11. `ch3.html:139` — "global convergence proof" overstates Remark 3.3.

Quote: `capacitor voltage. One is a nonlinear oscillator with a global convergence` / `proof.</p>`

Replacement:

```html
capacitor voltage. One is a nonlinear oscillator with a cited almost-global
synchronization proof (Remark 3.3).</p>
```

### 12. `ch3.html:1067–1069` — same overstatement in the §3.5 opening; 27-word sentence.

Quote:

```html
dispatch point. The motivation is the proof, which is global where the
other three families have only local results.</p>
```

Replacement:

```html
dispatch point. The motivation is the proof. It is almost global, in the sense
that Remark 3.3 states, where the other three families have only local
results.</p>
```

### 13. `ch3.html:134–137` — "grid codes and vendor data sheets" has no source; S17 can carry the grid-code half.

Quote:

```html
converter carry its own angle as an internal state. The claim made for it in
grid codes and in vendor data sheets is stronger than that: the claim is that a
grid-forming converter supplies inertia. Four control families compete for the
```

Replacement:

```html
converter carry its own angle as an internal state. The claim made for it in
grid codes is stronger than that: the claim is that a grid-forming converter
supplies inertia <span class="cite">[S17, National Grid ESO, Grid Code
modification GC0137, <em>Minimum Specification Required for Provision of GB Grid
Forming Capability</em>, the inertia requirement &mdash; location not yet checked
&mdash; verify]</span>. Four control families compete for the
```

### 14. `ch3.html:151–155` — the 1111 ratio is introduced without its two ratings.

Quote:

```html
<li><strong>Does an inertia number mean the energy exists?</strong> No.
Example 3.2 computes the energy in a converter's DC link, 14.4 kJ, and the energy
a 5-second inertial response asks for, 16 MJ. The two numbers differ by a factor
of 1111. Corollary 3.8 turns that gap into a bound.</li>
```

Defect: the reader meets 1111 here and learns only in Remark 3.2 that it compares a 1 MVA store with a 100 MVA demand. State the ratings at first mention.

Replacement:

```html
<li><strong>Does an inertia number mean the energy exists?</strong> No.
Example 3.2 computes the energy in a 1 MVA converter's DC link, 14.4 kJ, and the
energy a 5-second inertial response asks of a 100 MVA unit, 16 MJ. The two
numbers differ by a factor of 1111; scaled to one rating the factor is 11.11
(Remark 3.2). Corollary 3.8 turns that gap into a bound.</li>
```

### 15. `ch3.html:295–304` — Remark 3.1: "Published designs use all three" has no source, and "The literature is explicit that the terminal behaviour ... is the classifier [S07]" asks one design paper to carry a classification claim.

Quote: the paragraph from `<p>Definition 3.1 says nothing about the inner control structure.` to `concept &mdash; location not yet checked &mdash; verify]</span>.</p>`.

Defect: S07 (Zhang, Harnefors and Nee 2010) presents one control design. It is the plan's source for R24, and it is an instance of a converter that sets its angle from its own power measurement. It is not a source for the sentence "the literature is explicit that ... is the classifier". The classifier in this book is Definition 3.1, a definition, which needs no source. "Published designs use all three" is a claim about the literature with no source identifier; cut it.

Replacement (whole paragraph):

```html
<p>Definition 3.1 says nothing about the inner control structure. A converter can
satisfy (3.1) with a cascaded voltage-and-current loop, with a current loop whose
reference is computed from a virtual impedance, or with direct modulation and no
inner loop at all. Any claim of the form "grid-forming means no current control"
is a claim about one implementation, not about the class. The classifier in this
book is Definition 3.1 itself, a statement about terminals. Power-synchronization
control is one published design that advances its angle from its own power
measurement, in the sense of (3.1)
<span class="cite">[S07, Zhang, Harnefors and Nee 2010, <em>Power-Synchronization
Control of Grid-Connected Voltage-Source Converters</em>, the
power-synchronization loop &mdash; location not yet checked &mdash;
verify]</span>.</p>
```

### 16. `ch3.html:394–397` — 33-word sentence with three ideas.

Quote:

```html
rises. This section shows that the straight line,
once you write down the filter that every real implementation needs to measure
power, <em>is</em> the swing equation of Chapter 1 with two renamed
coefficients.</p>
```

Replacement:

```html
rises. Every real implementation needs a filter to measure power. This section
writes that filter down. With it, the straight line <em>is</em> the swing
equation of Chapter 1 with two renamed coefficients.</p>
```

### 17. `ch3.html:385–388` — Fig. 3.1 caption, 38-word sentence.

Quote:

```html
both drive (panel C). The figure illustrates Definition 3.1. Between panel A and panel B the arrows on the angle and
on the current are reversed: the angle is produced inside the box by an
integrator, and the current is whatever the circuit of panel C then draws.</figcaption>
```

Replacement:

```html
both drive (panel C). The figure illustrates Definition 3.1. Between panel A and
panel B the arrows on the angle and on the current are reversed. In panel B an
integrator inside the box produces the angle. The current is then whatever the
circuit of panel C draws.</figcaption>
```

### 18. `ch3.html:546–551` — "That is why the equivalence was published as a short note" asserts the authors' motive.

Quote:

```html
indistinguishable from a mass. That is why the equivalence was published as a
short note rather than as a control design
<span class="cite">[S09, D&rsquo;Arco and Suul 2014, <em>Equivalence of Virtual
```

Replacement:

```html
indistinguishable from a mass. The equivalence was published as a two-page
letter, not as a control design
<span class="cite">[S09, D&rsquo;Arco and Suul 2014, <em>Equivalence of Virtual
```

### 19. `ch3.html:641–644` — "ten times as damped" names the wrong quantity.

Quote:

```html
<p>This value holds for all three cases. Compare it with the machine of Chapter 1,
which had <var>K</var><sub>D</sub> = 2 pu (Example 1.1). The droop converter is
ten times as damped, and it is damped by design rather than by rotor losses.</p>
```

Defect: the damping ratio ζ = K<sub>D</sub>/(4Hω<sub>n</sub>) of R07 depends on H and ω<sub>n</sub> as well. The factor ten is a ratio of coefficients, not of damping ratios.

Replacement:

```html
<p>This value holds for all three cases. Compare it with the machine of Chapter 1,
which had <var>K</var><sub>D</sub> = 2 pu (Example 1.1). The droop converter's
damping coefficient is ten times the machine's, 20 pu against 2 pu, and a line
in the control law sets it rather than rotor losses. The damping ratio
<var>&zeta;</var> = <var>K</var><sub>D</sub>/(4<var>H</var><var>&omega;</var><sub>n</sub>)
of R07 also depends on <var>H</var><sub>eq</sub> and
<var>&omega;</var><sub>n</sub>, so this is a statement about the coefficient,
not about <var>&zeta;</var>.</p>
```

### 20. `ch3.html:758–763` — Model 3.4 assumption: 54-word sentence; the "filter fast" condition is stated without its quantity.

Quote: the paragraph from `<p><strong>Assumptions.</strong> The same four as Model 3.2.` to `from Theorem 3.3.</p>`.

Defect: with a filter the loop is second order, (2H<sub>v</sub>s + K<sub>D,v</sub>)(1 + s/ω<sub>c</sub>)Δω = −ΔP. At low frequency its inertia is H<sub>v</sub> + K<sub>D,v</sub>/(2ω<sub>c</sub>). The assumption "filter fast compared with K<sub>D,v</sub>/(2H<sub>v</sub>)" is exactly the condition that the second term is small; the sentence should say so with a number, so the reader can measure it. Table 3.1's VSM row inherits the assumption.

Replacement (whole paragraph):

```html
<p><strong>Assumptions.</strong> The same four as Model 3.2. In addition,
<var>P</var><sub>f</sub> is a measured power, so a filter of some cutoff
<var>&omega;</var><sub>c</sub> is still present in every implementation. With
that filter the loop is second order:
(2<var>H</var><sub>v</sub><var>s</var> + <var>K</var><sub>D,v</sub>)(1 +
<var>s</var>/<var>&omega;</var><sub>c</sub>) &Delta;<var>&omega;</var> =
&minus;&Delta;<var>P</var>. At low frequency its inertia is
<var>H</var><sub>v</sub> + <var>K</var><sub>D,v</sub>/(2<var>&omega;</var><sub>c</sub>),
the chosen constant plus the filter's contribution from Theorem 3.3. Equation
(3.11) and the pair (3.12) assume that the second term is small against the
first, that is <var>&omega;</var><sub>c</sub> &gt;&gt;
<var>K</var><sub>D,v</sub>/(2<var>H</var><sub>v</sub>). For
<var>H</var><sub>v</sub> = 2 s, <var>K</var><sub>D,v</sub> = 5 pu and a filter at
<var>&omega;</var><sub>c</sub> = 31.4159 rad/s, the second term is 0.080 s, that
is 4.0 % of <var>H</var><sub>v</sub>.</p>
```

### 21. `ch3.html:770–776` — "built on exactly this", 48-word sentence.

Quote:

```html
guarantee. Great Britain's grid-forming specification is built on exactly this:
a declared inertial capability, tested against a defined disturbance
<span class="cite">[S17, National Grid ESO, Grid Code modification GC0137,
<em>Minimum Specification Required for Provision of GB Grid Forming
Capability</em>, the inertia specification &mdash; location not yet checked
&mdash; verify]</span>. With a machine, <var>H</var> is whatever the rotor
```

Replacement:

```html
guarantee. Great Britain's grid-forming specification uses this. It asks for a
declared inertial capability and tests it against a defined disturbance
<span class="cite">[S17, National Grid ESO, Grid Code modification GC0137,
<em>Minimum Specification Required for Provision of GB Grid Forming
Capability</em>, the inertia specification &mdash; location not yet checked
&mdash; verify]</span>. With a machine, <var>H</var> is whatever the rotor
```

### 22. `ch3.html:800–804` — Δf appears in prose for the first time with no definition (§3.3, cost 3).

Quote:

```html
Nothing in (3.11) checks that the DC side can deliver
2<var>H</var><sub>v</sub><var>S</var><sub>base</sub>&Delta;<var>f</var>/<var>f</var><sub>0</sub>
joules, or that the current needed to deliver it fits under
```

Replacement:

```html
Nothing in (3.11) checks that the DC side can deliver
2<var>H</var><sub>v</sub><var>S</var><sub>base</sub>&Delta;<var>f</var>/<var>f</var><sub>0</sub>
joules over a frequency excursion of &Delta;<var>f</var> hertz (&sect;3.7
derives that energy), or that the current needed to deliver it fits under
```

### 23. `ch3.html:834–836` — P carries two units inside one derivation.

Quote:

```html
<var>i</var><sub>dc</sub> &minus; <var>P</var><span class="n">(3.14)</span></p>
<p>in watts, where <var>i</var><sub>dc</sub> is the current the DC source pushes
into the link. Choose the gain so that the nominal DC voltage produces the rated
```

Defect: the book defines P in per unit. (3.14) and (3.18) use it in watts and step 3 converts back. Say so once, where the watt form first appears.

Replacement:

```html
<var>i</var><sub>dc</sub> &minus; <var>P</var><span class="n">(3.14)</span></p>
<p>in watts, where <var>i</var><sub>dc</sub> is the current the DC source pushes
into the link. In (3.14) and (3.18) the symbols <var>P</var> and
&Delta;<var>P</var> are in watts; step 3 of the derivation divides by
<var>S</var><sub>base</sub> and returns them to per unit, their meaning
everywhere else in the book. Choose the gain so that the nominal DC voltage
produces the rated
```

### 24. `ch3.html:875` — "That is the whole trick." is a flourish without content.

Quote: `<p>The DC voltage is the per-unit frequency, scaled. That is the whole trick.</p>`

Replacement:

```html
<p>The DC voltage is the per-unit frequency, scaled. This one substitution is the
mechanism of matching control: every later step reads a frequency deviation off
a voltage measurement.</p>
```

### 25. `ch3.html:908` — (3.19) is presented as what devices do, with no source.

Quote:

```html
droop its current on the DC voltage, which is what a controlled rectifier or a
battery converter does:</p>
```

Replacement:

```html
droop its current on the DC voltage. Equation (3.19) is a model of one way a
controlled rectifier or a battery converter can be operated; it is not a
statement about every source:</p>
```

### 26. `ch3.html:1132–1136` — Remark 3.3 closing sentence, 31 words, two reasons in one clause.

Quote:

```html
on it. It is included because it is the only global claim in the four families,
and because a reader who meets the claim elsewhere should meet its hypotheses at
the same time.</p>
```

Replacement:

```html
on it. It is included for two reasons. It is the only almost-global claim among
the four families. A reader who meets the claim elsewhere should meet its
hypotheses at the same time.</p>
```

### 27. `ch3.html:1180–1181` — the "proved here" claim for (3.24)–(3.27) must carry the assumption of item 2.

Quote:

```html
<p>The distinction matters for the acceptance of the chapter: (3.22) and (3.23) are
cited; (3.24) to (3.27) are proved here from them.</p>
```

Replacement:

```html
<p>The distinction matters for the acceptance of the chapter: (3.22) and (3.23) are
cited; (3.24) to (3.27) are proved here from them under &Delta;<var>E</var> = 0.</p>
```

### 28. `ch3.html:1204–1211` — Theorem 3.7 statement: define "symmetric operating point" in its own sentence and inherit the model assumptions.

Quote:

```html
<p>Let a grid-forming converter satisfy Definition 3.1 under any one of
Model 3.2, Model 3.4, Model 3.5, or Model 3.6, each with its own stated
assumptions. Then about a symmetric operating point &mdash; one at which the
measured power equals its set point, the internal magnitude equals its set point,
and the current is inside the limit &mdash; the small-signal dynamics are</p>
```

Replacement:

```html
<p>Call an operating point <strong>symmetric</strong> when the measured power
equals its set point, the internal magnitude equals its set point, and the
current is inside the limit. Let a grid-forming converter satisfy Definition 3.1
under any one of Model 3.2, Model 3.4, Model 3.5, or Model 3.6, each with its
own stated assumptions, including &Delta;<var>E</var> = 0 where the model states
it. Then about a symmetric operating point the small-signal dynamics are</p>
```

### 29. `ch3.html:1293` — Table 3.1, dVOC row, first cell: add the assumption.

Quote:

```html
<td>Dispatchable virtual oscillator control,
<var>&kappa;</var> = &pi;/2; model cited [S11 &mdash; verify], reduction derived
here</td>
```

Replacement:

```html
<td>Dispatchable virtual oscillator control,
<var>&kappa;</var> = &pi;/2, &Delta;<var>E</var> = 0; model cited [S11 &mdash;
verify], reduction derived here</td>
```

### 30. `ch3.html:1374` — Fig. 3.5 caption: "matching control tuned to the same pair" hides a 2.78 F capacitor; 48-word sentence.

Quote:

```html
<var>K</var><sub>D,eq</sub><sup>2</sup>). <b>Teal:</b> droop
(<var>m</var><sub>p</sub> = 0.05 pu, <var>&omega;</var><sub>c</sub> = 5 rad/s) and
matching control tuned to the same pair; they give
<var>H</var><sub>eq</sub> = 2 s and <var>K</var><sub>D,eq</sub> = 20 pu, and the
two curves coincide exactly, which is Theorem 3.7 seen as a picture. <b>Orange:</b>
```

Defect: by (3.16), H<sub>eq</sub> = 2 s needs C<sub>dc</sub>v<sub>dc0</sub>²/S<sub>base</sub> = 4 s, that is C<sub>dc</sub> = 2.7778 F at 1200 V on 1 MVA, 139 times the 20 mF of Example 3.2. Exercise 3.4 says such a bank is not built as a DC link. The caption must say the tuning is a thought experiment, or the figure contradicts the chapter's own argument.

Replacement:

```html
<var>K</var><sub>D,eq</sub><sup>2</sup>). <b>Teal:</b> droop with
<var>m</var><sub>p</sub> = 0.05 pu and <var>&omega;</var><sub>c</sub> = 5 rad/s,
which gives <var>H</var><sub>eq</sub> = 2 s and <var>K</var><sub>D,eq</sub> = 20 pu.
Matching control tuned to the same pair draws the identical curve, so one teal
line serves both; that coincidence is Theorem 3.7 seen as a picture. The
matching tuning is a thought experiment: by (3.16) it needs
<var>C</var><sub>dc</sub><var>v</var><sub>dc0</sub><sup>2</sup>/<var>S</var><sub>base</sub>
= 4 s, that is 2.78 F at 1200 V on 1 MVA, 139 times the 20 mF of Example 3.2.
<b>Orange:</b>
```

### 31. `ch3.html:1381` — Fig. 3.5 caption: "merge above about 10 rad/s" is an impression; the ratio is 1.11 there.

Quote:

```html
freely chosen <var>K</var><sub>D,v</sub> = 5 pu; it separates from the teal curve
only below its corner, and the two merge above about 10 rad/s where the inertia
term dominates. <b>Dashed grey:</b>
```

Replacement:

```html
freely chosen <var>K</var><sub>D,v</sub> = 5 pu; it separates from the teal curve
below its corner. At 10 rad/s the orange curve is still 1.11 times the teal
one; at 30 rad/s the ratio is 1.013, and above that the inertia term
2<var>H</var><sub>eq</sub><var>&omega;</var> dominates both. <b>Dashed grey:</b>
```

### 32. `ch3.html:1404–1408` — Corollary 3.8 statement: three assumptions are used in the proof and not stated.

Quote:

```html
<p>Let a converter satisfy Definition 3.1 and any family of Table 3.1, exporting
active power through a reactance <var>X</var> into a source of magnitude
<var>V</var><sub>g</sub>, at an equilibrium angle <var>&delta;</var><sub>0</sub>.
Then:</p>
```

Defect: (a) the proof uses P = (E V<sub>g</sub>/X) sin δ, which needs the output impedance Z<sub>f</sub> of (3.1) to be a pure reactance lumped into X; (b) d<var>P</var>/d<var>δ</var> at constant E needs the magnitude channel held at its set point, which is assumption (iv) of Model 3.2 and the ΔE = 0 of item 2; (c) δ for a converter is defined only in item 8. State all three.

Replacement:

```html
<p>Let a converter satisfy Definition 3.1 and any family of Table 3.1. Let its
output impedance be a pure reactance, <var>Z</var><sub>f</sub> =
j<var>X</var><sub>f</sub>, and let <var>X</var> = <var>X</var><sub>f</sub> +
<var>X</var><sub>g</sub> be the total reactance to a source of magnitude
<var>V</var><sub>g</sub>. Let the magnitude <var>E</var> be held at its set
point, which is the decoupling assumption (iv) of Model 3.2 and the
&Delta;<var>E</var> = 0 of &sect;3.5.1. Let <var>&delta;</var> be the angle by
which <var>E</var> &ang; <var>&theta;</var> leads the source, with equilibrium
value <var>&delta;</var><sub>0</sub>. Then:</p>
```

### 33. `ch3.html:1444–1447` — Corollary 3.8(b) proof integrates to δω = Δf/f<sub>0</sub>; a falling frequency has δω negative.

Quote:

```html
unit, times <var>S</var><sub>base</sub>, integrated from
<var>&delta;&omega;</var> = 0 to
<var>&delta;&omega;</var> = &Delta;<var>f</var>/<var>f</var><sub>0</sub>, gives
```

Replacement:

```html
unit, times <var>S</var><sub>base</sub>, integrated from
<var>&delta;&omega;</var> = 0 to
|<var>&delta;&omega;</var>| = &Delta;<var>f</var>/<var>f</var><sub>0</sub>
&mdash; a falling frequency has <var>&delta;&omega;</var> negative, and the
energy is the magnitude &mdash; gives
```

### 34. `ch3.html:1486–1488` — "A battery of any commercial duration holds thousands of times more" carries no number.

Quote:

```html
4.4444 kWh. Whether that binds depends entirely on what sits behind the DC link.
A battery of any commercial duration holds thousands of times more. A photovoltaic
array running at its maximum power point holds none at all, and must be curtailed
```

Replacement:

```html
4.4444 kWh. Whether that binds depends on what sits behind the DC link. A battery
rated 100 MW with a 1-hour store holds 100 MWh = 360 GJ, which is 22 500 times
the 16 MJ. A photovoltaic array running at its maximum power point holds none at
all, and must be curtailed
```

### 35. `ch3.html:1493` — "This is the bound that usually binds" has no source or case behind it.

Quote:

```html
<p><strong>The current bound (3.31).</strong> This is the bound that usually
binds, and its arithmetic is short. Take a converter with
```

Replacement:

```html
<p><strong>The current bound (3.31).</strong> In the sizing case of Chapter 4
(R39) this bound binds and the energy bound does not. Its arithmetic is short.
Take a converter with
```

### 36. `ch3.html:1662–1666` — Exercise 3.5 statement: the four tunings that give H<sub>eq</sub> = 2 s are not given, and two of them are not obvious.

Quote:

```html
<p>Simulate the four families of &sect;3.6 under a 0.1 pu step in power, with
parameters tuned to a common <var>H</var><sub>eq</sub> = 2 s. Report the peak
frequency deviation and the settling time of each, and state the numerical
tolerance of the run.</p>
```

Replacement:

```html
<p>Simulate the four families of &sect;3.6 under a 0.1 pu step in power, with
parameters tuned to a common <var>H</var><sub>eq</sub> = 2 s. Use these tunings:
droop with <var>m</var><sub>p</sub> = 0.05 pu and <var>&omega;</var><sub>c</sub> =
5 rad/s; a virtual synchronous machine with <var>H</var><sub>v</sub> = 2 s;
matching control with
<var>C</var><sub>dc</sub><var>v</var><sub>dc0</sub><sup>2</sup>/<var>S</var><sub>base</sub>
= 4 s, that is 2.78 F at 1200 V on 1 MVA, a thought experiment by Exercise 3.4;
and dispatchable virtual oscillator control with <var>&eta;</var> from (3.26) at
<var>m</var><sub>p</sub> = 0.05 pu and a power filter at
<var>&omega;</var><sub>c</sub> = 5 rad/s, which (3.27) makes 2 s. Report the peak
frequency deviation and the settling time of each, and state the numerical
tolerance of the run.</p>
```

### 37. `ch3.html:1676–1677` — Exercise 3.5 answer: one 67-word sentence carries six numbers.

Quote: from `The steady states and settling` to `&minus;0.0200 pu = &minus;1.000 Hz.`

Replacement:

```html
The steady states and settling times differ, because
<var>K</var><sub>D,eq</sub> differs. At <var>K</var><sub>D,eq</sub> = 20 pu the
time constant 2<var>H</var><sub>eq</sub>/<var>K</var><sub>D,eq</sub> is 0.200 s.
Four time constants is 0.80 s. The steady-state deviation is
&minus;0.1/20 = &minus;0.0050 pu = &minus;0.250 Hz. At
<var>K</var><sub>D,eq</sub> = 5 pu the same three numbers are 0.800 s, 3.20 s
and &minus;0.0200 pu = &minus;1.000 Hz.
```

### 38. `ch3.html:1818–1824` — "against a real fleet" contradicts the Chapter 4 spec; 56-word sentence.

Quote:

```html
<p class="small"><strong>Where Chapter 4 continues.</strong> Corollary 3.8 bounds
one converter. Chapter 4 aggregates a fleet: system stored energy and the centre
of inertia (R34), the initial rate of change of frequency (R35), the frequency
nadir (R36), and a sizing case in which the three constraints of Corollary 3.8
are worked separately against a real fleet, so that the binding one is identified
and not assumed (R39).</p>
```

Defect: the plan's Chapter 4 acceptance check requires Example 4.2 to state that its fleet "is a design case defined by this book". "A real fleet" says the opposite.

Replacement:

```html
<p class="small"><strong>Where Chapter 4 continues.</strong> Corollary 3.8 bounds
one converter. Chapter 4 aggregates a fleet. It defines the system stored energy
and the centre of inertia (R34), derives the initial rate of change of frequency
(R35) and the frequency nadir (R36), and works a sizing case (R39). That case is
a design fleet that Chapter 4 defines, not a published one. It works the three
constraints of Corollary 3.8 separately, so that the binding one is identified
and not assumed.</p>
```

---

## C. Structural notes

### 39. The chapter has no closing statement of what the reader can now do. Insert one.

The skill requires every chapter to close with what the reader can now do. §3.7.4 lists limits; the ledger and source list follow. Nothing states the gain. The plan's Outcome 3 is the content. Insert the block below immediately before the `<hr>` that precedes `<h2 id="ex">Exercises</h2>` (line 1569). An `<h3>` keeps the plan's seven-section structure.

```html
<h3>3.7.5 What the reader can now do</h3>
<p>Before this chapter the reader could compute a machine's swing mode (R07) and
show that a grid-following fleet supplies neither <var>K</var><sub>s</sub> nor
<var>H</var> (R23). After it the reader can do three things.</p>
<ol>
<li>Take any of the four published control laws, linearise it about a symmetric
operating point, and read off its (<var>H</var><sub>eq</sub>,
<var>K</var><sub>D,eq</sub>) from Table 3.1, or derive the pair by the
coefficient matching of Theorem 3.3 (R26, R32).</li>
<li>Compute the synchronizing coefficient that a grid-forming converter restores
on a given network with (3.29), and check it digit for digit against the machine
it replaces (R33, &sect;3.7.2).</li>
<li>Test a declared inertia number against the energy bound (3.30) and the
current bound (3.31), with the arithmetic of &sect;3.7.3 and Exercise 3.6, so
that "5 seconds of inertia" becomes a set of checkable numbers (R33).</li>
</ol>
<p>Chapter 4 applies the third of these to a fleet.</p>
```

### 40. Length.

The draft reports 9 595 reader tokens against a target of 8 000 ± 20 % (6 400 to 9 600). My parser counts 11 240 prose words outside `<svg>` and `<style>`, including captions, the notation card, Table 3.1, the ledger, the source list and the exercise answers. The plan counts figures and exercises separately from the 8 000, so the two numbers measure different things. Not blocking. Items 5, 8, 20, 30 and 39 add about 450 words; nothing in this edit asks for a cut.

### 41. Plan correction: Example 3.1 spec, "interact with the current loop".

`book-plan.md`, Chapter 3, Example 3.1: "slow enough to interact with the current loop of §2.3 and with protection". Item 5 shows the current-loop half is reversed (α<sub>c</sub> = 3141.59 rad/s in `ch2.html:269` is three decades above the filter pole). The plan owner should change the spec to "slow enough to sit within one decade of the swing mode it creates (8.96 rad/s on the Example 1.1 network) and to span the 4 to 6 cycle protection window", so that edit2 does not re-flag the chapter for departing from the plan.

### 42. Plan correction: S16 cannot source Great Britain.

`book-plan.md` §5.2 standing warning and `HANDOFF.md` assign "the 1 Hz/s figure of Ireland DS3 and GB loss-of-mains" to S16 (EirGrid and SONI). S16 covers Ireland only. If the book wants the Great Britain setting, the plan owner must add a Great Britain document to the source list (a candidate class is the distribution-code engineering recommendation for loss-of-mains protection; I name no document, because I cannot open one). Until then, item 9 removes the claim from the chapter.

### 43. HTML rule deviations, low severity.

- Plan §5.3 item 5 asks for a class that names the result kind (`def`, `model`, `thm`, `cor`, `ex`, `rem`). Every result `<div>` uses `class="res"`; examples and remarks add `ex` and `rem`; definitions, models, theorems and the corollary carry no kind class. The `id` prefixes (`def-3-1`, `model-3-2`, `thm-3-3`, `cor-3-8`) carry the kind instead. Fix if the book-level link checker keys on class: add the kind as a second class, for example `class="res def"`, `class="res model"`, `class="res thm"`, `class="res cor"`.
- Plan §5.3 item 4 asks for the eight palette values as custom properties and no literals below `:root`. Lines 54, 68 and 87 use `#16213a` (equation and code background) and `#20304a` (table header), neither of which is in the eight-colour palette. The SVG `<style>` blocks (lines 320, 571, 603, 687, 1337) repeat palette values as literals. Fix if strictness is wanted: add `--eqbg:#16213a; --thbg:#20304a;` to `:root` and use `var(--eqbg)` and `var(--thbg)`; or replace both with `var(--bg)`. No visual judgement was made; the parser check found all eight palette values present and `<meta name="color-scheme" content="dark">` present.

### 44. Status label "stated here" is outside the plan's §5.4 list.

Models 3.2, 3.4 and 3.6 carry "stated here" or "model cited". §5.4 lists `proved here`, `proved in §`, `cited [S — verify]`, `computed in Example`, `assumed for this case`. A model is a definition-like object; "stated here" is the accurate label and `assumed for this case` would be wrong. Recommend that the plan owner add `stated here` to the §5.4 list rather than change the chapter.

### 45. File name.

The file is `ch3.html`; plan §5.3 names `ch03.html`. Sibling chapters use `ch1.html` to `ch4.html`. The plan's cross-chapter link format `ch01.html#thm-1-3` must be aligned to the file names in use before the book-level link check runs. Chapter 3 contains no cross-chapter `href`, so nothing breaks here.

### 46. Dependency map and figure plan.

Every dependency points backward: Theorem 3.3 uses R04; Model 3.5 uses R03; Corollary 3.8 uses R05, R06, Definition 3.1 and Theorem 3.7; Theorem 3.7 uses Models 3.2, 3.4, 3.5, 3.6. Items 5 and 6 add references to R06, R07, R08, R14, R18 and Example 2.1 only. No cycle. Forward mentions of §3.6 and §3.7 in §3.1 to §3.3 are announcements, not dependencies. Fig. 3.4: the plan asked for one per-MVA bar chart showing both 243 and 1111; those two ratios cannot appear on one per-MVA axis. The draft's four-bar absolute chart plus Remark 3.2 is the correct resolution. The plan owner should adopt it into the figure spec.

### 47. Prose scan summary.

501 sentences. The splitter flags 149 over 25 words, but most of those are the notation card, Table 3.1, the ledger and equation-bearing sentences that a reader follows term by term. The sentences that carry one idea a reader cannot follow are items 5, 12, 16, 17, 20, 21, 26, 28, 30, 37 and 38, all rewritten above. Hedge words: none of "obviously", "clearly", "it is easy to see", "simply", "very" (as a word), "powerful", "elegant" appears. Evaluative phrases without a measurement: items 18, 21, 24, 31, 34 and 35.

---

## D. Cross-chapter check (h)

Each cited R-id, compared with `book-plan.md` §2:

- R03 (H = E<sub>kin</sub>/S<sub>base</sub>): used at line 848 in the sense of the plan. Matches.
- R04 (2H dδω/dt = P<sub>m</sub> − P<sub>e</sub> − K<sub>D</sub>δω, per-unit damping): equation (3.3), stated with the alternative named and excluded. Matches §3.6 item 2 of the plan.
- R05 (P<sub>e</sub> = (E′V/X) sin δ): used in the proof of Corollary 3.8(a) with E in place of E′; the substitution is declared in the local notation. Matches.
- R06 (K<sub>s</sub> = (E′V/X) cos δ<sub>0</sub>, positive iff |δ<sub>0</sub>| < 90°): equation (3.29). Matches.
- R07 (ω<sub>n</sub>, ζ, stability iff K<sub>s</sub> > 0 and K<sub>D</sub> > 0): cited in §3.7 opening. Matches.
- R08 (δ<sub>0</sub> = 28.2°, K<sub>s</sub> = 1.49 pu/rad): §3.7.2 recomputes 28.21° and 1.491 pu/rad. Matches. `ch1.html:689` prints 1.4913.
- R14 (first-order current loop, bandwidth α<sub>c</sub>): used for assumption (iii) of Model 3.2 and, after item 5, with the value 3141.59 rad/s from `ch2.html:269`. Matches.
- R17 (current source in PLL frame behind jX<sub>g</sub>): §3.1 bullets. Matches.
- R18 (K<sub>pll</sub> = V<sub>g</sub> cos θ<sub>0</sub> → 0 at the current bound; P<sub>max</sub> = SCR V<sub>g</sub>²/2): §3.0 and §3.1; item 6 adds the P<sub>max</sub> comparison with Example 2.1's 0.600 pu. Matches.
- R23 (grid-following fleet supplies neither K<sub>s</sub> nor H): §3.0 and §3.7. Matches.
- Forward mention of R39 and R40 in §3.7.4 and the closing paragraph: statements agree with the plan after item 38.

---

## E. What already works

### 48. Theorem 3.3 and its proof.

I re-derived (3.8), (3.9) and (3.7) by hand and in `edit_ch3_check.py`. The proof defines ΔP once and uses it on both sides, states where the swing equation's P<sub>m</sub> goes, and matches two independent coefficients. It is exact under the stated assumptions. Fig. 3.2 draws the same two block diagrams. This is the passage to imitate.

### 49. The −P<sub>0</sub> term in (3.21) is correct. Do not "correct" it to the term-free form.

The draft asked the editor to check this. I re-derived it from (3.14), (3.19) and (3.20) with Δv<sub>dc</sub> = v<sub>dc0</sub>Δω: C<sub>dc</sub>v<sub>dc0</sub>² dΔω/dt = (i<sub>dc0</sub> − k<sub>dc</sub>v<sub>dc0</sub>)v<sub>dc0</sub>Δω − ΔP, and dividing by S<sub>base</sub> gives K<sub>D,eq</sub> = k<sub>dc</sub>v<sub>dc0</sub>²/S<sub>base</sub> − P<sub>0</sub>. The sign holds. The limit k<sub>dc</sub> = 0 gives K<sub>D,eq</sub> = −P<sub>0</sub>, which is the correct physics of a stiff current source feeding a rising voltage. The number k<sub>dc</sub> = 14.5833 A/V back-checks to K<sub>D,eq</sub> = 20.0000 pu. The literature form without −P<sub>0</sub> assumes a constant-power source or P<sub>0</sub> = 0; the chapter's form is the more general one and it says so.

### 50. δ<sub>0</sub> = 0.4924 rad is correct. Do not align it to the plan.

arcsin(0.472727) = 0.49237 rad. The plan's Example 1.1 prints 0.4926 rad; that is the plan's rounding error, and `ch1.html:689` uses the correct value (cos δ<sub>0</sub> = 0.881209, K<sub>s</sub> = 1.4913). The chapter's 0.4924 rad, 28.21°, cos = 0.8812 and K<sub>s</sub> = 1.491 pu/rad all recompute.

### 51. Example 3.2 and Remark 3.2.

All eleven printed numbers recompute. Remark 3.2 separates the three ratios 243, 1111 and 11.11 by the rating each compares, which repairs a defect in the plan's own figure spec (item 46). The like-for-like figure, 11.11, is the one a reader needs, and the chapter says so.

### 52. Every figure is drawn from computed numbers.

Forty-eight SVG coordinates in Figs. 3.3, 3.4 and 3.5 (17, 8 and 23) recompute to 0.1 px from the stated axes and formulas. One marker (Fig. 3.5, VSM corner, y = 110.9) recomputes as 110.8; the difference is below the 2.4 px stroke width and needs no fix. Each caption states what the figure illustrates and which result it belongs to.

### 53. Remark 3.3 carries the hypotheses with the claim.

The almost-global synchronization result is labelled cited, its four hypotheses are listed, and the text says that no result in the book depends on it. This is how a cited theorem should appear.

### 54. Remark 3.4 keeps the two RoCoF figures apart.

2 Hz/s over 500 ms is attributed to S15 only; 1 Hz/s to S16 only; the string "ENTSO-E" never appears within 200 characters of "1 Hz/s". The standing warning is obeyed. Item 9 narrows the S16 claim to Ireland.

### 55. Model environments.

Models 3.2, 3.4, 3.5 and 3.6 each state the law, list assumptions by number, and name omissions. Model 3.5 states that (3.16) holds only under the gain choice (3.15) and gives the general form. Model 3.2's omissions are repaid where the text says they are (§3.7 for the limiter).

### 56. Citations.

Twelve inline citations; each has the four parts and the word "verify"; nine source identifiers S01, S07, S09, S10, S11, S12, S15, S16, S17, all from the plan's list. No page or section number is invented; each location field names the topic and says "location not yet checked". After item 9 every source is used for a claim it can plausibly carry: S01 for governor droop and the H band, S09 for the equivalence letter (its page range 394–395 is consistent with a two-page letter), S10 for matching, S11 for dVOC and its theorem, S12 for the four-family comparison, S15 for the withstand figure, S16 for Ireland, S17 for the GB grid-forming specification. Item 15 narrows the S07 claim to what a design paper can carry.

### 57. The problem opens the chapter and each section returns to it.

§3.0 states the loss (R23), the claim under test, and three questions. §3.2 answers question 2 with Example 3.1. §3.4 and Example 3.2 answer question 3. §3.6 answers question 1. §3.7.2 closes the loop with the digit-for-digit K<sub>s</sub> match, and §3.7.3 turns the energy gap into two bounds. Theory and evidence are kept apart: every result carries "proved here", "computed here" or "cited".

### 58. Equation numbering.

Thirty-one numbered equations, (3.1) to (3.31), continuous; each is referenced at least once elsewhere; one intermediate display in the proof of Theorem 3.3 is left unnumbered per §5.1. Result counter continuous, Definition 3.1 to Corollary 3.8. `data-rid` R24 to R33 present and in order.

### 59. HTML self-containment.

Zero `<script>`, zero `<link>`, zero `<img>`, zero external `href` or `src`, zero occurrences of "http" or "data:" anywhere in the file. Twenty-eight `id` values, none duplicated. No internal anchors, so none broken. One `<h1>`, eleven `<h2>`, eight `<h3>`; six `<details>` for six exercises; five `<figure>` with inline `<svg>`. After item 1 the file parses with zero errors.

### 60. The exercises test what was taught, in ascending difficulty.

Exercise 3.1 tests Definition 3.1 against Corollary 3.8. Exercise 3.2 re-derives Theorem 3.3. Exercise 3.3 uses (3.11) and (3.5). Exercise 3.4 inverts (3.16) and returns the factor 243, and says why. Exercise 3.5 predicts the initial slope from H<sub>eq</sub> alone before asking for a run, which is the right habit. Exercise 3.6 turns the vendor claim into three numbers and adds the fourth the chapter itself raised. Every one is solvable from the text after items 36 and 37.

---

## F. Numbers recomputed

Every printed number in Examples 3.1 and 3.2, §3.2 to §3.7, the six exercises, and every SVG coordinate in Figs. 3.3 to 3.5 that follows from a stated formula. Rows marked `info` are editor computations that support a replacement text; they are not counted. Source: `edit_ch3_check.py`.


**Totals.** 127 printed numbers and coordinates recomputed; 2 do not match. One has a consequence: the "11 %" at line 670 (item 4). The other is the Fig. 3.5 VSM corner marker, printed y = 110.9 against 110.8 recomputed, a 0.1 px offset below the 2.4 px stroke width; no fix. Every other number in Examples 3.1 and 3.2, sections 3.2 to 3.7, the six exercises and the three computed figures recomputes to the printed digits.

| # | Location | Printed | Recomputed | Result | Note |
|---|---|---|---|---|---|
| 1 | 3.2.1 omega0 at 50 Hz | 314.159 | 314.159 | ok |  |
| 2 | 3.2.2 5% droop at 50 Hz (Hz) | 2.50 | 2.50 | ok |  |
| 3 | 3.2.2 5% droop at 60 Hz (Hz) | 3.0 | 3.0 | ok |  |
| 4 | Ex3.1 K_D,eq | 20 | 20 | ok |  |
| 5 | Ex3.1 wc1 | 31.4159 | 31.4159 | ok |  |
| 6 | Ex3.1 2*mp*wc1 | 3.14159 | 3.14159 | ok |  |
| 7 | Ex3.1 H_eq case1 | 0.3183 | 0.3183 | ok |  |
| 8 | Ex3.1 tau1 | 0.0318 | 0.0318 | ok |  |
| 9 | Ex3.1 wc2 | 6.2832 | 6.2832 | ok |  |
| 10 | Ex3.1 2*mp*wc2 | 0.62832 | 0.62832 | ok |  |
| 11 | Ex3.1 H_eq case2 | 1.5915 | 1.5915 | ok |  |
| 12 | Ex3.1 tau2 | 0.1592 | 0.1592 | ok |  |
| 13 | Ex3.1 wc3 in Hz | 0.3183 | 0.3183 | ok |  |
| 14 | Ex3.1 H_eq case3 | 5.000 | 5.000 | ok |  |
| 15 | Ex3.1 tau3 | 0.5000 | 0.5000 | ok |  |
| 16 | Ex3.1 wc for H=3.5 (rad/s) | 2.8571 | 2.8571 | ok |  |
| 17 | Ex3.1 wc for H=3.5 (Hz) | 0.4547 | 0.4547 | ok |  |
| 18 | Ex3.1 tau for H=3.5 | 0.3500 | 0.3500 | ok |  |
| 19 | Ex3.1 prose: 0.3183 s 'is 11 %' of 3.5 s  (percent) | 11 | 9.1 | WRONG (item 4) | 0.3183/3.5 = 9.09 %; 3.5/0.3183 = 11.0 -> the text inverted the ratio |
| 20 | Ex3.1 prose: 'ten times as damped' K_D ratio | 10 | 10 | ok |  |
| 21 | editor: swing mode of H_eq=3.5 s droop unit on Ex1.1 network (60 Hz) | - | omega_n=8.962 rad/s, zeta=0.1594, filter pole 2.857 rad/s | info |  |
| 22 | Fig3.3 pt(2,5.000) x | 308.7 | 308.7 | ok |  |
| 23 | Fig3.3 pt(2,5.000) y | 122.7 | 122.7 | ok |  |
| 24 | Fig3.3 pt(6.2832,1.5915) x | 396.9 | 396.9 | ok |  |
| 25 | Fig3.3 pt(6.2832,1.5915) y | 152.8 | 152.8 | ok |  |
| 26 | Fig3.3 pt(31.4159,0.3183) x | 520.8 | 520.8 | ok |  |
| 27 | Fig3.3 pt(31.4159,0.3183) y | 195.1 | 195.1 | ok |  |
| 28 | Fig3.3 H=3.5 dashed y | 132.1 | 132.1 | ok |  |
| 29 | Fig3.3 mp=0.05 line at wc=100: y | 225.5 | 225.5 | ok |  |
| 30 | Fig3.3 mp=0.02 line start x (H=100) | 148.6 | 148.6 | ok |  |
| 31 | Fig3.3 mp=0.02 line end y (wc=100) | 201.4 | 201.4 | ok |  |
| 32 | Fig3.3 mp=0.10 line start y (wc=0.1) | 62.2 | 62.2 | ok |  |
| 33 | Fig3.3 mp=0.10 line end y (wc=100) | 243.7 | 243.7 | ok |  |
| 34 | Fig3.3 grid x wc=1 | 255.3 | 255.3 | ok |  |
| 35 | Fig3.3 grid x wc=10 | 432.7 | 432.7 | ok |  |
| 36 | Fig3.3 grid y H=0.1 | 225.5 | 225.5 | ok |  |
| 37 | Fig3.3 grid y H=1 | 165 | 165 | ok |  |
| 38 | Fig3.3 grid y H=10 | 104.5 | 104.5 | ok |  |
| 39 | 3.4 k_dc for K_D,eq=20 at P0=1 | 14.5833 | 14.5833 | ok |  |
| 40 | 3.4 back-check K_D,eq | 20 | 20.0000 | ok |  |
| 41 | Ex3.2 omega0 | 314.1593 | 314.1593 | ok |  |
| 42 | Ex3.2 k_theta | 0.261799 | 0.261799 | ok |  |
| 43 | Ex3.2 vdc0^2 | 1.44e6 | 1.44e+06 | ok |  |
| 44 | Ex3.2 stored J | 14400 | 14400 | ok |  |
| 45 | Ex3.2 H_eq | 0.0144 | 0.0144 | ok |  |
| 46 | Ex3.2 ratio 243 | 243.06 | 243.06 | ok |  |
| 47 | Ex3.2 0.8/50 | 0.0160 | 0.0160 | ok |  |
| 48 | Ex3.2 16 MJ | 16 | 16 | ok |  |
| 49 | Ex3.2 kWh | 4.4444 | 4.4444 | ok |  |
| 50 | Ex3.2 ratio 1111 | 1111.11 | 1111.11 | ok |  |
| 51 | Rem3.2 0.16 MJ/MVA | 0.16 | 0.16 | ok |  |
| 52 | Rem3.2 11.11 | 11.11 | 11.11 | ok |  |
| 53 | Rem3.2 3.5 MJ per MVA at H=3.5 | 3.5 | 3.5 | ok |  |
| 54 | Fig3.4 bar 16 MJ | 334.8 | 334.8 | ok |  |
| 55 | Fig3.4 bar 3.5 MJ | 265.9 | 265.9 | ok |  |
| 56 | Fig3.4 bar 0.16 MJ | 125.8 | 125.8 | ok |  |
| 57 | Fig3.4 bar 0.0144 MJ | 16.5 | 16.5 | ok |  |
| 58 | Fig3.4 grid x for 0.1 MJ | 290.5 | 290.5 | ok |  |
| 59 | Fig3.4 grid x for 1 MJ | 395 | 395.0 | ok |  |
| 60 | Fig3.4 grid x for 10 MJ | 499.5 | 499.5 | ok |  |
| 61 | Fig3.4 grid x for 100 MJ | 604 | 604.0 | ok |  |
| 62 | 3.5.1 eta at 50 Hz | 15.7080 | 15.7080 | ok |  |
| 63 | 3.5.1 omega0 at 60 Hz | 376.9911 | 376.9911 | ok |  |
| 64 | 3.5.1 eta at 60 Hz | 18.8496 | 18.8496 | ok |  |
| 65 | Fig3.5 droop H_eq from mp=0.05, wc=5 | 2 | 2 | ok |  |
| 66 | Fig3.5 droop low-freq y (1/20) | 146.3 | 146.3 | ok |  |
| 67 | Fig3.5 droop corner w | 5 | 5 | ok |  |
| 68 | Fig3.5 droop corner x | 437 | 437 | ok |  |
| 69 | Fig3.5 droop corner y | 158.2 | 158.2 | ok |  |
| 70 | Fig3.5 VSM low-freq y (1/5) | 99.0 | 99.0 | ok |  |
| 71 | Fig3.5 VSM corner w | 1.25 | 1.25 | ok |  |
| 72 | Fig3.5 VSM corner x | 356.9 | 356.9 | ok |  |
| 73 | Fig3.5 VSM corner y | 110.9 | 110.8 | wrong (0.1 px; below stroke width; no fix) |  |
| 74 | Fig3.5 both at w=100 y | 248.7 | 248.7 | ok |  |
| 75 | Fig3.5 VSM at w=100 y | 248.7 | 248.7 | ok |  |
| 76 | Fig3.5 grid y 0.01 | 201.3 | 201.3 | ok |  |
| 77 | Fig3.5 grid y 0.1 | 122.7 | 122.7 | ok |  |
| 78 | Fig3.5 grid x w=0.1 | 211 | 211 | ok |  |
| 79 | Fig3.5 grid x w=1 | 344 | 344 | ok |  |
| 80 | Fig3.5 grid x w=10 | 477 | 477 | ok |  |
| 81 | Fig3.5 teal polyline y at x=78.0 | 146.3 | 146.3 | ok |  |
| 82 | Fig3.5 teal polyline y at x=344.0 | 147.0 | 147.0 | ok |  |
| 83 | Fig3.5 teal polyline y at x=437.1 | 158.2 | 158.2 | ok |  |
| 84 | Fig3.5 teal polyline y at x=530.2 | 202.2 | 202.2 | ok |  |
| 85 | Fig3.5 teal polyline y at x=610.0 | 248.7 | 248.7 | ok |  |
| 86 | Fig3.5 orange polyline y at x=78.0 | 99.0 | 99.0 | ok |  |
| 87 | Fig3.5 orange polyline y at x=344.0 | 107.4 | 107.4 | ok |  |
| 88 | Fig3.5 orange polyline y at x=437.1 | 147.5 | 147.5 | ok |  |
| 89 | Fig3.5 orange polyline y at x=530.2 | 201.5 | 201.5 | ok |  |
| 90 | Fig3.5 orange polyline y at x=610.0 | 248.7 | 248.7 | ok |  |
| 91 | editor: |G_VSM|/|G_droop| at 10 rad/s | - | 1.109 | info | caption says the curves merge above about 10 rad/s |
| 92 | editor: C_dc for H_eq=2 s at 1200 V, 1 MVA | - | 2.7778 F = 138.9 x 20 mF | info | Fig 3.5 caption does not say this |
| 93 | 3.7.2 P X/(E Vg) | 0.4727 | 0.4727 | ok |  |
| 94 | 3.7.2 delta0 rad | 0.4924 | 0.4924 | ok |  |
| 95 | 3.7.2 delta0 deg | 28.21 | 28.21 | ok |  |
| 96 | 3.7.2 E Vg/X | 1.6923 | 1.6923 | ok |  |
| 97 | 3.7.2 cos delta0 | 0.8812 | 0.8812 | ok |  |
| 98 | 3.7.2 K_s | 1.491 | 1.491 | ok |  |
| 99 | 3.7.2 K_s vs Ch1 1.49 | 1.49 | 1.49 | ok |  |
| 100 | 3.7.3 16 MJ | 16 | 16 | ok |  |
| 101 | 3.7.3 kWh | 4.4444 | 4.4444 | ok |  |
| 102 | 3.7.3 0.0144 MJ/MVA | 0.0144 | 0.0144 | ok |  |
| 103 | 3.7.3 shortfall 11.11 | 11.11 | 11.11 | ok |  |
| 104 | 3.7.3 RoCoF bound | 1.000 | 1.000 | ok |  |
| 105 | 3.7.3 inertial power at 1 Hz/s | 0.200 | 0.200 | ok |  |
| 106 | 3.7.3 inertial power at 2 Hz/s | 0.400 | 0.400 | ok |  |
| 107 | editor: 100 MW x 1 h battery vs 16 MJ | - | 22500 x | info | prose says 'thousands of times more' with no number |
| 108 | Ex3.4 C_dc | 4.8611 | 4.8611 | ok |  |
| 109 | Ex3.4 7e6/1.44e6 | 4.8611 | 4.8611 | ok |  |
| 110 | Ex3.4 ratio to 20 mF | 243.06 | 243.06 | ok |  |
| 111 | Ex3.5 slope pu/s | -0.0250 | -0.0250 | ok |  |
| 112 | Ex3.5 slope Hz/s | -1.2500 | -1.2500 | ok |  |
| 113 | Ex3.5 tau at K=20 | 0.200 | 0.200 | ok |  |
| 114 | Ex3.5 4 tau at K=20 | 0.80 | 0.80 | ok |  |
| 115 | Ex3.5 ss pu at K=20 | -0.0050 | -0.0050 | ok |  |
| 116 | Ex3.5 ss Hz at K=20 | -0.250 | -0.250 | ok |  |
| 117 | Ex3.5 tau at K=5 | 0.800 | 0.800 | ok |  |
| 118 | Ex3.5 4 tau at K=5 | 3.20 | 3.20 | ok |  |
| 119 | Ex3.5 ss pu at K=5 | -0.0200 | -0.0200 | ok |  |
| 120 | Ex3.5 ss Hz at K=5 | -1.000 | -1.000 | ok |  |
| 121 | Ex3.6 MJ on 50 MVA | 8.00 | 8.00 | ok |  |
| 122 | Ex3.6 kWh on 50 MVA | 2.222 | 2.222 | ok |  |
| 123 | Ex3.6 MW at 1 Hz/s on 50 MVA | 10.0 | 10.0 | ok |  |
| 124 | Ex3.6 MJ on 100 MVA | 16.00 | 16.00 | ok |  |
| 125 | Ex3.6 kWh on 100 MVA | 4.444 | 4.444 | ok |  |
| 126 | Ex3.6 MW at 1 Hz/s on 100 MVA | 20.0 | 20.0 | ok |  |
| 127 | Ex3.6 MJ on 200 MVA | 32.00 | 32.00 | ok |  |
| 128 | Ex3.6 kWh on 200 MVA | 8.889 | 8.889 | ok |  |
| 129 | Ex3.6 MW at 1 Hz/s on 200 MVA | 40.0 | 40.0 | ok |  |
| 130 | Ex3.3 m_p from K_D,v=20 | 0.0500 | 0.0500 | ok |  |
| 131 | Ex3.2 omega0 factor | 314.159 | 314.159 | ok |  |
| 132 | editor: dVOC d(dtheta/dt)/dE at operating point | - | 2*eta*P_ref/V_ref^3 (nonzero unless P_ref=0) | info | (3.25) drops this term; the reduction needs Delta E = 0 stated |
| 133 | editor: VSM with filter, low-frequency inertia | - | H_v + K_D,v/(2 omega_c) | info | Model 3.4 assumption 'filter fast' means K_D,v/(2 omega_c) << H_v |
| 134 | editor: filter registration 1-exp(-t/0.35) at t=0.067 s | - | 17.3 % | info | item 5 replacement text |
| 135 | editor: filter registration 1-exp(-t/0.35) at t=0.100 s | - | 24.9 % | info | item 5 replacement text |
| 136 | editor: zeta of H_eq=3.5 s droop unit, K_D,eq=20 pu, omega_n=8.96 rad/s (R07) | - | 0.159 | info | item 5 replacement text; machine of Example 1.1 has 0.016 |
| 137 | editor: K_D,eq/(2 H_eq) = 20/7 (open-loop pole of (3.10)) | - | 2.8571 rad/s | info | equals omega_c, item 5 replacement text |
