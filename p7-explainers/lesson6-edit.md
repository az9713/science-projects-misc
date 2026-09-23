# Lesson 6 edit: "Following on a weak grid"

Editor: science-editor standard. Date: 2026-09-22.
Line numbers refer to `lesson6.html` before the fixes.

## Verdict (before fixes)

**Revise before release.** The core derivation is correct: the d-q projection, the lock condition sin(theta_0) = X_g I_d / V_g, the current bound I_d <= SCR V_g, |V_t| = V_g cos(theta_0), P = (V_g^2 / 2X_g) sin(2 theta_0), K_pll = V_g cos(theta_0), and the second-order omega_n and zeta formulas. I re-ran `lesson6_weak_grid.py` and `lesson6_exercises.py`. Every number in the sweep table, the pole table, the Exercise 3 and 4 answers, and Fig. 6.1 and 6.2 geometry matches a recomputation. Four blocking defects remain: the code listing does not produce the printed output, the Fig. 6.3 runaway trace is not the simulation output, and two prose passages state wrong relations. Nine smaller defects follow.

## Checks run

- `python lesson6_weak_grid.py`: output identical to the printed block (lines 582-594).
- `python lesson6_exercises.py`: SCR = 1.016, zeta = 0.2973, K_pll = 0.177, theta_0 = 79.8 deg; retune k_p = 160.7, k_i = 7141.9; at SCR 10, omega_n = 84.3 rad/s, zeta = 0.949. All match the page.
- Pole table (lines 664-669): recomputed from s^2 + K k_p s + K k_i = 0; all six rows match to the printed digits.
- Fig. 6.1: both phasor diagrams recomputed at 120 px/pu; endpoints, V_t lengths (0.9950, 0.5528) and arc angles (5.74, 56.44 deg) match.
- Fig. 6.2: both polylines match K_pll(SCR) and SCR/2 on the stated axes.
- Fig. 6.3 left panel: resampled from RK4 at 6 ms spacing and 157.14 px/rad; matches (peak 1.348 rad at t = 0.054 s).
- Fig. 6.3 right panel: does not match (defect B4).
- P1 plan `../p1-textbook/book-plan.md` line 310: k_p = 88.86, omega_n = 46.72 rad/s, 7.44 Hz, as quoted.

## Defects

### Blocking

**B1. Section 4 listing, lines 489-580.** The listing is not the file `lesson6_weak_grid.py`. It has no header `print` in `part1()`, no `k_p_pll=... k_i_pll=...` line in `__main__`, and a different `simulate()`. Run as printed, it cannot produce the header row and the gains line in the "Actual output" block. Line 474 also says "about 90 lines"; the file has 99. **Fix:** replace the listing with the verbatim, HTML-escaped file; change "about 90 lines" to "99 lines, reproduced verbatim".

**B2. Section 2, lines 289-293.** "falls back toward zero as theta_0 continues to 56 deg, so it is exactly at the current bound itself ... that the model's derived power has fallen all the way back to zero". 56 deg is wrong (the fall is from 45 deg to 90 deg) and the sentence is garbled. **Fix:** "then falls back toward zero as theta_0 continues from 45 deg to 90 deg. At the current bound itself, where theta_0 = 90 deg, the model's delivered power is zero. Delivered power is therefore not monotonic in current on a weak grid: it rises with I_d until I_d = SCR V_g sin(45 deg) = 0.707 SCR V_g, then falls."

**B3. Section 3, lines 414-418, and Fig. 6.2 caption, lines 466-468.** The text says P_max "overtakes P far more slowly" and "stays well above the delivered figure until SCR gets close to 1"; the caption says P_max "is not the binding constraint anywhere near the bound". Recomputed: between SCR 3 and 1.2, P falls by 41% (0.9428 to 0.5528) and P_max by 60% (1.500 to 0.600). P = P_max exactly at SCR = sqrt(2) = 1.414 (theta_0 = 45 deg); at SCR 1.5 the gap is 0.0046 pu. **Fix:** state the two percentages with their endpoints, the touch point SCR = 1.414, the 0.0046 pu gap, and that below SCR 1.414 rated current is on the falling side of sin(2 theta_0). Caption: "P_max is linear in SCR (SCR/2). P at I_d = 1 pu touches P_max only at SCR = sqrt(2) = 1.414 (theta_0 = 45 deg) and is below it at every other SCR."

**B4. Fig. 6.3 right panel, line 618 and caption lines 634-640.** The polyline ends at 14.54 rad at t = 0.1 s (y = 41.96 at 15 px/rad). The script gives 15.86 rad. The caption says "already past 16 rad", which is also false. "Keeps accelerating" is false: over the run, d(theta_p)/dt varies between 42.6 and 1910 rad/s, slow near sin(theta_p) = 1. The left-panel top label "1.4" (line 626) sits at y = 20, which is 1.53 rad on the 157.14 px/rad scale. **Fix:** regenerate the right polyline from `simulate(0.95, t_end=0.1)` at 2.5 ms spacing; relabel the left top tick "1.53"; rewrite the caption with 15.86 rad, the 42.6-1910 rad/s range, the v_q minimum 0.0526 pu, and the sampling of both panels.

### Non-blocking

**N1. Section 2 equation, line 314.** zeta = 0.7071 sqrt(K_pll). The gains use zeta = 0.707 exactly, so k_p / (2 sqrt(k_i)) = 0.707. **Fix:** 0.707 sqrt(K_pll); state the identity in the parenthesis.

**N2. Section 3, lines 393-395.** "both are computed from the same closed form, so neither is wrong". The two k_p values come from different inputs: 88.86 = 2 x 0.7071 x 62.83, 88.84 = 2 x 0.707 x 62.83. 46.72 and 46.71 are two roundings of 46.715 rad/s. **Fix:** say exactly this.

**N3. Section 2, lines 324-331.** K_s and K_pll described as "a voltage-times-reactance-ratio term times the cosine". K_pll = V_g cos(theta_0) has no reactance factor. **Fix:** "an amplitude times the cosine"; add that K_s carries 1/X and K_pll does not; X_g enters K_pll only through theta_0.

**N4. Fig. 6.4, lines 688 and 705-712.** The K_pll = 0.1 markers are filled light grey, not "hollow". A vertical frame line at x = 50 reads as an imaginary axis; the real imaginary axis is the orange dashed line at x = 477.27. The axes are scaled 8.55 px per unit Re(s) and 2.60 px per unit Im(s), which is not stated. **Fix:** remove the x = 50 line; "teal circles" and "light grey circles"; add the scale note.

**N5. Exercise 2, lines 776-778 and 790-793.** The X_g I_d term's derivative is zero at every theta_p, not only "at lock". **Fix:** "identically zero"; in the answer, "drop out of the derivative at every theta_p, not only at lock".

**N6. Symbol table, line 217.** I_d listed as "state input". It is an input, not a state. **Fix:** "input (1.0 in the examples)".

**N7. Sources note, lines 863-865.** Says full listings of both scripts are reproduced above; `lesson6_exercises.py` is not listed. **Fix:** say that only `lesson6_weak_grid.py` is listed, and that the exercises script's results are quoted in Exercises 3 and 4.

**N8. Section 5, line 674, and Section 6, line 745.** "an oscillatory instability observed below [the static bound]" is ambiguous in direction. **Fix:** "before it is reached (at an SCR above the bound's value)".

**N9. Section 2, line 309.** "remarkably" gives no reason. **Fix:** "because both equal v_d at lock".

## Not changed (noted, outside what I could verify)

- S07 and S08 carry "verify" tags. The bibliographic data match the real papers (Zhang, Harnefors, Nee 2010, IEEE TPWRS 25(2) 809-820; Zhou et al. 2014, IEEE TPWRD 29(5) 2287-2296). I did not check the specific claims (P_max = SCR V_g |v| with reactive support; PLL/current-loop oscillatory instability) against the paper text, so the tags stay.
- "the same convention Lesson 2 used for E'" (line 228): not checked against Lesson 2.
- PLL gain units given as 1/s and 1/s^2; strictly rad/(s pu) and rad/(s^2 pu). Left as the series convention.

## Fix log

Applied 2026-09-22 to `lesson6.html` in place. Backup of the original: scratchpad `p7_l6_edit_backup.html`.

| ID | Status | Change |
|----|--------|--------|
| B1 | fixed | Listing replaced by the verbatim HTML-escaped `lesson6_weak_grid.py` (99 lines); "about 90 lines" changed to "99 lines, reproduced verbatim". |
| B2 | fixed | 45-to-90 deg sentence rewritten; power-maximising current 0.707 SCR V_g added. |
| B3 | fixed | Section 3 paragraph and Fig. 6.2 caption rewritten with 41% / 60%, SCR = 1.414 touch point, 0.0046 pu gap. |
| B4 | fixed | Fig. 6.3 right polyline regenerated from RK4 (41 points, 2.5 ms, 15 px/rad; ends 15.86 rad); left top label "1.4" to "1.53"; caption rewritten. |
| N1 | fixed | 0.7071 to 0.707; identity k_p/(2 sqrt k_i) = 0.707 stated. |
| N2 | fixed | Two-input explanation of 88.86 vs 88.84 and 46.72 vs 46.71 (46.715). |
| N3 | fixed | K_s / K_pll analogy corrected. |
| N4 | fixed | x = 50 line removed; marker colours named; axis-scale note added. |
| N5 | fixed | Exercise 2 statement and answer reworded. |
| N6 | fixed | "state input" to "input (1.0 in the examples)". |
| N7 | fixed | Sources note corrected. |
| N8 | fixed | "below" to "before it is reached (at an SCR above the bound's value)" in Sections 5 and 6. |
| N9 | fixed | "remarkably" replaced by the reason. |

Post-fix checks: all 20 replacement strings matched exactly once; the page has no `<script>` or `<link>` tags; the new right polyline appears once.
