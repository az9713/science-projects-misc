VERDICT: ACCEPT WITH CHANGES — the arithmetic and the two central theorems hold; eleven located defects (five derivation gaps, one symbol collision, one wrong bandwidth-versus-power relation, four smaller items) must be applied before a reader new to power systems can follow every step.

# Chapter 2 edit — Inverter-based resources and the limit of following

File judged: `p1-textbook/ch2.html` (736 lines, 102,943 bytes, read in full). Line numbers below are lines of that file. Editor: Fable, `science-editor` skill. Written 2026-09-22. Scratch files: `edit_ch2_check.py`, `edit_ch2_html.py`, `edit_ch2_numbers.tsv` in the session scratchpad.

Domain brief used: `book-plan.md` section 4 (Chapter 2 spec), section 3 (notation table), section 5 (rules), section 2 (result graph); `HANDOFF.md`; the chapter 2 entry of `draft-results.json`. I did not open any of the sources S01 to S20. Every citation judgement below is a plausibility judgement, not a page check.

---

## Verdict

**ACCEPT WITH CHANGES.** The arithmetic is right (185 numbers recomputed, 4 wrong, all in the last printed digit or in one range statement), every result carries its R identifier, its assumptions and a status label, and the two central theorems hold under test. Five derivation gaps, one symbol collision and one wrong relation stop a reader who is new to power systems: equation (2.13) is stated and not derived; the angle θ_p is never tied to the state θ_pll, so (2.9) and (2.17) cannot be reproduced from (2.8) with a pen; Definition 2.5 fixes V_g = 1 to obtain X_g = 1/SCR while Theorem 2.7 carries V_g as a symbol; Corollary 2.10 omits its timescale hypothesis; the bare symbol V means a peak amplitude in §2.1 and the infinite-bus voltage in the K_s formula, where Chapter 1 writes V_inf; and lines 507 and 708 say bandwidth falls by the same fraction as power, when it falls as the square root (25.7 % against 44.7 % at SCR = 1.2, by the chapter's own equation (2.19)). After the eleven blocking items below are applied, the target reader can learn this subject from these pages.

---

## 1. Blocking defects

Each item gives the location, the defect, the missing part of the five-part standard, and the full replacement text. The replacement text is plain HTML with `<var>` and `<sub>`, the chapter's own medium. Apply the items in this order.

### B1. Equation (2.13) is stated, not derived — ch2.html:335-336 and 345

**Defect.** Model 2.6 writes `v_d + jv_q = V_g e^{-jθ_p} + jX_g I_d` with no step between it and Definition 2.1. A reader new to the field cannot produce it. Three lines are missing: the complex form of the Park transform, the grid source seen in the loop frame, and Kirchhoff's voltage law across X_g with the current direction stated. The status label "derived here" overclaims until these lines land. Part 3 of the standard (proof in the smallest setting) is missing. The whole chapter rests on this equation.

**Replace line 335 with:**

```html
<p>The converter injects a constant current in its own phase-locked-loop frame: <var>I</var><sub>d</sub> on the d axis and <var>I</var><sub>q</sub> = 0 on the q axis. Operation is therefore at unity power factor <em>as the loop sees it</em>. The grid is a source of magnitude <var>V</var><sub>g</sub> at angle <var>&theta;</var><sub>g</sub> in the stationary frame, behind a reactance <var>X</var><sub>g</sub> = 1/SCR. The loop's frame sits at angle <var>&theta;</var><sub>pll</sub>. Let <var>&theta;</var><sub>p</sub> = <var>&theta;</var><sub>pll</sub> &minus; <var>&theta;</var><sub>g</sub> be the angle of the loop's frame measured from the grid source phasor.</p>
<p><strong>Derivation of the point-of-connection voltage.</strong> Three lines give it.</p>
<ol>
<li><em>The Park transform in complex form.</em> Multiply the second row of equation (2.2) by <var>j</var> and add it to the first row: <var>v</var><sub>d</sub> + <var>jv</var><sub>q</sub> = (cos <var>&theta;</var> &minus; <var>j</var> sin <var>&theta;</var>)(<var>v</var><sub>&alpha;</sub> + <var>jv</var><sub>&beta;</sub>) = e<sup>&minus;<var>j&theta;</var></sup>(<var>v</var><sub>&alpha;</sub> + <var>jv</var><sub>&beta;</sub>). A dq pair is the stationary complex phasor rotated back by the frame angle. The rotation is linear, so a sum of phasors rotates term by term.</li>
<li><em>The grid source in the loop frame.</em> A balanced set of peak value <var>V</var><sub>g</sub> at angle <var>&theta;</var><sub>g</sub> has <var>v</var><sub>&alpha;</sub> + <var>jv</var><sub>&beta;</sub> = <var>V</var><sub>g</sub>e<sup><var>j&theta;</var><sub>g</sub></sup> by equation (2.1); &sect;2.1 checked this at three instants. Line 1 with <var>&theta;</var> = <var>&theta;</var><sub>pll</sub> gives <var>V</var><sub>g</sub>e<sup><var>j</var>(<var>&theta;</var><sub>g</sub> &minus; <var>&theta;</var><sub>pll</sub>)</sup> = <var>V</var><sub>g</sub>e<sup>&minus;<var>j&theta;</var><sub>p</sub></sup>.</li>
<li><em>Kirchhoff's voltage law across <var>X</var><sub>g</sub>.</em> The current flows from the converter through <var>X</var><sub>g</sub> into the source. In the loop frame that current is the real number <var>I</var><sub>d</sub>. The voltage across a reactance is <var>j</var> times the reactance times the current, so the point-of-connection voltage exceeds the source voltage by <var>jX</var><sub>g</sub><var>I</var><sub>d</sub>.</li>
</ol>
<p>Add lines 2 and 3. The point-of-connection voltage in the loop's frame is</p>
```

**Replace line 337 (assumptions) with:**

```html
<p><strong>Assumptions.</strong> (1) The inner current loop is infinitely fast, so <var>i</var><sub>d</sub> = <var>I</var><sub>d</sub> at every instant (timescale separation, &sect;2.3). (2) The grid impedance is purely inductive. (3) The converter provides no reactive current: <var>I</var><sub>q</sub> = 0. (4) The system is balanced and at fundamental frequency. (5) The grid source runs at the rated frequency, so d<var>&theta;</var><sub>g</sub>/d<var>t</var> = <var>&omega;</var><sub>0</sub> and d<var>&theta;</var><sub>p</sub>/d<var>t</var> = <var>&omega;</var><sub>pll</sub> &minus; <var>&omega;</var><sub>0</sub>.</p>
```

**Replace line 345 (status) with:**

```html
<span class="status">Status: model, derived here from Definition 2.1, Definition 2.5, equation (2.6) and Kirchhoff's voltage law. Omissions 1 and 2 are repaid later in this chapter.</span>
```

### B2. θ_p is never tied to θ_pll and ω_0 — ch2.html:144, 301-305, 451-452

**Defect.** Definition 2.4 writes the loop in the state θ_pll. Equations (2.9) and (2.17) are in θ_p. The relation θ_p = θ_pll − θ_g, the consequence dθ_p/dt = ω_pll − ω_0, and the hypothesis that the grid runs at ω_0 appear nowhere. The sentence at line 303, "Substitute into equation (2.8) and differentiate once", cannot be executed with a pen. Part 3 of the standard is missing; an assumption is unstated.

**Replace line 144 (local notation entry) with two entries:**

```html
<li><var>&theta;</var><sub>g</sub> &mdash; angle of the grid Thevenin source phasor in the stationary frame, in rad. Under Model 2.6 assumption (5) the grid runs at rated frequency, so d<var>&theta;</var><sub>g</sub>/d<var>t</var> = <var>&omega;</var><sub>0</sub>.</li>
<li><var>&theta;</var><sub>p</sub> &mdash; angle of the phase-locked-loop reference frame measured from the grid source phasor, <var>&theta;</var><sub>p</sub> = <var>&theta;</var><sub>pll</sub> &minus; <var>&theta;</var><sub>g</sub>, in rad. Its time derivative is <var>&omega;</var><sub>pll</sub> &minus; <var>&omega;</var><sub>0</sub>. Its steady-state value is <var>&theta;</var><sub>0</sub>, which <em>is</em> in the book table.</li>
```

**Replace lines 301-303 with:**

```html
<p>Take the stiff-grid case first. Let the grid behind the point of connection be stiff, so the point-of-connection voltage is a fixed phasor of magnitude <var>V</var><sub>g</sub> at angle <var>&theta;</var><sub>g</sub> in the stationary frame, whatever current the converter injects. Let the grid run at rated frequency: d<var>&theta;</var><sub>g</sub>/d<var>t</var> = <var>&omega;</var><sub>0</sub>. Let <var>&theta;</var><sub>p</sub> = <var>&theta;</var><sub>pll</sub> &minus; <var>&theta;</var><sub>g</sub> be the angle of the loop's frame measured from that phasor, so that d<var>&theta;</var><sub>p</sub>/d<var>t</var> = <var>&omega;</var><sub>pll</sub> &minus; <var>&omega;</var><sub>0</sub>.</p>
<p>Apply the Park transform (2.2) with <var>&theta;</var> = <var>&theta;</var><sub>pll</sub> to the phasor <var>v</var><sub>&alpha;</sub> = <var>V</var><sub>g</sub> cos <var>&theta;</var><sub>g</sub>, <var>v</var><sub>&beta;</sub> = <var>V</var><sub>g</sub> sin <var>&theta;</var><sub>g</sub>. The second row gives <var>v</var><sub>q</sub> = <var>V</var><sub>g</sub>(&minus;sin <var>&theta;</var><sub>pll</sub> cos <var>&theta;</var><sub>g</sub> + cos <var>&theta;</var><sub>pll</sub> sin <var>&theta;</var><sub>g</sub>) = <var>V</var><sub>g</sub> sin(<var>&theta;</var><sub>g</sub> &minus; <var>&theta;</var><sub>pll</sub>) = &minus;<var>V</var><sub>g</sub> sin <var>&theta;</var><sub>p</sub>. For small <var>&theta;</var><sub>p</sub>, <var>v</var><sub>q</sub> &asymp; &minus;<var>V</var><sub>g</sub><var>&theta;</var><sub>p</sub>.</p>
<p>Subtract <var>&omega;</var><sub>0</sub> from both sides of equation (2.8). The left side becomes d<var>&theta;</var><sub>p</sub>/d<var>t</var>:</p>
<p style="padding-left:.5rem">d<var>&theta;</var><sub>p</sub>/d<var>t</var> = <var>k</var><sub>p,pll</sub><var>v</var><sub>q</sub> + <var>k</var><sub>i,pll</sub>&int;<var>v</var><sub>q</sub> d<var>t</var>.</p>
<p>Substitute <var>v</var><sub>q</sub> &asymp; &minus;<var>V</var><sub>g</sub><var>&theta;</var><sub>p</sub> and differentiate once with respect to time: d<sup>2</sup><var>&theta;</var><sub>p</sub>/d<var>t</var><sup>2</sup> + <var>V</var><sub>g</sub><var>k</var><sub>p,pll</sub> d<var>&theta;</var><sub>p</sub>/d<var>t</var> + <var>V</var><sub>g</sub><var>k</var><sub>i,pll</sub><var>&theta;</var><sub>p</sub> = 0. With &Delta;<var>&theta;</var><sub>p</sub> the deviation of <var>&theta;</var><sub>p</sub> from zero, the closed loop has the characteristic polynomial</p>
```

Line 305, equation (2.9), stays as it is.

**Replace lines 451-452 (opening of the proof of Theorem 2.8) with:**

```html
<p>Write <var>&theta;</var><sub>p</sub> = <var>&theta;</var><sub>0</sub> + &Delta;<var>&theta;</var><sub>p</sub> and <var>v</var><sub>q</sub> = 0 + &Delta;<var>v</var><sub>q</sub>. Equation (2.16) gives &Delta;<var>v</var><sub>q</sub> = &minus;<var>K</var><sub>pll</sub>&Delta;<var>&theta;</var><sub>p</sub> to first order. By Model 2.6 assumption (5), d<var>&theta;</var><sub>p</sub>/d<var>t</var> = <var>&omega;</var><sub>pll</sub> &minus; <var>&omega;</var><sub>0</sub>. At the operating point <var>v</var><sub>q</sub> = 0, <var>&omega;</var><sub>pll</sub> = <var>&omega;</var><sub>0</sub>, and the integrator output in equation (2.8) is zero. Subtract that operating point from equation (2.8). The loop reads, in deviation form,</p>
<p style="padding-left:.5rem">d(&Delta;<var>&theta;</var><sub>p</sub>)/d<var>t</var> = <var>k</var><sub>p,pll</sub>&Delta;<var>v</var><sub>q</sub> + <var>k</var><sub>i,pll</sub>&int;&Delta;<var>v</var><sub>q</sub> d<var>t</var>.</p>
```

**Replace line 443 (statement of Theorem 2.8, first sentence) with:**

```html
<p>Linearise the loop of Definition 2.4 about the operating point of Theorem 2.7, under Model 2.6 including assumption (5), with fixed gains <var>k</var><sub>p,pll</sub> and <var>k</var><sub>i,pll</sub>. The closed-loop characteristic polynomial in the angle deviation &Delta;<var>&theta;</var><sub>p</sub> is</p>
```

### B3. Definition 2.5 fixes V_g = 1 to reach X_g = 1/SCR, while Theorem 2.7 carries V_g as a symbol — ch2.html:322-323

**Defect.** Line 322 reads "take V_g = 1 pu. Then S_sc = V_g²/X_g in per unit, so X_g = 1/SCR". If S_sc were tied to the actual V_g, then X_g = V_g²/SCR, and the bound X_g I_d ≤ V_g of Theorem 2.7 would read I_d ≤ SCR/V_g, not I_d ≤ SCR · V_g. The chapter is saved only because every example sets V_g = 1. The precise statement (part 1 of the standard) is missing. The fix is to define S_sc at the nominal voltage, 1 pu on the converter base, which is how the short-circuit level is computed in practice; then (2.12) holds for any V_g and the theorem's symbolic V_g is legitimate. This tightens the plan's wording ("on the converter base, SCR = 1/X_g"); it does not depart from it.

**Replace lines 322-324 with:**

```html
<p>Take the grid Thevenin impedance to be purely inductive, so <var>R</var><sub>g</sub> = 0 and <var>Z</var><sub>g</sub> = <var>X</var><sub>g</sub>. The short-circuit level is computed at the <em>nominal</em> voltage of the point of connection, which is 1 pu on the converter base, not at the actual source magnitude <var>V</var><sub>g</sub>. Express <var>X</var><sub>g</sub> in per unit on the converter base <var>S</var><sub>rated</sub>. Then <var>S</var><sub>sc</sub> = 1<sup>2</sup>/<var>X</var><sub>g</sub> = 1/<var>X</var><sub>g</sub> in per unit, and <var>S</var><sub>rated</sub> = 1 pu, so</p>
<div class="eqn"><div class="eqbody"><var>X</var><sub>g</sub> = 1 / SCR&nbsp;&nbsp; (per unit, on the converter base; <var>S</var><sub>sc</sub> taken at nominal voltage 1 pu)</div><div class="eqno">(2.12)</div></div>
<p>Equation (2.12) holds whatever the actual value of <var>V</var><sub>g</sub>, because the definition of <var>S</var><sub>sc</sub> uses the nominal voltage and not <var>V</var><sub>g</sub>. The theorems of this chapter therefore carry <var>V</var><sub>g</sub> as a symbol; the examples set <var>V</var><sub>g</sub> = 1 pu. The nominal-voltage definition follows <span class="cite">[S19, IEEE Std 1204-1997, <i>Guide for Planning DC Links Terminating at AC Locations Having Low Short-Circuit Capacities</i>, definition of short-circuit ratio &mdash; verify]</span>.</p>
<p>Equation (2.11) is the planner's number and equation (2.12) is the control engineer's. A planner reports a short-circuit level in megavolt-amperes. A control engineer needs a per-unit reactance. Equation (2.12) converts one into the other.</p>
```

Note for the verifier: the locator "definition of short-circuit ratio" in the S19 citation above is editor-supplied and unverified, like every other locator in the chapter. I did not open the guide.

### B4. Bare V has two meanings, and the K_s formula mismatches Chapter 1 — ch2.html:113, 118, 181, 183, 187, 425, 698

**Defect.** Lines 181, 183 and 187 use V as the peak value of the balanced set in §2.1. Lines 113, 118, 425 and 698 write K_s = (E′V/X) cos δ_0, where V is the infinite-bus voltage. `ch1.html:1070` writes that same coefficient as K_s = (E′V_inf/X) cos δ_0, and `ch1.html:227` lists V_inf in its notation table. So V carries two meanings inside this chapter and the cross-chapter formula does not match Chapter 1. Notation is a contract (part 2 of the standard). Neither meaning of bare V appears in the local notation list.

**Fix, seven places:**

- Line 181: replace `Put <var>v</var><sub>a</sub> = <var>V</var> cos(` with `Put <var>v</var><sub>a</sub> = <var>V</var><sub>m</sub> cos(` and after `240&deg;.` add ` Here <var>V</var><sub>m</sub> is the peak value of the set, in pu.`
- Line 183: replace `<var>v</var><sub>d</sub> = <var>V</var>,` with `<var>v</var><sub>d</sub> = <var>V</var><sub>m</sub>,`.
- Line 187: replace `and <var>V</var> = 1 pu` with `and <var>V</var><sub>m</sub> = 1 pu`.
- Lines 113, 118, 425, 698: replace every `(<var>E</var>&prime;<var>V</var>/<var>X</var>)` with `(<var>E</var>&prime;<var>V</var><sub>inf</sub>/<var>X</var>)`.
- Line 118: after the first occurrence of `cos <var>&delta;</var><sub>0</sub>` insert `, with <var>V</var><sub>inf</sub> the infinite-bus voltage of Chapter 1,`.
- Local notation list, insert after the entry for |v| (line 148):

```html
<li><var>V</var><sub>m</sub> &mdash; peak value of a balanced three-phase set, in pu. Used in &sect;2.1 and Fig. 2.1 only.</li>
<li><var>V</var><sub>inf</sub> &mdash; infinite-bus voltage magnitude of Chapter 1, in pu. Appears here only inside the Chapter 1 formula for <var>K</var><sub>s</sub> (<span class="rid">R06</span>).</li>
```

### B5. Corollary 2.10 omits its timescale hypothesis — ch2.html:613, 617, 624

**Defect.** Item 1 argues "to first order dP/dδ = 0" because the loop re-aligns the frame. That holds only after the loop has settled, so the corollary needs the loop to be fast compared with the swing mode it is compared against. The hypothesis is unstated (part 4 of the standard: where the hypotheses bind). The numbers exist: the loop runs at 7.4 Hz to 10 Hz here; Example 1.1 (R08) has the swing mode at 1.43 Hz (`ch1.html:704`).

**Replace line 613 with:**

```html
<p>Under Model 2.6, and with the phase-locked loop fast compared with the swing mode of Chapter 1 &mdash; here 7.4 Hz to 10 Hz against 1.43 Hz in Example 1.1 (<span class="rid">R08</span>) &mdash; a population of grid-following converters contributes no synchronizing torque coefficient and no inertia constant to the system of Chapter 1, whatever its installed capacity.</p>
```

**Replace line 617 (item 1) with:**

```html
<li><strong>Synchronizing torque coefficient.</strong> <span class="rid">R06</span> defines <var>K</var><sub>s</sub> = d<var>P</var><sub>e</sub>/d<var>&delta;</var> at <var>&delta;</var><sub>0</sub>, the change in exported power caused by a change in the unit's <em>own</em> angle against the system. Model 2.6 fixes the exported current at <var>I</var><sub>d</sub>, <var>I</var><sub>q</sub> in the unit's own frame, and the loop re-aligns that frame onto whatever angle the grid presents. On the swing-mode timescale the loop has settled: its 2 % settling time is about 4/(<var>&zeta;</var><sub>pll</sub><var>&omega;</var><sub>n,pll</sub>) = 4/(0.7071 &middot; 62.83) = 0.090 s on a stiff grid and 4/(0.5257 &middot; 46.71) = 0.163 s at SCR = 1.2, against a swing period of 1/1.43 Hz = 0.70 s. Perturb the grid angle slowly on that scale and the converter follows it. Its injected current phasor rotates with the grid. To first order d<var>P</var>/d<var>&delta;</var> = 0. The converter supplies no restoring term. The separation here is a factor of 5 to 7 in frequency, against the factor of 50 that &sect;2.3 uses between the current loop and the angle loop; this hypothesis binds more tightly than that one. What happens inside the 0.09 s to 0.16 s of the loop's own transient is therefore handed to Cited Result 2.9 and is not settled by this corollary.</li>
```

**Replace line 624 (status) with:**

```html
<span class="status">Status: proved here, under the assumptions of Model 2.6 and the timescale hypothesis stated above, by comparison with R03, R04, R06 and R07.</span>
```

### B6. "Every weak-grid symptom falls out of K_pll" contradicts §2.6.3 — ch2.html:134

**Defect.** Line 134 says every weak-grid symptom follows from K_pll. Section 2.6.3 and Cited Result 2.9 say the oscillatory instability does not. The sentence is a wrong statement about the chapter's own scope, and it blurs the theory-versus-evidence line the plan requires.

**Replace line 134 with:**

```html
<p>This chapter answers that with one scalar. Build the current-source model, write the angle-loop equation, and every weak-grid symptom that the static model contains falls out of the single quantity <var>K</var><sub>pll</sub> = <var>V</var><sub>g</sub> cos <var>&theta;</var><sub>0</sub>: the loss of terminal voltage, the loss of export power, and the loss of loop bandwidth and damping. Grid strength enters the control loop of that model through this one number and nowhere else. The number is also the terminal voltage magnitude, and at unity power factor it is also the delivered power in per unit. One collapse therefore takes voltage, power, and control bandwidth together. One symptom is <em>not</em> among these: the oscillatory instability that a fuller model predicts. Section 2.6.3 says why, and what the static model cannot claim.</p>
```

### B7. Wrong range for the fault-current ratio — ch2.html:279

**Defect.** "1.1 to 1.3 pu against 5 to 7 pu, so the converter carries between 0.220 and 0.186 of the machine's fault current." The printed pair divides 1.1 by 5 and 1.3 by 7. The range of the ratio over both intervals is 1.1/7 = 0.157 to 1.3/5 = 0.260. The printed figures are not the range. Recomputed in `edit_ch2_check.py`.

**Replace the two sentences `Compare the two directly: ... of the machine's fault current.` in line 279 with:**

```html
Compare the two directly: 1.1 to 1.3 pu against 5 to 7 pu. The converter's fault current is between 0.157 (1.1/7) and 0.260 (1.3/5) of the machine's.
```

### B8. Citation breaks the four-part rule of plan §5.2 — ch2.html:635

**Defect.** `[S07, Zhang, Harnefors and Nee 2010, IEEE Trans. Power Systems 25(2), 809–820 — verify]` lacks the title and the location. The rule requires source id, author and year, title, and location.

**Replace the citation span in line 635 with:**

```html
<span class="cite">[S07, Zhang, Harnefors and Nee 2010, "Power-Synchronization Control of Grid-Connected Voltage-Source Converters," <i>IEEE Trans. Power Systems</i> 25(2), 809&ndash;820, weak-grid limit section &mdash; verify]</span>
```

### B9. Symbols used before definition in the summary card and the problem statement — ch2.html:107-113, 132-134

**Defect.** Check (a) of the task. These symbols appear before their definitions: X_g, v_q, I_d, V_g, θ_p (line 107; defined §2.4.1, §2.5); SCR (line 109; Definition 2.5); K_pll, θ_0 (lines 111, 134; Theorem 2.7); X_g again at line 132. The card is a chapter abstract and the paragraph is the problem statement, so the placement is right; the reader must be told that the definitions follow.

**Insert as the first line inside the card, after line 106:**

```html
<p><em>This card summarises the results proved below. Its symbols are defined in &sect;2.1 to &sect;2.5.</em></p>
```

**Insert after line 132 (before the paragraph that begins "This chapter answers"):**

```html
<p>The symbols in the next paragraph are defined in &sect;2.4 and &sect;2.5. The paragraph states the destination.</p>
```

### B10. Fig. 2.4 caption claims field evidence that the sources do not supply — ch2.html:598

**Defect.** "the oscillatory instability that real weak-grid plant shows" is an evidence claim. S07 and S08 are analytical and simulation studies. The chapter has no field source. Check (e): the theory-versus-evidence distinction.

**Replace the sentence `This figure is the reason Cited Result 2.9 is needed: ... real weak-grid plant shows.` in line 598 with:**

```html
This figure is the reason Cited Result 2.9 is needed: the static model of Theorem 2.7 predicts slowness, not the oscillatory instability that the fuller model of Cited Result 2.9 predicts <span class="cite">[S08, Zhou, Ding, Fan, Zhang and Gole 2014, "Impact of Short-Circuit Ratio and PLL Parameters on the Small-Signal Behavior of a VSC-HVDC Converter," <i>IEEE Trans. Power Delivery</i> 29(5), 2287&ndash;2296, eigenvalue-study sections &mdash; verify]</span>.
```

### B11. Bandwidth does not fall by the same fraction as power — ch2.html:507 and 708

**Defect.** Line 507 reads "a plant that loses export power on a weak grid loses control bandwidth by the same fraction at the same moment." Line 708 reads "loses terminal voltage, export power, and control bandwidth at the same rate, because all three are the same quantity V_g cos θ_0." Terminal voltage and power equal K_pll = V_g cos θ_0 and fall as K_pll. Bandwidth ω_n,pll = √(K_pll k_i,pll) and damping ratio ζ_pll fall as √K_pll, by equations (2.18) and (2.19). At SCR = 1.2 the first pair falls 44.7 % (1 − 0.5528) and the second pair 25.7 % (1 − 0.7435). Example 2.1 at line 478 prints the 25.7 % correctly. The two sentences state a wrong relation (part 1 of the standard, precise statement). Recomputed in `edit_ch2_check.py`.

**Replace line 507 with:**

```html
<p><strong>Reading 2 &mdash; <var>P</var> and <var>K</var><sub>pll</sub> are the same column.</strong> Both equal <var>V</var><sub>g</sub> cos <var>&theta;</var><sub>0</sub> at <var>I</var><sub>d</sub> = 1 pu. This is not a coincidence in the table; it is Theorem 2.7 Parts 2, 3 and 4 in one place. The consequence: a plant that loses export power on a weak grid loses loop bandwidth and damping ratio at the same moment, by the square root of the same factor, equation (2.19). At SCR = 1.2 the terminal voltage and the power are down 44.7 % (1 &minus; 0.5528) from the stiff-grid value, and the bandwidth and the damping ratio are down 25.7 % (1 &minus; &radic;0.5528 = 1 &minus; 0.7435), as Example 2.1 prints.</p>
```

**Replace the first sentence of the second paragraph at line 708, `A grid-following plant on a weak grid loses terminal voltage, ... at unity power factor.`, with:**

```html
A grid-following plant on a weak grid loses terminal voltage and export power at the same rate, because both are the same quantity <var>V</var><sub>g</sub> cos <var>&theta;</var><sub>0</sub> = <var>K</var><sub>pll</sub> in per unit at unity power factor. It loses loop bandwidth and damping ratio at the same moment, as &radic;<var>K</var><sub>pll</sub> (equation (2.19)). At SCR = 1.2 the first pair is down 44.7 % and the second pair 25.7 %.
```

---

## 2. Line-level rewrites

Quote, then rewrite. Apply in one pass.

### R1. ch2.html:128 — universal claim and evaluative triple with no measurement

Original: `The scheme is cheap, fast, and accurate. It runs every photovoltaic plant, every battery, and every full-converter wind turbine in service today.`

Rewrite:
```html
The scheme needs no model of the grid, and the 10 Hz loop of &sect;2.4 settles in about 0.09 s on a stiff grid. It has been the standard inverter control of the last three decades (book plan &sect;1.1); the grid-forming plant of Chapter 3 is the alternative under test.
```

### R2. ch2.html:253 — "obvious" is on the banned list

Original: `Equation (2.4) has an obvious control handle.`

Rewrite: `Equation (2.4) has one control input on each axis.`

### R3. ch2.html:110 — "well before" carries no number

Original: `Delivered power peaks at SCR &middot; <var>V</var><sub>g</sub><sup>2</sup>/2 well before that current bound, and then falls back toward zero`

Rewrite: `Delivered power peaks at SCR &middot; <var>V</var><sub>g</sub><sup>2</sup>/2 at the current <var>I</var><sub>d</sub> = SCR &middot; <var>V</var><sub>g</sub>/&radic;2, which is 0.707 of the current bound, and then falls back toward zero`

### R4. ch2.html:415 — "well below" is redundant next to the two numbers

Original: `that is <var>I</var><sub>d</sub> = 1.2/1.4142 = 0.8485 pu, well below the current bound of 1.2000 pu.`

Rewrite: `that is <var>I</var><sub>d</sub> = 1.2/1.4142 = 0.8485 pu, against the current bound of 1.2000 pu.`

### R5. ch2.html:507 — "severe" without a measurement

Original: `The consequence is severe: a plant that loses export power on a weak grid loses control bandwidth by the same fraction at the same moment.`

Rewrite: the word "severe" and the wrong relation in this sentence are both replaced by the full paragraph in B11. Apply B11; report R5 as applied through B11.

### R6. ch2.html:559 — "uncomfortable" is evaluative

Original: `Theorem 2.8 ended with an uncomfortable observation.`

Rewrite: `Theorem 2.8 ended with an observation that limits its reach.`

### R7. ch2.html:151 — wrong unit for the current-controller gains

Original: `proportional and integral gains of the inner current controller, in pu and pu/s.`

Rewrite: `proportional and integral gains of the inner current controller. With <var>k</var><sub>p,c</sub> = <var>&alpha;</var><sub>c</sub><var>L</var><sub>f</sub> and <var>k</var><sub>i,c</sub> = <var>&alpha;</var><sub>c</sub><var>R</var><sub>f</sub> their SI units are &Omega; and &Omega;/s; in per unit they are pu and pu/s when <var>L</var><sub>f</sub>, <var>R</var><sub>f</sub> and the gains share the converter base and <var>&alpha;</var><sub>c</sub> is in rad/s.`

### R8. ch2.html:237 — the per-unit sentence is not executable

Original: `or <var>m</var><sub>d</sub> and <var>m</var><sub>q</sub> scaled by the voltage base in per unit.`

Rewrite: `or, in per unit, <var>v</var><sub>d,conv</sub> = <var>m</var><sub>d</sub><var>v</var><sub>dc</sub>/(2<var>V</var><sub>pk,base</sub>) with <var>V</var><sub>pk,base</sub> the peak phase-voltage base, &radic;2 <var>V</var><sub>base</sub>/&radic;3 from <span class="rid">R01</span>.`

### R9. ch2.html:275 and 279 — "microseconds" twice, no source, and device physics is out of scope (plan §1.4)

Original (275): `Exceeding either destroys the device in microseconds.`
Rewrite: `Exceeding either destroys the device within a fraction of one fundamental cycle; the device physics behind that time is out of scope (plan &sect;1.4).`

Original (279): `the limit is a junction temperature reached in microseconds, not a winding temperature reached in seconds.`
Rewrite: `the limit is a junction temperature reached within a fraction of a cycle, not a winding temperature reached over seconds.`

### R10. ch2.html:660 — false attribution to Definition 2.1

Original: `which is the reason Definition 2.1 fixes the bases and the transform together.`

Rewrite: `which is why the transform of Definition 2.1 and the bases of <span class="rid">R01</span> must be chosen together: the peak phase-voltage base &radic;2 <var>V</var><sub>base</sub>/&radic;3 and the peak current base &radic;2 <var>I</var><sub>base</sub> multiply to (2/3)<var>S</var><sub>base</sub>.`

### R11. ch2.html:689 — 38-word sentence with two ideas

Original: `One fixed pair of gains cannot serve both ends of the range, which is the argument for gain scheduling or, as Chapter 3 argues, for a control law that does not need to measure the angle at all.`

Rewrite: `One fixed pair of gains cannot serve both ends of the range. That is the argument for gain scheduling. It is also, as Chapter 3 argues, the argument for a control law that does not measure the angle at all.`

### R12. ch2.html:731 — 55-word sentence

Original: `Chapter 3 defines grid-forming control by terminal behaviour (R24), shows that four control families reduce to one angle model with an equivalent inertia constant and an equivalent damping coefficient (R32), and recovers <var>K</var><sub>s</sub> &mdash; then bounds the recovered inertia by the direct-current-side energy reserve and by the current limit <var>I</var><sub>max</sub> of equation (2.7) (R33).`

Rewrite:
```html
Chapter 3 defines grid-forming control by terminal behaviour (<span class="rid">R24</span>). It shows that four control families reduce to one angle model with an equivalent inertia constant and an equivalent damping coefficient (<span class="rid">R32</span>). It recovers <var>K</var><sub>s</sub>. It then bounds the recovered inertia by the direct-current-side energy reserve and by the current limit <var>I</var><sub>max</sub> of equation (2.7) (<span class="rid">R33</span>).
```

### R13. ch2.html:118 — 60-word prerequisites sentence

Replace line 118 with (formulas as printed, with V_inf per B4):

```html
<p>From Chapter 1, three results. The per-unit system (<span class="rid">R01</span>). The synchronizing torque coefficient <var>K</var><sub>s</sub> = (<var>E</var>&prime;<var>V</var><sub>inf</sub>/<var>X</var>) cos <var>&delta;</var><sub>0</sub>, with <var>V</var><sub>inf</sub> the infinite-bus voltage of Chapter 1, and the condition |<var>&delta;</var><sub>0</sub>| &lt; 90&deg; (<span class="rid">R06</span>). The small-signal single-machine result <var>&omega;</var><sub>n</sub> = &radic;(<var>K</var><sub>s</sub><var>&omega;</var><sub>0</sub>/(2<var>H</var>)) with <var>&zeta;</var> = <var>K</var><sub>D</sub>/(4<var>H&omega;</var><sub>n</sub>) (<span class="rid">R07</span>). This chapter cites those results by identifier. It does not restate their proofs.</p>
```

This replacement also carries the B4 change for line 118; apply once.

### R14. ch2.html:343 — "simply" is a hedge

Original: `here <var>I</var><sub>d</sub> is simply given.` Rewrite: `here <var>I</var><sub>d</sub> is a given constant.`

### R15. ch2.html:301 — "easy" is evaluative

Original: `Take the easy case first.` Rewrite: `Take the stiff-grid case first.` (Already included in B2's replacement text.)

### R16. ch2.html:143-158 — three symbols missing from the local list

Insert three entries at the end of the list:
```html
<li><var>j</var> &mdash; the imaginary unit, <var>j</var><sup>2</sup> = &minus;1. Book-wide.</li>
<li><var>t</var> &mdash; time, in s. Book-wide.</li>
<li>Superscript T &mdash; transpose of a vector or matrix, as in equation (2.1).</li>
<li><var>V</var><sub>pk,base</sub> &mdash; peak phase-voltage base, &radic;2 <var>V</var><sub>base</sub>/&radic;3, in V. Used in &sect;2.2 (R8) and Exercise 2 (R10) only.</li>
```

### R17. ch2.html:41 and 55 — literal colours below `:root`

Plan §5.3 item 4 requires variables, not literals, below `:root`. `.ex{... background:#17233a}` and `.eqn{... background:#16213a}` are literals that are not in the palette. Rewrite: add `--card2:#17233a; --eqbg:#16213a;` to `:root` and use `background:var(--card2)` and `background:var(--eqbg)`. Or drop both and use `var(--card)`.

### R18. ch2.html:395, 406, 111 — unit of K_pll

The book table gives K_s in pu/rad and K_pll in pu. The two are called structural twins, so their units should match: K_pll = ∂v_q/∂θ_p is a voltage per radian, pu/rad. The numerical equality with the terminal voltage in pu still holds. Plan-level change: set K_pll to pu/rad in the notation table, and at line 395 write `It is numerically equal to the terminal voltage magnitude in per unit`. If the plan keeps pu, add one sentence at line 395: `Both are dimensionless per-unit numbers once the angle is in radians.`

### R19. ch2.html:279 — citation locator for the machine fault current

`[S01, Kundur 1994, ..., Ch. 3 — verify]` for "5 to 7 times rated current". The number follows from typical values of the subtransient reactance, which Kundur tabulates in his chapter on machine parameters, not in the chapter the draft names. The locator is doubtful. Do not change it from memory. Append `; locator doubtful, verifier to confirm` inside the bracket and leave `verify` in place. I did not open the book.

### R20. ch2.html:279 — source for I_max ≈ 1.1 to 1.3 pu

`[S18, IEEE Std 2800-2022, ..., current-injection clauses — verify]`. IEEE 2800 sets interconnection requirements; it does not set a device current limit. The value is plausible as industry practice, but the source is doubtful. Keep the sentence "The quoted range is an industry figure, not a computed one", keep `verify`, and add `; S18 states requirements, not device ratings, so a human must confirm or replace this source`. Do not substitute another source from memory.

### R21. ch2.html:265 — locator for "1.5 sample periods"

The 1.5-sample delay is a generic digital-control figure. S06 Ch. 8 may not state it. Doubtful locator; keep `verify` and add `location unconfirmed`.

### R22. ch2.html:325 — SCR classes pass

`[S19, IEEE Std 1204-1997, ..., strength-classification clause — verify]` with high > 3, low 2 to 3, very low < 2. Right source, values match the guide's classes. No change; the human verifier can remove the hedge "One common convention" once the page is read.

### R23. ch2.html:159 — the rendering-convention paragraph is house-keeping in the reader's face

Move the "Rendering convention" paragraph out of the local notation card into the closing paragraph at line 733, where the other plan-to-chapter conventions already sit. It is for the fix stage, not the reader.

---

## 3. Structural notes

- **S1. File name.** The plan (§5.3) names `ch02.html`; the file is `ch2.html`. The draft flagged it. The book-level link check expects `ch02.html`. Decide once for all four chapters.
- **S2. No cross-chapter hyperlinks.** The chapter writes zero `<a href>`. Plan §5.1 requires `<a href="ch01.html#thm-1-3">Theorem 1.3</a>`. `ch1.html` now exists with ids. The fix stage can convert every `<span class="rid">R0n</span>` for R01, R03, R04, R06, R07, R08 into a link, and delete the closing paragraph at line 733 that explains the absence.
- **S3. Position of the local notation card.** The card sits under the §2.1 heading (line 140) but applies to the whole chapter. Move it above the §2.1 heading, directly after the problem statement, so the reader meets it before any dq symbol.
- **S4. Section 2.6 is heavy.** It holds two theorems' worth of reading (Theorem 2.8, Examples 2.1 and 2.2, Figs. 2.3 and 2.4, Cited Result 2.9, Corollary 2.10, the scope list): about 3,300 words of 8,743. The plan fixes six sections, so keep the count, but promote the "what this chapter does not cover" list (§2.6.5) to sit after the exercises as an unnumbered closing section, next to the ledger. That shortens §2.6 to its argument.
- **S5. Exercise 2's answer is a sketch.** "Invert equations (2.1) and (2.2) for a balanced set and substitute. The cross terms cancel" gives the destination and not the road. A graduate reader can finish it, and it is an exercise, so this is acceptable. If space allows, add the two-line identity: with the inverse Clarke transform, v_a i_a + v_b i_b + v_c i_c = (3/2)(v_α i_α + v_β i_β) for a balanced set, and the Park rotation preserves the dot product.
- **S6. Word count.** 8,743 rendered words by my count (the draft reports 8,809), against a target of 7,500 ± 20 % (6,000 to 9,000). Inside the band. After B1, B2 and B5 the chapter grows by about 450 words to about 9,200, which is 2 % above the band. Cut R23's paragraph and the deviation notes at lines 480 and 510 to footnote length to recover it, or accept the overrun.
- **S7. Ledger row for Model 2.6.** After B1 the status column at line 720 stays "derived in §2.5"; that is now true.
- **S8. Fig. 2.1 and the word "locked".** The figure uses θ = ω_0 t, a known angle, not a loop output. The caption says "this figure is what 'locked' means". That is right, and it is enough.

---

## 4. What already works

Each item names the test I ran and that it held.

- **Theorem 2.7 (lines 388-409).** I tried to break the two-branch argument: for sin θ_0 = X_g I_d/V_g ∈ [0, 1) the solutions in [0, 180°) are θ_0 and 180° − θ_0; the chapter rejects the second by the sign of K_pll, which is the right criterion, and it names the merge at 90°. Part 3's substitution I_d = V_g sin θ_0/X_g into P = V_g cos θ_0 · I_d gives (V_g²/(2X_g)) sin 2θ_0; the peak at 45° and the zero at 90° both check. Part 4's sign is the negative feedback the loop needs, and the text says so.
- **Theorem 2.8 (lines 441-459).** The √K_pll scaling law follows from ζ = K k_p/(2√(K k_i)); I recomputed it at five points (Table 2.2) and it holds. The remark that both coefficients are positive for every K_pll > 0, so the linearised loop never crosses the axis, is correct and is the honest set-up for Cited Result 2.9.
- **Model 2.2, equation (2.4).** I re-derived the cross-coupling signs from d/dt(i_dq e^{jθ}) = (di_dq/dt + jω i_dq) e^{jθ}: +ω_0 L_f i_q on the d axis, −ω_0 L_f i_d on the q axis. The chapter has them right, and the sentence "They exist because the frame rotates, not because the circuit couples the axes" is the explanation a new reader needs.
- **Model 2.3, equation (2.6).** With k_p,c = α_c L_f and k_i,c = α_c R_f the controller is α_c(sL_f + R_f)/s; times the plant 1/(sL_f + R_f) the loop is α_c/s; the closed loop is α_c/(s + α_c). Exact.
- **Example 2.1 (lines 463-482).** Every step prints its factors and a cross-check by a second route (cos θ_0 from arccos and from √(1 − sin²); P from v_d I_d and from (2.15); ζ from (2.18) and from (2.19)). The rounding note at line 480 states both chains and picks one. This is the model for every worked example in the book.
- **Table 2.2 and its four readings (lines 486-512).** All 35 cells recompute. The deviation note names the plan's digits and the recomputed digits side by side. Reading 1 separates the two power columns as two objects; that is the single most useful paragraph for a plant engineer in the chapter.
- **Fig. 2.4 caption.** It states the real part −K_pll k_p,pll/2 in closed form, so the reader can verify the locus never crosses. All four marked roots and the three constant-ζ rays recompute to within 0.15 px.
- **Cited Result 2.9 (lines 601-607).** "Cited, not proved in this book" in the label, both sources with `verify`, a paragraph on why it sits here, and a paragraph on what the chapter therefore does not claim. This is the status-label rule of plan §5.4 done properly.
- **Model 2.6 omissions (lines 338-344)** are ordered by consequence, with reactive support first and the higher literature figure P_max = SCR · V_g · |v| recorded as "two different plants, not two opinions about one plant". That sentence resolves a confusion the literature itself often leaves open.
- **The K_s / K_pll parallel (Table 2.1)** is laid out row by row and ends on the row where it breaks: energy. The chapter does not oversell the analogy.
- **HTML rule.** Parsed with `html.parser`: zero tag errors, zero unclosed tags, 0 `<script>`, 0 `<link>`, 0 `<img>`, 0 `http`, 0 `data:` URIs, one `<style>`, `color-scheme` dark present, all nine palette hex values defined as `:root` custom properties, 4 figures with 4 inline SVGs and chapter-prefixed captions, 6 exercises each with a `<details>`, equations (2.1) to (2.19) continuous and each referenced, 12 `data-rid` values R12 to R23 with no duplicate ids.

---

## 5. Cross-chapter check (task item h)

| R-id cited | Plan statement | Chapter 2 statement | Match |
|---|---|---|---|
| R01 | per-unit system | line 118, prerequisites | yes |
| R03 | H = E_kin / S_base | line 618, "stored kinetic energy at rated speed divided by S_base" | yes |
| R04 | 2H d(dw)/dt = P_m − P_e − K_D dw | line 618, "puts 2H in front of the frequency derivative" | yes |
| R06 | K_s = (E′V/X) cos δ_0; K_s > 0 iff |δ_0| < 90° | lines 113, 118, 425 | formula yes; symbol V vs ch1's V_inf — see B4 |
| R07 | ω_n = √(K_s ω_0/(2H)), ζ = K_D/(4Hω_n) | lines 118, 428, 619 | yes |
| R08 | Example 1.1, 1.43 Hz | not cited; used in B5's fix | — |
| R24 | grid-forming defined by terminal behaviour | lines 627, 731 | yes |
| R32 | unified small-signal model, (H_eq, K_D_eq) table | line 731 | yes |
| R33 | restores K_s; inertia bounded by DC energy and I_max | lines 281, 731 | yes |
| R39 | sizing case, headroom binds | line 281 | yes |
| R40 | current limiting, fault current and protection | line 638 | yes |

---

## 6. Citation judgement (task item d)

14 citations in the file, every one with `verify`, source ids S01, S06, S07, S08, S18, S19. Format: 13 carry all four parts; one (line 635) does not — B8.

| Line | Source and locator | Value | Judgement |
|---|---|---|---|
| 178 | S06 Ch. 4, Park convention | — | right source; Y&I treat space phasors and frames in Ch. 4 |
| 246, 266, 296 | S06 Ch. 8, converter model, current-control design rule, PLL | — | right source and chapter |
| 249 | S06 Ch. 8, bandwidth one decade below f_sw | ratio ≈ 10 | plausible; generic design rule, locator unconfirmed |
| 265 | S06 Ch. 8, 1.5 sample periods | 1.5 | plausible value; doubtful locator — R21 |
| 279 | S18 current-injection clauses | I_max 1.1 to 1.3 pu | plausible value; doubtful source — R20 |
| 279 | S01 Ch. 3, machine fault current | 5 to 7 × rated | plausible value; locator likely Ch. 4 Table 4.2 — R19 |
| 325 | S19 strength-classification clause | > 3, 2 to 3, < 2 | right source, right values |
| 340 (×2) | S07, S08, reactive-supported limit | P_max = SCR·V_g·|v| | plausible; both papers treat the weak-grid transfer limit |
| 604 (×2) | S08, S07, PLL–current-loop interaction | — | right sources for R22 |
| 635 | S07, abbreviated | — | fix format — B8 |

No number in the chapter is printed without a source id or a computation. The forbidden string "ENTSO-E 1 Hz/s" does not appear.

---

## 7. Numbers recomputed (task item c)

Method: `edit_ch2_check.py` recomputes each printed value from the chapter's stated inputs (SCR, V_g = 1, I_d = 1, f_0 = 50 Hz, ω_n,pll = 2π·10, ζ = 1/√2) and compares to the printed digits at half a unit in the last printed place. SVG coordinates are checked against the axis mappings read from the figure (Fig. 2.2: 110 px = 1 pu; Fig. 2.3: x = 70 + (SCR − 1)·500/9, left y = 250 − 210·K_pll, right y = 250 − 84·P_max; Fig. 2.4: x = 520 + 9.2·σ, y = 250 − 4.2·ω).

**Checked: 186 (180 printed values plus 6 editor-side values used in this edit). Wrong: 4.**

The four wrong items:

1. Line 279, "between 0.220 and 0.186" — the ratio range is 0.157 to 0.260 (B7).
2. Line 687, `0.5528 · 7141.82 = 3947.99` — the product is 3947.998, which prints as 3948.00.
3. Line 688, `√(0.9950/0.5528) = √1.8001` — the ratio is exactly 1.8000, since 0.99/(11/36) = 3.24 and √3.24 = 1.8. Print 1.8000. The root 1.3416 is unaffected.
4. Line 688, `ω_n,pll = 62.83 · 1.3416 = 84.29 rad/s` — full precision gives 84.30 (√(0.994987 · 7141.91) = 84.298). The chapter's chain is internally consistent, and the plan's own figure is 84.3; print 84.30 to match the full-precision rule the chapter sets for itself at line 480.

Two rows that a naive full-precision check flags are not wrong: line 477 `0.552771 · 88.8577 = 49.1180` and line 687 `3948/0.5528 = 7141.82` both reproduce exactly from the chapter's printed intermediates.

Full table follows. Location, printed, recomputed, ok or wrong.

| # | Location | Printed | Recomputed | Result |
|---|---|---|---|---|
| 1 | L187 t=0ms va | 1.0000 | 1 | ok |
| 2 | L187 t=0ms vb | -0.5000 | -0.5 | ok |
| 3 | L187 t=0ms vc | -0.5000 | -0.5 | ok |
| 4 | L187 t=0ms valpha | 1.0000 | 1 | ok |
| 5 | L187 t=0ms vbeta | 0.0000 | 3.84593e-16 | ok |
| 6 | L187 t=0ms vd | 1.0000 | 1 | ok |
| 7 | L187 t=0ms vq | 0.0000 | 3.84593e-16 | ok |
| 8 | L187 t=4ms va | 0.3090 | 0.309017 | ok |
| 9 | L187 t=4ms vb | 0.6691 | 0.669131 | ok |
| 10 | L187 t=4ms vc | -0.9781 | -0.978148 | ok |
| 11 | L187 t=4ms valpha | 0.3090 | 0.309017 | ok |
| 12 | L187 t=4ms vbeta | 0.9511 | 0.951057 | ok |
| 13 | L187 t=4ms vd | 1.0000 | 1 | ok |
| 14 | L187 t=4ms vq | 0.0000 | 1.11022e-16 | ok |
| 15 | L187 t=8ms va | -0.8090 | -0.809017 | ok |
| 16 | L187 t=8ms vb | 0.9135 | 0.913545 | ok |
| 17 | L187 t=8ms vc | -0.1045 | -0.104528 | ok |
| 18 | L187 t=8ms valpha | -0.8090 | -0.809017 | ok |
| 19 | L187 t=8ms vbeta | 0.5878 | 0.587785 | ok |
| 20 | L187 t=8ms vd | 1.0000 | 1 | ok |
| 21 | L187 t=8ms vq | 0.0000 | 3.33067e-16 | ok |
| 22 | L249 ratio 2500/500 | 5.0 | 5 | ok |
| 23 | L269 alpha_c rad/s | 3141.59 | 3141.59 | ok |
| 24 | L269 tau_c ms | 0.318 | 0.31831 | ok |
| 25 | L269 ratio 500/10 | 50 | 50 | ok |
| 26 | L279 1.1/5 | 0.220 | 0.22 | ok |
| 27 | L279 1.3/7 | 0.186 | 0.185714 | ok |
| 28 | L311 omega_n 2pi10 | 62.8319 | 62.8319 | ok |
| 29 | L311 zeta | 0.7071 | 0.707107 | ok |
| 30 | L311 k_i full | 3947.84 | 3947.84 | ok |
| 31 | L311 k_i printed | 3948 | 3947.84 | ok |
| 32 | L311 k_p | 88.86 | 88.8577 | ok |
| 33 | L415 I_d at 45deg SCR1.2 | 0.8485 | 0.848528 | ok |
| 34 | L415 sqrt2 | 1.4142 | 1.41421 | ok |
| 35 | L415 bound | 1.2000 | 1.2 | ok |
| 36 | L429 700 MJ | 700 | 700 | ok |
| 37 | L466 X_g | 0.8333 | 0.833333 | ok |
| 38 | L467 theta0 rad | 0.9851 | 0.985111 | ok |
| 39 | L467 theta0 deg | 56.44 | 56.4427 | ok |
| 40 | L468 SCR*Vg | 1.2000 | 1.2 | ok |
| 41 | L469 cos theta0 | 0.5528 | 0.552771 | ok |
| 42 | L469 0.8333^2 | 0.6944 | 0.694444 | ok |
| 43 | L469 1-0.6944 | 0.3056 | 0.305556 | ok |
| 44 | L469 sqrt | 0.5528 | 0.552771 | ok |
| 45 | L470 P | 0.5528 | 0.552771 | ok |
| 46 | L470 1/1.6667 | 0.6000 | 0.6 | ok |
| 47 | L470 2theta0 deg | 112.89 | 112.885 | ok |
| 48 | L470 sin(2theta0) | 0.9213 | 0.921285 | ok |
| 49 | L470 0.6*0.9213 | 0.5528 | 0.552771 | ok |
| 50 | L471 Pmax | 0.6000 | 0.6 | ok |
| 51 | L471 Id at peak | 0.8485 | 0.848528 | ok |
| 52 | L472 K_pll | 0.5528 | 0.552771 | ok |
| 53 | L474 K_pll 6-digit | 0.552771 | 0.552771 | ok |
| 54 | L474 product | 2182.25 | 2182.25 | ok |
| 55 | L474 omega_n | 46.71 | 46.7146 | ok |
| 56 | L475 Hz | 7.435 | 7.43486 | ok |
| 57 | L476 sqrt K | 0.7435 | 0.743486 | ok |
| 58 | L476 zeta | 0.5257 | 0.525724 | ok |
| 59 | L477 k_p full | 88.8577 | 88.8577 | ok |
| 60 | L477 omega full | 46.7146 | 46.7146 | ok |
| 61 | L477 num (chain 0.552771*88.8577) | 49.1180 | 49.118 | ok |
| 62 | L477 den | 93.4292 | 93.4292 | ok |
| 63 | L477 zeta | 0.5257 | 0.525724 | ok |
| 64 | L478 bandwidth drop % | 25.7 | 25.6514 | ok |
| 65 | L478 zeta drop % | 25.7 | 25.6514 | ok |
| 66 | L480 0.5528*3948 | 2182.45 | 2182.45 | ok |
| 67 | L480 sqrt | 46.72 | 46.7167 | ok |
| 68 | L480 Hz | 7.44 | 7.4352 | ok |
| 69 | L498-502 Table2.2 SCR=10 Xg | 0.1000 | 0.1 | ok |
| 70 | L498-502 Table2.2 SCR=10 theta0 | 5.7392 | 5.73917 | ok |
| 71 | L498-502 Table2.2 SCR=10 Kpll | 0.9950 | 0.994987 | ok |
| 72 | L498-502 Table2.2 SCR=10 omega_n | 62.6742 | 62.6742 | ok |
| 73 | L498-502 Table2.2 SCR=10 zeta | 0.7053 | 0.705332 | ok |
| 74 | L498-502 Table2.2 SCR=10 P | 0.9950 | 0.994987 | ok |
| 75 | L498-502 Table2.2 SCR=10 Pmax | 5.0000 | 5 | ok |
| 76 | L498-502 Table2.2 SCR=3 Xg | 0.3333 | 0.333333 | ok |
| 77 | L498-502 Table2.2 SCR=3 theta0 | 19.4712 | 19.4712 | ok |
| 78 | L498-502 Table2.2 SCR=3 Kpll | 0.9428 | 0.942809 | ok |
| 79 | L498-502 Table2.2 SCR=3 omega_n | 61.0087 | 61.0087 | ok |
| 80 | L498-502 Table2.2 SCR=3 zeta | 0.6866 | 0.686589 | ok |
| 81 | L498-502 Table2.2 SCR=3 P | 0.9428 | 0.942809 | ok |
| 82 | L498-502 Table2.2 SCR=3 Pmax | 1.5000 | 1.5 | ok |
| 83 | L498-502 Table2.2 SCR=2 Xg | 0.5000 | 0.5 | ok |
| 84 | L498-502 Table2.2 SCR=2 theta0 | 30.0000 | 30 | ok |
| 85 | L498-502 Table2.2 SCR=2 Kpll | 0.8660 | 0.866025 | ok |
| 86 | L498-502 Table2.2 SCR=2 omega_n | 58.4716 | 58.4716 | ok |
| 87 | L498-502 Table2.2 SCR=2 zeta | 0.6580 | 0.658037 | ok |
| 88 | L498-502 Table2.2 SCR=2 P | 0.8660 | 0.866025 | ok |
| 89 | L498-502 Table2.2 SCR=2 Pmax | 1.0000 | 1 | ok |
| 90 | L498-502 Table2.2 SCR=1.2 Xg | 0.8333 | 0.833333 | ok |
| 91 | L498-502 Table2.2 SCR=1.2 theta0 | 56.4427 | 56.4427 | ok |
| 92 | L498-502 Table2.2 SCR=1.2 Kpll | 0.5528 | 0.552771 | ok |
| 93 | L498-502 Table2.2 SCR=1.2 omega_n | 46.7146 | 46.7146 | ok |
| 94 | L498-502 Table2.2 SCR=1.2 zeta | 0.5257 | 0.525724 | ok |
| 95 | L498-502 Table2.2 SCR=1.2 P | 0.5528 | 0.552771 | ok |
| 96 | L498-502 Table2.2 SCR=1.2 Pmax | 0.6000 | 0.6 | ok |
| 97 | L498-502 Table2.2 SCR=1.05 Xg | 0.9524 | 0.952381 | ok |
| 98 | L498-502 Table2.2 SCR=1.05 theta0 | 72.2472 | 72.2472 | ok |
| 99 | L498-502 Table2.2 SCR=1.05 Kpll | 0.3049 | 0.304911 | ok |
| 100 | L498-502 Table2.2 SCR=1.05 omega_n | 34.6949 | 34.6949 | ok |
| 101 | L498-502 Table2.2 SCR=1.05 zeta | 0.3905 | 0.390455 | ok |
| 102 | L498-502 Table2.2 SCR=1.05 P | 0.3049 | 0.304911 | ok |
| 103 | L498-502 Table2.2 SCR=1.05 Pmax | 0.5250 | 0.525 | ok |
| 104 | L508 (0.7053-0.6580)/0.7053 | 0.0671 | 0.067054 | ok |
| 105 | L508 6.7% | 6.7 | 6.7054 | ok |
| 106 | L508 (0.6580-0.3905)/0.6580 | 0.4066 | 0.406636 | ok |
| 107 | L508 40.7% | 40.7 | 40.6636 | ok |
| 108 | L509 2.9% at SCR3 | 2.9 | 2.90165 | ok |
| 109 | L509 25.7% at SCR1.2 | 25.7 | 25.6514 | ok |
| 110 | L357-380 Fig2.2 SCR=10 Xg | 0.1000 | 0.1 | ok |
| 111 | Fig2.2 SCR=10 theta0 | 5.74 | 5.73917 | ok |
| 112 | Fig2.2 SCR=10 |v| | 0.9950 | 0.994987 | ok |
| 113 | L357-380 Fig2.2 SCR=1.2 Xg | 0.8333 | 0.833333 | ok |
| 114 | Fig2.2 SCR=1.2 theta0 | 56.44 | 56.4427 | ok |
| 115 | Fig2.2 SCR=1.2 |v| | 0.5528 | 0.552771 | ok |
| 116 | L362 Fig2.2 left Vg px/110 | 1.0000 | 0.99956 | ok |
| 117 | L362 Fig2.2 left angle deg | 5.74 | 5.7417 | ok |
| 118 | L372 Fig2.2 right Vg px/110 | 1.0000 | 1.00023 | ok |
| 119 | L372 Fig2.2 right angle deg | 56.44 | 56.4544 | ok |
| 120 | L373 Fig2.2 right jXgI px/110 | 0.8333 | 0.833636 | ok |
| 121 | L374 Fig2.2 right |v| px/110 | 0.5528 | 0.552727 | ok |
| 122 | L554 SCR where Kpll=0.9 | 2.2942 | 2.29416 | ok |
| 123 | L554 SCR where Pmax=2.5 | 5 | 5 | ok |
| 124 | L554 SCR where Pmax=1 | 2 | 2 | ok |
| 125 | L547 Ex2.1 marker x | 81.1 | 81.1111 | ok |
| 126 | L547 Ex2.1 marker y | 133.9 | 133.918 | ok |
| 127 | L549 Pmax=1 marker x | 125.6 | 125.556 | ok |
| 128 | L549 Pmax=1 marker y | 166.0 | 166 | ok |
| 129 | L545 Kpll polyline first x | 71.1 | 71.1111 | ok |
| 130 | L545 Kpll polyline first y | 208.6 | 208.618 | ok |
| 131 | L545 Kpll polyline last y | 41.1 | 41.0526 | ok |
| 132 | L546 Pmax polyline first y (SCR1.02) | 207.2 | 207.16 | ok |
| 133 | L546 Pmax polyline last x (SCR 4.98) | 291.1 | 291.111 | ok |
| 134 | L546 Pmax last y | 40.8 | 40.84 | ok |
| 135 | L589-595 Fig2.4 K=1.0 real | 44.43 | 44.4288 | ok |
| 136 | Fig2.4 K=1.0 imag | 44.43 | 44.4288 | ok |
| 137 | L589-595 Fig2.4 K=0.552771 real | 24.56 | 24.559 | ok |
| 138 | Fig2.4 K=0.552771 imag | 39.74 | 39.738 | ok |
| 139 | L589-595 Fig2.4 K=0.1 real | 4.44 | 4.44288 | ok |
| 140 | Fig2.4 K=0.1 imag | 19.37 | 19.3661 | ok |
| 141 | L588 Fig2.4 marker K=1.0 x | 111.3 | 111.255 | ok |
| 142 | L588 Fig2.4 marker K=1.0 y | 63.4 | 63.3989 | ok |
| 143 | L590 Fig2.4 marker K=0.552771 x | 294.0 | 294.057 | ok |
| 144 | L590 Fig2.4 marker K=0.552771 y | 83.1 | 83.1004 | ok |
| 145 | L592 Fig2.4 marker K=0.3049 x | 395.4 | 395.374 | ok |
| 146 | L592 Fig2.4 marker K=0.3049 y | 115.9 | 115.85 | ok |
| 147 | L594 Fig2.4 marker K=0.1 x | 479.1 | 479.125 | ok |
| 148 | L594 Fig2.4 marker K=0.1 y | 168.7 | 168.662 | ok |
| 149 | L581 Fig2.4 ray zeta | 0.707 | 0.707029 | ok |
| 150 | L582 Fig2.4 ray zeta | 0.5 | 0.499923 | ok |
| 151 | L583 Fig2.4 ray zeta | 0.3 | 0.299881 | ok |
| 152 | L587 polyline first x | 111.3 | 111.255 | ok |
| 153 | L587 polyline last x (K=0.05) | 499.6 | 499.563 | ok |
| 154 | L587 polyline last y | 191.7 | 191.734 | ok |
| 155 | L650 Ex1 SCR | 1.5000 | 1.5 | ok |
| 156 | L650 Ex1 Xg | 0.6667 | 0.666667 | ok |
| 157 | L650 Ex1 theta0 | 41.81 | 41.8103 | ok |
| 158 | L650 Ex1 Kpll | 0.7454 | 0.745356 | ok |
| 159 | L650 Ex1 Pmax | 0.7500 | 0.75 | ok |
| 160 | L677 Ex4 K at zeta .3 | 0.1800 | 0.18 | ok |
| 161 | L677 Ex4 theta0 | 79.63 | 79.6302 | ok |
| 162 | L677 Ex4 SCR closed | 1.0166 | 1.0166 | ok |
| 163 | L678 Ex4 SCR=1.017 Kpll | 0.1821 | 0.182078 | ok |
| 164 | L678 Ex4 SCR=1.017 zeta | 0.3017 | 0.301726 | ok |
| 165 | L678 Ex4 SCR=1.016 Kpll | 0.1768 | 0.176771 | ok |
| 166 | L678 Ex4 SCR=1.016 zeta | 0.2973 | 0.297297 | ok |
| 167 | L687 Ex5 k_p | 160.7 | 160.75 | ok |
| 168 | L687 Ex5 k_i | 7142 | 7141.91 | ok |
| 169 | L687 Ex5 ki 7141.82 (chain 3948/0.5528) | 7141.82 | 7141.82 | ok |
| 170 | L687 Ex5 product | 3947.99 | 3948 | WRONG |
| 171 | L687 Ex5 omega | 62.83 | 62.8319 | ok |
| 172 | L688 Ex5 K10 | 0.9950 | 0.994987 | ok |
| 173 | L688 Ex5 ratio | 1.8001 | 1.8 | WRONG |
| 174 | L688 Ex5 ratio exact 0.99/(11/36)=3.24 root | 1.8000 | 1.8 | ok |
| 175 | L688 Ex5 sqrt ratio | 1.3416 | 1.34164 | ok |
| 176 | EDIT settle stiff 4/(0.7071*62.83) s | 0.090 | 0.0900316 | ok |
| 177 | EDIT settle SCR1.2 4/(0.5257*46.71) s | 0.163 | 0.162873 | ok |
| 178 | EDIT ratio range low 1.1/7 | 0.157 | 0.157143 | ok |
| 179 | EDIT ratio range high 1.3/5 | 0.260 | 0.26 | ok |
| 180 | EDIT B11 voltage and power drop % at SCR1.2 (1-K) | 44.7 | 44.7229 | ok |
| 181 | L688 Ex5 omega@10 | 84.29 | 84.2978 | WRONG |
| 182 | L688 Ex5 Hz | 13.42 | 13.4164 | ok |
| 183 | L688 Ex5 zeta@10 | 0.9487 | 0.948683 | ok |
| 184 | L689 Ex5 13.42/10 | 1.3416 | 1.34164 | ok |
| 185 | L723 ledger 7.435 Hz | 7.435 | 7.43486 | ok |
| 186 | L708 Pmax<rating at SCR | 2 | 2 | ok |

Rows marked WRONG at lines 687 and 688 are the last-digit items 2 to 4 above. The range item 1 (line 279) is the two EDIT rows 0.157 and 0.260 against the printed 0.220 and 0.186. The EDIT B11 row 44.7 and the L478 rows 25.7 are the two fractions that B11 separates.
