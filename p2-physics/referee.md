# Referee report: eight numerical reproductions (`p2-physics`)

Date: 2026-09-22. Referee: Fable 5.1. Inputs: `HANDOFF.md`, `referee-ising.md`, `draft-results.json`, `results/*.json`, `scripts/*.py`. Probe files: scratchpad `referee_*.py` (six files). No project file was edited except this one.

All eight scripts print RESULT=PASS. This report judges whether each pass is evidence of a correct reproduction. It gives the fix stage a numbered change list per target.

## Summary table

| target | verdict | changes | tolerance / error | bias term |
|---|---|---|---|---|
| ising | PASS WITH CHANGES | 6 | 20 (0.05 / 0.0025) | asserted: docstring 0.005; referee bound 0.0016 |
| lorenz | PASS WITH CHANGES | 3 | 3.83 (4.67e-4 / 1.22e-4) | asserted floor 1e-4; Richardson 1.1e-5 is noise / 15 |
| kuramoto | PASS WITH CHANGES | 4 | 4.19 (4.74e-4 / 1.13e-4) | measured (delta_N + delta_dt); delta_dt at the noise floor |
| three_body | PASS WITH CHANGES | 2 | 171 (1.886e-7 / 1.105e-9) | measured (IC rounding, 96 %); removable with 14-digit data |
| fpu | PASS WITH CHANGES | 4 | 18.3 (7.35 / 0.40) | measured half-width (84 %); the 95 % level is a free constant |
| feigenbaum | PASS | 0 | 3.55 (2.69e-6 / 7.57e-7) | measured (one successive difference) |
| kepler | PASS WITH CHANGES | 5 | 10.6 (a) and 5760 (b) | asserted: BIAS_A 0.02 (72 %), floor 0.01 (99.9 %) |
| poisson | PASS WITH CHANGES | 2 | 5.13 (2.51e-3 / 4.89e-4) | derived formula (analytic drift), not measured scatter |

Two of nine passes depend on the bias term: three_body (abs_diff 3.2e-8 against 3 x error 3.3e-9) and fpu (3.57 against 1.20). Both bias terms are measured. The other seven passes hold on 3 x error alone.

---

## 1. Ising (`scripts/ising.py`, `results/ising.json`)

`referee-ising.md` covers a to e. I agree with it. Summary of its findings:

- a. Published Tc = 2/ln(1+sqrt 2) = 2.269185. Exact (Onsager). Correct.
- b. The script prints no error bar. The referee measured sigma(Tc) = 0.0025 from the printed halves and a 20,000-draw noise Monte Carlo.
- c. TOL = 0.05 (line 36) is a fixed constant. 0.05 / 0.0025 = 20. The pass band 2.219 to 2.319 contains 5 of the 7 grid temperatures. The docstring bias 0.005 (line 13) is asserted; the run's own U16(Tc) - U* bounds it below 0.0016.
- d. Finite-size shift of the 16/32 crossing: magnitude below noise, sign unresolved.
- e. Wrong physics: a crossing at a wrong temperature inside 2.219 to 2.319 passes. Example: a coupling error that puts Tc at 2.30 (1.4 % high) passes at TOL 0.05 and fails at TOL 0.01. With change 2 the test catches it.

Two additions from this pass:

- `ising.py` does not print the `MEASURED=` / `PUBLISHED=` / `ERROR_ESTIMATE=` / `TOLERANCE=` / `ABS_DIFF=` / `RUNTIME_S=` / `RESULT=` block. HANDOFF line 19 says every script prints it. The other seven do. `results/ising.json` was filled from the free-text lines 123 to 130.
- Line 132 is a bare `assert`. Under `python -O` a FAIL exits 0.

**Verdict: PASS WITH CHANGES.** The physics is right (0.7 sigma from exact). The reporting is not: no error bar, a 20-sigma tolerance, and no standard output block.

### Changes (ising)

1. Compute sigma(U4) for each L from the two halves (lines 79 to 83). Propagate to sigma(Tc) through the cubic root, or by a 2,000-draw noise Monte Carlo of `crossing()`. Print `  Tc = 2.267 +/- 0.003`.
2. Line 36: replace `TOL = 0.05` with a run-time value `tol = 3.0 * sigma_tc + 0.002`. Expected value about 0.010. Print `  tolerance          : 0.0095  (3 sigma + 0.002 finite-size bound)`.
3. Docstring lines 12 to 14: replace "the residual shift is on the order of 0.005 in T, an order of magnitude below the 0.05 tolerance" with "the run's own U16(Tc) against U* = 0.61069 bounds the shift below about 0.0016; the sign is not resolved".
4. Line 92: replace the `assert` with `print("RESULT=FAIL  (expected exactly one U4 crossing, found %d)" % sign_change.size); sys.exit(1)`. Add `import sys`.
5. `results/ising.json` notes: change "smaller than the observed 0.0017 deviation" to "larger than the observed 0.0017 deviation". Delete the sentence that presents bit-identical repeat runs as a precision check.
6. Lines 122 to 134: print the standard block `MEASURED=%.4f`, `PUBLISHED=%.6f`, `ERROR_ESTIMATE=%.4f`, `TOLERANCE=%.4f`, `ABS_DIFF=%.4f`, `RUNTIME_S=%.1f`, `RESULT=%s`. Replace the line 132 `assert` with `if diff > tol: sys.exit(1)`.

---

## 2. Lorenz (`scripts/lorenz.py`)

**a. Published value and source.** 0.9056 is the 4-decimal value from Sprott, *Chaos and Time-Series Analysis* (2003); its rounding half-width is 5e-5. Sprott's web page for the same computation (RK4, step 0.001, 1e9 steps) prints (0.906, 0, -14.572), three significant digits. The docstring (line 19) quotes Viswanath 1998 as 0.90566. Secondary sources quote Viswanath as both 0.90566 (+/- 0.0007) and 0.905630. The primary thesis was not checked. The pass holds against each: 0.905763 - 0.90566 = 1.0e-4 (0.8 sem), 0.905763 - 0.905630 = 1.3e-4 (1.1 sem).

**b. Error estimate.** sem = std / sqrt(1024) = 0.003916 / 32 = 1.22e-4 over 1024 independent trajectories of T = 1500. This is a real statistical sigma. Check: the dt-halved run at T = 750 gives sem 1.8e-4; the ratio 1.8e-4 / 1.22e-4 = 1.48 against sqrt(2) = 1.41. The noise scales as 1 / sqrt(T), as a diffusive finite-time exponent must.

**c. Tolerance.** 4.67e-4 = 3 x 1.22e-4 + max(Richardson 1.1e-5, floor 1e-4). Ratio 3.83. The floor is 21 % of the tolerance and is asserted (docstring lines 37 to 39: alignment O(1/T) plus published rounding). The Richardson term (line 211) is |coarse - fine| / 15 with coarse - fine = -1.6e-4 and combined sem 2.2e-4. That is noise divided by 15, not a measurement. A 2-sigma upper bound is (1.6e-4 + 4.4e-4) / 15 = 4.0e-5. The pass does not need the floor: abs_diff 1.63e-4 against 3 sem + 4.0e-5 = 4.07e-4.

**d. Method bias.** RK4 step error: bounded at 4e-5 (see c). Alignment O(1/T): asserted "well under 1e-4" (line 36), not measured. Published rounding: 5e-5 (4 significant digits). The measured value sits 1.3 sem above Sprott and 0.8 sem above Viswanath's 0.90566. No cancellation by luck.

**e. Wrong physics.** A sign or factor error in one Jacobian term, for example `RHO * a` instead of `(RHO - z) * a` at line 98: self-check a (line 145) stops the script before the measurement. Dropping the transient (T_TRANSIENT = 0): the tangent alignment adds an O(1) log-projection term over T = 1500, about 1 / 1500 = 7e-4 in lambda_1, which fails the 4.67e-4 tolerance. The test discriminates at the 5e-4 level.

**Verdict: PASS WITH CHANGES.**

### Changes (lorenz)

1. Line 211: replace `richardson = abs(delta) / 15.0` with `richardson = (abs(delta) + 2.0 * delta_sem) / 15.0`. Line 228: print `    Richardson dt-error of the coarse run, 2-sigma upper bound: 0.000040`. Reason: the central value is noise / 15.
2. After line 229 print `  tolerance without the 1e-4 floor: 0.000407  -> PASS` computed as `3.0 * sem + richardson`. Reason: the reader sees that the pass does not depend on the asserted floor.
3. Docstring: line 19 and 20, replace "gives 0.90566" with "is quoted in secondary sources as 0.90566 and as 0.905630; the primary was not checked". Line 20 ("differ by 6e-5") and the line 87 comment ("0.9056 vs 0.90566 rounding") assume 0.90566; change both to "3e-5 to 6e-5, depending on which Viswanath figure is right". Line 38, replace "The bias allowance is max(Richardson estimate, 1e-4), the floor covering items 2 and 3" with "The bias allowance is max(Richardson 2-sigma bound, 1e-4). The floor is asserted, not measured. Items 2 and 3 together are 5e-5 (published rounding) plus an unmeasured O(1/T) term."

---

## 3. Kuramoto (`scripts/kuramoto.py`)

**a. Published value and source.** Kc = 2 / (pi g(0)) = 2 gamma = 2 for the Lorentzian with gamma = 1. Kuramoto (1975) and Strogatz, Physica D 143 (2000) 1, eqs. (1) to (8). Correct. r = sqrt(1 - Kc / K) is exact for the Lorentzian. Correct.

**b. Error estimate.** 1.13e-4 = sqrt(sigma_fit^2 + delta_T^2) with sigma_fit = 3.5e-5 (polyfit covariance, 8 points, 6 degrees of freedom) and delta_T = 1.08e-4 (one difference between two half-window fits). One half-window difference has expected magnitude about 1.6 sigma of the full window. So delta_T over-estimates the full-window sigma on average, from one draw. Acceptable.

**c. Tolerance.** 4.74e-4 = 3 x 1.13e-4 + 8e-6 (delta_N) + 1.26e-4 (delta_dt). Ratio 4.19. Both bias terms are measured by reruns (N = 4000; dt = 0.02). No free constant. Caveat: delta_dt = 1.26e-4 and delta_T = 1.08e-4 are the same size, so the dt bias is at the noise floor of this run. The O(dt) scaling rests on the N = 1000 prototype (draft note 5). Richardson to dt = 0, from the N = 4000 pair, gives Kc = 2.00011 +/- about 1.6e-4. The printed abs_diff 9e-6 is partly a cancellation of a -1.3e-4 dt bias and a +1.1e-4 statistical fluctuation. The draft agent says this (note 4). The script does not print it.

**d. Method bias.** The r^2 column sits 1.0 % low at every K: a = 0.989839, ratio r^2 / (1 - 2/K) from 0.989759 to 0.989897 (1.4e-4 relative range). A K-independent factor scales a and b alike and cancels in Kc = -b/a exactly. The 1.4e-4 K-dependence maps to a Kc shift of order 1e-4, which is what delta_dt measures. The argument holds. The slope-only estimator (Kc = -b with a fixed at 1) would give 1.980 and FAIL by 0.020. The intercept form is load-bearing and is legitimate: Kc is where r reaches 0.

The docstring (lines 35 to 45) attributes the deficit to a finite-dt break of the phase-density symmetry of the *drifting* oscillators. The draft agent calls this a hypothesis (note 3). I tested it (`referee_kuramoto_split.py`, `referee_kuramoto_sample.py`; N = 2000, K = 3.0, exact r^2 = 1/3):

| scheme | dt | 1 - r^2 / (1 - 2/K) |
|---|---|---|
| script: full drift, then Heun kick, z sampled after the drift | 0.02 | +2.048e-2 |
| same | 0.01 | +1.012e-2 |
| Strang: half drift, Heun kick, half drift, z sampled after the first half drift | 0.02 | +2.049e-2 |
| same | 0.01 | +1.013e-2 |
| RK4 on the full ODE | 0.02 | -2.4e-5 |
| Strang, z sampled at the step boundary | 0.02 | +5.6e-4 |
| same | 0.01 | +1.4e-4 |
| script scheme, z sampled before the drift | 0.02 | -1.949e-2 |
| same | 0.01 | -0.987e-2 |

Findings. (1) Strang splitting does not change the deficit (2.049e-2 against 2.048e-2), so the splitting order is not the cause. (2) RK4 on the full ODE has no deficit, so the ODE and the frequencies are right. (3) The deficit is a sampling-point artifact. In the split step, a locked oscillator's fixed point sits w dt/2 below its true phase before the drift and w dt/2 above it after the drift. The script samples z after the drift (line 143). Sampling before the drift flips the sign (-1.95e-2 against +2.05e-2). Sampling at the symmetric point of a Strang step leaves an O(dt^2) residual: 5.6e-4 at dt = 0.02, 1.4e-4 at dt = 0.01, ratio 3.8. Derivation for the locked population: the sampled in-phase contribution drops by w^2 dt / (2 K r) per oscillator; for the Lorentzian this gives delta r = -(dt / pi) (1 - arctan(Kr) / (Kr)) before self-consistency, times 1 / (1 - F'(r)) = 2 at K = 3. Predicted deficit at dt = 0.02: 0.0174 against 0.0205 measured (85 %). The drifting population supplies the rest and the K-uniformity; I did not derive that part.

**e. Wrong physics.** Gaussian frequencies with sigma = 1 give Kc = 2 sqrt(2 pi) / pi = 1.596: FAIL by 0.40. gamma = 1.01 gives Kc = 2.02: FAIL by 0.02 against 4.7e-4. A coupling of K / (2N) gives Kc = 4: FAIL. The test discriminates at 5e-4.

**Verdict: PASS WITH CHANGES.**

### Changes (kuramoto)

1. Docstring lines 35 to 45, replace item 1 with: "Discretization, multiplicative. The mean field is sampled after the exact drift and before the coupling kick. At that point each locked oscillator sits w dt/2 past its fixed point, so its in-phase contribution drops by w^2 dt / (2 K r). Summed over the Lorentzian and amplified by the self-consistency factor 1 / (1 - F'(r)), this gives a common factor lambda = 1 - O(dt): measured 0.990 at dt = 0.01, 0.979 at dt = 0.02. Sampling before the drift gives the opposite sign (+1.9 % at dt = 0.02). A Strang step sampled at its boundary leaves 1.4e-4 at dt = 0.01. A common factor cancels in -b/a; the K-dependent residual is what delta_dt measures."
2. After line 231 print two lines: `  Richardson Kc(dt -> 0) from the N=4000 pair: 2.000110  (uncertainty about 1.6e-4)` and `  summary: Kc = 2.0000 +/- 0.0001 (statistical) +/- 0.0001 (systematic); abs_diff 9e-6 is partly cancellation`.
3. Lines 247 to 249: replace the `assert` with `if result == "FAIL": sys.exit(1)`. Add `import sys` at line 73. Reason: `python -O` removes the assert and exits 0 on a FAIL.
4. OPTIONAL, recommended. In `step()` (lines 141 to 155): sample z at theta before any drift; then apply half the drift (`0.5 * dw`), the Heun kick, and the second half drift. Cost: one extra cos/sin pass per step, about +40 % runtime. The verify stage measured 101.3 s and 118.7 s (`results/kuramoto.json`); +40 % gives 142 to 166 s against the 180 s limit. The fix stage must confirm the budget, or cut T_MEAS of the two N_SMALL runs to compensate. Expected: a = 0.99986 at dt = 0.01 (against 0.98984 now), delta_dt drops by about 10 x. Re-verify after this change.

---

## 4. Three-body (`scripts/three_body.py`)

**a. Published value and source.** T = 6.32591398 with r1 = (0.97000436, -0.24308753), v3 = (-0.93240737, -0.86473146) is the 8-decimal form printed in Chenciner and Montgomery, Annals of Math. 152 (2000), from Simo's computation. Real and right. The quoted precision "8 decimals, half-width 5e-9" (line 29) is honest. A 14-digit form exists: r1 = (0.97000435669734, -0.24308753153583), v3 = (-0.93240737144104, -0.86473146092102), T = 6.32591398292621 (printed in M. Fenucci, arXiv:2201.01205, 2022, section 5, citing Chenciner-Montgomery). I verified it with the script's own period finder (`referee_threebody_full.py`): from the 14-digit data, T(rtol 1e-12) = 6.325913982918, which is 8.2e-12 from 6.32591398292621, with d_min = 5.6e-12. The actual rounding error of the published 8-decimal T is -2.9e-9.

**b. Error estimate.** |T(rtol 1e-12) - T(rtol 1e-10)| = 1.105e-9. From the 14-digit data the same difference is 1.105e-9, and the tight run is 8.2e-12 from the truth. So the estimate is a bound dominated by the loose run, 135 x the tight run's actual error. Conservative and honest.

**c. Tolerance.** 1.886e-7 = 3 x 1.105e-9 + 1.803e-7 (IC rounding, measured) + 5e-9 (published rounding). Ratio 171. The IC term is 96 % of the tolerance. The pass depends on it: abs_diff 3.2e-8 against 3 x error 3.3e-9. The IC term is measured by four +5e-9 perturbations. I checked linearity with -5e-9 perturbations: each dT flips sign, residual sum 1e-14 to 3e-14. The RSS of the four shifts is 1.01e-7; the linear sum 1.80e-7 is the worst case.

The bias is not only bounded; it is predicted. Actual rounding errors (8-decimal minus 14-digit): r1x +3.30e-9, r1y +1.54e-9, v3x +1.44e-9, v3y +0.92e-9. Sensitivities dT/dp from the script: +16.34, -3.64, -8.59, -7.49. Predicted shift: +5.40e-8 - 0.56e-8 - 1.24e-8 - 0.69e-8 = +2.90e-8. Predicted T from 8-decimal data: 6.32591398292621 + 2.90e-8 = 6.3259140120. The script measured 6.3259140120 (difference 7e-15). The full 3.2e-8 gap is the IC rounding (2.90e-8) plus the published-T rounding (0.29e-8).

**d. Method bias.** Only the IC truncation. It is measured, predicted, and removable (change 1).

**e. Wrong physics.** Force scaled by 1.000001 (`inv3 * 1.000001` at line 104): T = 6.3259036047, d_min = 4.0e-6, abs_diff 1.04e-5, FAIL at 1.886e-7. A wrong exponent (dist2 ** -1.0) gives no periodic orbit, d_min of order 1, and a garbage period. The test discriminates at 1e-6 relative in a constant. With change 1 it discriminates at 1e-9.

**Verdict: PASS WITH CHANGES.** The pass is honest, and the 96 % bias term is a property of the input data, not of the method. Change 1 removes it.

### Changes (three_body)

1. Lines 74 to 78: set `R1 = np.array([0.97000435669734, -0.24308753153583])`, `V3 = np.array([-0.93240737144104, -0.86473146092102])`, `T_PUBLISHED = 6.32591398292621`, `T_PUB_ROUND = 5e-15`, `IC_ROUND = 5e-15`. Docstring lines 8 to 9 and 23 to 30: state the 14-digit source (Fenucci arXiv:2201.01205 section 5, after Simo; Chenciner-Montgomery print the 8-decimal form). Expected output: `MEASURED=6.3259139829`, `ABS_DIFF` about 8e-12, IC bound about 1.8e-13, `TOLERANCE` about 3.3e-9. Ratio tolerance / error becomes 3.0. Print `PUBLISHED=%.14f`. Docstring lines 32 to 43 shrink to: "the 14-digit data carry a rounding half-width of 5e-15, times a summed sensitivity of 36, so the IC term is 1.8e-13". Docstring lines 56 to 60 and the printed line 225: replace "expect <~ 1e-8" with "of order 1e-11, set by the 14-digit rounding" (measured d_min from the 14-digit data: 5.6e-12).
2. Keep the 8-decimal data as a printed cross-check after the measurement: run `find_period` from the 8-decimal state and print `8-decimal Chenciner-Montgomery data: T = 6.3259140120; predicted from rounding errors x sensitivities: 6.3259140120; published 6.32591398 differs by 3.2e-8, of which 2.9e-8 is IC rounding and 0.3e-8 is the rounding of the published period`. Reason: it shows the earlier 3.2e-8 gap was explained, not tolerated.

---

## 5. FPU (`scripts/fpu.py`)

**a. Published value and source.** "After 157 periods of mode 1, all but 3 % of the energy is back in mode 1" (Fermi, Pasta, Ulam, LA-1940, 1955; restated in Dauxois, Physics Today 61(1) 55, 2008; Dauxois, Peyrard, Ruffo, Eur. J. Phys. 26 (2005) S3). Confirmed. The number 157 was read from a plotted curve. It is approximate. The script prints `PUBLISHED=157.0000` (line 237), four decimals for a plot reading. FPU's time step and their exact boundary convention are not verified; the docstring says so (line 39, 41 to 45).

**b. Error estimate.** 0.40 periods = dt shift 0.28 (full |peak(0.05) - peak(0.025)|, not the Richardson remainder 0.09) + estimator spread 0.12 (arg-max, mid-95 %, centroid). Deterministic convergence measures, not a sigma. Conservative.

**c. Tolerance.** 7.35 = 3 x 0.40 + 6.14. Ratio 18.3. The 6.14 is the half-width of the plateau where E_1 exceeds 95 % of the peak, measured in the run. The pass depends on it: abs_diff 3.57 against 3 x error 1.20. The 95 % level is a free constant. Anchored at the published 0.97 fraction of E_1(0) the half-width is 2.86 and the tolerance is 4.07; abs_diff 3.57 still passes, margin 0.50. The script prints this alternative (line 217 to 219) and does not adopt it.

E_1 at t = 157 T_1 is 0.9643 of E_1(0), which is 0.006 below the published 0.97. The peak is 0.9807 at 153.43 T_1. So 157 lies inside the 95 % plateau (132.0 to 177.0 hump; plateau half-width 6.14 around 153.56) and just outside the 0.97 band (150.6 to 156.3).

**d. Method bias.** dt: a coarser step moves the peak later (156.70 at dt 0.2, 153.72 at 0.05, 153.43 at 0.025). FPU's coarse second-order scheme is a plausible part of the 3.6-period gap; not verified. Boundary convention: I reran the script with N = 31 (`referee_fpu_n31.py`): peak 146.45 T_1, abs_diff 10.55, tolerance 7.05, RESULT=FAIL, exit 1. E_1(157 T_1) = 0.8415 for N = 31, a second discriminator. The 32-moving-mass reading is the closer one by 7 periods.

**e. Wrong physics.** N = 31: FAIL (verified above). Amplitude 0.9: the recurrence time scales about as 1 / E, so about 189 periods, FAIL. alpha = 0.5: recurrence time changes by a factor of 2 or more, FAIL. The test discriminates at about 5 % of 157.

**Verdict: PASS WITH CHANGES.** The bias term is a resolution bound on a plot-read number. It is measured given the level. The level is a choice.

### Changes (fpu)

1. Put the negative control in the script output. Make `OMEGA`, `SIN_MAT`, `MODE_NORM`, `T1` (lines 85 to 89) and `accel`, `integrate`, `recurrence` take `n` as a parameter. After the main runs, run `integrate(DT_COARSE)` with n = 31 and print `negative control, 31 moving masses at dt=0.050: peak 146.73 T_1, |157 - 146.73| = 10.27 > tolerance 7.35 -> that convention FAILS`. Cost about 3 s.
2. Before the parse block print `published value 157 is read from a plotted curve (LA-1940 Fig. 1); E_1 at 157 T_1 in this run is 0.9643 of E_1(0), 0.006 below the published 0.97`. Keep `PUBLISHED=157.0000` for the parser.
3. In the error budget (after line 231) print `  pass on 3*error alone: NO (3.57 > 1.20); pass at the 0.97-anchored tolerance 4.07: YES`. Docstring lines 27 to 34: add "The 95 % level is a chosen constant. The published 0.97 fraction gives half-width 2.86 and tolerance 4.07, which the result also passes."
4. `results/fpu.json` notes: add "The pass depends on the plateau half-width term (abs_diff 3.57 against 3 x error 1.20). It also passes at the 0.97-anchored tolerance 4.07. E_1(157 T_1) = 0.9643 against the published 0.97."

---

## 6. Feigenbaum (`scripts/feigenbaum.py`)

**a. Published value and source.** delta = 4.669201609102990 (Briggs, Math. Comp. 57 (1991) 435; discovery Feigenbaum, J. Stat. Phys. 19 (1978) 25). alpha = 2.502907875096, r_inf = 3.5699456718709. All correct. The script claims 6 significant figures, 4.66920, and says so (draft note).

**b. Error estimate.** 7.57e-7 = truncation |delta_10 - delta_9| = 4.14e-7 + roundoff sigma_round = 3.43e-7. Successive differences for a converging sequence: right method. The truncation term over-estimates the remaining truncation by about delta - 1 = 3.7 (actual |delta_10 - delta| = 9.5e-8). Roundoff is measured from the Newton limit-cycle width (1.73e-14 at n = 10) divided by the gap r_11 - r_10 = 2.49e-7. The error model holds at every level 5 to 12: |delta_n - delta| is inside its own estimate by a factor 2 to 8 at each n.

**c. Tolerance.** 2.69e-6 = 3 x 7.57e-7 + 4.14e-7. Ratio 3.55. The bias allowance is the same successive difference that already sits in the error estimate, so truncation is counted 4 times and roundoff 3 times. Stated in the docstring (lines 74 to 79). Conservative, no free constant. abs_diff 9.5e-8 is 0.13 of the error estimate.

**d. Method bias.** delta_n approaches delta from below for n >= 4; the measured value sits below by 9.5e-8. Sign consistent. The reporting level N = 10 is chosen by the minimum of the error estimate, without reading the published value; the full table is printed. Level 12 would be noise-dominated (5.7e-6 off).

**e. Wrong physics.** A map with a quartic maximum has delta = 7.28: FAIL. A Newton step that settles on a wrong root: the alpha check (line 252, 2.0 < alpha < 3.0) and the minimal-period check (line 203) stop it; alpha measured 2.502904. An off-by-one in N is not caught (delta_9 is 5.1e-7 off, delta_11 is 8.1e-7 off, both inside 2.69e-6), but every delta_n converges to delta, so that is not a physics error. Universality means a different unimodal map with a quadratic maximum also passes; that is the physics, not a blind spot.

**Verdict: PASS.** No changes.

---

## 7. Kepler (`scripts/kepler.py`)

**a. Published value and source.** Hairer, Lubich, Wanner, *Geometric Numerical Integration*, 2nd ed. (2006), chapter I; the e = 0.6 Kepler problem is the worked example of I.2. Real and right. The two "published values" are textbook statements: (a) Stormer-Verlet is second order (PUBLISHED = 2); (b) its energy error stays bounded (PUBLISHED_2 = 1 as a late/early ratio). Honest framing.

**b. Error estimate.** (a) 0.0026 = std (ddof 1) of the 4 pairwise orders 2.0058, 2.0014, 2.0004, 2.0001. These are a deterministic sequence converging to 2, not samples. The excess over 2 falls by 4.1, 3.5, 4.0 per halving: a clean h^2 term. The mean 2.0019 is above 2 by construction, and abs_diff 0.0019 is that construction bias. Richardson on the order sequence: p_inf = 2.0001 - (2.0004 - 2.0001) / 3 = 2.0000. (b) 1.74e-6 = std / mean of the 100 window maxima (3.181e-9 / 1.830675e-3). Measured, honest.

**c. Tolerance.** (a) 0.0279 = 3 x 0.0026 + BIAS_A 0.02. Ratio 10.6. BIAS_A was fixed before the first run from the argument "unless q is of order 10 this term is below 0.01" (docstring line 54). Asserted, 72 % of the tolerance. The run then measured q about 5.4, so the bias is now measurable: mean(p) - p_inf = 0.0019. The pass holds without BIAS_A (0.0019 < 0.0079). (b) 0.010008 = 3 x 1.74e-6 + 1.54 x 1.74e-6 + floor 0.01. Ratio 5760, the largest in the project. The floor is 99.9 % of the tolerance and is asserted ("twice a 0.5 % peak-sampling bound", line 95). The window-to-window wander sigma_b already measures the grid-phase effect the floor was meant to cover. The script prints the floor-free tolerance 7.889e-6 and passes it (abs_diff 6.7e-8). HANDOFF flags only BIAS_A; the floor is the larger problem.

**d. Method bias.** (a) even-power h^2 term: now measured (see b). (b) extreme-value shift 1.54 sigma: derived in form, scaled by the measured sigma. Angular momentum drift 6.4e-14 confirms the implementation.

**e. Wrong physics.** (a) A non-symmetric second-order method (Heun on the ODE) also gives order 2, so (a) passes and does not test symplecticity. A first-order scheme (drop the second half-kick at lines 233 to 234) gives order 1: FAIL. (b) is the physics test: RK4 gives ratio 88 (gate 10). A method with 1 % secular energy drift over 1000 periods gives ratio 1.01: it PASSES the floored tolerance 0.010008 and FAILS the floor-free 7.9e-6. The floor blinds test (b) by a factor 1000.

**Verdict: PASS WITH CHANGES.**

### Changes (kepler)

1. Line 167 and 348: replace the fixed `BIAS_A = 0.02` with a measured value. After line 346 add `p_inf = float(orders[-1] - (orders[-2] - orders[-1]) / 3.0)` and `bias_a = abs(measured_a - p_inf)`. Line 348: `tol_a = 3.0 * sigma_a + bias_a`. Line 376: print `    bias allowance  : 0.0019  (measured: mean of the 4 orders minus the Richardson limit 2.0000; pre-registered value was 0.02)`. Expected: `TOLERANCE=0.009793`, `ABS_DIFF=0.001910`, PASS. Ratio 3.7.
2. Line 174 and 358 to 359: remove the floor. `bias_b = EV_10 * sigma_b`, `tol_b = 3.0 * sigma_b + bias_b`. Expected `TOLERANCE_2=7.889e-06`, `ABS_DIFF_2=6.708e-08`, PASS. Line 389 to 393: replace the floor lines with `    a 1 % secular drift (ratio 1.01) would fail this tolerance`. Delete `BIAS_B_FLOOR`.
3. Lines 415 and 417: print `ERROR_ESTIMATE_2=%.3e` and `ABS_DIFF_2=%.3e`. `0.000002` and `0.000000` hide the digits.
4. Docstring lines 48 to 72 and 82 to 116: rewrite to match changes 1 and 2. State: "the 4 pairwise orders are a converging sequence; their std is a spread, not a sigma; the bias of their mean is measured against the Richardson limit". Delete the 0.01 floor paragraph (lines 90 to 99, 106 to 116).
5. `results/kepler.json` notes: the two blocks are mislabeled. "Block 1 (leapfrog long-run energy-drift ratio vs RK4)" is the convergence order (quantity a). "Block 2 (self-check / RK4 control ratio)" is the leapfrog late/early energy-error ratio (quantity b); the RK4 ratio 87.988 is its control, not the measured quantity. Replace both labels.

---

## 8. Poisson (`scripts/poisson.py`)

**a. Published value and source.** Second-order convergence in the max norm for the 5-point stencil; LeVeque, *Finite Difference Methods for ODEs and PDEs*, SIAM 2007, chapter 3. Real and right.

**b. Error estimate.** 4.89e-4 = spread of the three finest p_k (2.000522, 2.000130, 2.000033). Not a sigma; the docstring says so (lines 48 to 52). The test function sin(pi x) sin(pi y) is an exact eigenvector of the discrete operator, so e_N = x^2 / sin^2(x) - 1 with x = pi h / 2 is analytic, and so is every p_k: p_k - 2 = 0.2164 x^2 at the coarser grid, 5.2e-4, 1.3e-4, 3.3e-5, matching the printed digits. The order test therefore cannot fail unless the closed-form gate (line 107, 1e-8 relative) has already failed. The gate is the discriminating test: observed mismatch 6.9e-14 to 7.4e-10, 13 x inside the gate at N = 256.

**c. Tolerance.** 2.51e-3 = 3 x 4.89e-4 + 1.04e-3. Ratio 5.13. The allowance is 2 x 0.2164 x (pi / 64)^2, a derived formula, not a number fitted to the run and not a measured scatter. The factor 2 is a choice. The pass holds without it (2.28e-4 < 1.47e-3).

**d. Method bias.** All p_k sit above 2 by construction; the mean excess 2.28e-4 equals abs_diff. Richardson on the order sequence: p_inf = 2.000033 - (2.000130 - 2.000033) / 3 = 2.000001.

Probe with a non-eigenvector, u = sin(pi x) sin(pi y) (1 + x), f = 2 pi^2 (1 + x) sin(pi x) sin(pi y) - 2 pi cos(pi x) sin(pi y) (`referee_poisson_alt.py`): p_k = 1.994014, 2.000523, 2.000131, 2.000033. The three fine orders agree with the eigenvector case to 1e-6; the coarsest pair flips to below 2. The degeneracy affects interpretation, not the fine-grid numbers.

**e. Wrong physics.** A one-sided first-order difference in `t` (line 80): the gate exits 2 first, and if bypassed, p about 1, FAIL. A wrong 1 / h^2 factor: gate exits 2. A 9-point fourth-order stencil: p about 4, FAIL. A grid off by one (xs misaligned with u_exact): gate exits 2.

**Verdict: PASS WITH CHANGES.**

### Changes (poisson)

1. Docstring lines 26 to 35 and 45 to 52: add "With an exact eigenvector the p_k are analytic, 2 + 0.2164 x^2 + ..., so the order test is a consistency check on the closed form. The 1e-8 closed-form gate is the discriminating test." After line 124 compute and print `Richardson limit of the order sequence: p_inf = 2.000001`.
2. OPTIONAL. Add a second problem, u = sin(pi x) sin(pi y) (1 + x) with the f above, solved on the same five grids. Print its four p_k (expected 1.994014, 2.000523, 2.000131, 2.000033) under the heading `non-eigenvector control`. Gate: `|p_finest - 2| <= 0.01`, exit 2 with a distinct message on failure. Keep MEASURED unchanged.

---

## Cross-cutting

### Patterns across the eight scripts

1. **Two passes depend on the bias term.** three_body (abs_diff 3.2e-8 against 3 x error 3.3e-9) and fpu (3.57 against 1.20). Both bias terms are measured. three_body's term is fully predicted from the input rounding (7e-15 residual) and disappears with the 14-digit data. fpu's term is the resolution of a plot-read number. The other seven passes hold on 3 x error alone.
2. **"3 x error" is a sigma in three scripts only.** ising, lorenz, kuramoto are stochastic and their error is a statistical sigma. In three_body, fpu, feigenbaum, kepler, poisson the error is a deterministic convergence measure: tolerance halving, dt halving, successive differences, or the spread of a monotone sequence. Multiplying these by 3 is a convention, not a confidence level. The report must not call them "3 sigma".
3. **Asserted constants and their share of the tolerance.** ising TOL 0.05 (100 %, fixed); kepler floor 0.01 (99.9 %); kepler BIAS_A 0.02 (72 %); lorenz floor 1e-4 (21 %). Chosen levels inside otherwise measured terms: fpu's 95 %-of-peak level; poisson's factor 2. Measured terms: kuramoto delta_N + delta_dt; three_body IC bound; fpu plateau half-width at the chosen level; feigenbaum successive difference.
4. **Deterministic sequences reported as means.** kepler (a) and poisson average a monotone converging sequence and report the mean; the mean sits above the limit by construction and abs_diff equals that construction bias. A Richardson limit of the order sequence (p_inf) is the honest central value; both are 2.0000 to 4 decimals.
5. **assert after RESULT.** `ising.py:132` and `kuramoto.py:247` use a bare `assert`. `python -O` removes it; a FAIL then exits 0. The other six use `sys.exit(1)`.
6. **Printed precision.** ising prints Tc to 6 decimals with 3 supported. fpu prints `PUBLISHED=157.0000` for a plot reading. kepler prints `ERROR_ESTIMATE_2=0.000002`. three_body prints 10 decimals with 9 supported (acceptable).
7. **Mechanisms stated in docstrings without verification.** kuramoto's drifting-population attribution is wrong as the main cause (staggered sampling of the locked population is; verified by four probes). lorenz's O(1/T) term is asserted. fpu's MANIAC time step is flagged as unverified by the draft agent. Docstrings must mark a hypothesis as a hypothesis.
8. **Independent gates work.** Every script has a wrong-physics gate separate from the tolerance: U4* near 0.61 (ising), Jacobian and linear-flow checks (lorenz), alias count (kuramoto), d_min and the body-3 event (three_body), recurrence fraction and energy drift (fpu), alpha from the same orbits (feigenbaum), RK4 control and angular momentum (kepler), closed-form gate (poisson). These gates, not the tolerances, catch most implementation errors.

### Rule for the report stage: how to present a tolerance

Print five numbers per row, in this order, and never the ratio tolerance / error alone:

1. `abs_diff`.
2. `3 x error`, with the kind of error named in one word: `sigma` (ising, lorenz, kuramoto), `tolerance-halving` (three_body), `dt-halving + estimator spread` (fpu), `successive difference` (feigenbaum), `spread of a converging sequence` (kepler a, poisson), `window-to-window wander` (kepler b).
3. `bias term`, with a tag: `M` (measured in the run) or `A` (asserted before or outside the run), and its share of the tolerance in percent.
4. `tolerance = 3 x error + bias`.
5. `pass on 3 x error alone: yes / no`.

Read out the two ratios `abs_diff / (3 x error)` and `abs_diff / tolerance`, not `tolerance / error`. A row such as three_body then reads "abs_diff 3.2e-8; 3 x tolerance-halving error 3.3e-9; bias 1.8e-7 (M, 96 %, input-data rounding, predicted to 7e-15); pass on 3 x error alone: no", and a reader knows what the 171 means. A row such as kepler (b) reads "abs_diff 6.7e-8; 3 x wander 5.2e-6; bias 0.01 (A, 99.9 %); pass on 3 x error alone: yes", and the 5760 is exposed as an asserted floor, not as a claim about the measurement. After the fix stage, the three_body ratio is 3 and the kepler (b) ratio is 4.5.

### Notes for the fix stage

- Runtimes after the changes: kuramoto optional change 4 adds about 40 % (to about 120 s). fpu change 1 adds about 3 s. All others are unchanged.
- After three_body change 1 and kepler changes 1 to 2, the printed MEASURED, TOLERANCE and ABS_DIFF values change. Re-verify those two and update `results/three_body.json` and `results/kepler.json`.
- Referee probe files, all in the session scratchpad: `referee_kuramoto_split.py`, `referee_kuramoto_sample.py`, `referee_poisson_alt.py`, `referee_threebody_probe.py`, `referee_threebody_full.py`, `referee_fpu_n31.py`.
