# Lesson 2 edit — science-editor pass

File: `p7-explainers/lesson2.html` (690 lines before fixes). Code: `p7-explainers/lesson2_smib.py`.

## Verdict (before fixes)

**Revise before publication.** The core computation is correct. I re-ran `lesson2_smib.py`. Its output is byte-identical to `lesson2_smib_output.txt`. Every headline number reproduces: P_max 1.6923 pu, delta_0 0.4924 rad = 28.2115 deg, K_s 1.4913 pu/rad, omega_n 8.9618 rad/s = 1.4263 Hz, zeta 0.01594, eigenvalues -0.1429 +/- j8.9607, step case 1.4129 Hz (linearised) and 1.4127 Hz (zero crossings), H sweep and finite-difference sweep. The derivation of omega_n = sqrt(K_s omega_0 / 2H) and zeta = K_D / (4 H omega_n) is correct. Figures 2.1 and 2.2 are plotted to the correct data scale (I checked marker positions, tangent slope 0.689 px/px = K_s, and the envelope ratio 0.424 = exp(-0.1429 x 6)).

The page has 24 defects. Six are blocking: two wrong equations or derivation steps (D1, D2), a wrong physical statement (D3), a wrong arithmetic value (D4), a false claim that an output block is verbatim (D12), and a wrong error figure with a wrong cause (D13). The others are wrong cross-references, unsupported claims, figure errors, and editorial notes left in customer-facing text.

## Defects (location = line in the pre-fix file)

| # | Location | Problem | Fix |
|---|---|---|---|
| D1 | L262 | Linearised equation reads `2H d(ΔΔω)/dt`. Δω is already a deviation (its equilibrium value is 0), so ΔΔω is a typo. | Write `2H d(Δω)/dt`, and add the companion equation dΔδ/dt = ω0Δω. |
| D2 | L224-228 | Equilibrium reasoning is swapped. The text says the *second* equation gives Δω = 0 and the *first* then holds for any δ. In fact dδ/dt = ω0Δω = 0 (first equation) forces Δω = 0; the second equation then gives the torque balance. The bracketed remark about "drive term" is incorrect. | Rewrite in the correct order. |
| D3 | L269-271 | "K_D resists the rate of change of Δω". The term K_DΔω is proportional to Δω itself, that is to the rate of change of δ, not to dΔω/dt. | "It opposes the speed deviation Δω, which is the rate of change of δ." |
| D4 | L271-272 | cos(28.2115°) printed as 0.8815. The correct value is 0.8812 (0.8815 x 1.6923 = 1.4918, not the printed 1.4913). | Print 0.8812. |
| D5 | L238-249 | The note says the book plan's delta_0 = 0.4926 rad and K_s = 1.4915 differ from the probe by "rounding in the earlier hand pass, not an error in either script". This is not rounding: arcsin(0.4727) = 0.4925 and the exact ratio gives 0.4924; the book plan's cos(delta_0) = 0.8814 is also off (exact 0.8812). The book plan is not a script. The note points to "Section 4" for the probe (it is Section 5). The last sentence ("An editor must not…") is an internal note. | Rewrite: state that the book plan's values do not reproduce, give the exact values, and say the lesson uses the computed values. Delete the editor sentence. |
| D6 | L241, L281, L637 | Three references to "Section 4" for the code and the Jacobian check. The code is Section 5. | Change to Section 5. |
| D7 | L200, L511-512 | Internal notes in customer-facing text: "exactly as specified", "An editor must never 'fix' one of them". | Delete; keep the physics statement. |
| D8 | L207-215 | Claim that "Park's transformation is amplitude-invariant here and the d-axis is aligned to the measured terminal voltage, which is the convention used to get E′". No source supports it; the book plan gives E′ = 1.1 pu directly; aligning the d-axis to terminal voltage is not the usual classical-model convention. | Replace with: E′ is given as 1.1 pu in Example 1.1; no dq frame is needed in this lesson. |
| D9 | L194 | X decomposition "0.45 machine + 0.40/2 line". Per the book plan, 0.45 pu is X′d plus transformer, and 0.40/2 is two parallel 0.40 pu lines. | Say so. |
| D10 | L299-305 | Says H of 2-8 s and K_s of 1-2 pu/rad give a result "in the 0.7-2 Hz band". The formula gives 0.77 Hz (K_s 1, H 8) to 2.19 Hz (K_s 2, H 2). The citation puts the band at Kundur §3.9 Table 3.2; that table location is for typical H values; the local-mode band is in the small-signal chapter (Ch. 12). | State the computed range 0.77-2.19 Hz and that it overlaps the 0.7-2 Hz band; split the citation (H range §3.9 Table 3.2; local-mode band §12.1), both marked verify. |
| D11 | L358-360 | "does four things in about 40 lines of working code" and "(b) … prints it beside the hand-derived A". The listing has 75 non-blank lines and it contains no print statements (it is a condensed excerpt of the script). | Say it is a condensed excerpt of 75 non-blank lines, and that the full script prints the results. |
| D12 | L465-493 | Output block is labelled "probe values, not hand-typed", but the two Jacobian lines are reformatted (the script prints tuples to 17 digits), two of four diff lines are dropped, a comment "(agrees to about 6 digits)" is added, and the H sweep and step-size sweep that Exercises 3 and 4 quote are omitted. | Replace with the verbatim script output (all sections). |
| D13 | L507-509 | "1.4129 Hz against 1.4127 Hz, a difference of about 0.02 Hz, i.e. under 0.2%". The difference is 0.0002 Hz, about 0.01%. The cause is not the window or step size: zero crossings measure the damped frequency omega_n sqrt(1-zeta^2), which at the new point is 1.41272 Hz and matches 1.4127 Hz; 1.4129 Hz is the undamped omega_n. | Give the correct difference and cause. |
| D14 | Fig. 2.1, L331-339, L347 | Caption says the P_m = 0.8 pu line is drawn dashed. No such line exists; the dashed line at y = 140 is the P = 0 axis, and the label "P_m = 0.8 pu" sits next to that axis. | Draw the line at y = 83.53 (0.8 pu on the plot scale 70.59 px/pu) and move the label to it. |
| D15 | Fig. 2.3, L570, L582, L585-592 | (a) The arc uses sweep-flag 1, so it is drawn in the right half-plane (Re > 0), away from the eigenvalues. (b) The "Re" label is at x = 565, outside the 560-wide viewBox, so it is not visible. (c) The axes use 40 px per unit on Re and 12 px per unit on Im, so the circle is drawn as an ellipse; the caption does not say so. | Sweep-flag 0; label at x = 536; add the scale note to the caption. |
| D16 | Fig. 2.2, L528-532 | No values on the δ axis. | Add tick labels for δ0 = 28.21° and δ_new = 30.15° (scale 22.5 px/deg). |
| D17 | L559-561 | "remove any one of E′, X, H, or the sine nonlinearity and there is no oscillation left". False for the sine: a linear spring P = K_sδ still oscillates. "in a precise sense" is rhetorical. | Remove the sine from the list; give the reason for each of E′, X, H. |
| D18 | L548-549 | Saliency described as "the reactance X is the same in every direction". | "the same on the d-axis and the q-axis". |
| D19 | L656-662 (Ex. 4) | Round-off explanation is imprecise ("agree to within machine precision"). No error model is given. | Give the two terms: truncation (h/2)·P_m/(2H) = 0.0571·h (5.71e-4 at h = 1e-2, observed 5.750e-4); round-off ≈ ε·0.8/(2H)/h ≈ 2.5e-9 at h = 1e-8 (observed 8.2e-10, same order); minimum near h = sqrt(2.5e-17/0.0571) ≈ 2e-8. |
| D20 | L669-676 (Ex. 5) | "about 10% per cycle" (exact: 9.5%, ratio exp(-2πζ/√(1-ζ²)) = 0.905). "without changing the frequency it oscillates at": omega_n is unchanged, but the damped frequency drops (8.9607 to 8.7018 rad/s at K_D = 30, run output). "beat against neighbouring machines' modes" is outside a one-machine model. PSS citation "§3.9" is the swing-equation section; PSS is in Ch. 12. | Correct all four; mark citation verify. |
| D21 | L684-686 | Sources: Example 1.1 is at `book-plan.md` §4 (Chapter 1 specification), not §5.2 (the citation rule). "full, runnable listing … reproduced above" is false; the page shows an excerpt. | Correct both. |
| D22 | L319-320 | "time constant ≈ 7 s, which is why … tens of seconds" gives no count. | Add: amplitude falls to e^-4 ≈ 2% after 4τ ≈ 28 s. |
| D23 | L306-308 | "an inertia-and-stiffness product that produces omega_n" — omega_n depends on the ratio, not a product. | "a stiffness-to-inertia ratio that gives omega_n ≈ 9 rad/s". |
| D24 | L462-463 | "every number below is its real printed output" — true only after D12 is fixed. | No text change beyond D12. |

## What already works

- The opening problem states a real question (why 1.4 Hz, why slow decay) and the lesson answers both with computed numbers.
- The finite-difference Jacobian check is a correct and useful method to catch a sign or factor-of-two error.
- The step-case trap (1.4263 Hz against 1.4127-1.4129 Hz at two operating points) is correct and well placed.
- Exercises 1-3 are correct: K_s(95°) = -0.1475 pu/rad; zeta x omega_0 = 6.01; H^-0.5 scaling holds (0.0211/0.0105 = 2.0 = sqrt(8/2)).

## Fix log (applied to lesson2.html in place, 2026-09-22)

| # | Status | What changed |
|---|---|---|
| D1 | fixed | Equation now `dΔδ/dt = ω0Δω, 2H dΔω/dt = −K_sΔδ − K_DΔω`, plus one sentence on why Δω needs no second Δ. |
| D2 | fixed | Equilibrium paragraph rewritten: first equation forces Δω = 0, second gives the torque balance. |
| D3 | fixed | K_D now "opposes the speed deviation Δω, which is the rate of change of δ". |
| D4 | fixed | 0.8815 changed to 0.8812. |
| D5 | fixed | Note rewritten: book-plan values 0.4926 rad / 0.8814 / 1.4915 do not reproduce; exact 0.4924 / 0.8812 / 1.4913; rounded ratio gives 0.4925. Editor sentence deleted. |
| D6 | fixed | Three "Section 4" references changed to Section 5. |
| D7 | fixed | "exactly as specified" and "An editor must never…" deleted. |
| D8 | fixed | Park/d-axis sentence replaced: E′ = 1.1 pu is given; no dq frame needed. |
| D9 | fixed | Table row now names X′d plus transformer and two parallel 0.40 pu lines. |
| D10 | fixed | Computed range 0.77-2.19 Hz stated; citation split to §3.9 Table 3.2 (H) and §12.1 (band), both "verify". |
| D11 | fixed | Code intro now says condensed excerpt, 75 non-blank lines, no print statements; full script prints. Excerpt re-run: 28 crossings, 1.41266 Hz. |
| D12 | fixed | Output block replaced with the verbatim script output, including H sweep and step-size sweep. |
| D13 | fixed | Difference now 0.0002 Hz, about 0.01%; cause given as damped (1.41272 Hz) against undamped (1.4129 Hz) frequency. |
| D14 | fixed | P_m = 0.8 pu dashed line drawn at y = 83.53; label moved to it; P = 0 axis labelled; caption updated. |
| D15 | fixed | Arc sweep-flag 1 → 0 (left half-plane); "Re" label moved to x = 536; caption states 40 px vs 12 px per unit scales. |
| D16 | fixed | δ-axis tick labels 28.21 and 30.15 added; caption states 22.5 px per degree. |
| D17 | fixed | Paragraph rewritten with a reason for each of H, E′, X; sine removed from the list; rhetorical phrase removed. |
| D18 | fixed | Saliency now "same on the d-axis and the q-axis". |
| D19 | fixed | Ex. 4 answer now gives the truncation (0.0571·step) and round-off (2.5e-17/step) terms and the predicted best step ≈ 2e-8. |
| D20 | fixed | Ex. 5: 9.5% per cycle (ratio 0.905); ω_n unchanged, damped frequency 8.9607 → 8.7018 rad/s; neighbouring-machine clause removed; citation §12.5 "verify". |
| D21 | fixed | Sources: book-plan §4 (Chapter 1 specification); "condensed excerpt … and its full printed output". |
| D22 | fixed | Added: e^-4 ≈ 2% after 4 time constants, about 28 s. |
| D23 | fixed | "stiffness-to-inertia ratio". |
| D24 | no change needed | Resolved by D12. |

Checks after fixes: HTML tag balance clean (Python HTMLParser); no external scripts, stylesheets, or links; excerpt code executes; no remaining "Section 4", "editor", "0.8815", or "ΔΔω" strings. Not done: Kundur section numbers (§3.9, §12.1, §12.5) are not checked against the book; they stay marked "verify".
