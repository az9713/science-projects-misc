# Lesson 7 edit — "Forming Instead of Following: Droop Is a Swing Equation"

File: `p7-explainers/lesson7.html` (41,411 bytes before edit). Standard: science-editor (precise statement, every term defined, proof in the smallest setting, limit case, tie to something concrete).

## Verdict (before fixes)

**Minor revision.** The central result is correct. `H_eq = 1/(2 m_p omega_c)` and `K_D,eq = 1/m_p` follow exactly from the two equations. Every number in the lesson reproduces. One step of the derivation text has a sign error. The explanation of the Part 2 frequency gap is wrong. Two figures render wrong labels or colours. The energy comparison lacks its limit case (a capacitor cannot be drained to 0 V).

## Re-run and recompute

- `python lesson7_droop_vs_swing.py` reproduces the printed output line for line (Part 1 gap 8.7e-19 pu; final dw -0.005000; K_s 1.4913; omega_d 12.77; sigma -3.148; E_dc 14.4 kJ; ratios 243, 1111, 11.1).
- Table (m_p = 0.05): omega_c = 2pi*5 -> 0.3183 s; 2pi*1 -> 1.5915 s; 2 -> 5.000 s; 2.857 -> 3.500 s; 2/(2pi) = 0.318 Hz; 2.857/(2pi) = 0.4547 Hz; tau = 0.35 s. All correct.
- Linearised droop + grid: omega_n^2 = omega_0 K_s m_p omega_c = 376.99 * 1.4913 * 0.31416 = 176.6; omega_n = 13.29 rad/s (2.115 Hz); zeta = 0.2364; eigenvalues -3.1416 +/- j12.913. Correct. Ratio 0.2364/0.01594 = 14.8. Correct.
- Fig. 7.2 coordinates: x = 280 px/decade, y = 106.7 px/decade. All curve vertices, the 3.5 s line (y = 143.2) and all four dots are on the correct positions.
- Fig. 7.3 coordinates: 115 px/decade. Bars 3.5 MJ (y 47.8), 0.16 MJ (y 201.7), 14.4 kJ (y 321.8) are correct.
- Exercise 3: C = 2 * 3.5e6 / 1200^2 = 4.861 F = 243.1 x 20 mF. Correct.
- Inertial energy: 2 H S df/f0 = 16.00 MJ is the first-order value; the exact value H S [1 - (1 - df/f0)^2] = 15.87 MJ.

## Defects (location, problem, fix)

| # | Location | Problem | Fix |
|---|---|---|---|
| D1 (blocking) | lines 396-401 | Sign error. From Δω = -m_p(P_f - P_ref), P_ref - P_f = +Δω/m_p, so P - P_f = dP + Δω/m_p. The text says "dP - Δω/m_p". The displayed equation is correct; the justification of it is wrong. | Write "= dP + Δω/m_p". |
| D2 | lines 372-406 | `s` is used as an operator and never defined. The filter uses `P`, the imbalance uses `P_e`, with no statement that they are the same. The swing-equation match needs P_m = P_ref; the text says only "constant P_m". | Define s = d/dt, state P = P_e, state P_m = P_ref. |
| D3 (blocking) | lines 782-790 | Wrong explanation of the Part 2 gap. The 12.91 rad/s target is linearised at the pre-step point (P_ref = 0.8). The simulated oscillation is about the post-step point (P_ref = 0.85), where K_s = 1.4634 pu/rad, omega_n = 13.16 rad/s, omega_d = 12.78 rad/s. The measured 12.77 matches that to 0.1 %. "Within a few percent" is also imprecise: the gaps are 1.1 % (omega_d) and 0.2 % (sigma). | Rewrite the paragraph with both linearisation points and the measured percentages. |
| D4 | lines 776-779 | Refers to "the lesson's own estimate of about 3e-17", which does not appear in the lesson. | Delete; state the gap relative to 0.005 pu (about 2e-16, near one unit of double-precision roundoff). |
| D5 | listing vs `lesson7_droop_vs_swing.py` | The script file had a dead line `rising_prev = 0.0` absent from the listing, so the claim "run as printed" was false. | Delete the dead line from the script. Listing and printed output now match the file and its run byte for byte (checked). |
| D6 | line 485 | Fig. 7.2 y-axis label uses `&#8330;` (subscript plus) and renders "H₊₊ (s)". | Replace with H + `<tspan>` subscript "eq". |
| D7 | lines 465, 497-498 | In SVG, a class CSS `fill` overrides a `fill` attribute. The 3.5 s dot and label render teal/white, not orange. The dot radius exists only as CSS `r`. | Use `style="fill:..."`, add `r="4"` attributes. |
| D8 | Fig. 7.1, lines 291-322 | Caption and figure text say the circuit is "identical in both panels", but the left source is a controlled current source and the right a controlled voltage source. The left source symbol (a dot and a cross) is not a standard symbol. The `font-size` attributes on classed text are overridden by the class CSS. | Say the network (X, V∠0) is identical and the source type differs; draw the current source as a circle labelled I; move font sizes to `style`. |
| D9 | lines 203-204 | "1.59 s ... in the same range as a real turbo-generator" is not supported. The lesson's own reference machine is 3.5 s; Lesson 2 sweeps 2.0-8.0 s. | State 1.59 s as 0.45 of the 3.5 s machine used in Lesson 2. |
| D10 | lines 205-207 | "at typical ratings" is unsupported (the ratings are Example 3.2's). "243 times less" is an imprecise ratio. | Name the ratings; write "1/243 of". |
| D11 | line 444 (also 569) | "P1" is never defined in the lesson. | Define it once: the companion P1 textbook. |
| D12 | lines 577-590, Fig. 7.3 | (a) 16 MJ is the first-order value (exact 15.87 MJ). (b) The demand bar uses H_v = 5 s while the machine bar uses 3.5 s, and the chart does not say so. (c) The 11.1 ratio assumes the DC link can be drained to 0 V. With a 10 % DC-voltage dip the capacitor releases 1 - 0.9^2 = 19 % of 14.4 kJ = 2.74 kJ, and the per-MVA ratio becomes 58. | Mark "≈" with the exact value; label the demand bar H_v = 5 s; add the limit case. |
| D13 | lines 796-802 | Limitation bullet says the coefficient match holds only near θ0. That contradicts the (correct) statement that the match needs no linearisation. Only K_s and the eigenvalues need it. | Split the two claims. |
| D14 | lines 810-816 | "a few capacitor time constants" is undefined; "treats v_dc0 as freely available" is vague. | Give the concrete duration: 14.4 kJ at 0.1 pu (100 kW) lasts 0.144 s if drained fully. |
| D15 | lines 552-553 | Matching control ties the frequency (ω ∝ v_dc) to the DC voltage; the angle is its integral. Text says "angle directly". | Correct the statement. |
| D16 | lines 346-348 | Units "rad/s or p.u." are ambiguous; the derivation and code need per-unit ω with m_p in pu/pu. | State per unit. |
| D17 | lines 363-364 | "no memory and no dynamics" is false: θ is still an integrator state. The filter adds a frequency state. | Say "no frequency dynamics". |

Not changed: the DVOC citation (Colombino, Groß, Brouillon, Dörfler 2019, IEEE TAC 64(11) 4496-4511) keeps its `verify` tag. This pass did not check it against the journal.

## Fix log

All fixes applied in place to `lesson7.html` on 2026-09-22. Script `lesson7_droop_vs_swing.py` edited for D5 only (dead line removed; output unchanged).

- D1: sign corrected to "dP + Δω/m_p".
- D2: s = d/dt defined; P = P_e stated; P_m = P_ref stated at the swing-equation comparison.
- D3: Part 2 commentary rewritten: 1.1 % / 0.2 % gaps; post-step linearisation K_s = 1.4634, omega_d = 12.78 rad/s, 0.1 % from the measured 12.77.
- D4: phantom 3e-17 estimate removed; relative gap stated.
- D5: script dead line removed; listing = file, printed output = fresh run (checked by script).
- D6: y-axis label now H<sub>eq</sub>.
- D7: orange dot and label use inline style; `r="4"` on all dots.
- D8: Fig. 7.1 left source redrawn as a circle labelled I; caption and in-figure note corrected; font sizes moved to style.
- D9: turbo-generator claim replaced with "0.45 of the 3.5 s machine".
- D10: ratings named; "1/243 of".
- D11: P1 defined at first use.
- D12: 16 MJ marked first-order (exact 15.87 MJ); demand bar labelled H_v = 5 s; 10 % dip limit case (2.74 kJ, ratio 58) added to text and Fig. 7.3 caption.
- D13: limitation bullet split into exact match vs linearised K_s/eigenvalues.
- D14: capacitor duration 0.144 s at 100 kW added.
- D15: matching control statement corrected (ω ∝ v_dc).
- D16: per-unit convention stated.
- D17: "no frequency dynamics" wording.
- D18 (found during the fix pass): Exercise 5's answer called 11.1 "the honest" ratio, which conflicted with the new D12 limit case. Changed to "the same-rating 11.1 (or 58 once only the usable energy above a 10 % DC-voltage dip is counted)".

Note: line numbers in the Defects table refer to the file before the edit (41,411 bytes). The file after the edit is about 44.2 kB.
