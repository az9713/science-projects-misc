# Chapter 1 edit — The classical picture: machines that swing

**Verdict: ACCEPT WITH CHANGES.** Both central proofs hold (Theorem 1.7, R07; Theorem 1.8, R09). 115 of 119 printed numbers reproduce to the printed digit. The HTML is self-contained. Eight defects stop a reader who knows no power systems. One printed number, 0.17009 s, carries precision its method cannot deliver. The fixes below are written out in full.

Editor: Fable 5.1, science-editor skill. Date 2026-09-22. File judged: `p1-textbook/ch1.html` (1185 lines, 86,156 bytes). Brief: `book-plan.md` §2, §3, §4 (Chapter 1), §5; `draft-results.json` chapter 1 notes; `HANDOFF.md` flags. Scratch scripts: `edit_ch1_check.py`, `edit_ch1_html.py`, `edit_ch1_ste.py`, `edit_ch1_vars.py`, `edit_ch1_conv.py`, `edit_ch1_window.py`, `edit_ch1_rk2win.py` in the session scratchpad.

Rules for the fix stage:

1. Apply items 1 to 8 first, then items 9 to 29, then read items 30 to 37.
2. Do not move any chapter number toward the plan's 1.4915, 8.963, or 0.4401. Item 33 explains why.
3. Do not remove or tighten any `verify` mark. Item 35 lists the citations a human must check.
4. Every replacement below is HTML in the chapter's own idiom: `<var>`, `<sub>`, `<sup>`, `&nbsp;`, Unicode Greek. No MathML, no LaTeX.
5. Line numbers refer to the file as drafted at 12:58. Re-locate by the quoted text if lines have moved.

---

## Part 1 — Blocking defects (ranked by severity)

### 1. ch1.html:663–665 — the mass–spring–dashpot triple mixes the two conventions the chapter itself excludes

**Quoted.** `The mass is 2<var>H</var>/<var>ω<sub>0</sub></var>, the spring is <var>K<sub>s</sub></var>, the dashpot is <var>K<sub>D</sub></var>.`

**Defect.** Wrong statement (part 1 of the standard). Eliminate `Δω̄` from the linearised pair in the proof. With `Δδ` as position, the equation is `(2H/ω₀) Δδ'' + (K_D/ω₀) Δδ' + K_s Δδ = 0`. If the mass is `2H/ω₀` and the spring is `K_s`, the dashpot is `K_D/ω₀`, not `K_D`. The printed triple is off by the factor `ω₀ = 376.99`, the exact mixture that §1.3 and Exercise 3 warn against. This sits in the Reading of the chapter's central theorem.

**Replace lines 663–668 with:**

```html
  <p><strong>Reading.</strong> The machine is a mass, a spring and a dashpot. To see the
  three constants, write the linearised pair with Δ<var>δ</var> as the position. From
  dΔ<var>δ</var>/d<var>t</var> = <var>ω<sub>0</sub></var><var>Δω̄</var>, the speed deviation
  is <var>Δω̄</var> = (1/<var>ω<sub>0</sub></var>) dΔ<var>δ</var>/d<var>t</var>. Substitute
  it into the first equation of the proof:</p>
  <div class="eqc">(2<var>H</var>/<var>ω<sub>0</sub></var>) d<sup>2</sup>Δ<var>δ</var>/d<var>t</var><sup>2</sup> + (<var>K<sub>D</sub></var>/<var>ω<sub>0</sub></var>) dΔ<var>δ</var>/d<var>t</var> + <var>K<sub>s</sub></var> Δ<var>δ</var> = 0.</div>
  <p>The mass is 2<var>H</var>/<var>ω<sub>0</sub></var>, the dashpot is
  <var>K<sub>D</sub></var>/<var>ω<sub>0</sub></var>, and the spring is <var>K<sub>s</sub></var>.
  Check against (1.10): (dashpot)<sup>2</sup>/(mass × spring) =
  <var>K<sub>D</sub></var><sup>2</sup>/(2<var>H</var><var>ω<sub>0</sub></var><var>K<sub>s</sub></var>)
  = 4<var>ζ</var><sup>2</sup>. Do not read the dashpot as <var>K<sub>D</sub></var> alone.
  That pairs a per-unit damping coefficient with a position in radians, which is the
  convention mixture excluded in §1.3. Both numbers in (1.10) are inherited from hardware:
  <var>H</var> from the steel, <var>K<sub>s</sub></var> from the network reactance and the
  operating angle. Neither is chosen by a control engineer. Chapter&nbsp;3 asks what happens
  when both become settings in a firmware file.</p>
```

Arithmetic behind the check: `4ζ² = K_D²/(4H²ω_n²) = K_D²/(4H² · K_sω₀/(2H)) = K_D²/(2Hω₀K_s)`.

### 2. ch1.html:776–786, 794–795, 819–823 — Theorem 1.8 uses a hypothesis it never states

**Quoted.** Line 777: `Suppose the machine starts at rest at <var>δ<sub>0</sub></var>.` Line 780: `Call <var>A<sub>acc</sub></var> the accelerating area accumulated while the fault is on.` Lines 819–823: assumptions (i) to (iv).

**Defect.** Unstated assumption (part 4 of the standard). Equation (1.13) is derived with `P_e = 0` during the fault, but that condition appears only inside the proof ("While the fault is on, P_e = 0"). The theorem statement and the assumptions list do not carry it. A fault at a remote bus leaves a reduced power-angle curve and (1.13) is then false as printed. Three smaller gaps sit in the same result. First, "at rest" is not defined; it means `Δω̄ = 0`, not zero mechanical speed. Second, the change of variable from `t` to `δ` needs `δ(t)` strictly increasing. That holds until the first stop, and the proof does not say so. Third, `A_acc` as "the area while the fault is on" is the whole accelerating area only when the clearing angle lies above the post-fault equilibrium. Example 1.2 satisfies this (63.9° above 38.18°); the theorem does not say so.

**Replace lines 776–778 with:**

```html
  <p>Take (1.7) with <var>K<sub>D</sub></var> = 0 and constant <var>P<sub>m</sub></var>.
  Suppose the machine starts at the equilibrium <var>δ<sub>0</sub></var> at synchronous
  speed, so <var>Δω̄</var> = 0. Suppose a fault holds <var>P<sub>e</sub></var> = 0 from
  <var>δ<sub>0</sub></var> up to a clearing angle, and that after clearing
  <var>P<sub>e</sub></var> = <var>P<sub>max,post</sub></var> sin <var>δ</var>. Write
  <var>δ<sub>max</sub></var> = π − arcsin(<var>P<sub>m</sub></var>/<var>P<sub>max,post</sub></var>)
  for the far intersection of the post-fault curve with <var>P<sub>m</sub></var>. Then the
  rotor first stops swinging at the angle <var>δ</var> at which</p>
```

**Replace lines 780–785 with** (line 786, `<div class="proof">`, stays):

```html
  <p>Split that integral at the clearing angle. Call <var>A<sub>acc</sub></var> the integral
  of <var>P<sub>m</sub></var> − <var>P<sub>e</sub></var> over the angles where that
  difference is positive: the rotor gains kinetic energy there. Call
  <var>A<sub>dec</sub></var> the integral of <var>P<sub>e</sub></var> − <var>P<sub>m</sub></var>
  over the angles after clearing where that difference is positive, up to
  <var>δ<sub>max</sub></var>. The rotor loses kinetic energy there. When the clearing angle
  lies above the post-fault equilibrium arcsin(<var>P<sub>m</sub></var>/<var>P<sub>max,post</sub></var>),
  <var>A<sub>acc</sub></var> is the rectangle of height <var>P<sub>m</sub></var> between
  <var>δ<sub>0</sub></var> and the clearing angle. Example&nbsp;1.2 is such a case. The
  machine keeps synchronism exactly when <var>A<sub>dec</sub></var> ≥ <var>A<sub>acc</sub></var>.
  The critical clearing angle <var>δ<sub>cr</sub></var> is the clearing angle at which the two
  areas are equal. It satisfies (1.13).</p>
```

**Lines 793–795: replace the sentence from `Integrate both sides in time,` to `from <var>t</var> to <var>δ</var>:</p>` with the text below.** Keep the opening `<p>` and the paragraph's first sentence: `The left side is <var>H</var><var>ω<sub>0</sub></var> d(<var>Δω̄</var><sup>2</sup>)/d<var>t</var>.`

```html
Integrate both sides in time from the start of the disturbance to the instant the angle
  reaches <var>δ</var>. On the right, change the variable of integration from <var>t</var>
  to <var>δ</var>. The change is valid because d<var>δ</var>/d<var>t</var> =
  <var>ω<sub>0</sub></var><var>Δω̄</var> &gt; 0 until the rotor first stops, so
  <var>δ</var>(<var>t</var>) is strictly increasing on that interval:</p>
```

**Replace lines 819–823 with:**

```html
  <p><strong>Assumptions.</strong> (i) No damping. (ii) <var>P<sub>m</sub></var> constant:
  the governor does not act inside the swing. (iii) <var>E′</var> constant, as in
  Model&nbsp;1.5. (iv) One machine against an infinite bus, so there is a single angle to
  integrate. The criterion does not extend to three or more machines without further
  argument. (v) <var>P<sub>e</sub></var> = 0 while the fault is on. A fault at a bus further
  from the machine leaves a reduced power-angle curve in place during the fault. Equation
  (1.12) still holds, because it holds for any <var>P<sub>e</sub></var>(<var>δ</var>).
  Equation (1.13) then gains the extra term −(1/<var>P<sub>max,post</sub></var>) × (integral
  of the fault-on power from <var>δ<sub>0</sub></var> to <var>δ<sub>cr</sub></var>).
  Re-derive it from (1.12).</p>
```

### 3. ch1.html:974 and 1139 — "0.17009 s to a tolerance of 1 μs" depends on an unstated simulation window

**Quoted.** Line 974: `A bisection on clearing time over the same integration, to a tolerance of 1&nbsp;μs, puts the boundary at 0.17009&nbsp;s, against the 0.170081&nbsp;s that (1.14) gives`. Line 1139: `bisection to 1&nbsp;μs) returns 0.17009&nbsp;s.`

**Defect.** A plausible figure with unsupported precision (numbers rule). I re-ran the bisection with the stated method: second-order Runge–Kutta, step 10 μs, failure when `δ` passes 200°. Only the simulation window varied. A 1.2 s window gives 0.170265 s; 1.5 s gives 0.170105 s; 3 s gives 0.170085 s (`edit_ch1_rk2win.py`). With an exact fault-on solution and a fourth-order integrator, 3 s and 6 s windows give 0.170081 s, the equal-area value to six digits (`edit_ch1_window.py`). A rotor cleared just after `t_cr` lingers near `δ_max` before it runs away. A short window classes it as stable and biases the boundary upward. The remaining 4 μs at 3 s is the 10 μs step. The printed 0.17009 s therefore depends on an unstated window, and the "1 μs tolerance" measures the bisection interval, not the answer.

**Replace, in the Fig. 1.3 caption (lines 973–975), the sentence from `A bisection on clearing time` to `that (1.14) gives in Example&nbsp;1.2.` with:**

```html
A bisection on clearing time over the same integration, with failure declared when
<var>δ</var> passes 200° inside the simulated window, depends on the window length. A
1.2&nbsp;s window gives 0.1703&nbsp;s; a 1.5&nbsp;s window gives 0.1701&nbsp;s; a 3&nbsp;s
window gives 0.170085&nbsp;s. The last value sits 4&nbsp;μs above the 0.170081&nbsp;s of
(1.14). That residual is the 10&nbsp;μs step: an exact fault-on solution followed by a
fourth-order integrator converges to 0.170081&nbsp;s. The window matters because a rotor
cleared just after <var>t<sub>cr</sub></var> lingers near <var>δ<sub>max</sub></var>
before it runs away.
```

**In lines 1137–1140, replace the two sentences from `The reference integration behind Fig.&nbsp;1.3` to `the threshold you used.` with:**

```html
The reference integration behind Fig.&nbsp;1.3 uses second-order Runge–Kutta, step
10&nbsp;μs, failure threshold 200°. It returns 0.1701&nbsp;s with a 1.5&nbsp;s window and
0.170085&nbsp;s with a 3&nbsp;s window. Report the value <em>your</em> run returns, with the
step size, the threshold and the window you used. A short window biases the result upward:
a rotor cleared just after <var>t<sub>cr</sub></var> lingers near <var>δ<sub>max</sub></var>
before it runs away. A finite step leaves a residual of a few microseconds.
```

### 4. ch1.html:478–479 — `X′_d` and `E′` are named, not defined, inside the statement of Model 1.5

**Quoted.** `Represent the machine as a voltage source of <strong>constant</strong> magnitude <var>E′</var> behind the direct-axis transient reactance <var>X′<sub>d</sub></var>.`

**Defect.** Undefined terms of art (part 2 of the standard). "Direct-axis", "transient reactance" and "emf" are power-systems vocabulary. The plan's reader knows none of it (§1.3 of the plan), and the acceptance check requires each §3.2 symbol defined in prose, not only named. The notation table repeats the name.

**Replace lines 478–480 (up to and including `of Definition&nbsp;1.2. Let`) with:**

```html
  <p>Represent the machine as a voltage source of <strong>constant</strong> magnitude
  <var>E′</var> behind a reactance <var>X′<sub>d</sub></var>. Here <var>E′</var> is the
  internal voltage that the rotor field induces in the stator winding. The prime marks it
  as the value fixed by the field flux in the first second after a disturbance. The
  reactance <var>X′<sub>d</sub></var> is the <strong>transient reactance</strong>. It is the
  reactance the machine presents between that internal voltage and its terminals on the
  same timescale, before the field flux has changed. The qualifier <em>direct-axis</em>
  names the rotor axis that lies along the field winding. Under assumption (iii) below the
  two rotor axes have equal reactance, so the qualifier carries no content in this chapter.
  The symbol keeps it because it is standard. Typical values lie near 0.3&nbsp;pu on the
  machine base <span class="cite">[S01, Kundur 1994, <em>Power System Stability and
  Control</em>, Ch.&nbsp;3 — verify]</span>. The angle of that source is the rotor angle
  <var>δ</var> of Definition&nbsp;1.2. Let
```

The citation repeats the one already at line 330 for the same number; it adds no new claim.

### 5. ch1.html:150–155 — "synchronous generator" is never defined

**Quoted.** `Every synchronous generator connected to it turns at a speed locked to that frequency through its number of magnetic poles.`

**Defect.** Undefined term of art at first use (part 2). The chapter is about synchronous machines and the reader "knows nothing about synchronous machines" (plan §1.3). The paragraph also asserts the restoring-torque mechanism that §1.4 proves, with no pointer.

**Replace lines 150–155 with:**

```html
<p>An alternating-current grid carries power at one frequency. In the classical grid this
chapter describes, that power comes from <strong>synchronous generators</strong>. A
synchronous generator is a rotating
machine whose rotor carries a magnetic field, set up by a direct current in a field
winding. Its stationary winding, the stator, produces an alternating voltage as that field
sweeps past it. The voltage frequency is fixed by the rotor speed and by the number of
magnetic poles on the rotor; Definition&nbsp;1.2 gives the relation. In steady state every
such machine on the grid turns at the one speed that produces the grid frequency. That is
what <em>synchronous</em> means. The lock is not a control law. It is a physical restoring
torque. If one rotor advances in angle against the rest of the system, the electrical power
it exports rises. That loads the shaft and pulls the rotor back; §1.4 derives this as
equation (1.8). If it falls behind, its export drops, which unloads the shaft and lets it
catch up. The machines are coupled like masses on springs, and §1.5 makes the spring
constant exact.</p>
```

### 6. ch1.html:457–459 — `ζ` is used in §1.3, two sections before its definition

**Quoted.** `Exercise&nbsp;3 carries the mixture through Example&nbsp;1.1 and obtains <var>ζ</var> = 6.01 instead of 0.01594, that is a badly damped machine reported as overdamped.`

**Defect.** Symbol before definition (plan acceptance check a; `edit_ch1_vars.py` finds first body use at line 458, definition at line 624). "Badly damped" is an impression without a measurement.

**Replace with:**

```html
Exercise&nbsp;3 carries the mixture through Example&nbsp;1.1 and obtains a damping ratio
(the symbol <var>ζ</var>, defined in §1.5) of 6.01 instead of 0.01594. A machine whose
swing decays by the factor e in 7.0&nbsp;s is then reported as overdamped, with no
oscillation at all.
```

### 7. ch1.html:1000–1001 — the classification being extended is dated 2004, not 1994

**Quoted.** `The 2021 revision of that classification adds two classes that did not exist in the 1994 picture`

**Defect.** Wrong statement about a cited source. The classification cited is S02, Kundur et al. 2004. Kundur 1994 (S01) is a textbook, not the classification.

**Replace with:**

```html
The 2021 revision of that classification adds two classes that the 2004 classification did
not contain
```

### 8. ch1.html:874, 876, 1121, 1167 — three printed arithmetic lines whose operands do not give the printed result

**Defect.** Factual mismatch at the last printed digit. Each printed result comes from unrounded inputs, but the printed operands, multiplied as shown, give a different last digit. A reader checking with a pen finds the chapter wrong.

| Line | Printed | Printed operands give | Fix |
|---|---|---|---|
| 874 | `14 × 0.623166 = 8.724319` | 8.724324 | print `8.724324`; line 876 then reads `√(8.724324 / 301.5929) = √0.0289275`, unchanged result |
| 1121 | `376.9911 × 0.015941 = 6.0095` | 6.0096 | print `376.9911 × 0.0159407 = 6.0095` |
| 1167 | `log(0.010540/0.021090)/log(8/2) = −0.50000` | −0.50034 | print the unrounded operands `0.0105438/0.0210875` and say so; the table's rounded values give −0.5003 |

**Line 874, replace** `= 14 × 0.623166 = 8.724319;` **with** `= 14 × 0.623166 = 8.724324;`
**Line 876, replace** `√(8.724319 / 301.5929)` **with** `√(8.724324 / 301.5929)`
**Line 1121, replace** `376.9911 × 0.015941 = 6.0095` **with** `376.9911 × 0.0159407 = 6.0095`
**Lines 1167–1168, replace** `and log(0.010540/0.021090)/log(8/2) = −0.50000 for
<var>ζ</var>.` **with** `and log(0.0105438/0.0210875)/log(8/2) = −0.50000 for <var>ζ</var>, using the unrounded values 0.0210875 and 0.0105438 that the table prints as 0.02109 and 0.01054. The rounded table values give −0.5003.`

The exact values: `ζ(H = 2) = 0.0210875`, `ζ(H = 8) = 0.0105438`, ratio 0.500000; `ζ(H = 3.5) = 0.0159407`; `14 × 0.6231656 = 8.724319`.

---

## Part 2 — Line-level rewrites

### 9. ch1.html:503–510 — write out the derivation of (1.8)

**Quoted.** `The derivation of (1.8) is one line of circuit theory. ... Forming the complex power at the receiving end and taking the real part gives ...`

**Reason.** A reader fluent in phasors can reproduce the step. But the power convention (`S = V I*`), the current direction and the reference phase are not stated. This is the whole electrical side of the chapter (part 3 of the standard: write the arithmetic).

**Replace lines 503–510 with:**

```html
<p>The derivation of (1.8) is four lines of phasor circuit theory. Take the infinite-bus
voltage as the phase reference, <var>V<sub>inf</sub></var>∠0, and the internal voltage as
<var>E′</var>∠<var>δ</var> = <var>E′</var>(cos <var>δ</var> + <var>j</var> sin <var>δ</var>).
The two sources are joined by the reactance <var>X</var>, whose impedance is
<var>j</var><var>X</var>. The current <var>I</var> from the machine toward the bus is</p>
<div class="eqc"><var>I</var> = (<var>E′</var>∠<var>δ</var> − <var>V<sub>inf</sub></var>∠0) / (<var>j</var><var>X</var>).</div>
<p>The complex power <var>S</var> delivered to the bus is
<var>S</var> = <var>V<sub>inf</sub></var> <var>I</var>*, where the asterisk denotes the
complex conjugate. Substitute <var>I</var> and use 1/(−<var>j</var>) = <var>j</var>:</p>
<div class="eqc"><var>S</var> = <var>j</var><var>V<sub>inf</sub></var> (<var>E′</var> cos <var>δ</var> − <var>j</var><var>E′</var> sin <var>δ</var> − <var>V<sub>inf</sub></var>) / <var>X</var>.</div>
<p>Multiply out. The real part is <var>P<sub>e</sub></var> =
(<var>E′</var><var>V<sub>inf</sub></var>/<var>X</var>) sin <var>δ</var>, which is (1.8). The
imaginary part is the reactive power
(<var>E′</var><var>V<sub>inf</sub></var> cos <var>δ</var> − <var>V<sub>inf</sub></var><sup>2</sup>)/<var>X</var>,
which this chapter does not use. In per unit <var>S</var> = <var>V</var><var>I</var>* carries
no factor 3, by the first convenience of §1.2.</p>
```

Add `I` and `S` to the local notation list; item 26 gives the text.

### 10. ch1.html:369–371 — (1.4) reuses `ω_m` for a constant

**Quoted.** `A rotor of moment of inertia <var>J</var> turning at rated mechanical speed stores kinetic energy` / `<var>E<sub>kin</sub></var> = ½ <var>J</var> <var>ω<sub>m</sub></var><sup>2</sup>.`

**Reason.** Definition 1.2 defines `ω_m` as the variable mechanical speed. (1.4) uses the same symbol for the rated value, with only the prose to say so. `H`, a book-wide constant, rests on this line. Write the rated speed out; no new symbol is needed.

**Replace lines 369–371 with:**

```html
  <p>A rotor of moment of inertia <var>J</var> turning at rated mechanical speed stores
  kinetic energy. By Definition&nbsp;1.2 the rated mechanical speed of a machine with
  <var>p</var> poles is 2<var>ω<sub>0</sub></var>/<var>p</var>, so</p>
  <div class="eq"><div class="body"><var>E<sub>kin</sub></var> = ½ <var>J</var> (2<var>ω<sub>0</sub></var>/<var>p</var>)<sup>2</sup>.</div><div class="num">(1.4)</div></div>
  <p><var>E<sub>kin</sub></var> is a constant of the machine, evaluated at rated speed. It is
  not the instantaneous kinetic energy, which varies with <var>ω<sub>m</sub></var>.</p>
```

Exercise 2 (line 1090) already computes `ω_m = 2ω/p` at rated speed; it needs no change.

### 11. ch1.html:395–399 — Step 1 needs the torque base

**Quoted.** `Power equals torque times speed exactly, but the per-unit torque and the per-unit power of a machine are equal only at rated speed.`

**Replace with:**

```html
Power equals torque times speed exactly. Take the torque base as <var>S<sub>base</sub></var>
divided by the rated mechanical speed 2<var>ω<sub>0</sub></var>/<var>p</var>. Then per-unit
torque equals per-unit power exactly at rated speed, and differs from it by the factor
1 + <var>Δω̄</var> off rated speed.
```

### 12. ch1.html:406–411 — Step 2 replaces `ω_m` by its rated value without saying so

**Replace lines 406–411 (the whole Step 2 paragraph) with:**

```html
<p><strong>Step 2 — normalise by the rating.</strong> Divide by
<var>S<sub>base</sub></var>. The coefficient on the left is
<var>J</var><var>ω<sub>m</sub></var>/<var>S<sub>base</sub></var>. Under the assumption of
Step&nbsp;1, replace the <var>ω<sub>m</sub></var> in it by the rated value
2<var>ω<sub>0</sub></var>/<var>p</var>. By (1.4),
<var>J</var> = 2<var>E<sub>kin</sub></var>/(2<var>ω<sub>0</sub></var>/<var>p</var>)<sup>2</sup>,
so the coefficient becomes
2<var>E<sub>kin</sub></var>/[(2<var>ω<sub>0</sub></var>/<var>p</var>) <var>S<sub>base</sub></var>]
= 2<var>H</var>/(2<var>ω<sub>0</sub></var>/<var>p</var>) by (1.5). The left side is then
2<var>H</var> times the time derivative of
<var>ω<sub>m</sub></var>/(2<var>ω<sub>0</sub></var>/<var>p</var>) = <var>ω</var>/<var>ω<sub>0</sub></var>
= 1 + <var>Δω̄</var>, whose derivative is d<var>Δω̄</var>/d<var>t</var> by (1.2). The pole
factor <var>p</var>/2 has cancelled between mechanical and electrical speed.</p>
```

### 13. ch1.html:158 — "governor" undefined

**Quoted.** `Suppose demand rises and no governor has yet responded.`

**Replace with:**

```html
Suppose demand rises and no governor has yet responded. (The governor is the controller that
adjusts the mechanical power of a turbine when its speed changes. It acts within seconds;
§1.3 lists it among the omissions of the swing equation.)
```

### 14. ch1.html:414–415 — "damper windings" undefined; "a little" unmeasured

**Quoted.** `Real machines lose a little power to damper windings, and real load falls when frequency falls.`

**Replace with:**

```html
Real machines dissipate power in damper windings. These are short-circuited conductors on
the rotor; current flows in them only when the rotor speed differs from the speed of the
stator field.
Real load also falls when frequency falls.
```

### 15. ch1.html:157 — "Electrical energy is not stored in the network" is too strong

**Replace** `Electrical energy is not stored in the network.` **with:**

```html
The network itself holds no usable energy store. The electric and magnetic fields of its
lines and transformers exchange energy every half cycle. They hold no net reserve on the
timescale of this chapter, tenths of a second to seconds.
```

### 16. ch1.html:159–160 — "The only store large enough" needs its number

**Quoted.** `The only store large enough is the kinetic energy of the spinning masses.`

**Replace with:**

```html
The one store of the required size is the kinetic energy of the spinning masses. A
200&nbsp;MVA machine with the inertia constant of Example&nbsp;1.1 holds 700&nbsp;MJ, enough
to supply its full rating for 3.5&nbsp;s (Definition&nbsp;1.3).
```

Arithmetic: `3.5 s × 200 MVA = 700 MJ`.

### 17. ch1.html:380–381 — "well under half" is an impression

**Quoted.** `Exercise&nbsp;2 shows that the generator rotor alone accounts for well under half of that, so the turbine mass carries most of it.`

**Replace with:**

```html
Exercise&nbsp;2 computes 0.444&nbsp;s for a generator rotor alone, which is 22&nbsp;% of the
2&nbsp;s lower end. The turbine stages carry the remainder.
```

### 18. ch1.html:707–712 — "A system operator will not accept" is an unsourced claim

**Quoted.** `A system operator will not accept a mode that rings for seven seconds after every load step. That is the reason power system stabilisers exist: they add a supplementary signal to the excitation system whose only purpose is to raise the effective damping of this mode`

**Replace with:**

```html
After a load step this mode is still at 36.8&nbsp;% of its initial amplitude ten swings
later. Power system stabilisers exist to raise that damping. They add a supplementary signal
to the excitation system whose purpose is to increase the damping of this mode
```

(Keep the S01 Ch. 12 citation that follows.)

### 19. ch1.html:138 — "completely" contradicts the omissions lists

**Replace** `This chapter derives that picture completely, in the smallest setting that contains it:` **with** `This chapter derives that picture in the smallest setting that contains it:`

### 20. ch1.html:465–467 — "a sensible answer"

**Replace** `This section supplies that function under the smallest set of assumptions that produces a sensible answer.` **with:**

```html
This section supplies that function under four assumptions, listed in Model&nbsp;1.5. They
are the fewest that make <var>P<sub>e</sub></var> a function of <var>δ</var> alone.
```

### 21. ch1.html:471–472 — "so much larger" without a measure

**Replace** `It idealises a machine connected to a system so much larger than itself that the machine cannot move it.` **with:**

```html
It idealises a machine whose own swing does not measurably move the system voltage or
frequency. Chapter&nbsp;4 replaces it with a network of finite size.
```

### 22. ch1.html:488 and 496 — "round-rotor" and "salient-pole" undefined

**Line 488, replace** `(iii) The machine is round-rotor, so the reactance is the same on both axes.` **with:**

```html
(iii) The rotor is cylindrical (a round rotor), so the reactance the machine presents does
not depend on the rotor position.
```

**Line 496, replace** `<em>Saliency:</em> a salient-pole machine adds a second-harmonic reluctance term to (1.8).` **with:**

```html
<em>Saliency:</em> a rotor with projecting poles, as in hydro machines, presents a reactance
that varies with rotor position. It adds a term in sin&nbsp;2<var>δ</var> to (1.8).
```

### 23. ch1.html:849 — the fault is at a bus, not at the machine terminal

**Quoted.** `It holds the terminal voltage at zero, so <var>P<sub>e</sub></var> = 0 while the fault is on.`

**Replace with:**

```html
It holds the voltage of that bus at zero. The path from <var>E′</var> to that bus is a pure
reactance, so no active power leaves the machine. <var>P<sub>e</sub></var> = 0 while the
fault is on.
```

### 24. ch1.html:568–570 — Fig. 1.1 caption uses `δ_max` two sections before its definition

**Quoted.** `and the far intersection at 141.82°, named <var>δ<sub>max</sub></var> and defined in §1.6, beyond which no decelerating area remains.`

**Replace with:**

```html
and the far intersection of the post-fault curve with <var>P<sub>m</sub></var> at 141.82°.
§1.6 names that angle <var>δ<sub>max</sub></var>; beyond it the post-fault curve lies below
<var>P<sub>m</sub></var> again.
```

### 25. ch1.html:523 and 585–590, 211 — define `δ_0` in §1.4, as the plan's notation table says

**Reason.** Plan §3.2 places `δ_0` in §1.4. The chapter defines it in §1.5 (line 587) and the draft flagged the deviation. Fig. 1.1, in §1.4, already marks two equilibria. Define the angle where the figure needs it.

**Insert after line 523 (`</ol>`), before `<figure id="fig-1-1">`:**

```html
<p>Take a mechanical power <var>P<sub>m</sub></var> &lt; <var>P<sub>max</sub></var>. The
<strong>equilibrium angle</strong> <var>δ<sub>0</sub></var> is the angle at which electrical
output equals mechanical input: <var>P<sub>max</sub></var> sin <var>δ<sub>0</sub></var> =
<var>P<sub>m</sub></var>. There are two solutions in (0,&nbsp;π), one below 90° and one
above; §1.5 shows why only the first is usable. Fig.&nbsp;1.1 marks
<var>δ<sub>0</sub></var> for the pre-fault and post-fault networks of Example&nbsp;1.2.</p>
```

**Replace lines 585–590 with:**

```html
<p>An equilibrium needs both derivatives to be zero, so <var>Δω̄</var> = 0 and
<var>P<sub>max</sub></var> sin <var>δ<sub>0</sub></var> = <var>P<sub>m</sub></var>: the
equilibrium angle <var>δ<sub>0</sub></var> of §1.4. The rest of this section shows why only
the solution below 90° is usable.</p>
```

**Line 211, replace** `<td>§1.5</td>` **with** `<td>§1.4</td>` (the `δ_0` row only).

### 26. ch1.html:240–274 — local notation list is missing four symbols the chapter uses

**Reason.** `edit_ch1_vars.py`: `K_D,v` and `K_D,eq` appear at line 443 and are declared nowhere in the chapter. Items 9 adds `I` and `S`.

**Insert before line 274 (`</ul>`):**

```html
<li><var>K<sub>D,v</sub></var>, <var>K<sub>D,eq</sub></var> — the virtual and equivalent
damping coefficients of Chapter&nbsp;3. Named once, in the notation decision of §1.3, so
that the reader meets the book's spelling of them; not used in this chapter.</li>
<li><var>I</var>, <var>S</var> — the phasor current from the machine to the infinite bus, and
the complex power delivered to the bus. Both are used only in the derivation of (1.8) in
§1.4.</li>
```

### 27. ch1.html:78, 88–102, 114 — hex literals below `:root` (plan §5.3 item 4)

**Reason.** The plan requires the palette tokens on `:root` and variables, not literals, in every rule below it. `edit_ch1_html.py` counts 19 literals below `:root`, two of them (`#16233c`, `#243352`) outside the eight-colour palette. `var()` works on SVG `stroke` and `fill` in page CSS.

**Line 78, replace** `background:#16233c` **with** `background:var(--bg)`
**Line 114, replace** `background:#16233c;` **with** `background:var(--bg);`
**Replace lines 88–102 with:**

```css
.ax{stroke:var(--border2); stroke-width:1; fill:none}
.grid{stroke:var(--border2); stroke-opacity:.55; stroke-width:1; fill:none}
.c1{stroke:var(--accent); stroke-width:2; fill:none}
.c2{stroke:var(--accent2); stroke-width:2; fill:none}
.c3{stroke:var(--muted); stroke-width:2.5; fill:none; stroke-dasharray:6 4}
.c4{stroke:var(--text); stroke-width:1.5; fill:none; stroke-dasharray:3 3}
.mark{stroke:var(--muted); stroke-width:1; fill:none; stroke-dasharray:3 3}
.fillA{fill:var(--accent); fill-opacity:.22; stroke:none}
.fillD{fill:var(--accent2); fill-opacity:.22; stroke:none}
.pt{fill:var(--accent); stroke:var(--bg); stroke-width:1.5}
.pt2{fill:var(--accent2); stroke:var(--bg); stroke-width:1.5}
text{font:12px system-ui,sans-serif; fill:var(--muted)}
text.lab{fill:var(--text); font-weight:600}
text.lab2{fill:var(--accent2); font-weight:600}
text.lab3{fill:var(--accent); font-weight:600}
```

### 28. ch1.html:1062 — section id

**Replace** `<h2 id="s1-8">Exercises</h2>` **with** `<h2 id="s1-ex">Exercises</h2>`. There is no §1.7, so `s1-8` misleads a link author. No internal link targets it.

### 29. ch1.html:308–310 and 323–327 — two sentences over 25 words that carry two ideas each

The STE scan (`edit_ch1_ste.py`) finds 29 sentences over 25 words in 478. Most are enumerations, displayed arithmetic, or sentences inflated by a four-part citation, and a reader can follow them. These two are not.

**Lines 308–310, replace** `Now pick one <var>S<sub>base</sub></var> for the whole circuit, and choose the base voltage on each side in the ratio of the turns:` **with:**

```html
Now pick one <var>S<sub>base</sub></var> for the whole circuit. Choose the base voltages in
the ratio of the turns:
```

**Lines 323–327, replace** `Second, machine parameters expressed in per unit on the machine's own rating fall in narrow numerical ranges across a wide range of machine sizes, so a per-unit number carries engineering meaning that an ohm does not.` **with:**

```html
Second, machine parameters in per unit on the machine's own rating fall in narrow numerical
ranges, whatever the machine size. A per-unit number therefore carries engineering meaning
that an ohm does not.
```

Also replace, at line 754, `It looks almost flat because the horizontal axis is stretched about ten times against the vertical one.` **with** `It looks nearly flat because one unit on the horizontal axis spans 10.2 times the length of one unit on the vertical axis.` (137.1 px per s⁻¹ against 13.5 px per rad/s.)

---

## Part 3 — Structural notes

### 30. Figure numbers are not in document order

Figures appear as 1.1 (line 528), 1.4 (line 717), 1.2 (line 890), 1.3 (line 934). The plan fixes each number to a content, and the draft placed each figure where its content belongs. A reader who meets "Fig. 1.4" before "Fig. 1.2" looks for two missing figures. `grep` over `ch2.html`, `ch3.html`, `ch4.html` finds no reference to any `Fig. 1.x`, so renumbering is safe. Recommendation: renumber in document order and record the mapping in HANDOFF. Old 1.4 (eigenvalues) → new 1.2; old 1.2 (areas) → new 1.3; old 1.3 (time response) → new 1.4. Update the four `<figure id>` values and the four caption prefixes. Update the Exercise 4 reference to Fig. 1.3 (it becomes 1.4) and the plan's §4 figure list. Two references stay as they are: "The same curves as Fig. 1.1" in the areas caption, and "Fig. 1.1 shows exactly that" at line 521. If the book wants the plan's numbers kept, move the eigenvalue figure to after Fig. 1.3 instead. That costs the reader the plot at the point where Theorem 1.7 needs it. I recommend renumbering.

### 31. The notation tables sit before any symbol is used

Lines 192–275 hold a 30-row table and a 13-item local list, about 600 words, between the motivating §1.1 and the first definition. The reader meets 53 symbols before one of them is used. Move the two tables to a subsection "Notation of this chapter" after §1.6.3 and before Exercises. Leave one sentence at line 192: "A table of every symbol used in this chapter, with the section that defines it, stands before the Exercises." Plan §5.3 item 7 requires the list; it does not fix its position.

### 32. The chapter does not close with what the reader can now do

§1.6.2 traces every result to the rotor and §1.6.3 lists exclusions. Neither states the capability gained. Add, at the end of §1.6.2 (after line 1039), a short list tied to Outcome 1 of the plan:

```html
<p><strong>What you can now do.</strong> (1) Write the swing equation of a machine in per
unit from its moment of inertia and rating, Model&nbsp;1.4. (2) Compute the synchronizing
torque coefficient of a machine against an infinite bus, Lemma&nbsp;1.6. (3) From it,
compute the natural frequency and damping ratio of the swing mode, Theorem&nbsp;1.7.
(4) Decide small-signal stability from the sign of two coefficients. (5) Compute a critical
clearing angle and time by the equal-area criterion, Theorem&nbsp;1.8. Chapter&nbsp;2 asks which of these survive
when the rotor is removed.</p>
```

### 33. The plan's Example 1.1 and 1.2 intermediates carry rounding errors; the chapter is right

`edit_ch1_check.py` recomputes both examples from the fixed inputs. Chapter: `cos δ₀ = 0.881209`, `K_s = 1.4913`, `ω_n = 8.9618 rad/s`, `cos δ_cr = 0.4397`. Plan §4 and HANDOFF: `cos δ₀ = 0.8814`, `K_s = 1.4915`, `ω_n = 8.963`, `cos δ_cr = 0.4401`. The plan rounded `cos δ₀` to 0.8814 (correct is 0.88121) and the error propagated; for `cos δ_cr` the plan rounded three intermediates. The plan's R08 row (`K_s = 1.49`, `ω_n = 8.96`, `ζ = 0.0159`) agrees with the chapter at that precision. The fix stage must leave the chapter's numbers. Record in HANDOFF that the spec's fourth digits are superseded by the chapter's arithmetic, so that the edit2 stage does not flag a mismatch.

### 34. Book-level notation collision: `Δω̄` in Chapter 1, `Δω` in Chapters 3 and 4

Chapter 1 writes the per-unit speed deviation as the single glyph `Δω̄` (34 occurrences) and states that the bar distinguishes it from a perturbation. `ch3.html` writes `Δω` (35 occurrences, as `&Delta;<var>&omega;`) and `ch4.html` writes `Δω` (17 occurrences). The plan's §2 row R02 says "omega-bar deviation", which supports Chapter 1. Resolve in the Chapter 3 and 4 edits, not here. Do not change Chapter 1's glyph.

### 35. Citations: all carry `verify`; six of thirteen support claims outside the plan's assignment for their source

Every citation has four parts and `verify` (13 of 13). Locations are chapter-level only (`Ch. 3`, `Ch. 12`), coarser than the plan's own example `§3.9, Table 3.2`. The plan's "Used for" column assigns S01 to the swing equation, the H range, the local-mode band and the single-machine analysis. It assigns S04 to the equal-area criterion. The chapter also uses them for:

| Line | Source | Claim | Plan assignment | Judgement |
|---|---|---|---|---|
| 330 | S01 Ch. 3 | transient reactance near 0.3 pu | not assigned | plausible value; the location may be a later chapter of S01; human to check |
| 430 | S01 Ch. 15 | torsional modes above 5 Hz | not assigned | plausible; keep verify |
| 492 | S01 Ch. 3 | flux-decay time constant in seconds | not assigned | plausible; keep verify |
| 711 | S01 Ch. 12 | power system stabilisers raise damping | not assigned | plausible; keep verify |
| 1050 | S01 Ch. 12 | excitation can change the damping sign | not assigned | plausible; keep verify |
| 881 | S04 Ch. 2 | fault cleared in 4 to 6 cycles | plan gives no source for this number | value plausible; S04 Ch. 2 may not contain it; highest priority for the human check |

No citation is wrong on its face. The fix stage must not tighten a location from memory. The one location the brief itself supplies is `§3.9, Table 3.2` for the H range (plan §5.2 example). The fix stage may use it at lines 330, 379 and 1095, with the plan as the source of that location. It must keep `verify`.

### 36. File name and length

The file is `ch1.html`; plan §5.3 names `ch01.html` and the link checker `scripts/check_book_links.py` will look for that name. Rename at the link pass, as the draft flagged. Length: 8,310 words by `edit_ch1_html.py` (prose, tables and captions, SVG excluded), 7,344 by the draft's count. The plan target is 6,500 ± 20 % (5,200 to 7,800). Item 31 moves 600 words but does not remove them. The D/D_load/D_v/D_eq entry of the local list (lines 265–272) repeats the §1.3 note (lines 438–446); cut one of the two.

### 37. Not checked

No browser rendering check at 360 px was made, by the task's rule (parser only). The draft did not make one either. The fix stage should open the file at 360 px once and confirm no horizontal page scroll (plan §5.3 item 6).

---

## Part 4 — What already works

38. Theorem 1.7 (lines 616–669): full linearisation, elimination to a scalar second-order equation, and coefficient matching. Routh–Hurwitz carries the stability claim. Both boundary cases are stated (`K_D = 0` marginal; `K_s < 0` one positive real root). This is the standard the rest of the book should copy.
39. Example 1.2, Step 4 (lines 866–871): the two areas are computed separately and agree to six digits. That is the equal-area criterion made checkable with a pen.
40. The excluded-convention note (lines 448–460) with Exercise 3: the factor-377 trap is named, excluded, and then demonstrated on the chapter's own numbers.
41. Fig. 1.4 caption (lines 745–759): the axis stretch is stated, so the reader does not misread a circle as a line. Every plotted number is printed.
42. §1.6.2 table (lines 1018–1030): every result traced to the rotor, which is the sentence the whole book hangs on.
43. Status labels on all 11 results; `data-rid` R01 to R11 in order; 14 equation numbers, each referenced. 13 citations, each with four parts and `verify`. Zero external assets, zero parse errors.
44. Definition 1.3's reading of `H` as "the time for which the machine could supply its own rated power" (lines 373–376) is exact and concrete.
45. §1.1 opens with a physical event (a kettle and a turbine shaft), states the two questions the chapter answers, and says which section answers each.

---

## Part 5 — Numbers recomputed

Counting rule: one row per printed value per computation. The value 0.17009 s appears at two lines (974, 1139) from one computation and counts once. Tolerance: half a unit in the last printed digit. Rows marked **wrong** are the three arithmetic mismatches of item 8 and the bisection value of item 3. Plan-versus-chapter comparisons are in the second table and do not count against the chapter.

Totals: 119 chapter numbers checked, 115 ok, 4 wrong.

### Chapter numbers

| # | Location | Quantity | Printed | Recomputed | Result |
|---|---|---|---|---|---|
| 1 | §1.2 Definition 1.1 | omega0 | 376.9911 | 376.9911 | ok |
| 2 | Example 1.1 | X | 0.65 | 0.65 | ok |
| 3 | Example 1.1 | Pmax_pre | 1.6923 | 1.692308 | ok |
| 4 | Example 1.1 | Pmax_pre 6dp | 1.692308 | 1.692308 | ok |
| 5 | Example 1.1 | sin d0 | 0.472727 | 0.4727273 | ok |
| 6 | Example 1.1 | d0 rad | 0.492383 | 0.4923831 | ok |
| 7 | Example 1.1 | d0 deg | 28.211 | 28.21148 | ok |
| 8 | Example 1.1 | cos d0 | 0.881209 | 0.8812088 | ok |
| 9 | Example 1.1 | Ks | 1.4913 | 1.491276 | ok |
| 10 | Example 1.1 | Ks 6dp | 1.491276 | 1.491276 | ok |
| 11 | Example 1.1 | Ks*w0 | 562.198 | 562.198 | ok |
| 12 | Example 1.1 | Ks*w0/2H | 80.314 | 80.31399 | ok |
| 13 | Example 1.1 | wn | 8.9618 | 8.961808 | ok |
| 14 | Example 1.1 | wn Hz | 1.4263 | 1.426316 | ok |
| 15 | Example 1.1 | 4Hwn | 125.465 | 125.4653 | ok |
| 16 | Example 1.1 | zeta | 0.015941 | 0.01594066 | ok |
| 17 | Example 1.1 | -zeta*wn | -0.142857 | -0.1428571 | ok |
| 18 | Example 1.1 | zeta^2 | 0.000254 | 0.0002541047 | ok |
| 19 | Example 1.1 | wd | 8.9607 | 8.960669 | ok |
| 20 | Example 1.1 | period | 0.7012 | 0.701196 | ok |
| 21 | Example 1.1 | tau | 7.0 | 7 | ok |
| 22 | Example 1.1 | periods in tau | 9.98 | 9.982943 | ok |
| 23 | Example 1.1 | exp(-1)% | 36.8 | 36.78794 | ok |
| 24 | Example 1.1 | 1.6% | 1.6 | 1.594066 | ok |
| 25 | Fig. 1.4 (eigenvalues) | KD=0 re | 0 | 0 | ok |
| 26 | Fig. 1.4 (eigenvalues) | KD=0 im | 8.9618 | 8.961808 | ok |
| 27 | Fig. 1.4 (eigenvalues) | KD=0 zeta | 0 | 0 | ok |
| 28 | Fig. 1.4 (eigenvalues) | KD=2 re | -0.1429 | -0.1428571 | ok |
| 29 | Fig. 1.4 (eigenvalues) | KD=2 im | 8.9607 | 8.960669 | ok |
| 30 | Fig. 1.4 (eigenvalues) | KD=2 zeta | 0.01594 | 0.01594066 | ok |
| 31 | Fig. 1.4 (eigenvalues) | KD=10 re | -0.7143 | -0.7142857 | ok |
| 32 | Fig. 1.4 (eigenvalues) | KD=10 im | 8.9333 | 8.933297 | ok |
| 33 | Fig. 1.4 (eigenvalues) | KD=10 zeta | 0.0797 | 0.07970331 | ok |
| 34 | Fig. 1.4 (eigenvalues) | KD=30 re | -2.1429 | -2.142857 | ok |
| 35 | Fig. 1.4 (eigenvalues) | KD=30 im | 8.7018 | 8.701848 | ok |
| 36 | Fig. 1.4 (eigenvalues) | KD=30 zeta | 0.23911 | 0.2391099 | ok |
| 37 | Fig. 1.4 (eigenvalues) | KD=2 px x | 451.8 | 451.8095 | ok |
| 38 | Fig. 1.4 (eigenvalues) | KD=2 px y | 34.0 | 34.01527 | ok |
| 39 | Fig. 1.4 (eigenvalues) | KD=10 px x | 373.5 | 373.4476 | ok |
| 40 | Fig. 1.4 (eigenvalues) | KD=10 px y | 34.4 | 34.38484 | ok |
| 41 | Fig. 1.4 (eigenvalues) | KD=30 px x | 177.6 | 177.5429 | ok |
| 42 | Fig. 1.4 (eigenvalues) | KD=30 px y | 37.5 | 37.50981 | ok |
| 43 | Example 1.2 | Pmax_post | 1.2941 | 1.294118 | ok |
| 44 | Example 1.2 | Pmax_post 6dp | 1.294118 | 1.294118 | ok |
| 45 | Example 1.2 | 0.8/Pp | 0.618182 | 0.6181818 | ok |
| 46 | Example 1.2 | near crossing rad | 0.666427 | 0.6664275 | ok |
| 47 | Example 1.2 | near crossing deg | 38.183 | 38.18348 | ok |
| 48 | Example 1.2 | dmax rad | 2.475165 | 2.475165 | ok |
| 49 | Example 1.2 | dmax deg | 141.817 | 141.8165 | ok |
| 50 | Example 1.2 | dmax-d0 | 1.982782 | 1.982782 | ok |
| 51 | Example 1.2 | Pm(dmax-d0) | 1.586226 | 1.586226 | ok |
| 52 | Example 1.2 | cos dmax | -0.786035 | -0.7860351 | ok |
| 53 | Example 1.2 | Pp cos dmax | -1.017222 | -1.017222 | ok |
| 54 | Example 1.2 | numerator | 0.569004 | 0.5690037 | ok |
| 55 | Example 1.2 | cos dcr | 0.439685 | 0.4396847 | ok |
| 56 | Example 1.2 | dcr rad | 1.115549 | 1.115549 | ok |
| 57 | Example 1.2 | dcr deg | 63.916 | 63.91624 | ok |
| 58 | Example 1.2 | dcr-d0 | 0.623166 | 0.6231656 | ok |
| 59 | Example 1.2 | Aacc | 0.498533 | 0.4985325 | ok |
| 60 | Example 1.2 | dmax-dcr | 1.359616 | 1.359616 | ok |
| 61 | Example 1.2 | Pp(cos dcr - cos dmax) | 1.586226 | 1.586226 | ok |
| 62 | Example 1.2 | Pm(dmax-dcr) | 1.087693 | 1.087693 | ok |
| 63 | Example 1.2 | Adec | 0.498533 | 0.4985325 | ok |
| 64 | Example 1.2 | 14*(dcr-d0) exact | 8.724319 | 8.724319 | ok — the unrounded product; what the draft actually printed |
| 65 | Example 1.2 | 14*0.623166 as printed | 8.724319 | 8.724324 | **wrong** — printed operands give 8.724324 (item 8) |
| 66 | Example 1.2 | w0*Pm | 301.5929 | 301.5929 | ok |
| 67 | Example 1.2 | tcr^2 | 0.0289275 | 0.02892747 | ok |
| 68 | Example 1.2 | tcr | 0.170081 | 0.1700808 | ok |
| 69 | Example 1.2 | cycles | 10.205 | 10.20485 | ok |
| 70 | Example 1.2 | 1/60 | 0.016667 | 0.01666667 | ok |
| 71 | Example 1.2 | half-H factor | 0.7071 | 0.7071068 | ok |
| 72 | Example 1.2 | half-H tcr | 0.1203 | 0.1202653 | ok |
| 73 | Example 1.2 | half-H cycles | 7.2 | 7.215916 | ok |
| 74 | Example 1.2 | ratio 10.2/6 | 1.7 | 1.700833 | ok |
| 75 | Fig. 1.1 (SVG coordinates) | x d0 | 135.2 | 135.2306 | ok |
| 76 | Fig. 1.1 (SVG coordinates) | x near post | 161.8 | 161.8226 | ok |
| 77 | Fig. 1.1 (SVG coordinates) | x dmax | 438.2 | 438.1774 | ok |
| 78 | Fig. 1.1 (SVG coordinates) | y Pm | 170 | 170 | ok |
| 79 | Fig. 1.1 (SVG coordinates) | y Pmax_pre | 36.2 | 36.15385 | ok |
| 80 | Fig. 1.1 (SVG coordinates) | y Pmax_post | 95.9 | 95.88235 | ok |
| 81 | Fig. 1.2 (SVG coordinates) | x dcr | 230.4 | 230.4433 | ok |
| 82 | Fig. 1.2 (SVG coordinates) | y post at dcr | 115.7 | 115.6528 | ok |
| 83 | Exercise 1 | cos95 | -0.087156 | -0.08715574 | ok |
| 84 | Exercise 1 | cos95 7dp | -0.0871557 | -0.08715574 | ok |
| 85 | Exercise 1 | Ks95 | -0.147494 | -0.1474943 | ok |
| 86 | Exercise 1 | KD/2H | 0.285714 | 0.2857143 | ok |
| 87 | Exercise 1 | Ks w0/2H | -7.943436 | -7.943436 | ok |
| 88 | Exercise 1 | root+ | 2.679 | 2.679171 | ok |
| 89 | Exercise 1 | root- | -2.965 | -2.964886 | ok |
| 90 | Exercise 2 | wm | 188.4956 | 188.4956 | ok |
| 91 | Exercise 2 | rpm | 1800 | 1800 | ok |
| 92 | Exercise 2 | Ekin MJ | 88.826 | 88.82644 | ok |
| 93 | Exercise 2 | H | 0.44413 | 0.4441322 | ok |
| 94 | Exercise 2 | 22% | 22 | 22.20661 | ok |
| 95 | Exercise 2 | 12.7% | 12.7 | 12.68949 | ok |
| 96 | Exercise 3 | w0*zeta exact | 6.0095 | 6.009488 | ok — the unrounded product |
| 97 | Exercise 3 | w0*0.015941 as printed | 6.0095 | 6.009615 | **wrong** — printed operands give 6.0096 (item 8) |
| 98 | Exercise 3 | factor 377 | 377 | 376.9911 | ok |
| 99 | Exercise 5 | H=2.0 wn | 11.8554 | 11.85536 | ok |
| 100 | Exercise 5 | H=2.0 Hz | 1.8868 | 1.886839 | ok |
| 101 | Exercise 5 | H=2.0 zeta | 0.02109 | 0.02108751 | ok |
| 102 | Exercise 5 | H=3.5 wn | 8.9618 | 8.961808 | ok |
| 103 | Exercise 5 | H=3.5 Hz | 1.4263 | 1.426316 | ok |
| 104 | Exercise 5 | H=3.5 zeta | 0.01594 | 0.01594066 | ok |
| 105 | Exercise 5 | H=6.0 wn | 6.8447 | 6.844694 | ok |
| 106 | Exercise 5 | H=6.0 Hz | 1.0894 | 1.089367 | ok |
| 107 | Exercise 5 | H=6.0 zeta | 0.01217 | 0.01217488 | ok |
| 108 | Exercise 5 | H=8.0 wn | 5.9277 | 5.927679 | ok |
| 109 | Exercise 5 | H=8.0 Hz | 0.9434 | 0.9434193 | ok |
| 110 | Exercise 5 | H=8.0 zeta | 0.01054 | 0.01054376 | ok |
| 111 | Exercise 5 | exponent wn (exact) | -0.5 | -0.5 | ok |
| 112 | Exercise 5 | exponent wn (printed 5.9277/11.8554) | -0.5 | -0.5 | ok |
| 113 | Exercise 5 | exponent zeta (exact) | -0.5 | -0.5 | ok — with unrounded ζ values |
| 114 | Exercise 5 | exponent zeta (printed 0.010540/0.021090) | -0.5 | -0.5003421 | **wrong** — printed operands give −0.50034 (item 8) |
| 115 | Fig. 1.3 (integration) | 0.15s first peak deg | 106.7 | 106.7061 | ok |
| 116 | Fig. 1.3 (integration) | 0.19s cross 200deg time | 0.5662 | 0.56615 | ok |
| 117 | Fig. 1.3 (integration) | 0.19s angle at 1.2s | 1206 | 1206.083 | ok |
| 118 | Fig. 1.3 (integration) | bisection tcr | 0.17009 | 0.1701045 | **wrong** — depends on an unstated window: RK2 10 μs gives 0.170265 (1.2 s), 0.170105 (1.5 s), 0.170085 (3 s); RK4 converges to 0.170081 (item 3) |
| 119 | Fig. 1.3 (integration) | y start px | 251.9 | 251.9145 | ok |

Chapter rows: 119; wrong: 4.

### Plan §4 values compared with the chapter (not counted against the chapter)

| Quantity | Plan prints | Recomputed from fixed inputs | Chapter prints | Judgement |
|---|---|---|---|---|
| Ks 1.4915 | 1.4915 | 1.49128 | 1.4913 | chapter is right; plan rounded an intermediate (item 33) |
| wn 8.963 | 8.963 | 8.96181 | 8.9618 | chapter is right; plan rounded an intermediate (item 33) |
| cos dcr 0.4401 | 0.4401 | 0.439685 | 0.439685 | chapter is right; plan rounded an intermediate (item 33) |

