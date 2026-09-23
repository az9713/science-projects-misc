# Lesson 8 edit (science-editor standard)

File: `p7-explainers/lesson8.html` (1191 lines before fixes).

## Verdict (before fixes)

**Accept with minor revisions.** The core results are correct. I re-ran both listings. `lesson8_nadir.py` and `lesson8_two_unit.py` print exactly the output embedded in the page. I recomputed each closed-form number by hand: RoCoF_0 = 0.125 Hz/s, the nadirs 49.583 / 49.375 / 48.750 / 47.500 Hz, the floor 104.2 GVA·s, 5600 MVA·s, 179.2 MJ = 49.8 kWh, 224 MW, 0.20 pu, 1120 MVA, and 22,500x. All are correct. I also checked the Fig. 8.1 and 8.3 plotted coordinates against the model; they are correct to 0.1 px. The nadir derivation and the factor-4 explanation are correct.

The defects are these: one symbol with two meanings (`dP`), a missing substitution step in the key derivation, three "exact / agree to digits printed" claims that the numbers do not support, one unit error (GVA x h given as kWh), one wrong scale ratio in a caption, one causality error, an exercise answer that asserts a result it was asked to show, and two figure-layout collisions. None of them changes a headline number.

## Checks run

- `python lesson8_nadir.py`: output identical to the page listing output.
- `python lesson8_two_unit.py`: output identical to the page listing output.
- Independent script (scratch, `p7_l8_edit_check.py`): full-precision eigenvalues and eigenvectors for X12 = 2.0 and 4.0 pu, the Exercise 3 damped-nadir RK4 at D_load = 0 / 500 / 5000 MW/Hz, and the sizing arithmetic.
  - X12 = 2.0: eigenvalues 0, -0.28000320, -0.15166507 +/- j11.834796. |lambda| = 11.8358, omega_n formula = 11.8358, zeta = 0.01281. Relative-mode angle ratio d1/d2 = -0.5625 = -M2/M1.
  - X12 = 4.0: delta = 46.52 deg, K12 = 0.1897, f = 1.1443 Hz. The page value 1.144 Hz is correct.
  - Exercise 3: nadir -0.6250 Hz at t = 10.00 s, -0.4464 Hz at t = 7.77 s, -0.1366 Hz at t = 3.17 s. The page values are correct.
  - Exact energy release for a 0.8 Hz drop: 177.8 MJ, against the linearized 179.2 MJ.

## Defects found

| # | Location (line before fix) | Problem | Fix |
|---|---|---|---|
| 1 | L353-356, key derivation | `dP(t)` is defined as "net imbalance power, positive when power is missing". The equation then uses a constant `dP` in `-dP + dP t/T`. One symbol has two meanings, and the sign of `dP(t)` does not match the sign of the right-hand side. | Define `dP` as the size of the loss (MW, positive). State the net surplus as `-dP(1 - t/T)` for 0 <= t <= T and zero after. |
| 2 | L367-370 | The step from the per-unit COI equation to `(2 E_kin,sys / f0) d(df)/dt` is stated as "converts ... into energy and hertz" and is not shown. | Show the two substitutions, `Sum M_i = 2 E_kin,sys / S_sys` and `dw_COI = df/f0`, then multiply by `S_sys`. Units: MVA·s = MJ, power in MW. State K_D = 0. |
| 3 | L553-558 | "-0.280 1/s exactly". The solver gives -0.280003. The formula `-(KD1+KD2)/(M1+M2)` is exact only when KD1/M1 = KD2/M2. Here the ratios are 0.25 and 0.333 1/s. | Give the solver value. State the exactness condition. Say it holds to five decimals. |
| 4 | L562-567 | "omega_n = 11.84 rad/s, matching the eigenvalue's imaginary part to three figures." omega_n equals the eigenvalue magnitude, 11.8358. The imaginary part is the damped frequency, 11.8348. The printed 11.84 / 11.83 split is a rounding effect across 11.835. | Give both values to 4 decimals. Identify the imaginary part as omega_n sqrt(1 - zeta^2). Explain the rounding split. |
| 5 | L1020-1024 | "both agree with the solver to the number of digits printed". False as printed: 11.84 against 11.83. | Replace with the 4-decimal values and "agree to four decimals". |
| 6 | L647-648, Fig. 8.2 caption | "real-axis scale about 28 times finer". 28 is the ratio of axis ranges (14/0.5). The pixel spans are different: real 260 px per unit, imaginary 360/28 = 12.9 px per unit. The scale ratio is 20.2. | "about 20 times finer", with both px-per-unit figures. |
| 7 | L697-701, energy paragraph | "1.12 GVA x 1 h = 1,120,000 kWh". VA·h is not W·h. "A modest battery already holds hours" contradicts the one-hour store. | State unity power factor as an assumption (1120 MVA carries 1120 MW), then 1120 MWh. Replace "hours" with "the event lasts about 10 s and the store lasts 3600 s". |
| 8 | L684 / energy paragraph | 179.2 MJ is the linearized release 2E df/f0. This is not stated. | Add the exact value 177.8 MJ (0.8% lower) and name 179.2 MJ as linearized. |
| 9 | L774-775, Fig. 8.3 caption | "differ by four and a half orders of magnitude". 4.032e6 / 179.2 = 22,500, which is 4.35 orders. | "a factor of 22,500, or 4.35 orders of magnitude". |
| 10 | L745, L776, Fig. 8.3 | The bar label "1.12 GVA, 1 h" and the caption carry the same VA-for-energy error as #7. | Label "1120 MWh store". Caption states 1120 MW, unity power factor assumed. |
| 11 | L711-713 | `I_max` = 1.2 pu is called "the assumed I_max" but no assumed tag is attached where it is used. Adding 0.2 pu and 1.0 pu current as plain magnitudes assumes both are in phase. | Add the `assumed for this case` tag. State the in-phase (unity power factor dispatch) assumption. |
| 12 | L788-791, code intro | "RK4, accurate for a right-hand side that changes with time, unlike forward Euler". Forward Euler also handles a time-varying right-hand side; the difference is order. For a t-only right-hand side, RK4 is Simpson's rule and is exact on a linear ramp. | State the order (fourth power against first power). State that RK4 is exact here up to rounding. |
| 13 | L1099-1100, Exercise 2 answer | "the 1 ms RK4 step is far below the tolerance that would show any difference". Wrong mechanism: the agreement is exact for any step. | Replace with the Simpson's-rule exactness statement. |
| 14 | L1114-1130, Exercise 3 answer | The exercise asks to *show* that the nadir is shallower. The answer gives only three numeric cases. It also omits that the damped nadir occurs before T. | Add a comparison proof: y = df_damped - df_undamped satisfies y' + a y = -a df_undamped >= 0, with y(0) = 0, so y >= 0. Add the nadir times 7.77 s and 3.17 s. |
| 15 | L1141-1143, Exercise 4 answer | "a smaller K12 needs a larger angle". This reverses the cause: K12 is the result of the angle, not the cause. The cause is the smaller peak transfer E1E2/X12. | "the peak transfer E1E2/X12 falls from 0.5513 to 0.2756 pu, so a larger angle is needed". |
| 16 | L490-497, Fig. 8.1 | The legend at x = 430-620, y = 30-84 overlaps the 300 GVA·s curve, which runs at y = 80-81.7 px across that span. | Move the legend to the empty lower-left region (x = 80, y = 266-320). No curve enters that region. |
| 17 | L768, Fig. 8.3 | The "1.0 pu dispatch" label sits at y = 80, inside the orange headroom segment (y = 60-86.7), not the teal dispatch segment. | Move it to y = 156 inside the teal segment, in dark fill for contrast. |
| 18 | L931 in page listing and `lesson8_two_unit.py` docstring | The docstring says `2H d(dw)/dt`. The code and text use system-base M_i = 2 H_i S_i / S_sys. | The docstring now says `M_i d(dw_i)/dt` and defines M_i. Comment only; the output does not change. |

## What already works

- The factor-4 explanation (one 2 from the swing coefficient, one from integrating the ramp) is correct and complete.
- Every listing output is real, and it matches a re-run to the last digit.
- The three sizing constraints are kept in separate units and never added together. This is the right discipline.
- Each number is tagged with its source or assumption status (cited, assumed), and the RoCoF sources are kept apart.
- The zero-eigenvalue explanation is correct.

## Fix log

All 18 fixes are applied in place to `lesson8.html` by one scripted replacement pass (26 exact-match replacements; each old string was asserted to occur exactly once). Fix #18 is also applied to `lesson8_two_unit.py`.

Post-fix checks:
- The HTML tag-balance parse reports no unclosed or mismatched tags.
- The page has no external `http`, `<script>` or `<link>` references.
- `lesson8_two_unit.py` re-run after the docstring change: output unchanged (11.84 rad/s, 1.884 Hz, 0.0128).
- The Fig. 8.1 legend region (x 80-220, y 262-320) is clear of all four curves. The 50 GVA·s curve is at y <= 200 for x <= 250.

Not changed: the external citations S05, S13-S18 (GB 2019 figures of 931 MW and 1878 MW, Machowski, Anderson and Mirheydar, GC0137, IEEE 2800, the ENTSO-E and GB RoCoF figures) keep their existing "verify" tags. I did not check them against the primary sources in this pass.
