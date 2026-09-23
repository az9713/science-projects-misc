# Lesson 3 edit — "When the Integrator Lies"

File: `p7-explainers/lesson3.html` (886 lines before fixes). Editor standard: science-editor (precise statement, every term defined, proof in the smallest setting, limit case, tie to something concrete).

## Verdict (before fixes)

**Revise.** The core argument is correct. I re-ran `lesson3_euler_drift.py` and `lesson3_exercises.py`. Every printed number in §4 and §6 matches the page: λ = −0.1429 ± j8.9607 1/s, |1 + hλ| = 1.00258, g = +0.258 1/s, 13.203 against 0.240, h_crit = 3.56 ms (formula and bisection), 0.358 at 1 ms, 1.94°, 22.306° / 0.609° / 0.609°, slip at 16.93 s. I also recomputed these independently: RK4 boundary h|λ| = 2.8595 (h = 0.3191 s), pure-imaginary limit 2√2 = 2.8284, ω_d at Pm = 0.85 pu = 8.8764 rad/s, W(0) = −1.9098, Euler δ = 59.93° at t = 11 s (Fig. 3.2), and all four point positions in Fig. 3.1's zoom panel.

One defect is blocking: Fig. 3.3 plots the wrong simulation. Its forward-Euler trace is the **damped** run (K_D = 2), but the label, caption and text say undamped (K_D = 0). One derivational defect: Exercise 5 asks for a crossing that does not exist. The remaining defects are errors in a derivation line, a sign, a stability figure, and wording.

## Defects

| # | Severity | Location | Problem | Fix |
|---|---|---|---|---|
| 1 | Blocking | Fig. 3.3 (lines 536–646), §4.1 paragraph | The orange trace ends at ΔW = +0.885 at 15 s. I reproduced 0.8849 only with **K_D = 2** (h = 10 ms, Pm = 0.85 pu, start δ0). The undamped (K_D = 0) run gives ΔW = +1.1848 at t = 10 s, and δ passes 180° at t = 10.19 s (δ = 34354° at 15 s; ΔW after the slip has no meaning). The teal inset is the undamped run (max \|ΔW\| = 3.94×10⁻⁵), so the figure compares two different machines. The inset label says ±6×10⁻⁵; the caption says ±4×10⁻⁵. The caption says "resampled every step"; the trace uses every second step. "Almost half its starting magnitude" and "four to five orders of magnitude" are impressions, not ratios. | Regenerate the orange trace from the K_D = 0 run over 0–10 s. Rescale the y-axis to 0–1.2 and the x-axis to 0–10 s. Move the inset so that it does not cover the trace. Set the inset label to ±4×10⁻⁵. Rewrite the caption and the §4.1 paragraph with the ratios: 1.185 / 1.910 = 0.62; 1.185 / 3.9×10⁻⁵ ≈ 3×10⁴. State the slip at 10.19 s. |
| 2 | Major (derivation) | Exercise 5 (lines 861–871); `lesson3_exercises.py` flag | ln\|1 + hλ\| = hσ + (h²/2)(ω_d² − σ²) + O(h³), so the 10 s factor is ≈ 0.240·e^{5h(ω_d² − σ²)}. This is above 0.240 for **every** h > 0 (check at 1 ms: 0.2397·e^{0.401} = 0.358). No crossing exists. The answer says "the crossing lies below 1 ms", which is false. The script's "crosses 0.240" flag cannot fire. | Reword the exercise: show that the factor never reaches 0.240, and find the step at which it is within 10% of 0.240. Answer: h ≈ 0.237 ms (bisection; factor 0.2636 against 0.2397). |
| 3 | Major (derivation) | §3.3 line 234 | First line of the energy derivation: `2HΔω d(Δω)/dt = (P_m − P_max sinδ)ω_0Δω`. The left side is missing the factor ω_0 that the text says to multiply by. | `2Hω_0Δω d(Δω)/dt = (P_m − P_max sinδ)ω_0Δω`. |
| 4 | Major (sign) | Exercise 2 answer (line 824) | The answer writes (Pm − Pmax sinδ)dδ/dt as −d/dt[Pmδ + Pmax cosδ]. The derivative of Pmδ + Pmax cosδ is (Pm − Pmax sinδ)dδ/dt, so the sign is +. | "…term as +d/dt[Pmδ + Pmax cosδ], which moves to the left side with a minus sign to form W". |
| 5 | Major (figure) | Fig. 3.1 inset (line 280) and caption | The small "full disc" is drawn with centre at the origin (cx = 492.3, the "0" tick). The disc must have centre −1 (cx = 415.4, the "−1" tick). The orange zoom marker sits at Re = +1 (cx = 569.2), outside the true disc; it must sit at the origin, where the zoom window is. The zoom panel's axes are not to equal scale (x about 41 times y), so the arc looks like a steep curve; the caption does not say so. | Move the circle to cx = 415.4. Move the zoom marker to (492.3, 140). Caption: "right edge" and "axes not to equal scale". |
| 6 | Minor (derivation) | §3.2 lines 215–217 | "Keep the term linear in h since h is small" describes an approximation. There is none: \|1 + hλ\|² < 1 ⇔ h(2σ + h\|λ\|²) < 0 ⇔ h < −2σ/\|λ\|² exactly, for h > 0. | "(expand the square to get 2hσ + h²\|λ\|² < 0, then divide by h > 0; no approximation)". |
| 7 | Minor (number) | §3.4 line 261 | 0.2232 s = 2/ω_n is the limit for the **undamped** linear oscillator. The paragraph applies it "for the same eigenvalue", which has K_D = 2. The damped linearised semi-implicit map has spectral radius 1 at h = 0.2196 s, which is 61.7 times 3.56 ms, not 63 times. | State that 0.2232 s is the K_D = 0 bound, and add the K_D = 2 value 0.2196 s (about 62 times). |
| 8 | Minor (definition) | §2 line 170 | `g(δ_k)` is not defined, and g already means the growth rate in §3.1. The code's update also uses Δω_k (damping). | Write the update out: Δω_(k+1) = Δω_k + h(P_m − P_max sinδ_k − K_DΔω_k)/(2H). |
| 9 | Minor (definition) | §2 lines 175–177 | RK4 "exact to O(h⁵) per step" is imprecise. | "local truncation error O(h⁵) per step, global error O(h⁴)". |
| 10 | Minor (claim) | §3.4 lines 269–272 | "Figure 3.1 draws all of this as one picture" — Fig. 3.1 draws only the forward-Euler disc, not the semi-implicit or RK4 limits. | "Figure 3.1 draws the forward-Euler part of this…". |
| 11 | Minor (method) | Exercise 3 answer (lines 838–843) | §4 defines "late amplitude" over the last 2 s of a 10 s run. `rk4_amplitude` runs to max(10, 6/h) s: 60, 30, 20, 17.1 s. The near-zero values at 0.2 s and 0.3 s also include strong RK4 numerical damping, not only physical decay. The 0.319 s limit is for the base-point eigenvalue; the simulation settles at the Pm = 0.85 pu eigenvalue, whose limit is 0.3221 s. Both are between 0.3 s and 0.35 s. | State the run lengths, the numerical damping, and both limits. |
| 12 | Minor (reference) | §4.1 line 536 | "A second listing (lesson3_exercises.py, §6)" — §6 quotes only its output; the listing is not on the page. | "(lesson3_exercises.py, shipped beside this page; §6 quotes its output)". |
| 13 | Minor (reference) | §5 | "by §3.1's Lesson 2 arithmetic" — §3.1 does not compute the Pm = 0.85 pu eigenvalue. | "by Lesson 2's eigenvalue formula applied at Pm = 0.85 pu". |
| 14 | Cosmetic | Fig. 3.1 / Fig. 3.2 SVG | `aria-labelledby` ids are swapped (fig32title in Fig. 3.1, fig31title in Fig. 3.2). | Rename to match the figure numbers. |

Not fixed (outside what I can verify offline): §1 cites "[S01, Kundur 1994, §12.1 — verify]" for the 0.7–2 Hz local-mode band. I cannot check the book here. The "verify" tag stays visible so the reader knows the range is unconfirmed.

## What already works

The opening problem is concrete and every number in it is reproduced by the listing. The split between "stable" and "accurate" in §3.2 (0.358 against 0.240 at 1 ms) is the lesson's most useful point. The listing is stdlib-only and matches its printed output exactly. §5 states the linearisation limit honestly.

## Fix log

Applied 2026-09-22 to `lesson3.html` in place by one scripted pass (every replacement asserted to match exactly once). Backup of the pre-fix page: `%TEMP%/p7_l3_edit_backup.html`.

1. **Fig. 3.3 (defect 1)** — Replaced the SVG and caption. Orange trace regenerated from the K_D = 0 forward-Euler run, h = 10 ms, Pm = 0.85 pu, start (δ0, 0), sampled every 100 ms over 0–10 s; mapping x = 50 + 55t, y = 240 − 175·ΔW. Axes now 0–10 s and 0–1.2. Inset moved to the upper left (x 60–260) so that the rising trace stays visible; inset trace regenerated from the K_D = 0 semi-implicit run, every second step over 0–4 s, ±5×10⁻⁵ = ±28 px. Inset label now ±4×10⁻⁵ (measured max 3.94×10⁻⁵). Caption states +1.185 at 10 s, ratio 0.62 to \|W(0)\| = 1.910, slip at 10.19 s, ratio ≈ 3×10⁴. The §4.1 paragraph now says 10 s, not 15 s.
2. **Exercise 5 (defect 2)** — Question reworded to "show it never reaches 0.240; find the step within 10%". Answer adds the expansion and h < 0.237 ms.
3. **§3.3 (defect 3)** — Added ω_0 to the left side of the first derivation line.
4. **Exercise 2 (defect 4)** — Sign corrected to +d/dt[Pmδ + Pmax cosδ], with the move to the left side stated.
5. **Fig. 3.1 (defect 5)** — Full-disc circle moved to cx = 415.4 (centre −1). Zoom marker moved to the origin (492.3, 140), label "zoom window". Caption now says where the marker is and that the zoom axes are not to equal scale (about 41:1).
6. **§3.2 (defect 6)** — The h_crit step now says "divide by h > 0; no approximation is made … gives exactly".
7. **§3.4 (defect 7)** — 0.2232 s labelled as the K_D = 0 bound; K_D = 2 value 0.2196 s (about 62 times 3.56 ms) added, with "spectral radius" defined in place (the larger eigenvalue magnitude of the one-step map).
8. **§2 (defect 8)** — Semi-implicit update written out with P_m, P_max, K_D and 2H; the undefined g is gone.
9. **§2 (defect 9)** — RK4: local truncation error O(h⁵), global error O(h⁴).
10. **§3.4 (defect 10)** — "draws the forward-Euler part of this".
11. **Exercise 3 (defect 11)** — Answer now states the run lengths (60, 30, 20, 17.1 s), the RK4 numerical damping, and both limits (0.319 s base point, 0.322 s at Pm = 0.85 pu).
12. **§4.1 (defect 12)** — Listing reference now says "shipped beside this page; §6 quotes its output".
13. **§5 (defect 13)** — "by Lesson 2's eigenvalue formula applied at Pm = 0.85 pu".
14. **SVG ids (defect 14)** — Fig. 3.1 uses fig31title, Fig. 3.2 uses fig32title.

Checks after the fix: 3 `<svg>` / 3 `</svg>`; no `<script>`, `<link>` or external `src`; page size 46,242 bytes.

Not changed:
- The Kundur "[S01 … — verify]" citation in §1: not checkable offline.
- `lesson3_exercises.py`: its Exercise 5 "crosses 0.240" flag can never fire and the script does not print the new 0.237 ms figure. The page no longer depends on the flag. The 0.237 ms value comes from a bisection I ran separately (factor 0.2636 against 0.2397).
