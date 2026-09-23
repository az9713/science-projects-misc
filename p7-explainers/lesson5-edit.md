# Lesson 5 edit: Park transform and PLL (science-editor pass)

Files checked: `p7-explainers/lesson5.html`, `lesson5_pll.py`, `lesson5_fig53.py`,
`lesson5_ex3_negseq.py`, `lesson5_ex4_20hz.py`. All four scripts were run again (Python, stdlib).
Line numbers refer to `lesson5.html` before the fixes.

## Verdict (before fixes)

**Major revision.** The derivations are correct. Two statements are false: the §4.3 explanation of
the angle-error bias, and the last sentence of Exercise 5. Three "computed by the listing" labels
point to numbers that the named listing does not print. One quantity has two values (0.0778 s and
0.0779 s). The Fig. 5.3 table gives a settling time that changes with the chosen time window. The
word "bandwidth" is used for the natural frequency. A graduate reader can learn the method from the
page, but the reader would learn a wrong cause for the -0.0314 rad bias and a wrong claim about ramp
tracking.

## What is correct (checked, no change)

- Clarke and Park algebra (lines 232-247): v_alpha = V cos(theta_g), v_beta = V sin(theta_g),
  v_d = V cos(theta_g - theta_pll), v_q = V sin(theta_g - theta_pll). Checked by hand.
- K_pll = V (§3, Exercise 2).
- Characteristic equation s^2 + K kp s + K ki = 0 and omega_n = sqrt(K ki), zeta = K kp/(2 omega_n).
  From e' = (omega_g - omega_0) - K kp e - K ki integral(e), differentiated once, omega_g constant.
- Gains: kp = 88.8442 1/s, ki = 3947.8418 1/s^2 (rerun matches). 20 Hz gains 177.6885 and
  15791.3670 (rerun matches).
- 4/(zeta omega_n) = 4/(0.707 x 62.8319) = 0.09005 s. -ln(0.02) = 3.912.
- de/dt(0) = -2 zeta omega_n Delta_theta (linearised): at the jump z = 0, so
  d(theta_pll)/dt - d(theta_g)/dt = kp K Delta_theta.
- Exercise 3 output (0.10044 pu ripple, -0.000001 pu mean) matches the rerun. The negative-sequence
  set in the script is a true negative sequence. The 100 Hz argument in §5 is correct.
- Exercise 4 settling time 0.0388 s matches the rerun.
- Overshoot-past-zero values 0.2225 / 0.1403 / 0.1024 rad and their percentages are arithmetically
  correct (checked by a separate script), but no listing printed them (defect 3).

## Defects

Ranked most serious first.

### D1. §4.3 bias cause is wrong, and "the bias is the same before and after" is false (blocking)
- Location: lines 572-586.
- Problem: The text says -0.031416 rad is "the digital phase detector reading theta_pll one sample
  late" and that "the bias is the same before and after the frequency step". The loop has no such
  delay: the Park transform uses the correct angle for sample k, and v_q goes to zero at lock. The
  bias comes from the error metric. `run()` computes e after it advances theta_pll, so it compares
  theta_g(k) with the angle for sample k+1, which gives -omega_g x DT. omega_g changes at the step,
  so the bias changes: -2 pi 50 x 1e-4 = -0.031416 rad before, -2 pi 50.5 x 1e-4 = -0.031730 rad
  after. The observed change, -0.000309 rad, is this bias shift (0.000314 rad). The loop's own
  residual error is 2.84e-8 rad before and 4.84e-6 rad 200 ms after the step. The text also has
  Markdown `*change*` inside HTML.
- Fix: Rewrite the paragraph with the correct mechanism and both bias values. Add one print line
  to `lesson5_pll.py` that prints the residual after the bias is removed. Quote it in the text.

### D2. Exercise 5 last sentence contradicts the sentence before it (blocking)
- Location: lines 700-701.
- Problem: "a type-2 loop tracks a ramp input with a bounded but non-zero steady error". A type-2
  loop tracks a ramp with zero error (the same answer says so on line 694). The correct statement is
  about a parabolic input.
- Fix: Replace "ramp input" with "parabolic input". Add the value:
  e_ss = R/(K ki) = R/omega_n^2 for a frequency ramp of R rad/s^2 (final-value theorem on
  E(s) = s^2/(s^2 + K kp s + K ki) x R/s^3).

### D3. Fig. 5.3 table overshoot column: the named listing does not produce it (blocking)
- Location: lines 521-528.
- Problem: `lesson5_fig53.py` prints `peak|err|(first 40 pts)` (0.49 rad), not the overshoot. Also,
  "overshoot past zero" includes the -0.0314 rad metric bias of D1. The loop's overshoot past its
  final value is 0.1912 / 0.1089 / 0.0710 rad (36.5% / 20.8% / 13.6% of the jump). The zeta = 1 value
  agrees with theory: minimum of (1 - omega_n t) e^(-omega_n t) is -e^-2 = -0.135.
- Fix: Make `lesson5_fig53.py` print both overshoots. Put the "past final value" column in the table
  first, keep "past zero" as a second column, and explain the difference.

### D4. zeta = 0.4 settling time depends on the time window (blocking)
- Location: line 522 (0.1663 s) and line 530 (0.166 s).
- Problem: `lesson5_fig53.py` measured settling in a 0.1-0.3 s window. At t = 0.3 s the zeta = 0.4
  error is -0.028409 rad, not yet at its final value, so the settling reference is wrong. With the
  0.1-0.4 s window of the main listing: 0.1593 s (zeta 0.4), 0.0779 s (0.707), 0.0858 s (1.0).
- Fix: Compute settling and overshoot in `lesson5_fig53.py` over 0.1-0.4 s (the plotted points keep
  the 0.3 s run, so the SVG does not change). Update the table and prose.

### D5. One quantity reported as 0.0779 s and as 0.0778 s
- Location: lines 201 (0.078), 492 and 497 (0.0779), 523, 532, 679-681 (0.0778);
  `lesson5_ex4_20hz.py` hard-codes 0.0778.
- Problem: The two values come from the two windows of D4. The reader sees two answers for one
  measurement.
- Fix: Use 0.0779 s everywhere (after D4). Make `lesson5_ex4_20hz.py` compute the 10 Hz time instead
  of hard-coding it. New ratio 0.0388/0.0779 = 0.498.

### D6. Fig. 5.1 provenance label is not true
- Location: lines 252-254 and 280-281.
- Problem: "computed to 1e-15 pu by the listing in §4" and "Numbers from §4's listing". The listing
  prints no v_d or v_q. A direct evaluation of `clarke_park` with theta_pll = theta_g gives
  (1.0000000000000002, 1.7e-16) pu. In the running loop at t = 0.099 s, |v_q| = 2.5e-4 pu.
- Fix: State the direct evaluation and the in-loop value. Relabel the caption "derived here".

### D7. "Bandwidth" has two meanings
- Location: line 196, §3 tuning, Exercise 4 (lines 670, 679-681), §5 line 591.
- Problem: "10 Hz closed-loop bandwidth" means omega_n = 2 pi x 10. The -3 dB bandwidth of
  (2 zeta omega_n s + omega_n^2)/(s^2 + 2 zeta omega_n s + omega_n^2) at zeta = 0.707 is
  2.058 omega_n, which is 20.6 Hz for this loop.
- Fix: Define "bandwidth" in the symbol list (§2.1) as omega_n/(2 pi) and give the -3 dB value.
  Say "natural frequency" in §1, and point Exercise 4 to the definition.

### D8. Fig. 5.3 plus/minus 2% band drawn around the wrong value
- Location: lines 546-548.
- Problem: The band is at y = 132.0 and 136.5, centred on e = 0 (y = 134.3). The settling criterion
  uses the final value (-0.0314 rad), where the traces end (y = 141.1). Scale 216 px/rad (from the
  zeta = 0.4 minimum -0.2225 rad at y = 182.4), so 2% of the jump is 2.26 px.
- Fix: Move the band to y = 138.8 and 143.4, label it "plus/minus 2% of final", and say in the
  caption what the grey line and the band are.

### D9. §1 cross-reference points to the wrong section
- Location: line 203. "(§4.3)" should be "(§4.1)"; §4.1 discusses the gap. §1 also says 0.078 s;
  use 0.0779 s.

### D10. Standard-form symbol zeta_n is not defined
- Location: line 344. "2 zeta_n omega_n s". The symbol list has zeta_pll only.
- Fix: Write "2 zeta omega_n s".

### D11. Exercise 1 answer asserts the result and omits its assumption
- Location: lines 617-623.
- Problem: "the cross terms between different frequencies cancel" is not the mechanism. The identity
  is algebraic: p = 1.5(v_alpha i_alpha + v_beta i_beta) + 3 v_0 i_0. It needs i_0 = 0 (three-wire)
  or v_0 = 0. V_base and I_base are not defined (peak or RMS).
- Fix: Write the inverse Clarke map with v_0, give the coefficients (1.5, 1.5, 0, 3 v_0 i_0), state
  the three-wire assumption, and define V_base and I_base as peak phase values
  (S_base = 3 V_rms I_rms).

### D12. Listing in the page differs from the file
- Location: line 457 comment ("semi-implicit:" against the file's "semi-implicit Euler:"); line 489
  says 72 lines.
- Fix: Copy the file's comment. After D1 the file has 75 lines; update the count and the printed
  output block.

### D13. Exercise 3 prose drops a sign
- Location: line 662. Text says 0.000001 pu; the script prints -0.000001 pu. Fix: "-0.000001 pu".

### D14. Imprecise phrasing
- Location: line 497 "13% below" (0.0779/0.0900 = 0.865, 13.5%); line 531 "slightly longer"
  (0.0858 against 0.0779, 10%); line 573 "effectively zero at this precision" (removed by D1);
  lines 563-564 "not free speed" (removed).
- Fix: Give the numbers.

### D15. Source note carries an unresolved "verify" tag
- Location: lines 708-711.
- Fix: Give the full title (Voltage-Sourced Converters in Power Systems: Modeling, Control, and
  Applications, Wiley-IEEE Press, 2010) and delete "verify". Chapter numbers were not checked
  against the book.

## Fix log

Applied 2026-09-22. All scripts were run again after the edits. The listing in the page matches
`lesson5_pll.py` exactly (checked by `diff`). The HTML tag structure is balanced (parser check).

| Defect | Change applied |
|---|---|
| D1 | §4.3 paragraph rewritten (metric compares theta_g(k) with theta_pll(k+1); bias -0.031416 then -0.031730 rad; residual 2.84e-8 and 4.84e-6 rad). `lesson5_pll.py` prints `residual beyond -omega*DT bias`. Output block and listing in the page updated. `*change*` removed. |
| D2 | Exercise 5: "ramp input" changed to "parabolic input"; added e_ss = R/(K_pll k_i,pll) = R/omega_n,pll^2. Exercise 5 now quotes the 4.84e-6 rad residual, not the 0.0003 rad change. |
| D3 | `lesson5_fig53.py` prints overshoot past zero and past final value. Table has both columns: 0.1912 (36.5%), 0.1089 (20.8%), 0.0710 (13.6%) past final; 0.2225 (42.5%), 0.1403 (26.8%), 0.1024 (19.6%) past zero. Prose explains the bias and gives the zeta = 1 closed form (-0.135 Delta_theta). |
| D4 | `lesson5_fig53.py` measures settling and overshoot over 0.1-0.4 s. Table: 0.1593, 0.0779, 0.0858 s. Plotted SVG points not changed. |
| D5 | 0.0779 s used throughout. `lesson5_ex4_20hz.py` computes the 10 Hz time; prints ratio 0.498. Page output block and prose updated. |
| D6 | §2 text states the direct evaluation (1.0000000000000002, 1.7e-16) pu and the in-loop 2.5e-4 pu. Fig. 5.1 caption relabelled "derived here". |
| D7 | New "bandwidth" entry in §2.1 (omega_n = 2 pi f; -3 dB = 2.058 omega_n = 20.6 Hz). §1 says "natural frequency of 10 Hz". Exercise 4 prompt gives omega_n = 2 pi x 20 and points to §2.1. §3 and §5 wording kept; they now use the defined term. |
| D8 | Band moved to y = 138.8 / 143.4, label "plus/minus 2% of final"; caption describes the grey line and the band, with final value -0.0314 rad (same value as §4.2 and §4.3). |
| D9 | §1: "(§4.1)" and "0.0779 s". |
| D10 | "2 zeta_n omega_n s" changed to "2 zeta omega_n s". |
| D11 | Exercise 1 answer now shows the inverse Clarke map with v_0, the coefficients, the three-wire assumption, and peak-value bases. |
| D12 | Listing comment copied from the file; line count 75. |
| D13 | Exercise 3 prose: -0.000001 pu. |
| D14 | "13.5% below ... (0.0779/0.0900 = 0.865)"; "10% longer"; rhetorical phrases removed. |
| D15 | Source note: full title and publisher; "verify" removed. |

Script outputs after the fixes:

```
lesson5_pll.py
settling time (2% of 30 deg jump) = 0.0779 s
angle error just before freq step = -0.031416 rad
angle error at end (after freq step)  = -0.031725 rad
residual beyond -omega*DT bias: before = 2.84e-08 rad, after = 4.84e-06 rad
lesson5_fig53.py
zeta=0.400 settle=0.1593 s; overshoot past zero 0.2225 rad (42.5%), past final 0.1912 rad (36.5%)
zeta=0.707 settle=0.0779 s; overshoot past zero 0.1403 rad (26.8%), past final 0.1089 rad (20.8%)
zeta=1.000 settle=0.0858 s; overshoot past zero 0.1024 rad (19.6%), past final 0.0710 rad (13.6%)
lesson5_ex4_20hz.py
settling time (2% of 30 deg jump) = 0.0388 s
ratio to 10 Hz settling time (0.0779 s) = 0.498
lesson5_ex3_negseq.py (unchanged)
v_q ripple amplitude = 0.10044 pu (predicted 0.10000 pu)
mean v_q over tail = -0.000001 pu
```

Not done:
- Chapter or page numbers for the S06 source were not checked against the book.
- The Fig. 5.3 polylines were not regenerated. They come from the 0.3 s run, and the points in the
  plotted window (0 to 0.18 s after the jump) are the same in the 0.4 s run.
- I did not open the page in a browser. The checks were a tag-balance parse and a diff of the
  listing against the file.
