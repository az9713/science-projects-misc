# Lesson 1 edit — science-editor pass

File: `p7-explainers/lesson1.html` (777 lines before fixes).

## Verdict (before fixes)

**Revise — minor-to-moderate.** The central physics and every headline number are correct. I re-ran the listing and recomputed each figure (table below). The defects are in derivation steps that the text skips, three incorrect statements (per-unit bases, H called per unit, sign reversal at 2π), a sign mismatch between the RoCoF equation and the code, one unsupported causal claim built on an invented J, a feedback arrow in Fig. 1.1 that ends away from the summing junction, and some rhetorical phrasing. No defect changes an answer in the opening problem.

## Numbers re-checked

| Claim | Location | Recomputed | Status |
|---|---|---|---|
| RoCoF0 = 50 × 1000 / (2 × 200000) = 0.125 Hz/s | l.493–497 | 0.125 | OK |
| t(49.2 Hz) = 6.40 s, t(48.8 Hz) = 9.60 s | l.197–198 | 0.8/0.125 = 6.4, 1.2/0.125 = 9.6 | OK |
| Listing output | l.557–559 | re-ran listing: `-0.125`, `6.40`, `9.60` | OK |
| 640 additions of -0.00125 = -0.7999999999999885 | l.563–564 | -0.7999999999999885 | OK |
| "one part in 10^13 short" | l.565 | relative error 1.44e-14 | Wrong order of magnitude (defect D9) |
| Without EPS prints 6.41 s | l.566–567 | 6.41 s, and 9.61 s for 48.8 Hz | OK, incomplete (D9) |
| Fig. 1.2 times 3.2/6.4/12.8 and 4.8/9.6/19.2 s | l.626–631, 645–646 | same | OK |
| Fig. 1.2 SVG coordinates (28 px/s, 188.25 px/Hz) | l.610–625 | all line ends and dots match | OK |
| Ex.1: ω_m = 188.5 rad/s, E = 88.8 MJ, H = 0.444 s | l.683–689 | 188.496, 88.83 MJ, 0.4441 s | OK |
| Ex.2: 3.20 s, 12.80 s | l.703 | same | OK |
| Ex.3: 25,000 MW·s | l.716 | 50 × 1000 / 2 = 25,000 | OK |
| Ex.5: 37.7 rad, 6.0 turns | l.761 | 37.699 rad, 6.0 | OK |
| ω0 ≈ 314 at 50 Hz | l.385 | 314.16 | OK |
| "twenty lines of Python" | l.183 | listing is 25 lines | Wrong (D14) |

## Defects (location, problem, fix)

**D1 — l.239–255, per-unit bases.** Text says "Four bases are chosen, and the rest follow", then lists I_base and Z_base as derived. Only two bases are chosen. Fix: "Two bases are chosen; the other two follow from circuit laws."

**D2 — l.260–263, transformer base rule.** "Choose the base voltage on each side … equal to its own rated turns ratio" is not a valid rule (a voltage cannot equal a ratio). Fix: choose the base voltages on the two sides in the same ratio as the rated turns ratio.

**D3 — l.264–265, H called per unit.** "every quantity in the swing equation (P, Δω, H) is in per unit" — H is in seconds (the lesson says so at l.287). Fix: P and Δω are per unit; H is in seconds on the machine's own S_base.

**D4 — l.287–295, unsupported causal claim.** The range 2–8 s alone does not show that the turbine dominates stored energy. The Ex.1 answer (l.690–693) draws the same conclusion from an invented J = 5000 kg·m². An invented number cannot support a claim about real machines; generator rotors hold a large share of turbo-set inertia in many real units. Fix: remove the causal claim in both places; state that J in Ex.1 is illustrative and that a real set's total J (generator plus turbine) sets H.

**D5 — l.355–361, skipped derivation step.** The text says "multiply the H definition by 2 and divide through" but never shows the step that converts dω_m/dt to d(Δω)/dt, and never says why the mechanical and electrical per-unit deviations are equal. Fix: write the step explicitly: dω_m/dt = ω_m0 d(Δω)/dt (because ω = p·ω_m, so the per-unit deviation is the same for both), giving (J ω_m0² / S_base) d(Δω)/dt = 2H d(Δω)/dt = P_m − P_e.

**D6 — l.380–385, damping convention.** "proportional to the rotor speed in rad/s" should be the speed *deviation* in electrical rad/s; the factor ω0 holds only for electrical rad/s (mechanical rad/s adds the pole-pair count). Fix wording.

**D7 — l.387–395 and title, "one integrator".** The paragraph says "exactly one integrator" and then describes two. Fix: the frequency dynamics is one integrator; the angle δ is a second integrator downstream that does not feed back in this isolated model.

**D8 — l.434 (Fig. 1.1 SVG), feedback wire.** The damping arrow ends at (108,150), 42 px below the summing junction (centre (90,90), r = 18), and carries no minus sign. Fix: route it to the junction bottom (90,108) and add a "−" label. Caption l.452 "literally … no other path": delete the intensifier, state that Δω is the integral of imbalance minus damping.

**D9 — l.562–569, float explanation.** Relative error is 1.44e-14, about 1.4 parts in 10^14, not "one part in 10^13". The 48.8 Hz threshold also needs the guard (960 additions give -1.19999999999998; without EPS it prints 9.61 s). Fix both.

**D10 — l.493–498 vs l.517–518 and l.534, sign.** RoCoF0 is defined positive (f0 ΔP / 2E), but the Euler update "df ← df + RoCoF0·h" and the code's `rocof0` are negative. Fix: state that the code carries the sign (`rocof0` = −RoCoF0) and write the update as Δf ← Δf − RoCoF0·h.

**D11 — l.474–486, notation d(df)/dt.** Using `df` and `dP` as quantities next to the differential operator d gives "d(df)/dt", which reads as a second differential. Fix: use Δf and ΔP in the maths; keep `df` / `DP` only as code names (stated once).

**D12 — l.456–472, aggregation step not shown; Σ rendering.** The summed equation that produces E_kin,sys is not written, and "Σi" renders with i on the baseline. Also missing caveat: 200 GVA·s must be the stored energy *after* the trip (the tripped station's rotor leaves the system). Fix: write Σ_i 2H_i S_i d(Δω)/dt = Σ_i (P_m,i − P_e,i) S_i = −ΔP; subscript i; add the caveat.

**D13 — l.203–210, rhetorical phrasing.** "not decorative", "the single most consequential number", "exactly one physical quantity per unit of power lost". Fix: state the measured relation: the time to a threshold is proportional to E_kin,sys and inversely proportional to ΔP, and it sets the time budget for a control action.

**D14 — l.183, line count; l.554–555, missing file.** Listing is 25 lines, not twenty. The text cites `lesson1_rocof.py`, which does not exist in `p7-explainers/`. Fix: "twenty-five lines"; say the output is from running the listing as printed, without naming a missing file.

**D15 — l.760–768, Ex.5 wrong period.** "every time δ sweeps through a multiple of 2π the power flow reverses sign" — sin δ changes sign at every multiple of π (180°), as l.220–221 correctly says. Fix: π (180°); the 0.1 Hz slip gives 12 sign reversals per minute.

**D16 — l.588 and l.619–625, Fig. 1.2 markers.** Dot radius is set only by CSS `r:3.5`; renderers without SVG2 geometry-property support draw no dot. Threshold labels at x = 565 overlap the 400 GVA·s line and the 19.2 s marker. Fix: add `r="3.5"` attributes; move threshold labels to x = 66.

## What already works

- The opening problem states its assumption (200 GVA·s) with a verify tag and answers with two computed numbers.
- Every symbol is defined before use; K_D vs D convention is flagged.
- Fig. 1.2 geometry is exact to 0.1 px against the closed form.
- The EPS explanation is a real, reproduced floating-point effect.
- The limits card names each missing mechanism and the lesson that adds it.

## Fix log

All fixes applied in place to `p7-explainers/lesson1.html` on 2026-09-22 by an exact-match replacement script (each target matched exactly once). Line numbers above refer to the file before fixes.

| Defect | Status | Change made |
|---|---|---|
| D1 | fixed | "Two bases are chosen (S_base and V_base); the other two follow from circuit laws." |
| D2 | fixed | Base voltages chosen "in the same ratio as its rated turns ratio". |
| D3 | fixed | P and Δω stated as per unit; H stated as seconds on the machine's own S_base. |
| D4 | fixed | Causal "turbine dominates" claim removed from the H section and the Ex.1 answer. Ex.1 now says J = 5000 kg·m² is illustrative; 2–8 s is 4.5 to 18 times 0.444 s; a real H comes from generator plus turbine J. |
| D5 | fixed | Added ω = p·ω_m, per-unit deviation equality, dω_m/dt = ω_m0 d(Δω)/dt, and an intermediate display equation (J ω_m0² / S_base) d(Δω)/dt = P_m − P_e before substituting 2H. |
| D6 | fixed | D defined per speed deviation in electrical rad/s, K_D = ω0·D; factor 314 at 50 Hz applies to the coefficient and so to the damping ratio; mechanical rad/s adds the pole-pair count. |
| D7 | fixed | "the frequency dynamics is one integrator"; added that δ does not feed back in this isolated model (it does in Lesson 2 through P_e). |
| D8 | fixed | Fig. 1.1 feedback now a polyline 240,190 → 90,190 → 90,110 ending at the junction bottom, with a "−" label at (100,128). Caption intensifier "literally … no other path" replaced with the exact statement. |
| D9 | fixed | "about 1.4 parts in 10^14"; added the 48.8 Hz case (960 additions give -1.19999999999998; 9.61 s without the guard). Both values reproduced by re-running. |
| D10 | fixed | RoCoF0 stated as a positive magnitude, d(Δf)/dt = −RoCoF0; Euler update written Δf ← Δf − RoCoF0·h; code `rocof0` = −RoCoF0 explains the printed −0.125. |
| D11 | fixed | Maths uses Δf and ΔP (derivation, RoCoF equation, unit note, Ex.3); code names `df` and `DP` stated once. |
| D12 | fixed | Summed equation Σ_i 2H_i S_i d(Δω)/dt = Σ_i (P_m,i − P_e,i) S_i added; Σ index set as subscript; E_kin,sys unit MW·s shown; post-trip caveat added. |
| D13 | fixed | Rhetorical paragraph rewritten as the proportional relation and the time-budget consequence. |
| D14 | fixed | "twenty-five lines"; reference to the missing file `lesson1_rocof.py` removed. |
| D15 | fixed | Ex.5: sign reversal at every multiple of π (180°), 12 reversals in the minute. |
| D16 | fixed | CSS `.dot { r:3.5; }` removed; `r="3.5"` added to all 6 circles; threshold labels moved from x = 565 to x = 66. |

Post-fix checks: the listing extracted from the edited HTML re-runs and prints `RoCoF0 = -0.125 Hz/s`, `t(49.2 Hz) = 6.40 s`, `t(48.8 Hz) = 9.60 s` (code unchanged). An HTML tag-balance parse reports no unclosed or mismatched tags. No external scripts or stylesheets were added; the palette is unchanged.

Not done: citations S01, S15, S16 stay marked "verify" — this pass had no source list to check them against. No visual render check in a browser was run.
