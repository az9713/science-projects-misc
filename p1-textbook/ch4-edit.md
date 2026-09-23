# ch4-edit.md — Editor's edit of Chapter 4 (System-level stability and a sizing case)

**Verdict: ACCEPT WITH CHANGES.** The arithmetic and both proofs are correct, but eight statement-level defects stop a reader new to power systems.

The eight, in order of severity: a self-contradicting sweep definition (B1); an unreproducible reduction check (B2); a model labelled "proved" with no derivation (B3); an imprecise theorem statement (B4); nine undefined terms of art (B5); one forward reference (B6); one number attributed to a source that cannot hold it (B7); a wrong opening sentence (B8). Numbers: 267 printed values recomputed in 187 checks, 0 wrong (§5).

Editor: science-editor pass, 2026-09-22. Files read in full: `book-plan.md` (§1 to §6), `ch4.html` (1602 lines), `draft-results.json` (chapter 4 entry), `HANDOFF.md`. Domain brief: assembled from `book-plan.md` §2, §3, §4 (Chapter 4 spec) and §5. No PDF source was opened; every citation stays `verify`. Scratch scripts: `edit_ch4_check.py`, `edit_ch4_html.py`, `edit_ch4_ste.py`, `edit_ch4_table.py` in the session scratchpad. No project file other than this one was written.

Numbering: B = blocking defect, L = line-level rewrite, S = structural note, W = what works. Every item has one number. The fix stage reports by that number.

How to read a replacement: the text after "Replace with:" is complete HTML in the chapter's own markup. Paste it over the quoted lines. Line numbers refer to `ch4.html` as drafted (13:29 PDT).

---

## 1. Blocking defects

### B1 — The sweep definition contradicts itself (ch4.html:704-712)

**Quoted.** "total rating is held at 1000 MVA and total dispatch at 630 MW; ... each unit keeps its H, K_D, per-unit internal reactance and per-unit dispatch; ..."

**Defect.** Part 1 of the standard (precise statement). The two clauses cannot both hold. With per-unit dispatch fixed, total dispatch at c = 0 is 571.4 × 0.75 + 428.6 × 0.60 = 685.7 MW. At c = 1 it is 500.0 MW. Neither is 630 MW. The printed eigenvalues follow the first clause. Evidence: with total dispatch scaled to 630 MW, the modes are −2.2151 + j17.3463 (c = 20 %) and −0.7671 + j12.9359 (c = 80 %). Those match the chapter to four decimals. With per-unit dispatch fixed they are −2.2158 + j17.3489 and −0.7621 + j12.9316. The draft's probe script confirms the rule it ran: `draft_ch4_check.py:161-163` scales each `S_i × d_i` by one common factor `630/tot`.

**Replace lines 704-712 with:**

```html
<p>The question that matters for the purchase decision is not what TS4 does at one
operating point. It is what happens as machines are replaced by converters. The sweep
is defined by the six rules below. The rules are a choice of this case, not a result.
<em>Assumed for this case:</em></p>
<ol>
<li>Total rating stays at 1000 MVA. A converter share <var>c</var> puts
1000<var>c</var> MVA on units 3 and 4, split 2:1 as in the base case, and
1000(1 − <var>c</var>) MVA on units 1 and 2, split 4:3.</li>
<li>Total dispatch stays at 630 MW. Each unit's dispatch starts as its rating times its
base-case per-unit dispatch. One common factor then scales all four so that they sum to
630 MW. A unit's per-unit dispatch therefore changes with <var>c</var>. At
<var>c</var> = 0.20 the unscaled sum is 648.6 MW and the factor is 630/648.6 = 0.9713.
Unit 1 then runs at 0.75 × 0.9713 = 0.7285 pu instead of 0.75 pu.</li>
<li>Each unit keeps its <var>H</var>, its <var>K</var><sub>D</sub> and its internal
reactance in per unit on its own base.</li>
<li>Each unit's reactive injection stays proportional to its rating, as in §4.1.3, so
the four sum to 120 Mvar.</li>
<li>The connecting reactances on the system base do not change.</li>
<li>A unit of zero rating is removed from the model.</li>
</ol>
<p>The base case is <var>c</var> = 0.30, where the factor in rule 2 is 1.</p>
```

### B2 — The reduction check cannot be reproduced from the printed numbers (ch4.html:443-455, caption 536-538)

**Quoted.** "Substituting these numbers into (4.2) returns P_e,1 = 0.3000, P_e,2 = 0.1800, P_e,3 = 0.1000 and P_e,4 = 0.0500 pu ... The reduction is therefore exact to the digits printed here."

**Defect.** Part 3 of the standard (a reader must reproduce every line with a pen). The chapter prints six off-diagonal B_ij and six off-diagonal G_ij. Equation (4.2) sums over all j, including j = i, and the j = i term is E_i² G_ii. The four diagonal conductances are not printed. With the printed twelve numbers alone the sum returns 0.2193, 0.1448, 0.0537 and 0.0383 pu, not the dispatches. Recomputed G_ii: 0.0703, 0.0307, 0.0436, 0.0110 pu.

**Replace lines 443-455 with:**

```html
<p>Reducing the five-bus network (four internal nodes and bus L) by (4.1) gives the
transfer terms of the reduced mesh. The six transfer susceptances are
<var>B</var><sub>12</sub> = 0.2555, <var>B</var><sub>13</sub> = 0.3043,
<var>B</var><sub>14</sub> = 0.1529, <var>B</var><sub>23</sub> = 0.2011,
<var>B</var><sub>24</sub> = 0.1010 and <var>B</var><sub>34</sub> = 0.1203 pu. The matching
conductances are <var>G</var><sub>12</sub> = 0.0465, <var>G</var><sub>13</sub> = 0.0553,
<var>G</var><sub>14</sub> = 0.0278, <var>G</var><sub>23</sub> = 0.0366,
<var>G</var><sub>24</sub> = 0.0184 and <var>G</var><sub>34</sub> = 0.0219 pu. The
diagonal of <strong>Y</strong><sub>red</sub> also carries a conductance at each internal
node: <var>G</var><sub>11</sub> = 0.0703, <var>G</var><sub>22</sub> = 0.0307,
<var>G</var><sub>33</sub> = 0.0436 and <var>G</var><sub>44</sub> = 0.0110 pu. The
diagonal susceptances <var>B</var><sub><var>ii</var></sub> do not enter (4.2), because
sin(δ<sub><var>i</var></sub> − δ<sub><var>i</var></sub>) = 0.</p>

<p>The conductances are not numerical noise. They are the load, redistributed onto every
branch and every node of the reduced mesh. In (4.2) the <var>j</var> = <var>i</var> term
is <var>E</var><sub><var>i</var></sub>²<var>G</var><sub><var>ii</var></sub>. For unit 1 it
is 1.0716² × 0.0703 = 0.0807 pu, which is 27 % of that unit's dispatch. Substituting all
sixteen entries into (4.2) returns
<var>P</var><sub>e,1</sub> = 0.3000, <var>P</var><sub>e,2</sub> = 0.1800,
<var>P</var><sub>e,3</sub> = 0.1000 and <var>P</var><sub>e,4</sub> = 0.0500 pu, which are
the four dispatches. With the diagonal terms left out, the same sum returns 0.2193,
0.1448, 0.0537 and 0.0383 pu. Run both sums; the difference is the load. The reduction is
therefore exact to the digits printed here.</p>
```

**Replace in the caption, lines 536-538,** "it turns the real power of the load into the six conductances <var>G</var><sub><var>ij</var></sub>." with: "it turns the real power of the load into the six transfer conductances <var>G</var><sub><var>ij</var></sub> and the four self-conductances <var>G</var><sub><var>ii</var></sub> listed in §4.1.3."

### B3 — Model 4.2 says "proved here" and shows no derivation (ch4.html:333-356)

**Quoted.** "Model 4.2 — Reduced multi-unit power injection [proved here] ... Write Y_red,ij = G_ij + jB_ij and hold each internal voltage magnitude E_i constant. The active power leaving internal node i is (4.2)."

**Defect.** Part 3 of the standard. The status label promises a proof; none is present. The derivation is three lines. A reader new to the field needs them, because the sign of the B_ij sin term depends on the convention Y_ij = −y_ij of Definition 4.1. The same reader will read B_12 = 0.2555 as a branch susceptance and get its sign wrong.

**Insert after line 346 (the `(4.2)` equation div) and before line 347 (`<p><strong>Assumptions.`):**

```html
<div class="proof">
<p class="proof-h">Derivation.</p>
<p>Row <var>i</var> of (4.1) gives the current leaving internal node <var>i</var>:
<var>I</var><sub><var>i</var></sub> = Σ<sub><var>j</var></sub>
<strong>Y</strong><sub>red,<var>ij</var></sub> <var>E</var><sub><var>j</var></sub>
e<sup>jδ<sub><var>j</var></sub></sup>. Here j outside a subscript is the imaginary unit
and <var>j</var> inside a subscript is a node index. The complex power leaving the node
is <var>S</var><sub><var>i</var></sub> = <var>E</var><sub><var>i</var></sub>
e<sup>jδ<sub><var>i</var></sub></sup> conj(<var>I</var><sub><var>i</var></sub>). Substitute
<strong>Y</strong><sub>red,<var>ij</var></sub> = <var>G</var><sub><var>ij</var></sub> +
j<var>B</var><sub><var>ij</var></sub>:</p>
<p><var>S</var><sub><var>i</var></sub> = Σ<sub><var>j</var></sub>
<var>E</var><sub><var>i</var></sub><var>E</var><sub><var>j</var></sub>
(<var>G</var><sub><var>ij</var></sub> − j<var>B</var><sub><var>ij</var></sub>)
e<sup>j(δ<sub><var>i</var></sub> − δ<sub><var>j</var></sub>)</sup>.</p>
<p>Write the exponential as cos(δ<sub><var>i</var></sub> − δ<sub><var>j</var></sub>) +
j sin(δ<sub><var>i</var></sub> − δ<sub><var>j</var></sub>) and take the real part. The
product (<var>G</var> − j<var>B</var>)(cos + j sin) has real part
<var>G</var> cos + <var>B</var> sin, because (−j)(j) = +1. That is (4.2). The imaginary
part, <var>G</var> sin − <var>B</var> cos, is the reactive power
<var>Q</var><sub><var>i</var></sub>, which this chapter does not use. ∎</p>
<p><strong>Sign of <var>B</var><sub><var>ij</var></sub>.</strong>
<var>B</var><sub><var>ij</var></sub> is an element of <strong>Y</strong><sub>red</sub>,
not the susceptance of a physical branch. For a lossless branch of reactance
<var>X</var> between nodes <var>i</var> and <var>j</var>, the branch admittance is
−j/<var>X</var>, and by Definition 4.1 the matrix element is
<strong>Y</strong><sub><var>ij</var></sub> = +j/<var>X</var>. So
<var>B</var><sub><var>ij</var></sub> = +1/<var>X</var>, and the values printed in §4.1.3
are positive for that reason.</p>
</div>
```

### B4 — Theorem 4.5 leaves three things unstated (ch4.html:847-883)

**Quoted.** "Let a system of n units obey (4.3), with system stored energy E_kin_sys from (4.4) in MJ. At t = 0 an infeed of ΔP MW is lost as a step. Assume no load damping, no primary response inside the first instant, and no change in any angle at t = 0+." Proof: "By (4.5), the left side is 2E_kin_sys dΔω_COI/dt. ... the remaining units' electrical outputs rise at once to cover the lost infeed ..."

**Defect.** Part 1 (precise statement) and part 2 (every term defined). (i) The theorem does not say whether E_kin_sys counts the unit that trips. It must not; Example 4.1 uses the post-loss value without saying so. (ii) Δω_COI is used in the proof and defined nowhere; the notation table defines ω_COI only. (iii) "Electrical outputs rise at once to cover the lost infeed" is an assumption about the load, not a consequence of the algebraic network. A constant-impedance load changes power when the bus voltages move at the trip. Part 4 (where hypotheses bind) is also absent.

**Replace lines 847-883 with:**

```html
<div class="thm" id="thm-4-5" data-rid="R35">
<span class="rhead">Theorem 4.5 — Initial rate of change of frequency
<span class="status">proved here</span><span class="rid">R35</span></span>
<p>Let <var>n</var> units obey (4.3) and stay connected through a disturbance. Let
<var>E</var><sub>kin,sys</sub> be their stored energy from (4.4), in MJ, counting those
<var>n</var> units only and not any unit that trips. At <var>t</var> = 0 an infeed of
Δ<var>P</var> MW is lost as a step. Assume:</p>
<ol>
<li>no load damping and no primary response inside the first instant, so every
<var>P</var><sub>m,<var>i</var></sub> is unchanged at <var>t</var> = 0<sup>+</sup>;</li>
<li>no angle δ<sub><var>i</var></sub> changes at <var>t</var> = 0<sup>+</sup>;</li>
<li>the total electrical load is unchanged at <var>t</var> = 0<sup>+</sup>, so the
<var>n</var> units together supply the whole pre-event load.</li>
</ol>
<p>Let Δω<sub>COI</sub> = (ω<sub>COI</sub> − ω<sub>0</sub>)/ω<sub>0</sub> be the
centre-of-inertia speed deviation declared in the §4.2 local notation panel. By (4.5) it
equals Σ<sub><var>i</var></sub> <var>H</var><sub><var>i</var></sub><var>S</var><sub><var>i</var></sub>
Δω<sub><var>i</var></sub> / <var>E</var><sub>kin,sys</sub>. Then the centre-of-inertia
frequency falls at</p>
<div class="eq"><div class="body">
RoCoF<sub>0</sub> = −
<span class="frac"><span class="n"><var>f</var><sub>0</sub> Δ<var>P</var></span><span class="d">2 <var>E</var><sub>kin,sys</sub></span></span>
&nbsp;Hz/s
</div><div class="num">(4.8)</div></div>
<p>The chapter quotes the magnitude
<var>f</var><sub>0</sub>Δ<var>P</var>/(2<var>E</var><sub>kin,sys</sub>) when the direction is
clear from the sentence.</p>
<div class="proof">
<p class="proof-h">Proof.</p>
<p>Multiply each unit's speed equation in (4.3) by <var>S</var><sub>sys</sub> and sum over
the <var>n</var> connected units:</p>
<p>Σ<sub><var>i</var></sub> 2<var>H</var><sub><var>i</var></sub><var>S</var><sub><var>i</var></sub>
dΔω<sub><var>i</var></sub>/d<var>t</var> = Σ<sub><var>i</var></sub>
(<var>P</var><sub>m,<var>i</var></sub> − <var>P</var><sub>e,<var>i</var></sub>)<var>S</var><sub>sys</sub>
− Σ<sub><var>i</var></sub> <var>K</var><sub>D,<var>i</var></sub><var>S</var><sub><var>i</var></sub>
Δω<sub><var>i</var></sub>.</p>
<p>At <var>t</var> = 0<sup>+</sup> every Δω<sub><var>i</var></sub> is still zero, so the
damping sum is zero. By the definition of Δω<sub>COI</sub>, the left side is
2<var>E</var><sub>kin,sys</sub> dΔω<sub>COI</sub>/d<var>t</var>. On the right, assumption 1
holds every <var>P</var><sub>m,<var>i</var></sub> at its pre-event value, so
Σ<sub><var>i</var></sub> <var>P</var><sub>m,<var>i</var></sub><var>S</var><sub>sys</sub> is
the pre-event output of the <var>n</var> units. That output is the pre-event load minus
Δ<var>P</var>, because the lost infeed supplied Δ<var>P</var> of that load. By assumption
3 and the algebraic network of Model 4.2, the <var>n</var> units' electrical outputs sum
to the whole pre-event load at <var>t</var> = 0<sup>+</sup>. The sum of mechanical
minus electrical power is therefore −Δ<var>P</var> in MW. Hence</p>
<p>2<var>E</var><sub>kin,sys</sub> dΔω<sub>COI</sub>/d<var>t</var> = −Δ<var>P</var>.</p>
<p>Frequency in hertz is <var>f</var> = <var>f</var><sub>0</sub>(1 + Δω<sub>COI</sub>), so
d<var>f</var>/d<var>t</var> = <var>f</var><sub>0</sub> dΔω<sub>COI</sub>/d<var>t</var>.
Substituting gives (4.8). ∎</p>
</div>
<p><strong>Where the hypotheses bind.</strong> Assumption 3 is not exact for the
constant-impedance load of Model 4.2. The bus voltages move at the instant of the trip,
and the load power moves with them to first order in the voltage change. This theorem
neglects that change. Assumption 2 fails after the first swing, which is why (4.8) is an
initial rate and not a trajectory; Theorem 4.6 supplies the trajectory. If the tripped
unit's stored energy is counted in <var>E</var><sub>kin,sys</sub> by mistake, (4.8)
understates the rate by the ratio of the two energies.</p>
</div>
```

**Also, in the §4.2 local notation panel, insert after line 565** (the ΔΔω bullet), because the chapter's own rule at lines 185-186 declares a new symbol only in a panel:

```html
<li>Δω<sub>COI</sub> — centre-of-inertia speed deviation,
(ω<sub>COI</sub> − ω<sub>0</sub>)/ω<sub>0</sub>, dimensionless. By (4.5) it equals
Σ<sub><var>i</var></sub> <var>H</var><sub><var>i</var></sub><var>S</var><sub><var>i</var></sub>
Δω<sub><var>i</var></sub> / <var>E</var><sub>kin,sys</sub>. Used in Theorem 4.5.</li>
```

**Also, in Example 4.1 line 1034**, after "E_kin,sys = 200 GVA·s = 200 000 MJ." add: "This is the stored energy of the units that stay connected after the loss, as Theorem 4.5 requires."

### B5 — Nine terms of art are used and never defined (first uses: ch4.html:129, 201, 843, 910, 923, 954, 1002, 1072, 1155)

**Quoted.** "synchronous condensers" (129), "loss of infeed" (201, 842), "governor" (843), "loss-of-mains protection" (910), "island" (923), "Primary response" (954), "deadband" (1002), "low-frequency demand disconnection" (1072), "embedded generation" (1155). Also "headroom" (150) is used before P_headroom is declared at 1141.

**Defect.** Part 2 of the standard. The plan's reader "is assumed to know nothing about power systems: not per unit, not the dq frame, not synchronous machines, not grid codes." Plan §4 lists synchronous condenser, headroom, primary response and low-frequency demand disconnection under "Definitions introduced" for this chapter. None of the nine is defined in chapters 1 to 3 either. A grep of `ch1.html`, `ch2.html` and `ch3.html` returns zero hits for all nine; "headroom" appears once in ch2 as a phrase.

**Insert after line 225 (the closing `</div>` of the chapter-notation table) and before the `<!-- 4.1 -->` comment:**

```html
<h3>Terms used in this chapter</h3>

<div class="localnot">
<strong>Terms of art.</strong> Each term below is used in this chapter and is defined
nowhere else in the book. Each definition names where the chapter uses it.
<ul>
<li><strong>Synchronous condenser</strong> — a synchronous machine with no turbine and
no mechanical load on its shaft. It runs connected to the grid and supplies reactive
power, short-circuit current and the inertia of its rotor. On average it generates no
active power; it draws a small amount to cover its losses. A <strong>flywheel</strong>
is a mass added to the shaft to raise <var>H</var>. Used in Example 4.2.</li>
<li><strong>Infeed</strong> — active power injected into the system by a generating unit
or an import link. A <strong>loss of infeed</strong> is the sudden disconnection of that
injection; Δ<var>P</var> is its size in MW. Used in Theorems 4.5 and 4.6.</li>
<li><strong>Governor</strong> — the controller on a machine that changes mechanical power
in response to a measured frequency deviation. A <strong>deadband</strong> is the band of
frequency deviation around <var>f</var><sub>0</sub> inside which the governor does not
act. Used in §4.3 and §4.4.1.</li>
<li><strong>Primary response</strong> — the active-power increase that governors, and
equivalent converter controls, deliver in response to a frequency fall within seconds and
without an operator instruction. <var>R</var><sub>p</sub> is its volume in
MW and <var>T</var> the time by which it is fully delivered. On a grid-forming converter
the droop law of R25 produces it. Used in Theorem 4.6.</li>
<li><strong>Headroom</strong> — the active power a unit or a fleet can add above its
present dispatch, in MW or in per unit of rating. For a converter it is bounded by
<var>I</var><sub>max</sub> (R33). Used in Example 4.2 as
<var>P</var><sub>headroom</sub>.</li>
<li><strong>Low-frequency demand disconnection</strong> — a relay scheme that
disconnects blocks of demand automatically when the frequency falls to preset levels,
to stop the fall. In Great Britain it acted at 48.8 Hz on 9 August 2019
<span class="cite">[S14, National Grid ESO 2019, <em>Technical Report on the events of
9 August 2019</em>, event summary — verify]</span>. Used in Example 4.1 and
Citation 4.7.</li>
<li><strong>Embedded generation</strong> — generation connected to the distribution
network rather than to the transmission network. The system operator does not measure
its output directly, and it carries its own protection. Used in Citation 4.7.</li>
<li><strong>Loss-of-mains protection</strong> — protection on embedded generation that
disconnects the unit when it detects that its part of the network has separated from
the main system. That separated state is called <strong>islanding</strong>. One
detection method measures RoCoF and trips above a threshold. A system-wide frequency
fall can exceed the same threshold, so the relay cannot tell islanding from a system
event. Used in §4.3 and Exercise 4.1.</li>
</ul>
</div>
```

### B6 — Example 4.1 and Fig. 4.3 cite Citation 4.7 before it exists (ch4.html:1072-1073, 1124-1125)

**Quoted.** "the 48.8 Hz at which Great Britain's low-frequency demand disconnection acted in 2019 (Citation 4.7)" and "The dashed orange line is the 48.8 Hz setting of Citation 4.7." Citation 4.7 is at line 1149, in §4.5.

**Defect.** A forward reference. The plan's dependency graph has R37 depending on R36 only; the draft made R37 lean on R38, which comes later. Primary fix (no renumbering): give the number its own four-part citation at the point of use and say that §4.5 restates it. Alternative fix, in three steps:
1. Move the Citation 4.7 block (lines 1149-1163) to a new §4.4.3 "The reference event", before Example 4.1.
2. Renumber "4.4.3 Worked case" to 4.4.4.
3. Leave one pointer sentence in §4.5.

Use the primary fix unless the fix stage prefers the cleaner structure.

**Replace lines 1070-1074 with:**

```html
<p><strong>Reading.</strong> Both quantities scale as 1/<var>E</var><sub>kin,sys</sub>, so
halving stored energy doubles the initial rate and doubles the depth. The halved-inertia
nadir of 48.750 Hz sits 0.050 Hz below 48.8 Hz. That is the frequency at which Great
Britain's low-frequency demand disconnection acted on 9 August 2019
<span class="cite">[S14, National Grid ESO 2019, <em>Technical Report on the events of
9 August 2019</em>, event summary — verify]</span>. §4.5 restates it with the event's
two other figures as Citation 4.7. That is a scale check, not a claim about the event,
which had a different loss, system and response.</p>
```

**Replace in the caption, lines 1124-1125,** "The dashed orange line is the 48.8 Hz setting of Citation 4.7." with: "The dashed orange line is 48.8 Hz. That is the frequency at which Great Britain's low-frequency demand disconnection acted in 2019 [S14, National Grid ESO 2019, <em>Technical Report on the events of 9 August 2019</em>, event summary — verify]. §4.5 restates it as Citation 4.7."

### B7 — The Great Britain 1 Hz/s figure is attributed to an Irish source (ch4.html:909-913, 1215-1218; also 1462-1463)

**Quoted.** "The 1 Hz/s figure is the one used in Ireland under the DS3 programme and in Great Britain loss-of-mains protection policy [S16, EirGrid and SONI, DS3 programme documentation, ... — verify]" and "It is the figure used in Ireland under DS3 and in Great Britain loss-of-mains policy [S16 ...]".

**Defect.** Wrong source for a number (check d). S16 is EirGrid and SONI documentation. EirGrid operates Ireland and SONI operates Northern Ireland; both are on the all-island synchronous system, not on the Great Britain system. A DS3 document cannot be the source for a Great Britain protection setting. The plan's own standing warning (§5.2) makes the same attribution, so the draft followed the plan; the plan is wrong here (S5). The source list S01 to S20 has no entry for Great Britain loss-of-mains policy (S17 is the grid-forming specification GC0137, a different document). Plan §5.4: a number no source supports does not go in the book.

**Replace lines 909-913 with:**

```html
<li>The <strong>1 Hz/s</strong> figure is the rate-of-change-of-frequency standard adopted
in Ireland under the DS3 programme
<span class="cite">[S16, EirGrid and SONI, DS3 programme documentation,
rate-of-change-of-frequency standard — verify, including which document and which
year]</span>. It is a system operating limit and a relay setting. This book's source
list has no entry for the corresponding Great Britain loss-of-mains setting, so no Great
Britain value is printed here.</li>
```

**Replace lines 1215-1218 (first two sentences of the paragraph) with:**

```html
<p>The 1 Hz/s here is a design input of this case. It is the figure adopted in Ireland
under DS3
<span class="cite">[S16, EirGrid and SONI, DS3 programme documentation,
rate-of-change-of-frequency standard — verify]</span>. It is <em>not</em> the ENTSO-E withstand
```

(the rest of the paragraph, from "figure, which is reported as 2 Hz/s over 500 ms", stays as drafted).

**Exercise 4.1 answer, lines 1462-1463:** "The same quantity is the input to loss-of-mains protection on embedded generation" makes no numerical claim and needs no change.

### B8 — The opening sentence is wrong about the object of the chapter (ch4.html:129-134)

**Quoted.** "A system operator has eight synchronous condensers. They do no useful work. They spin, they store kinetic energy, and they release it when the frequency falls."

**Defect.** Part 1 of the standard: a wrong statement. A synchronous condenser exists to supply reactive power and short-circuit current. The chapter itself says so in §4.5 Constraint 3, lines 1246-1247: "There is no current for voltage support at the same instant, no current for a fault contribution". A reader who takes the opening at face value learns that the condensers are idle masses, and then cannot see why Constraint 3 matters. The sentence also uses "synchronous condenser" before any definition.

**Replace lines 129-134 with:**

```html
<p class="lead">A system operator has eight synchronous condensers. A synchronous
condenser is a synchronous machine with no turbine and no load on its shaft. It supplies
reactive power, short-circuit current and inertia; on average it generates no active
power. The operator must decide whether grid-forming converters can replace the inertia
of those eight machines, and how much converter plant to buy. That decision needs a
number, and the number is not "1.6 GW of grid-forming plant". It is three numbers, in
three different units, and only one of them binds. Reactive power and short-circuit
current are two further services the condensers supply. This chapter sizes the inertia
replacement only; §4.5 Constraint 3 shows why the other two cannot be ignored at the same
instant.</p>
```

---

## 2. Line-level rewrites

### L1 — Rhetorical antithesis (ch4.html:1061-1062)
Quoted: "The system does not run out of energy. It runs out of time."
Rewrite: "The released energy is 2.5 % of the store. The depth of the nadir is set by the 10 s delivery time <var>T</var> in (4.10), not by the size of the store."

### L2 — "often called conservative" has no source (ch4.html:993-994)
Quoted: "Equation (4.10) is often called conservative. That word hides the mechanism, and two of its assumptions push in opposite directions."
Rewrite: "A reader may meet the claim that (4.10) is conservative, that is, that it overstates the depth. The formula alone does not support that claim. Two of its assumptions push in opposite directions."

### L3 — Unsourced time figure (ch4.html:892-897)
Quoted: "so a local measurement can read a higher rate for the first few hundred milliseconds."
Rewrite the paragraph: "<strong>Two.</strong> RoCoF<sub>0</sub> is a centre-of-inertia quantity. Equation (4.8) is exact for ω<sub>COI</sub> and not for any single bus. Immediately after the loss, the units electrically closest to the lost infeed supply most of the missing power and slow fastest. A local measurement can therefore read a rate higher than (4.8) until the angles have redistributed the deficit. A relay measures a bus, not the centre of inertia, so the planner's number and the relay's number differ." Delete the quantity; do not add a source from memory.

### L4 — "several times rated current" has no source (ch4.html:1396-1397)
Quoted: "Machines supply several times rated current into a fault; a converter supplies a current close to I_max."
Rewrite: "A synchronous machine delivers 5 to 7 times rated current into a close fault, set by its subtransient reactance <span class="cite">[S01, Kundur 1994, <em>Power System Stability and Control</em>, Ch. 3 — verify]</span>. Chapter 2 prints the same figure beside equation (2.7). A converter supplies a current close to <var>I</var><sub>max</sub>, which is 1.2 pu in Example 4.2." The citation is copied from `ch2.html:279`, not supplied from memory.

### L5 — Impression instead of number (ch4.html:1204-1205)
Quoted: "It is short of binding by four orders of magnitude."
Rewrite: "It is short of binding by a factor of 22 500, that is 10<sup>4.35</sup>."

### L6 — "worth naming" (ch4.html:748)
Quoted: "There is a third mode worth naming."
Rewrite: "A third mode changes the reading."

### L7 — "worth stating, one worth refusing" (ch4.html:1315)
Quoted: "Two comparisons are worth stating, one worth refusing."
Rewrite: "This section makes two comparisons and refuses a third."

### L8 — Cite the result that proves the bounds, and bridge H_v to H_eq (ch4.html:1195-1199, 1223-1225, 1232-1237)
(a) Quoted (1195): "Equation (4.11) is the linearisation of the exact expression ..." Prepend: "Equation (4.11) is the fleet form of the energy bound (3.30) of R33 (Corollary 3.8), with <var>E</var><sub>kin,fleet</sub> in place of <var>H</var><sub>eq</sub><var>S</var><sub>base</sub>."
(b) Quoted (1223-1225): "By R28 and R32, a converter with virtual inertia constant H_v delivers, in per unit of its own rating,"
Rewrite: "By R33 (Corollary 3.8, inequality (3.31)), a converter with equivalent inertia constant <var>H</var><sub>eq</sub> delivers, in per unit of its own rating, 2<var>H</var><sub>eq</sub> RoCoF/<var>f</var><sub>0</sub>. For a virtual synchronous machine, R32 gives <var>H</var><sub>eq</sub> = <var>H</var><sub>v</sub>, the chosen virtual inertia constant of R28. So" (Chapter 3 states this in Table 3.1, `ch3.html:1270`: "Virtual synchronous machine — H_v — K_D,v — (3.12), by construction".)
(c) Quoted (1232-1234): "1120 MVA at H_v = 5.0 s carries 1120 × 5.0 = 5600 MVA·s of equivalent stored energy, which is exactly E_kin,fleet."
Rewrite: "1120 MVA at <var>H</var><sub>eq</sub> = <var>H</var><sub>v</sub> = 5.0 s carries <var>H</var><sub>eq</sub><var>S</var><sub>gfm</sub> = 1120 × 5.0 = 5600 MVA·s of equivalent stored energy, which is exactly <var>E</var><sub>kin,fleet</sub>. Plan rule §3.6 item 4 keeps <var>H</var>, <var>H</var><sub>v</sub> and <var>H</var><sub>eq</sub> apart. The equality <var>H</var><sub>eq</sub> = <var>H</var><sub>v</sub> is a result of R32 for this family, not an identification."

### L9 — Unsourced frequency figure (ch4.html:1442-1443)
Quoted: "Fig. 4.2 could not show a converter-driven oscillation at 300 Hz, because the model has no state that could carry one."
Rewrite: "Fig. 4.2 could not show a converter-driven oscillation set by the current controller and the filter, because the model has no state that could carry one."

### L10 — Unit cell mixes magnitudes (ch4.html:198)
Quoted: "MJ (GVA·s)"
Rewrite: "MJ; 1 GVA·s = 1000 MJ"

### L11 — Two symbols for one quantity (ch4.html:246-247)
Quoted: "P_i, Q_i — active and reactive power injected by unit i at its point of connection."
Rewrite: "<var>P</var><sub><var>i</var></sub>, <var>Q</var><sub><var>i</var></sub> — active and reactive power injected by unit <var>i</var> at its internal node, at the equilibrium. <var>P</var><sub>e,<var>i</var></sub> and <var>P</var><sub>m,<var>i</var></sub> — electrical output and mechanical or commanded input of unit <var>i</var> in (4.3), on the system base; at the equilibrium <var>P</var><sub>e,<var>i</var></sub> = <var>P</var><sub>m,<var>i</var></sub> = <var>P</var><sub><var>i</var></sub>."

### L12 — Three symbols used without declaration (ch4.html:239-241, 422, 581, 642)
Add three bullets to the §4.1 local notation panel, after line 241:
"<li><var>K</var><sub>D,<var>i</var></sub> — damping coefficient of unit <var>i</var>, in per unit on its own base.</li>
<li><var>I</var><sub><var>i</var></sub> — current phasor injected by unit <var>i</var> at its internal node, in per unit on <var>S</var><sub>sys</sub>.</li>
<li>δ<sub><var>i</var>,0</sub> — equilibrium value of δ<sub><var>i</var></sub>.</li>"

### L13 — B not written; participation factors not normalised (ch4.html:654-664)
Quoted: "The input u holds the mechanical or commanded power deviations; ... The participation factor p_ki = |v_ki w_ik|, built from the right and left eigenvectors of A, ..."
Rewrite: "The input <strong>u</strong> = [Δ<var>P</var><sub>m,1</sub> … Δ<var>P</var><sub>m,<var>n</var></sub>]<sup>T</sup> holds the mechanical or commanded power deviations on the system base, and <strong>B</strong> = [<strong>0</strong> ; <strong>M</strong><sup>−1</sup>]. The output <strong>y</strong> = <strong>C x</strong> + <strong>D u</strong> selects whatever is measured; for frequency work <strong>C</strong> picks the speed states and <strong>D</strong> = <strong>0</strong>. Eigenvalues λ<sub><var>i</var></sub> = σ<sub><var>i</var></sub> + jω<sub>d,<var>i</var></sub> of <strong>A</strong> give the modes. The damping ratio is ζ<sub><var>i</var></sub> = −σ<sub><var>i</var></sub> / √(σ<sub><var>i</var></sub>² + ω<sub>d,<var>i</var></sub>²). Scale the right and left eigenvectors of <strong>A</strong> so that Σ<sub><var>k</var></sub> <var>v</var><sub><var>ki</var></sub><var>w</var><sub><var>ik</var></sub> = 1 for each mode. The participation factor <var>p</var><sub><var>ki</var></sub> = |<var>v</var><sub><var>ki</var></sub><var>w</var><sub><var>ik</var></sub>| then sums to 1 over <var>k</var>, and it says how much state <var>k</var> takes part in mode <var>i</var>. That is what labels a mode "machine" or "converter"."

### L14 — Kron reduction: state the rescue for a constant-power load (ch4.html:320-323)
Quoted: "It fails for a constant-power load, and it fails for any bus with its own dynamics."
Rewrite: "It fails for a constant-power load, and it fails for any bus with its own dynamics. A constant-power load can be brought inside the condition: replace it with the constant impedance that draws the same power at the operating-point voltage. The replacement is exact at that point and approximate away from it, which is the same trade Model 4.4 makes when it linearises."

### L15 — "leaves I" is ambiguous (ch4.html:289-291)
Quoted: "so it enters Y_ii and leaves I."
Rewrite: "so it enters <strong>Y</strong><sub><var>ii</var></sub> and contributes zero to <strong>I</strong><sub>bus</sub>."

### L16 — The locus beyond 80 % is not reported, and it crosses ζ = 0.05 (ch4.html:748-754, 1541-1552, 1582-1584)
Recomputed under the rule of B1. The mode at −0.7671 + j12.9359 (ζ = 0.0592) at c = 80 % continues along its locus:

| c | mode | ζ | least-damped (machine) mode ζ |
|---|---|---|---|
| 85 % | −0.5839 + j12.7436 | 0.0458 | 0.0203 |
| 90 % | −0.4028 + j12.6077 | 0.0319 | 0.0212 |
| 95 % | −0.2581 + j12.5296 | 0.0206 | 0.0185 |

The machine mode's ζ falls back between 90 % and 95 %.
(a) Append to the paragraph at 748-754: "Beyond 80 % the same branch keeps falling: ζ = 0.0458 at 85 %, 0.0319 at 90 % and 0.0206 at 95 %. It crosses ζ = 0.05 between <var>c</var> = 80 % and 85 %. It is never the least-damped mode, because the machine mode sits below it at every step."
(b) Exercise 4.5 answer, replace "Along the way it rises: 0.0138 at 30 %, 0.0145 at 50 %, 0.0187 at 80 %, 0.0212 at 90 %." with: "Along the way it rises to 0.0138 at 30 %, 0.0145 at 50 %, 0.0187 at 80 % and 0.0212 at 90 %, then falls back to 0.0185 at 95 %. The mode that Fig. 4.2 shows losing damping does cross ζ = 0.05: it is 0.0592 at 80 %, 0.0458 at 85 %, 0.0319 at 90 % and 0.0206 at 95 %. It is never the least-damped mode, so it does not answer the question as asked. Report both."
(c) Chapter summary, line 1583-1584: "and another degraded from ζ = 0.1267 to 0.0592" → "and another degraded from ζ = 0.1267 at 20 % to 0.0592 at 80 % and 0.0206 at 95 %".

### L17 — Fig. 4.5 asserts an order the draft did not read (ch4.html:1348-1349, 1365-1371)
The figure places the embedded-generation disconnection with "loss 2". That order is a claim about the event, and the draft states it read no clock time from S14. Make the order carry `verify`; do not state what the true order was.
(a) SVG line 1348: "loss 2 + embedded" → "further loss + embedded". Add after line 1337: `<text x="40" y="186" fill="#fb923c" font-family="system-ui,sans-serif" font-size="10">order of the losses as drawn: not read from S14 — verify</text>`.
(b) Caption, replace lines 1365-1371 with: "<b>Fig. 4.5</b> — The reported sequence of the Great Britain event of 9 August 2019: a first loss, a further loss compounded by embedded generation disconnecting on its own protection, a nadir at 48.8 Hz, and low-frequency demand disconnection shedding about 931 MW at that frequency. The total infeed loss was about 1878 MW. No clock time is drawn, because none was read from the source. The order of the losses and of the embedded-generation disconnection is drawn as the draft understood it. It was not read from S14, so it carries verify like the values. The figure shows that the outcome followed from the sequence and not from any one of the three numbers. It illustrates Citation 4.7 (R38). Every value carries [S14 — verify]."

### L18 — Literal colour outside the token set (ch4.html:93)
Quoted: `th{color:var(--text);font-weight:600;background:#17233a}`
Rewrite: `th{color:var(--text);font-weight:600;background:var(--bg)}`. Plan §5.3 item 4: use the variables, not literals, below `:root`.

### L19 — Journal name does not match the source list (ch4.html:1409)
Quoted: "<em>IEEE JESTPE</em> 8(2)"
Rewrite: "<em>IEEE J. Emerging and Selected Topics in Power Electronics</em> 8(2)"

### L20 — Claim about real governors needs its source (ch4.html:1001-1004)
Quoted: "Real primary response has a deadband, a measurement delay and a governor time constant. It does not start at the instant of the loss."
Rewrite: "Real primary response has a deadband, a measurement delay and a governor time constant (Terms panel) <span class="cite">[S13, Anderson and Mirheydar 1990, "A Low-Order System Frequency Response Model", <em>IEEE Trans. Power Systems</em> 5(3), 720–729, governor model — verify]</span>. It does not start at the instant of the loss." S13 is the plan's designated source for the nadir model and its assumptions.

### L21 — Glyph note for the speed deviation (ch4.html:216)
Quoted: "δ, Δω | delta, dw | rotor or internal angle, and per-unit speed deviation"
Rewrite the meaning cell: "rotor or internal angle, and per-unit speed deviation (ω − ω<sub>0</sub>)/ω<sub>0</sub>. Chapter 1 writes the deviation Δω̄ with a bar (R02); this chapter drops the bar." See S1 for the book-level decision.

### L22 — Sentence of 40 words (ch4.html:1034-1040)
Quoted: "This figure is an input of this example, of the order reported for Great Britain in 2019 [S14 ...]. It is not a value this book has read from that report, so treat it as assumed for this case — verify the figure and its year before quoting it elsewhere."
Rewrite: "This figure is an input of this example. It is of the order reported for Great Britain in 2019 <span class="cite">[S14, National Grid ESO 2019, <em>Technical Report on the events of 9 August 2019</em>, system inertia at the time of the event — verify]</span>. This book has not read the value from that report. Treat it as <span class="verify">assumed for this case</span>, and verify the figure and its year before quoting it elsewhere."

### L23 — Sentences of 41 and 33 words (ch4.html:154-161)
Rewrite the paragraph: "The answer for the case defined in this chapter is stated here, so that the reader can check the argument against it. <strong>Power headroom binds. The current limit binds at the same instant. Stored energy is not close to binding.</strong> A 1.6 GVA condenser fleet releases 179.2 MJ over a 0.8 Hz excursion. A 1120 MVA converter fleet with a one-hour store holds 4 032 000 MJ, which is 22 500 times as much. The same fleet must hold 224 MW of power above its dispatch. A converter running at 1.0 pu with a current limit of 1.2 pu has exactly 0.20 pu of current left. Every one of those numbers is derived in Example 4.2."

### L24 — Sentence of 42 words (ch4.html:1246-1248)
Rewrite: "Nothing is left. There is no current for voltage support at the same instant and none for a fault contribution. A converter running at its limit is no longer described by the linear model of R32."

### L25 — Sentence of 84 words (ch4.html:1506-1514)
Replace the numerical-check sentence with a sentence and a table:
"Numerical check on the Example 4.1 system, by fourth-order Runge-Kutta with step 1 × 10<sup>−4</sup> s. The three <var>D</var><sub>load</sub> values test the grouping only and come from no source."

```html
<div class="tw"><table>
<thead><tr><th class="num"><var>D</var><sub>load</sub> (MW/Hz)</th><th class="num"><var>T</var>/τ</th><th class="num">nadir deviation (Hz)</th><th class="num">time of nadir (s)</th></tr></thead>
<tbody>
<tr><td class="num">0</td><td class="num">0</td><td class="num">−0.6250</td><td class="num">10.000</td></tr>
<tr><td class="num">500</td><td class="num">0.6250</td><td class="num">−0.4464</td><td class="num">7.768</td></tr>
<tr><td class="num">1000</td><td class="num">1.2500</td><td class="num">−0.3513</td><td class="num">6.487</td></tr>
<tr><td class="num">2000</td><td class="num">2.5000</td><td class="num">−0.2494</td><td class="num">5.011</td></tr>
</tbody></table></div>
```
"Against the undamped row, the nadir is both shallower and earlier, and it no longer occurs at <var>t</var> = <var>T</var>." (All four rows recomputed; see the table in §5.)

### L26 — Sentences of 64 and 58 words (ch4.html:1561-1569)
Rewrite (a) and (b): "(a) A required response duration of minutes instead of seconds. A rate-of-change-of-frequency requirement implies a few seconds. The energy term grows with duration while the headroom term does not. At a 224 MW draw the 4 032 000 MJ store lasts 4 032 000/224 = 18 000 s = 5.0 h, so the reversal needs a duration of that order or a much smaller store. (b) A converter fleet with no long-duration store, such as photovoltaic without a battery. Then <var>E</var><sub>res</sub> is whatever the DC link holds. R30 computes a DC-link store of 14.4 kJ on a 1 MVA base, that is 0.0144 MJ per MVA. The one-hour store assumed here holds 3600 MJ per MVA. The ratio is 3600/0.0144 = 250 000."

### L27 — Sentence of 54 words (ch4.html:1403-1410)
Rewrite: "The question is what a fleet of mixed droop, virtual synchronous machine, matching and dispatchable virtual oscillator plant does together under a large disturbance, when the plant comes from different vendors <span class="cite">[S12, Tayyebi, Groß, Anta, Kupzog and Dörfler 2020, "Frequency Stability of Synchronous Machines and Grid-Forming Power Converters", <em>IEEE J. Emerging and Selected Topics in Power Electronics</em> 8(2), 1004–1018, side-by-side comparison of the families — verify]</span>."

### L28 — Sentence of 40 words (ch4.html:416-421)
Rewrite as a list: "The equilibrium needs three assumptions, all choices of this case. <em>Assumed for this case:</em></p><ol><li>the load-bus voltage is <var>V</var><sub>L</sub> = 1.0∠0° pu;</li><li>each unit's reactive injection is proportional to its rating, <var>Q</var><sub><var>i</var></sub> = 120 × <var>S</var><sub><var>i</var></sub>/1000 Mvar, so the four sum to 120 Mvar;</li><li>each unit's active injection is its dispatch.</li></ol><p>With these, ..."

### L29 — Sentence of 40 words (ch4.html:1484-1487)
Rewrite: "The factor 4 is 2 × 2. One 2 is the 2 in 2<var>E</var><sub>kin,sys</sub> from the swing equation of R04. The other 2 is the ½ of the triangular area under the ramp, which appears as <var>T</var> − <var>T</var>/2 = <var>T</var>/2 in the integration."

### L30 — Caption of 52 words (ch4.html:1365-1371)
Covered by L17(b).

### L31 — "How to read" box is out of date (ch4.html:165-171)
Quoted: "Prerequisites from earlier chapters are cited by their global identifier only, because chapters 1 to 3 assign their own local numbers."
Rewrite once S2 is applied: "Prerequisites from earlier chapters are cited by their global identifier and linked to the result in the chapter that proves them."

---

## 3. Structural notes

### S1 — One symbol, two glyphs across the book
Chapter 1 writes the per-unit speed deviation Δω̄ with a bar, 34 times, and defines it there (R02, `ch1.html:250, 353`). Chapters 3 and 4 write Δω without the bar (ch3 as `&Delta;&omega;`, ch4 17 times). The plan's table calls it "dw (omega-bar deviation)". The book pass must pick one glyph. If the bar stays, chapter 4 replaces Δω with Δω̄ and ΔΔω with ΔΔω̄ at lines 216, 239-241, 563-565, 575-583, 610-616, 635-636, 867-880 and in the B4 text. L21 is the interim patch.

### S2 — Cross-chapter links are now possible
Chapters 1 to 3 exist, so plain R-numbers can become links per plan §5.1. Anchor map, verified by grep of `data-rid`:

| R-id | Link | Local number |
|---|---|---|
| R01 | `ch1.html#def-1-1` | Definition 1.1 |
| R03 | `ch1.html#def-1-3` | Definition 1.3 |
| R04 | `ch1.html#model-1-4` | Model 1.4 |
| R05 | `ch1.html#model-1-5` | Model 1.5 |
| R06 | `ch1.html#lem-1-6` | Lemma 1.6 |
| R11 | `ch1.html#rem-1-1` | Remark 1.1 |
| R24 | `ch3.html#def-3-1` | Definition 3.1 |
| R25 | `ch3.html#model-3-2` | Model 3.2 |
| R26 | `ch3.html#thm-3-3` | Theorem 3.3 |
| R28 | `ch3.html#model-3-4` | Model 3.4 |
| R30 | `ch3.html#ex-3-2` | Example 3.2 |
| R32 | `ch3.html#thm-3-7` | Theorem 3.7 |
| R33 | `ch3.html#cor-3-8` | Corollary 3.8 |

The files are named `ch1.html` to `ch4.html`, not `ch01.html` as plan §5.3 says. Use the names on disk, or rename all four and update the plan. Then apply L31.

### S3 — Theorem 4.6 needs its limit case (rescue, part 4 of the standard)
The theorem assumes R_p = ΔP. Add a remark after line 989: "<div class="rem" id="rem-4-1"><span class="rhead">Remark 4.1 — When the response does not match the loss</span><p>Keep the ramp but let <var>R</var><sub>p</sub> ≠ Δ<var>P</var>. The slope of Δ<var>f</var> is zero when <var>R</var><sub>p</sub><var>t</var>/<var>T</var> = Δ<var>P</var>. If <var>R</var><sub>p</sub> ≥ Δ<var>P</var>, the nadir is at <var>t</var>* = <var>T</var>Δ<var>P</var>/<var>R</var><sub>p</sub> ≤ <var>T</var>, with Δ<var>f</var><sub>nadir</sub> = −<var>f</var><sub>0</sub>Δ<var>P</var>²<var>T</var>/(4<var>E</var><sub>kin,sys</sub><var>R</var><sub>p</sub>). More response arrives sooner and the nadir is shallower by the factor Δ<var>P</var>/<var>R</var><sub>p</sub>. If <var>R</var><sub>p</sub> &lt; Δ<var>P</var>, the slope never reaches zero. After <var>t</var> = <var>T</var> the frequency keeps falling at the constant rate <var>f</var><sub>0</sub>(Δ<var>P</var> − <var>R</var><sub>p</sub>)/(2<var>E</var><sub>kin,sys</sub>). There is no nadir until something else acts. For Example 4.1 with <var>R</var><sub>p</sub> = 1500 MW, <var>t</var>* = 6.667 s and Δ<var>f</var><sub>nadir</sub> = −0.4167 Hz. A Runge-Kutta run returns −0.416667 Hz at 6.6667 s.</p></div>" (Both numbers recomputed; see §5.)

### S4 — Departure from the plan on "lower bound", accepted
Plan §4 asks §4.4 to "state the assumptions that make it a lower bound in practice". §4.4.1 argues instead that two assumptions push in opposite signs, so (4.10) is a screening formula and not a bound. The argument is correct and the chapter should keep it. Record the departure in the plan's Chapter 4 spec so that edit2 does not re-raise it.

### S5 — Plan-level correction: the standing warning mis-sources the Great Britain figure
Plan §5.2 "Standing warning" and the S16 row attribute "the 1 Hz/s figure used in Ireland and in Great Britain loss-of-mains protection policy" to S16 (EirGrid and SONI). B7 removes the Great Britain attribution from the chapter. If the book wants the Great Britain figure, the plan needs a new source id (S21) for the Great Britain loss-of-mains policy document. The chapter then prints the figure with that id and `verify`.

### S6 — Length: 8333 words against a 7000 target (19 % over)
Cuts that lose no content:
- The "How to read the results" box (lines 163-179) is book-wide and belongs in front matter.
- §4.6.1 (lines 1435-1450) repeats Model 4.2's omissions and Example 4.2's closing paragraph.
- Exercise answers 4.4 and 4.5 each carry a sentence of method advice that the exercise statement can hold.

Together about 600 words.

### S7 — Close with what the reader can now do
The summary (lines 1578-1594) lists the results. Add, after line 1594: "<p>The reader can now do what plan Outcome 4 asks. Given a mixed fleet, compute <var>E</var><sub>kin,sys</sub> by (4.4), the initial rate by (4.8) and the nadir by (4.10). Given a replacement decision, write it as three sizing problems in three units by the method of Example 4.2, and name the one that binds. Given an eigenvalue plot, read damping from the constant-ζ rays and label each mode by its participation factors.</p>"

### S8 — Tie TS4's converter parameters back to Chapter 3
TS4 gives the converters H_eq = 2.0 s and K_D,eq = 20 pu without saying which droop settings produce them. By R26, K_D,eq = 1/m_p = 20 gives m_p = 0.05, and H_eq = 1/(2 m_p ω_c) = 2.0 s gives ω_c = 5.0 rad/s = 0.80 Hz. Chapter 3's figure at `ch3.html:1354` prints the same pair. Add after line 396: "By R26 those two values are the droop law with <var>m</var><sub>p</sub> = 0.05 pu. The power-filter cutoff is then ω<sub>c</sub> = 1/(2<var>m</var><sub>p</sub><var>H</var><sub>eq</sub>) = 1/(2 × 0.05 × 2.0) = 5.0 rad/s, which is 0.80 Hz."

### S9 — Plan items to record, no chapter change
(a) Result class `cit` is used for R38 and R40; plan §5.3 item 5 lists no such class, plan §2 has the kind. Add `cit` to §5.3. (b) Plan §5.4 has no status word for a definition; the chapter uses "stated here". Add it to §5.4. (c) Citation locations name a topic, not a page, because no source was opened; this is the plan's own rule for the draft stage and is acceptable until a human reads the sources.

---

## 4. What already works

### W1 — The arithmetic
267 printed values recomputed independently in 187 checks. They include the Kron reduction, the 4 × 4 synchronizing matrix, and every eigenvalue and participation factor in the sweep. They also include all 88 polyline points of Fig. 4.3, all 8 squares and 6 circles of Fig. 4.2, and the three Runge-Kutta checks. Zero mismatches. The drafted claim "recomputed before printing" is true.

### W2 — Theorems 4.5 and 4.6
Both proofs are correct and narrated in prose. The factor-4 explanation at lines 982-983 names the mechanism: one 2 from the swing equation, one from the ramp triangle. That is what the standard asks for. B4 tightens the statement of 4.5; it does not change the argument.

### W3 — The three-constraint discipline in Example 4.2
Lines 1183-1185 and 1250-1253 keep megajoules, megawatts and per-unit current apart and refuse to add them. The consistency check at 1232-1237 shows that matching headroom at one RoCoF is the same as matching H × S, so the 1 Hz/s cancels. A reader will keep that.

### W4 — The mode-by-mode honesty of §4.2.4
Lines 739-754 and Fig. 4.2 report that stored energy falls 44 % while one mode's damping rises and another's falls. They state that neither "converters damp" nor "converters undamp" holds in general. Exercise 4.5 reports no crossing rather than adjusting parameters to make one. L16 extends the same honesty to 95 %.

### W5 — The standing warning is obeyed
The two RoCoF figures appear in separate list items with separate sources at lines 902-918 and again at 1215-1222. The string "ENTSO-E 1 Hz/s" appears only inside the prohibition.

### W6 — Theory against evidence
Every result carries a status word. Citation 4.7 takes three figures from the event report and refuses clock times it did not read. §4.5.1 "What is refused" (lines 1326-1329) declines to call a 0.05 Hz agreement a validation. §4.6 states six open problems as questions with sources and no dates.

### W7 — Local notation panels
Each section that needs symbols outside the book table declares them at its top (lines 230-260, 545-567, 935-945, 1133-1147). The naming decisions recorded in the draft notes (group B not L; I_n not I) avoid two real collisions.

### W8 — HTML rule
Parser check: no tag mismatch, no unclosed tag, no duplicate id. Zero `href`, zero `src`, zero `<script>`, zero `<link>`, zero `<img>`, zero `data:` URI, zero occurrences of "http". All eight dark-mode hex values are `:root` custom properties; one literal remains (L18). One `<h1>`, nine `<h2>`, thirteen `<h3>`. Ten `data-rid` containers cover R34 to R40. Thirteen numbered equations, each referenced at least once more.

---

## 5. Numbers recomputed

Each row: location in `ch4.html`, the printed value, the recomputed value, and ok or wrong. A value is ok when the recomputed value rounds to the printed digits. Source: `edit_ch4_check.py` and its `_results.json`. Counts: 181 table rows; 267 printed values, because the row `fig43_polyline_points_checked` folds the 88 y-coordinates of the four Fig. 4.3 polylines and the row below it reports their mismatch count; 187 script checks, because the six least-damped ζ values were tested under both readings of the sweep rule (B1). Wrong: 0.

| location | quantity | printed | recomputed | result |
|---|---|---|---|---|
| ch4.html:390 | omega_0 | 314.159 | 314.159 | ok |
| ch4.html:410-413, 435-438 | X_1 | 0.85 | 0.85 | ok |
| ch4.html:410-413, 435-438 | X_2 | 1.2867 | 1.28667 | ok |
| ch4.html:410-413, 435-438 | X_3 | 1.08 | 1.08 | ok |
| ch4.html:410-413, 435-438 | X_4 | 2.15 | 2.15 | ok |
| ch4.html:435-438 | E_1 | 1.0716 | 1.07158 | ok |
| ch4.html:435-438 | E_2 | 1.0716 | 1.07165 | ok |
| ch4.html:435-438 | E_3 | 1.0316 | 1.03159 | ok |
| ch4.html:435-438 | E_4 | 1.0314 | 1.03142 | ok |
| ch4.html:435-438 | delta_1_deg | 13.767 | 13.7665 | ok |
| ch4.html:435-438 | delta_2_deg | 12.481 | 12.481 | ok |
| ch4.html:435-438 | delta_3_deg | 6.009 | 6.00947 | ok |
| ch4.html:435-438 | delta_4_deg | 5.983 | 5.98255 | ok |
| ch4.html:435-438 | Q_1 | 0.048 | 0.048 | ok |
| ch4.html:435-438 | Q_2 | 0.036 | 0.036 | ok |
| ch4.html:435-438 | Q_3 | 0.024 | 0.024 | ok |
| ch4.html:435-438 | Q_4 | 0.012 | 0.012 | ok |
| ch4.html:445-447; Fig. 4.1 507-512 | B_12 | 0.2555 | 0.255459 | ok |
| ch4.html:448-450; Fig. 4.1 526-528 | G_12 | 0.0465 | 0.0464508 | ok |
| ch4.html:445-447; Fig. 4.1 507-512 | B_13 | 0.3043 | 0.304343 | ok |
| ch4.html:448-450; Fig. 4.1 526-528 | G_13 | 0.0553 | 0.0553396 | ok |
| ch4.html:445-447; Fig. 4.1 507-512 | B_14 | 0.1529 | 0.152879 | ok |
| ch4.html:448-450; Fig. 4.1 526-528 | G_14 | 0.0278 | 0.0277985 | ok |
| ch4.html:445-447; Fig. 4.1 507-512 | B_23 | 0.2011 | 0.201055 | ok |
| ch4.html:448-450; Fig. 4.1 526-528 | G_23 | 0.0366 | 0.0365585 | ok |
| ch4.html:445-447; Fig. 4.1 507-512 | B_24 | 0.101 | 0.100995 | ok |
| ch4.html:448-450; Fig. 4.1 526-528 | G_24 | 0.0184 | 0.0183643 | ok |
| ch4.html:445-447; Fig. 4.1 507-512 | B_34 | 0.1203 | 0.120322 | ok |
| ch4.html:448-450; Fig. 4.1 526-528 | G_34 | 0.0219 | 0.0218784 | ok |
| ch4.html:453-454 | Pe_1_from_4.2 | 0.3 | 0.3 | ok |
| ch4.html:453-454 | Pe_2_from_4.2 | 0.18 | 0.18 | ok |
| ch4.html:453-454 | Pe_3_from_4.2 | 0.1 | 0.1 | ok |
| ch4.html:453-454 | Pe_4_from_4.2 | 0.05 | 0.05 | ok |
| ch4.html:688-691 | K_11 | 0.7804 | 0.780434 | ok |
| ch4.html:688-691 | K_12 | -0.2921 | -0.292087 | ok |
| ch4.html:688-691 | K_13 | -0.3251 | -0.325095 | ok |
| ch4.html:688-691 | K_14 | -0.1633 | -0.163251 | ok |
| ch4.html:688-691 | K_21 | -0.2945 | -0.294481 | ok |
| ch4.html:688-691 | K_22 | 0.6194 | 0.619392 | ok |
| ch4.html:688-691 | K_23 | -0.2163 | -0.216295 | ok |
| ch4.html:688-691 | K_24 | -0.1086 | -0.108617 | ok |
| ch4.html:688-691 | K_31 | -0.3416 | -0.341609 | ok |
| ch4.html:688-691 | K_32 | -0.2254 | -0.225405 | ok |
| ch4.html:688-691 | K_33 | 0.695 | 0.695025 | ok |
| ch4.html:688-691 | K_34 | -0.128 | -0.128011 | ok |
| ch4.html:688-691 | K_41 | -0.1716 | -0.171574 | ok |
| ch4.html:688-691 | K_42 | -0.1132 | -0.113212 | ok |
| ch4.html:688-691 | K_43 | -0.128 | -0.128033 | ok |
| ch4.html:688-691 | K_44 | 0.4128 | 0.412818 | ok |
| ch4.html:400-401 | E_kin_sys_base | 3100 | 3100 | ok |
| ch4.html:402 | H_sys_base | 3.1 | 3.1 | ok |
| ch4.html:589 | unit1_H_sysbase | 1.6 | 1.6 | ok |
| ch4.html:590 | unit1_KD_sysbase | 0.8 | 0.8 | ok |
| ch4.html:592 | factor_2.5 | 2.5 | 2.5 | ok |
| ch4.html:392 | YL_re | 0.63 | 0.63 | ok |
| ch4.html:392 | YL_im | -0.12 | -0.12 | ok |
| ch4.html:729-734; 817 (SVG strip) | Ekin_c0 | 3571.4 | 3571.43 | ok |
| ch4.html:729-734; 817 (SVG strip) | Ekin_c20 | 3257.1 | 3257.14 | ok |
| ch4.html:729-734; 817 (SVG strip) | Ekin_c40 | 2942.9 | 2942.86 | ok |
| ch4.html:729-734; 817 (SVG strip) | Ekin_c60 | 2628.6 | 2628.57 | ok |
| ch4.html:729-734; 817 (SVG strip) | Ekin_c80 | 2314.3 | 2314.29 | ok |
| ch4.html:729-734; 817 (SVG strip) | Ekin_c100 | 2000 | 2000 | ok |
| ch4.html:729-734 | zeta_min_c0 | 0.0134 | 0.0134196 | ok |
| ch4.html:729-734 | zeta_min_c20 | 0.0136 | 0.0136287 | ok |
| ch4.html:729-734 | zeta_min_c40 | 0.0141 | 0.0140931 | ok |
| ch4.html:729-734 | zeta_min_c60 | 0.0152 | 0.015207 | ok |
| ch4.html:729-734 | zeta_min_c80 | 0.0187 | 0.0186723 | ok |
| ch4.html:729-734 | zeta_min_c100 | 0.1393 | 0.139277 | ok |
| ch4.html:749; Fig. 4.2 caption 827 | mode20_re | -2.2151 | -2.21511 | ok |
| ch4.html:749; Fig. 4.2 caption 827 | mode20_im | 17.3463 | 17.3463 | ok |
| ch4.html:749; Fig. 4.2 caption 827 | mode20_zeta | 0.1267 | 0.126671 | ok |
| ch4.html:751; Fig. 4.2 caption 827 | mode80_re | -0.7671 | -0.767132 | ok |
| ch4.html:751; Fig. 4.2 caption 827 | mode80_im | 12.9359 | 12.9359 | ok |
| ch4.html:751; Fig. 4.2 caption 827 | mode80_zeta | 0.0592 | 0.0591986 | ok |
| ch4.html:752 | damping_ratio_factor | 2.1 | 2.13976 | ok |
| ch4.html:1543-1545 | ex45_zeta_c30 | 0.0138 | 0.013815 | ok |
| ch4.html:1543-1545 | ex45_zeta_c50 | 0.0145 | 0.0145197 | ok |
| ch4.html:1543-1545 | ex45_zeta_c90 | 0.0212 | 0.0212387 | ok |
| ch4.html:1543-1545 | ex45_zeta_c95 | 0.0185 | 0.0185422 | ok |
| ch4.html:740 | Ekin_fall_pct | 44 | 43.9996 | ok |
| ch4.html:718 | Ekin_formula_slope | 1571.4 | 1571.43 | ok |
| ch4.html:715-718 | Ekin_formula_intercept | 3571.4 | 3571.43 | ok |
| ch4.html:794 (SVG) | fig42_m20_x | 191.1 | 191.108 | ok |
| ch4.html:794 (SVG) | fig42_m20_y | 93.9 | 93.9691 | ok |
| ch4.html:790 (SVG) | fig42_m80_x | 414.5 | 414.532 | ok |
| ch4.html:790 (SVG) | fig42_m80_y | 159.04 | 159.066 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c0_x | 509.44 | 509.482 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c0_y | 183.07 | 183.088 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c20_x | 508.77 | 508.806 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c20_y | 180.88 | 180.906 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c40_x | 507.62 | 507.658 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c40_y | 178.66 | 178.683 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c60_x | 505.28 | 505.317 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c60_y | 176.49 | 176.51 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c80_x | 498.68 | 498.718 | ok |
| ch4.html:785-789 (SVG) | fig42_machine_c80_y | 174.9 | 174.92 | ok |
| ch4.html:794-801 (SVG) | fig42_square_186.6_89.4_x | 191.1 | 191.108 | ok |
| ch4.html:794-801 (SVG) | fig42_square_186.6_89.4_y | 93.9 | 93.9691 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.6_59.0_x | 147.1 | 147.151 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.6_59.0_y | 63.5 | 63.4957 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.7_65.6_x | 147.2 | 147.152 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.7_65.6_y | 70.1 | 70.1594 | ok |
| ch4.html:794-801 (SVG) | fig42_square_242.5_117.2_x | 247 | 246.998 | ok |
| ch4.html:794-801 (SVG) | fig42_square_242.5_117.2_y | 121.7 | 121.72 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.7_71.8_x | 147.2 | 147.153 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.7_71.8_y | 76.3 | 76.3743 | ok |
| ch4.html:794-801 (SVG) | fig42_square_314.7_138.6_x | 319.2 | 319.245 | ok |
| ch4.html:794-801 (SVG) | fig42_square_314.7_138.6_y | 143.1 | 143.097 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.6_77.7_x | 147.1 | 147.152 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.6_77.7_y | 82.2 | 82.1885 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.6_83.1_x | 147.1 | 147.15 | ok |
| ch4.html:794-801 (SVG) | fig42_square_142.6_83.1_y | 87.6 | 87.6435 | ok |
| ch4.html:779-782 (SVG) | fig42_ray_zeta_0.05 | 0.05 | 0.0500034 | ok |
| ch4.html:779-782 (SVG) | fig42_ray_zeta_0.1 | 0.1 | 0.0999926 | ok |
| ch4.html:926 | rocof_TS4_base_100MW | 0.8065 | 0.806452 | ok |
| ch4.html:928 | rocof_TS4_c100_100MW | 1.25 | 1.25 | ok |
| ch4.html:929 | rocof_ratio_1.55 | 1.55 | 1.55 | ok |
| ch4.html:1045-1052 | ex41_rocof | 0.125 | 0.125 | ok |
| ch4.html:1045-1052 | ex41_dfnadir | -0.625 | -0.625 | ok |
| ch4.html:1045-1052 | ex41_fnadir | 49.375 | 49.375 | ok |
| ch4.html:1059-1061 | ex41_energy_to_nadir_MJ | 5000 | 5000 | ok |
| ch4.html:1059-1061 | ex41_energy_pct | 2.5 | 2.5 | ok |
| ch4.html:1059-1061 | ex41_ramp_energy_MJ | 5000 | 5000 | ok |
| ch4.html:1064-1068 | ex41_half_rocof | 0.25 | 0.25 | ok |
| ch4.html:1064-1068 | ex41_half_dfnadir | -1.25 | -1.25 | ok |
| ch4.html:1064-1068 | ex41_half_fnadir | 48.75 | 48.75 | ok |
| ch4.html:1072 | ex41_gap_to_48.8 | 0.05 | 0.05 | ok |
| ch4.html:1054-1057 | ex41_rk4_nadir | -0.625 | -0.625 | ok |
| ch4.html:1054-1057 | ex41_rk4_tnadir | 10 | 10 | ok |
| ch4.html:1104-1107 (SVG) | fig43_nadir_E300 | 49.583 | 49.5833 | ok |
| ch4.html:1100-1101 (SVG) | fig43_nadir_y_E300 | 84 | 83.9583 | ok |
| ch4.html:1104-1107 (SVG) | fig43_nadir_E200 | 49.375 | 49.375 | ok |
| ch4.html:1100-1101 (SVG) | fig43_nadir_y_E200 | 102.2 | 102.188 | ok |
| ch4.html:1104-1107 (SVG) | fig43_nadir_E100 | 48.75 | 48.75 | ok |
| ch4.html:1100-1101 (SVG) | fig43_nadir_y_E100 | 156.9 | 156.875 | ok |
| ch4.html:1104-1107 (SVG) | fig43_nadir_E50 | 47.5 | 47.5 | ok |
| ch4.html:1100-1101 (SVG) | fig43_nadir_y_E50 | 266.2 | 266.25 | ok |
| ch4.html:1091 (SVG) | fig43_48.8_line_y | 152.5 | 152.5 | ok |
| ch4.html:1094-1097 (SVG) | fig43_200_t0.5_y | 52.8 | 52.832 | ok |
| ch4.html:1094-1097 (SVG) | fig43_50_t0.5_y | 68.8 | 68.8281 | ok |
| ch4.html:1094-1097 (SVG) | fig43_polyline_points_checked | 88 | 88 | ok |
| ch4.html:1094-1097 (SVG) | fig43_polyline_points_bad | 0 | 0 | ok |
| ch4.html:1180 | ex42_Ekin_fleet | 5600 | 5600 | ok |
| ch4.html:1193 | ex42_E_released | 179.2 | 179.2 | ok |
| ch4.html:1195 | ex42_kWh | 49.78 | 49.7778 | ok |
| ch4.html:1197-1198 | ex42_exact_release | 177.77 | 177.766 | ok |
| ch4.html:1198-1199 | ex42_second_order | 1.43 | 1.4336 | ok |
| ch4.html:1198-1199 | ex42_second_order_pct | 0.8 | 0.8 | ok |
| ch4.html:1203 | ex42_store_MJ | 4032000 | 4032000 | ok |
| ch4.html:1204 | ex42_ratio | 22500 | 22500 | ok |
| ch4.html:1213 | ex42_headroom | 224 | 224 | ok |
| ch4.html:1228 | ex42_Pinertial | 0.2 | 0.2 | ok |
| ch4.html:1231 | ex42_Sgfm | 1120 | 1120 | ok |
| ch4.html:1233 | ex42_consistency_HS | 5600 | 5600 | ok |
| ch4.html:1243-1244 | ex42_current_left | 0.2 | 0.2 | ok |
| ch4.html:1318 | ex42_fleet_share_of_200GVAs_pct | 2.8 | 2.8 | ok |
| ch4.html:1205 (L5) | ex42_log_ratio_orders | 4.35 | 4.35218 | ok |
| ch4.html:1273-1301 (SVG) | fig44_ratio1_y | 91.67 | 91.6667 | ok |
| ch4.html:1273-1301 (SVG) | fig44_energy_ratio | 4.44e-05 | 4.44444e-05 | ok |
| ch4.html:1273-1301 (SVG) | fig44_energy_y | 273.01 | 273.008 | ok |
| ch4.html:1509-1511 | ex43_group_D500 | 0.625 | 0.625 | ok |
| ch4.html:1509-1512 | ex43_nadir_D500 | -0.4464 | -0.446375 | ok |
| ch4.html:1509-1512 | ex43_tnadir_D500 | 7.768 | 7.7681 | ok |
| ch4.html:1509-1511 | ex43_group_D1000 | 1.25 | 1.25 | ok |
| ch4.html:1509-1512 | ex43_nadir_D1000 | -0.3513 | -0.351256 | ok |
| ch4.html:1509-1512 | ex43_tnadir_D1000 | 6.487 | 6.4874 | ok |
| ch4.html:1509-1511 | ex43_group_D2000 | 2.5 | 2.5 | ok |
| ch4.html:1509-1512 | ex43_nadir_D2000 | -0.2494 | -0.249447 | ok |
| ch4.html:1509-1512 | ex43_tnadir_D2000 | 5.011 | 5.0111 | ok |
| ch4.html:1523 | ex44_closed_T5 | -0.3125 | -0.3125 | ok |
| ch4.html:1525 | ex44_rk4_T5 | -0.3125 | -0.3125 | ok |
| ch4.html:1523 | ex44_closed_T10 | -0.625 | -0.625 | ok |
| ch4.html:1525 | ex44_rk4_T10 | -0.625 | -0.625 | ok |
| ch4.html:1523 | ex44_closed_T20 | -1.25 | -1.25 | ok |
| ch4.html:1525 | ex44_rk4_T20 | -1.25 | -1.25 | ok |
| ch4.html:1523 | ex44_closed_T30 | -1.875 | -1.875 | ok |
| ch4.html:1525 | ex44_rk4_T30 | -1.875 | -1.875 | ok |
| ch4.html:1564-1569 | ex46_hours | 5 | 5 | ok |
| ch4.html:1564-1569 | ex46_seconds | 18000 | 18000 | ok |
| ch4.html:1564-1569 | ex46_dc_ratio | 250000 | 250000 | ok |
| ch4.html:1564-1569 | ex46_kJ_per_MVA | 0.0144 | 0.0144 | ok |

Rows shown: 181 (the six sweep rows were checked under both readings of the sweep rule; the table keeps the reading the chapter's numbers follow, see B1). Under the other reading the six least-damped ζ values agree to four decimals but the two named modes do not (B1). Total distinct checks run: 187; ok 187; wrong 0.

---

## 6. Evidence per check (a to h)

**a. Symbols defined before use.** Every symbol in the chapter is in the book table (§3.5) or in one of the four local panels, with these exceptions: Δω<sub>COI</sub> (used at 873 and 878, defined nowhere; B4); <var>K</var><sub>D,<var>i</var></sub> (581), <var>I</var><sub><var>i</var></sub> (422) and δ<sub><var>i</var>,0</sub> (642) (L12); <var>P</var><sub>e,<var>i</var></sub> and <var>P</var><sub><var>i</var></sub> name one quantity (L11); j is both the imaginary unit and an index in the same expression (B3). The glyph for the speed deviation differs from Chapter 1 (S1, L21).

**b. Results, assumptions, derivations.** Ten containers carry `data-rid` R34 to R40 and each states its assumptions. Attempts to break the derivations: the sign of the <var>B</var><sub><var>ij</var></sub> sin term holds under the matrix-element convention of Definition 4.1 (B3 makes the convention explicit); the factor 4 in (4.10) is 2 × 2 as stated; the zero eigenvalue follows from <strong>K</strong> row sums of zero, and the printed rows sum to −0.0001, 0.0000, 0.0000, 0.0000; the asymmetry <var>K</var><sub>12</sub> − <var>K</var><sub>21</sub> = 2<var>E</var><sub>1</sub><var>E</var><sub>2</sub><var>G</var><sub>12</sub> sin δ<sub>12</sub> = 0.0024 matches −0.2921 against −0.2945; the linearisation in (4.11) drops 0.80 %. Defects found: Model 4.2 has no derivation (B3); Theorem 4.5 does not say E<sub>kin,sys</sub> excludes the tripped unit and relies on an unstated load assumption (B4); Theorem 4.6 has no limit case for <var>R</var><sub>p</sub> ≠ Δ<var>P</var> (S3).

**c. Numbers.** 267 printed values in 187 checks, 0 wrong (§5). Both worked examples, every table, every SVG coordinate of Figs. 4.2 to 4.4, and every exercise answer were recomputed with `edit_ch4_check.py`. The Runge-Kutta round-off figures 1.8 × 10<sup>−13</sup> Hz (Example 4.1) and 2.8 × 10<sup>−12</sup> Hz (Exercise 4.4) were reproduced to order of magnitude.

**d. Citations.** 28 `verify` marks; sources used S03, S05, S12, S13, S14, S15, S16, S17, S18, S20. Every citation carries the four parts; locations name a topic, not a page, because no source was opened (plan rule for the draft stage). Wrong source: S16 (EirGrid and SONI) cannot hold the Great Britain 1 Hz/s figure (B7, S5). Plausibility of the values, from my general knowledge and not from the sources: 48.8 Hz, about 931 MW and about 1878 MW for 9 August 2019 are the widely reported figures; 2 Hz/s over 500 ms for the ENTSO-E withstand guidance and 1 Hz/s for Ireland DS3 are the usual figures; 200 GVA·s is the right order for Great Britain in 2019 and is correctly marked assumed; <var>H</var> = 3.5 s for a condenser with flywheel is plausible and correctly marked assumed. None of these removes a `verify`. Two format items: the S12 journal name (L19) and one unsourced quantifier and one unsourced time figure (L3, L4).

**e. Problem, tie-back, theory against evidence.** The chapter opens with the condenser-replacement decision (129-161) and each section returns to it: §4.2 closes with what eigenvalues cannot say about stored energy (835-837), §4.3 applies RoCoF to TS4 (925-930), §4.4 works Example 4.1, §4.5 sizes the case. The opening sentence about condensers is wrong and contradicts §4.5 Constraint 3 (B8). Theory and evidence stay apart: every result has a status word, Citation 4.7 takes three figures and refuses clock times, §4.5.1 refuses to call a 0.05 Hz agreement a validation.

**f. HTML.** Parsed with `html.parser`: no mismatch, no unclosed tag, no duplicate id, zero external references of any kind. Eight dark-mode tokens on `:root`; one literal hex remains in a rule (L18). One `<h1>`, nine `<h2>`, thirteen `<h3>`, five `<h4>`. Class `cit` is not in plan §5.3 (S9). File is `ch4.html`, plan says `ch04.html` (S2). Visual rendering at 360 px was not judged.

**g. ASD-STE100.** 73 chapter sentences exceed 25 words. Eleven carry one idea in a way a reader cannot follow in one pass and are rewritten: lines 704 (80 words, B1), 1496 (84, L25), 1561 (64 and 58, L26), 1365 (52, L17), 1403 (54, L27), 154 (41, L23), 416 (40, L28), 1034 (40, L22), 1246 (42, L24), 1480 (40, L29), 1539 (43, L16). The rest are lists of numbers, citations, or compound sentences a reader can follow, and are not flagged. Evaluative phrases without a measurement: "interesting" (704, B1), "worth naming" (748, L6), "worth stating ... worth refusing" (1315, L7), "often called conservative" (993, L2), "four orders of magnitude" (1205, L5), "several times" (1396, L4), "few hundred milliseconds" (895, L3), "300 Hz" (1442, L9), "runs out of time" (1062, L1).

**h. Cross-chapter results.** R03, R04, R05, R06 and R11 are stated as in plan §2 and as in `ch1.html` (the swing convention 2<var>H</var> dΔω/d<var>t</var> = <var>P</var><sub>m</sub> − <var>P</var><sub>e</sub> − <var>K</var><sub>D</sub>Δω matches Model 1.4, equation (1.7)). R24, R26, R28, R30 and R32 match `ch3.html` (K<sub>D,eq</sub> = 1/<var>m</var><sub>p</sub>; 14.4 kJ at `ch3.html:964`; Definition 3.1 as a voltage source behind an impedance with the angle as a state). R33 in `ch3.html` (Corollary 3.8) proves the two bounds (3.30) and (3.31) that Example 4.2 uses as (4.11) and (4.13); the chapter cites R28 and R32 for them instead of R33 (L8). The draft notes list R22 among the chapter's cross-references; the chapter does not cite R22, which is no defect. Anchor map for links: S2.

**Word count.** 8333 body words against the 7000 target (S6).
