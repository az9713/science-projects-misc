# P7 outline — Power-system dynamics for programmers

Status: outline stage complete. Pre-approved by `../PLAN.md` section 6, block P7. Eight lessons. Written 2026-09-22.

Every number in this outline was recomputed by the outline agent with a Python probe (`p7_outline_check.py`, `p7_outline_check2.py`, session scratchpad). A draft agent must recompute every number again in its own probe before printing it.

## Series statement

**Reader.** A working programmer. Comfortable with Python, loops, functions, floating point, and basic algebra. Knows what a derivative is and has seen complex numbers. Knows nothing about power systems: not per unit, not phasors, not the dq frame, not generators.

**Promise.** After eight lessons the reader can write, from a blank file, a simulation of each of these: one generator on a stiff grid, a fault and its clearing, a phase-locked loop, a grid-following converter on a weak grid, a grid-forming converter, and a whole-system frequency event. The reader can also say which number in each simulation decides stability, and why.

**Relation to the P1 textbook.** The P1 book (`../p1-textbook/book-plan.md`) covers the same physics for graduate engineers. These lessons reuse its notation and its worked numbers so that a reader can move between the two. These lessons differ in three ways: code comes first, every model is an ODE the reader integrates, and each lesson opens with one problem a program must answer.

## Shared rules (every lesson spec repeats the short form)

1. **Output.** One self-contained HTML file per lesson: `lesson1.html` to `lesson8.html` in `p7-explainers/`. No `<script src>`, no `<link rel="stylesheet">`, no web font, no CDN, no image file, no `data:` image URI. All CSS in one `<style>` block. An inline `<script>` is allowed only for the code-block Copy button.
2. **Mathematics.** MathML or plain HTML (`<sub>`, `<sup>`, `<var>`, Unicode Greek). Do not use the MathJax scaffold of the `rigorous-explainer` template, because it loads an external script. No LaTeX source left in the page.
3. **Figures.** Inline `<svg>` only. Each figure is drawn from numbers the lesson computes; the caption or a nearby table states them. Figure numbers carry the lesson prefix: `Fig. 3.2`.
4. **Dark mode.** `<meta name="color-scheme" content="dark">`. `:root` custom properties: background `#0f172a`, card `#1e293b`, text `#e2e8f0`, secondary text `#cbd5e1`, muted `#94a3b8`, accents `#fb923c` and `#2dd4bf`, borders `#1e293b` and `#334155`. Rules below `:root` use the variables. No horizontal page scroll at 360 px width; tables and code scroll inside their own box.
5. **Code.** Python 3 standard library only (`math`, `cmath`). Exception: numpy is allowed for linear algebra (`numpy.linalg.eigvals`) in Lesson 8 only. No matplotlib in the lesson code; the page figures are SVG. Listings are PEP8, lines at most 79 characters, no blank lines between related statements. Each listing must run as printed and must print the numbers the prose quotes. Each probe file a draft agent writes in the shared scratchpad uses the lesson prefix, for example `lesson3_euler_drift.py`, because three draft agents run at once and share that directory.
6. **Swing-equation convention.** `2H d(dw)/dt = P_m - P_e - K_D dw`, with `dw = (omega - omega_0)/omega_0` in per unit, and `d(delta)/dt = omega_0 dw`. The damping coefficient is `K_D`, never `D`. The alternative form with damping on a speed in rad/s is named once in Lesson 1 and not used; mixing the two multiplies the damping ratio by `omega_0`.
7. **Park convention.** Amplitude-invariant (factor 2/3). The d axis lies on the measured voltage, so `v_q = 0` when the phase-locked loop is locked. In per unit `P = v_d i_d + v_q i_q`; the factor 3/2 appears only in SI.
8. **Structure per lesson.** One `<h1>`. Sections in this order: the opening problem; the model and its symbols; the key derivation; the code; the figures inside the sections they serve; what the model captures and what it misses; exercises, each in `<div class="exercise">` with its answer target in a `<details>` element. Every symbol is defined in prose before first use.
9. **Sources.** Every published number that the lesson does not compute carries an inline citation with source identifier, author and year, title, location, and `— verify`. Source identifiers are those of `../p1-textbook/book-plan.md` §5.2 (S01 to S20). Never remove a `verify` mark.
10. **Standing warning.** Two rate-of-change-of-frequency figures circulate. Never merge them and never print "ENTSO-E 1 Hz/s". The ENTSO-E withstand guidance is reported as 2 Hz/s measured over 500 ms [S15 — verify]. The 1 Hz/s figure is the one used in Ireland and in Great Britain loss-of-mains protection policy [S16 — verify].
11. **Status labels.** Each claim carries its status at the claim: `derived here`, `computed by the listing`, `cited [Sxx — verify]`, or `assumed for this lesson`.

## Dependency order

L1 → L2 → L3 → L4 (machines). L5 → L6 (grid-following). L1, L2, L6 → L7 (grid-forming). L1, L2, L7 → L8 (system). L3 is a tool lesson that every later listing relies on: all later listings use RK4 or semi-implicit Euler, never forward Euler, and say why by reference to L3.

---

## Lesson 1 — Frequency is shared state: the swing equation as one integrator

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson1.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson1_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** A 50 Hz grid stores `E_kin_sys = 200 GVA.s` of kinetic energy in its spinning machines [value assumed for this lesson; if attributed to a real grid, cite it with year and `verify`]. A 1000 MW power station trips. No control acts. How many seconds until frequency reaches 49.2 Hz, and how many until 48.8 Hz? Answer computed by the lesson: the frequency falls at 0.125 Hz/s, so 6.4 s to 49.2 Hz and 9.6 s to 48.8 Hz.

**Learning goals.**
1. Explain why every synchronous machine on an AC grid must run at the same average electrical frequency, so frequency is one shared state variable.
2. Convert quantities to per unit: `S_base`, `V_base`, `I_base = S_base/(sqrt(3) V_base)`, `Z_base = V_base^2/S_base`, and state why per unit removes transformer ratios.
3. Define the inertia constant `H` (stored kinetic energy at rated speed divided by `S_base`, unit second) and compute it from a moment of inertia.
4. Derive the per-unit swing equation and read it as an integrator: power imbalance in, frequency out.
5. Write a forward-Euler loop for the aggregated one-mass grid and check it against the closed form.

**Key derivation.** Start from Newton for a rotor, `J d(omega_m)/dt = T_m - T_e`. Multiply by `omega_m`, use `P = T omega_m`, and assume `omega_m` stays near rated speed. Divide by `S_base` and substitute `H = 0.5 J omega_m0^2 / S_base`. Result: `2H d(dw)/dt = P_m - P_e - K_D dw`, with `dw` the per-unit speed deviation and `K_D` a damping coefficient in per unit. State the convention of shared rule 6 and name the excluded alternative. Aggregate: sum the equations of all machines, with `E_kin_sys = sum of H_i S_i`, and convert `dw` to hertz with `df = f_0 dw`. For a step loss `dP` and no response or damping: `d(df)/dt = -f_0 dP / (2 E_kin_sys)`, so `RoCoF_0 = f_0 dP / (2 E_kin_sys) = 50 * 1000 / (2 * 200000) = 0.125 Hz/s` (MW and MW.s). State the assumption that makes the aggregation valid: all machines swing together, which Lesson 8 relaxes.

**Python snippet idea.** `lesson1_rocof.py`, about 20 lines. Constants `F0 = 50`, `E_KIN = 200e3` (MW.s), `DP = 1000` (MW), `H_STEP = 0.01`. A forward-Euler loop integrates `d(df)/dt = -F0*DP/(2*E_KIN)` and prints the first time the frequency crosses 49.2 Hz and 48.8 Hz. Expected output: 6.40 s and 9.60 s. State that forward Euler is exact here because the right-hand side is constant, and that Lesson 3 shows a case where it is not.

**Figures.**
- Fig. 1.1: a block diagram of the swing equation as one integrator with a feedback path `K_D`: imbalance in, `dw` out, a second integrator to `delta`. Must show that frequency is the integral of power imbalance.
- Fig. 1.2: frequency against time for the opening problem at `E_kin_sys` = 100, 200, 400 GVA.s, with horizontal lines at 49.2 Hz and 48.8 Hz. Must show that halving stored energy halves the time to each line (3.2 s, 6.4 s, 12.8 s to 49.2 Hz).

**Model limits.** No governor or primary response (repaid in Lesson 8), no load damping `D_load` (named, repaid in Lesson 8 exercises), one mass (repaid in Lesson 8), no network (repaid in Lesson 2).

**Exercises.**
1. *(Derivational)* A 4-pole, 60 Hz, 200 MVA machine has a rotor with `J = 5000 kg m^2`. Compute `H`. **Target:** `omega_m = 2 pi 60 / 2 = 188.5 rad/s`; `E_kin = 0.5 J omega_m^2 = 88.8 MJ`; `H = 0.444 s`. Comment: typical turbo-set values are 2 s to 8 s [S01 — verify], so the turbine mass dominates.
2. *(Computational)* Change `E_KIN` in the listing to 100e3 and 400e3 and report the time to 49.2 Hz. **Target:** 3.2 s and 12.8 s.
3. *(Computational)* A rate-of-change-of-frequency relay set at 1 Hz/s [S16 — verify] trips embedded generation. Find the `E_kin_sys` below which a 1000 MW loss at 50 Hz trips it. **Target:** `E_kin_sys = f_0 dP / (2 * 1) = 25 GVA.s`. Do not attribute the 1 Hz/s value to ENTSO-E (shared rule 10).
4. *(Derivational)* Show that `H` has the unit second, and that `H` does not change when the machine is described on a different voltage base.
5. *(Conceptual)* Two machines on one grid run at 50.0 Hz and 50.1 Hz for one minute. Compute the angle between them after that minute and say why the grid cannot operate that way. **Target:** `2 pi * 0.1 * 60 = 37.7 rad`, that is 6 full slips; the power between them reverses each slip.

---

## Lesson 2 — One machine on a stiff grid: linearise, then read the eigenvalues

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson2.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson2_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** A 60 Hz generator gets a small bump in mechanical power. It then oscillates at about 1.4 Hz, and the oscillation takes tens of seconds to die. Why that frequency, and why so slow? The lesson answers with two numbers from Example 1.1 of the P1 book: `omega_n = 8.96 rad/s = 1.43 Hz` and `zeta = 0.0159`.

**Learning goals.**
1. Model a generator as a constant voltage `E'` behind a reactance `X`, connected to an infinite bus of voltage `V_inf`, and derive `P_e = (E' V_inf / X) sin(delta)`.
2. Find an equilibrium numerically and in closed form.
3. Linearise a nonlinear ODE by hand and by finite differences, and get the synchronizing torque coefficient `K_s = (E' V_inf / X) cos(delta_0)`.
4. Compute the eigenvalues of the 2-by-2 state matrix, and read `omega_n` and `zeta` from them.
5. State the stability condition `K_s > 0` and `K_D > 0`, and interpret `K_s` as a spring and `K_D` as a dashpot.

**Key derivation.** State `x = (delta, dw)`. ODE: `d(delta)/dt = omega_0 dw`; `2H d(dw)/dt = P_m - P_max sin(delta) - K_D dw` with `P_max = E' V_inf / X`. Equilibrium: `delta_0 = arcsin(P_m / P_max)`, `dw = 0`. Jacobian: `A = [[0, omega_0], [-K_s/(2H), -K_D/(2H)]]`. Characteristic polynomial: `s^2 + (K_D/(2H)) s + K_s omega_0/(2H) = 0`. So `omega_n = sqrt(K_s omega_0 / (2H))` and `zeta = K_D / (4 H omega_n)`. Numbers (Example 1.1 of P1): `H = 3.5 s`, `K_D = 2 pu`, `E' = 1.1 pu`, `V_inf = 1.0 pu`, `P_m = 0.8 pu`, `X = 0.45 + 0.40/2 = 0.65 pu`, `omega_0 = 376.99 rad/s`. Then `P_max = 1.6923 pu`, `delta_0 = 28.21 deg = 0.4924 rad`, `K_s = 1.4913 pu/rad`, `omega_n = 8.962 rad/s = 1.426 Hz`, `zeta = 0.01594`, eigenvalues `-0.1429 +/- j 8.961 1/s`. Note for the draft: the P1 plan prints `0.4926 rad` and `K_s = 1.4915`; the probe gives `0.4924 rad` and `1.4913`; print the probe values to four digits and the three-digit values `1.49 pu/rad`, `8.96 rad/s`, `0.0159` where the P1 book is quoted. Cite the 0.7 Hz to 2 Hz local-mode band [S01 — verify].

**Trap to state explicitly.** The listing steps `P_m` from 0.8 to 0.85 pu. The simulated oscillation then runs at 1.413 Hz, not 1.426 Hz. The reason: the machine oscillates about the new equilibrium `delta = 30.15 deg`, where `K_s = 1.4634 pu/rad`, `omega_n = 8.878 rad/s`, and the damped frequency is 1.413 Hz. Linearising at the new operating point matches the simulation (1.4127 Hz against a zero-crossing estimate of 1.4126 Hz). Both numbers are correct. An editor must not "fix" one to match the other.

**Python snippet idea.** `lesson2_smib.py`, about 40 lines, stdlib only. (a) A function `f(x)` for the ODE. (b) A finite-difference Jacobian with step `1e-6`, printed beside the analytic `A`. (c) Eigenvalues from the quadratic formula with `cmath.sqrt`. (d) An RK4 integration at `h = 0.001 s` for 10 s after the step `P_m = 0.8 -> 0.85`, with the oscillation frequency measured from zero crossings of `delta - delta_new`. Expected output: finite-difference and analytic Jacobians agree to about 6 digits; eigenvalues `-0.1429 +/- j8.961`; zero-crossing frequency 1.413 Hz; linearised frequency at the new point 1.413 Hz.

**Figures.**
- Fig. 2.1: the power-angle curve `P_e = 1.6923 sin(delta)` with `P_m = 0.8` as a horizontal line, both intersections marked, and the slope `K_s` drawn as a tangent at 28.2 deg. Must show why the left intersection is stable and the right one (151.8 deg) is not.
- Fig. 2.2: `delta(t)` from the listing after the step, with the envelope `exp(-0.1429 t)` drawn. Must show that the decay rate is the real part of the eigenvalue.
- Fig. 2.3: eigenvalues in the complex plane for `K_D` = 0, 2, 10, 30 pu. Must show the pair moving left on a circle of radius `omega_n = 8.962 rad/s`.

**Model limits.** No flux decay, no excitation control, no saliency, no stator resistance [S01 — verify]; the infinite bus has fixed frequency and voltage. The classical model is the smallest one that has a swing mode.

**Exercises.**
1. *(Conceptual)* A machine sits at `delta_0 = 95 deg`. Is it small-signal stable? **Target:** no; `K_s = P_max cos(95 deg) < 0`, so one eigenvalue is real and positive.
2. *(Derivational)* Show that writing the damping as `K_D' (omega - omega_0)` with `omega` in rad/s, while keeping `2H d(dw)/dt` on the left, multiplies `zeta` by `omega_0`. **Target:** `zeta` becomes `376.99 * 0.01594 = 6.01`, which is overdamped and wrong.
3. *(Computational)* Repeat the eigenvalue computation for `H` = 2, 3.5, 6, 8 s. **Target:** `omega_n` = 11.86, 8.96, 6.84, 5.93 rad/s; `zeta` = 0.0211, 0.0159, 0.0122, 0.0105; both scale as `H^-0.5`.
4. *(Computational)* Replace the analytic Jacobian by the finite-difference one for step sizes `1e-2` to `1e-12`, and report where the error is smallest. **Target:** report the value the run returns; the error falls then rises because of floating-point cancellation.
5. *(Conceptual)* Say in one sentence why `zeta = 0.016` motivates power system stabilisers [S01 — verify].

---

## Lesson 3 — When the integrator lies: step size and false instability

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson3.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson3_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** A programmer simulates the Lesson 2 machine with forward Euler at `h = 10 ms`, a step that looks small against a 0.7 s oscillation period. The machine loses synchronism (the angle passes 180 deg) at `t = 16.93 s`. Lesson 2 proved it is stable. Which one is wrong, and how does a programmer know before trusting a plot?

**Learning goals.**
1. Apply a numerical method to the linear test equation `dx/dt = lambda x` and compute its amplification factor.
2. Compute the largest stable step for forward Euler for a given eigenvalue, and see that "stable" is not the same as "accurate".
3. Compare forward Euler, semi-implicit (symplectic) Euler, and RK4 on the same machine.
4. Use a conserved energy function to test an integrator.
5. Pick a step size from the fastest eigenvalue of the model.

**Key derivation.** Forward Euler maps `x_(k+1) = (1 + h lambda) x_k`. For `lambda = sigma + j omega_d` with `sigma = -0.1429 1/s` and `omega_d = 8.961 rad/s`: `|1 + h lambda|^2 = (1 + h sigma)^2 + (h omega_d)^2`. At `h = 0.01 s`: `|1 + h lambda| = 1.00258`, a growth rate of `+0.258 1/s` against the physical decay rate of `-0.143 1/s`. Over 10 s, forward Euler multiplies the oscillation amplitude by 13.2; the true system multiplies it by 0.240. Stability condition: `|1 + h lambda| < 1` gives `h < -2 sigma / |lambda|^2 = 3.56 ms`. At `h = 1 ms` Euler decays by 0.358 over 10 s, still not the true 0.240. For the undamped machine derive the energy function `W = H omega_0 dw^2 - P_m delta - P_max cos(delta)`, show `dW/dt = -K_D omega_0 dw^2`, so `W` is conserved when `K_D = 0`. Semi-implicit Euler (update `dw` first, then `delta` with the new `dw`) keeps `W` bounded for `h omega_n < 2` (here `h < 0.223 s`). RK4's stability boundary for this eigenvalue is `h = 0.319 s` (`h |lambda| = 2.86`).

**Python snippet idea.** `lesson3_euler_drift.py`, about 45 lines. The Lesson 2 machine after the `P_m = 0.8 -> 0.85` step, integrated three ways at `h = 0.01 s` for 10 s: forward Euler, semi-implicit Euler, RK4. Print the late oscillation amplitude (largest `|delta - delta_new|` over 8 s to 10 s) for each. Expected: forward Euler about 22.3 deg, semi-implicit Euler 0.609 deg, RK4 0.609 deg, against an initial amplitude of 1.94 deg. Then run forward Euler to 60 s and print the slip time: 16.93 s. Print `h_crit = 3.56 ms` from the formula and confirm it by bisection on the step size.

**Figures.**
- Fig. 3.1: `delta(t)` for the three methods at `h = 0.01 s` on one axis, 0 s to 20 s. Must show forward Euler growing while the other two decay together.
- Fig. 3.2: the forward-Euler stability region (disc of radius 1 centred at -1) in the `h lambda` plane, with `h lambda` plotted for `h` = 1, 3.56, 5, 10 ms. Must show the eigenvalue leaving the disc as `h` grows.
- Fig. 3.3: the energy function `W(t)` for the undamped machine (`K_D = 0`) under forward Euler and semi-implicit Euler. Must show drift for the first and a bounded ripple for the second.

**Model limits.** The analysis is exact for the linearised model only. For large swings the eigenvalue changes along the trajectory. Variable-step solvers are named but not used; the lesson keeps fixed steps so the reader can see the error.

**Exercises.**
1. *(Computational)* Find by bisection the largest forward-Euler step for which the linearised machine decays. **Target:** 3.56 ms.
2. *(Derivational)* Derive `dW/dt = -K_D omega_0 dw^2` from the swing equation. **Target:** multiply the swing equation by `omega_0 dw` and use `d(delta)/dt = omega_0 dw`.
3. *(Computational)* Run RK4 at `h` = 0.1, 0.2, 0.3, 0.35 s and report where it stops decaying. **Target:** between 0.3 s and 0.35 s; the formula gives 0.319 s.
4. *(Conceptual)* A simulation tool reports a machine "unstable" at a 20 ms step. List two checks before believing it. **Target:** halve the step and compare; compute `|1 + h lambda|` (or the method's equivalent) for the fastest eigenvalue.
5. *(Computational)* Plot the forward-Euler amplitude after 10 s against `h` from 1 ms to 10 ms and mark where it crosses the true value 0.240. **Target:** report the run's values; at `h = 1 ms` it is 0.358, so the crossing is below 1 ms.

---

## Lesson 4 — Big faults: the equal-area criterion and a bisection for clearing time

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson4.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson4_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** A short circuit next to the Lesson 2 machine drops its electrical output to zero. Protection trips the faulted line. How many milliseconds does protection have before the machine can no longer recover? Answer computed by the lesson: 170 ms, that is 10.2 cycles at 60 Hz. Typical transmission protection clears in 4 to 6 cycles [S01 or S04 — verify], so this machine has margin.

**Learning goals.**
1. Model a fault as a switch between three networks: pre-fault, fault-on, post-fault.
2. Derive the equal-area criterion from the energy function of Lesson 3.
3. Compute the critical clearing angle and the critical clearing time in closed form.
4. Find the same critical clearing time by bisection over simulations, and compare.
5. Explain why a small-signal eigenvalue says nothing about this question.

**Key derivation.** With `K_D = 0`, integrate the swing equation once: `H omega_0 dw^2 = integral from delta_0 to delta of (P_m - P_e) d(delta)`. The machine returns if the decelerating area after clearing can absorb the kinetic energy gained during the fault: `A_acc = A_dec`. Numbers (Example 1.2 of P1): fault-on `P_e = 0`; post-fault `X_post = 0.45 + 0.40 = 0.85 pu`, `P_max_post = 1.2941 pu`. `delta_max = pi - arcsin(P_m / P_max_post) = 2.4752 rad`. `cos(delta_cr) = [P_m (delta_max - delta_0) + P_max_post cos(delta_max)] / P_max_post = 0.4397`, so `delta_cr = 63.92 deg = 1.1155 rad`. With `P_e = 0` during the fault, `delta(t) = delta_0 + omega_0 P_m t^2 / (4H)`, so `t_cr = sqrt(4 H (delta_cr - delta_0) / (omega_0 P_m)) = 0.1701 s`, 10.2 cycles.

**Python snippet idea.** `lesson4_cct.py`, about 45 lines. A function `stable(t_clear)` integrates the fault-on system with RK4 (`h = 0.5 ms`) to `t_clear`, switches to the post-fault system, runs to 5 s, and returns `False` if `delta` passes `delta_max`. A bisection over `t_clear` in [0.10, 0.25] s stops at 1 ms resolution or finer. Expected output: bracket 0.1697 s to 0.1700 s, against the equal-area value 0.1701 s. State that the two agree because both neglect damping; state the resolution used.

**Figures.**
- Fig. 4.1: power-angle curves for pre-fault (`P_max = 1.6923`), fault-on (0), and post-fault (`1.2941`), with `P_m = 0.8` and the three angles `delta_0 = 28.2 deg`, `delta_cr = 63.9 deg`, `delta_max = 141.8 deg` marked. Must show that losing a line lowers the curve.
- Fig. 4.2: the same axes with `A_acc` and `A_dec` shaded. Must show that equal areas define `delta_cr`.
- Fig. 4.3: `delta(t)` for clearing at 0.15 s and 0.19 s. Must show one return and one runaway, with the boundary between them near 0.170 s.

**Model limits.** No damping during the swing, a classical machine, a single machine against an infinite bus, and a bolted fault with `P_e = 0` exactly. Multi-machine transient stability needs time-domain simulation; equal area is exact only for one machine against an infinite bus (or two machines reduced to one).

**Exercises.**
1. *(Derivational)* Derive `A_acc = A_dec` from `W` of Lesson 3.
2. *(Computational)* Tighten the bisection to 0.1 ms and report the bracket. **Target:** it contains 0.1701 s within the integrator's error; report the run's bracket and the step used.
3. *(Computational)* Add `K_D = 2 pu` to the simulation and report the new critical clearing time. **Target:** report the value the run returns; it is longer than 0.170 s because damping removes energy.
4. *(Conceptual)* Protection clears in 5 cycles. State the time margin in milliseconds against `t_cr`. **Target:** `5/60 = 83.3 ms`, margin `170.1 - 83.3 = 86.8 ms`, with the 4 to 6 cycle figure cited [verify].
5. *(Conceptual)* Explain why the eigenvalues of Lesson 2 are the same for this machine before and after the fault is cleared on a strong network, yet the machine can still be lost. **Target:** eigenvalues describe small deviations about an equilibrium; a fault moves the state far from it, into the region where the nonlinear `sin(delta)` decides.

---

## Lesson 5 — Rotating frames: the Park transform and the phase-locked loop

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson5.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson5_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** An inverter must inject current in step with a 50 Hz grid voltage that it can only sample. After a disturbance, the grid voltage angle jumps by 30 deg. How does code find the new angle, and how long does it take? Answer computed by the lesson: a phase-locked loop tuned for 10 Hz bandwidth and damping ratio 0.707 settles in about `4 / (zeta omega_n) = 0.090 s`.

**Learning goals.**
1. Apply the Clarke and Park transforms in amplitude-invariant form, and show that a balanced three-phase set becomes two constants in a frame that rotates with it.
2. Define the synchronous-reference-frame phase-locked loop: `v_q` is the error signal, a PI controller sets the frequency, and an integrator sets the angle.
3. Linearise the loop and derive `omega_n_pll = sqrt(K_pll k_i_pll)` and `zeta_pll = K_pll k_p_pll / (2 omega_n_pll)`.
4. Tune `k_p_pll` and `k_i_pll` for a target bandwidth and damping on a stiff grid (`K_pll = 1`).
5. Implement the loop on sampled data and measure its lock time.

**Key derivation.** Clarke with factor 2/3 maps `(a, b, c)` to `(alpha, beta)`; Park rotates by `theta_pll`. For `v_a = V cos(theta_g)` (and b, c shifted by 120 deg): `v_d = V cos(theta_g - theta_pll)`, `v_q = V sin(theta_g - theta_pll)`. Near lock, `v_q` is approximately `V (theta_g - theta_pll)`, so the loop gain from angle error to `v_q` is `K_pll = V` on a stiff grid. Loop: `omega_pll = omega_0 + k_p_pll v_q + k_i_pll * integral(v_q)`, `d(theta_pll)/dt = omega_pll`. Closed loop in the angle error: `s^2 + K_pll k_p_pll s + K_pll k_i_pll = 0`. Tuning for `omega_n_pll = 2 pi 10 = 62.83 rad/s`, `zeta_pll = 0.707` at `K_pll = 1`: `k_i_pll = 3948 1/s^2`, `k_p_pll = 88.84 1/s`. State the Park convention of shared rule 7 before the first dq quantity.

**Python snippet idea.** `lesson5_pll.py`, about 40 lines, stdlib only. Sample a balanced 50 Hz three-phase voltage at 10 kHz. Apply Clarke and Park with the loop's own angle. Run the PI loop. At `t = 0.1 s` jump the grid angle by 30 deg; at `t = 0.4 s` step the grid frequency to 50.5 Hz. Print the time for the angle error to stay inside 2 % of the jump, and the steady angle error after the frequency step. Expected: settling near 0.09 s (report the measured value and the tolerance); zero steady angle error after the frequency step, because the loop has two integrators.

**Figures.**
- Fig. 5.1: three phase voltages against time beside `v_d` and `v_q` after lock. Must show a rotating problem becoming two constants.
- Fig. 5.2: block diagram of the phase-locked loop (Park, PI, integrator) with `K_pll` marked as the gain between angle error and `v_q`. Must show where grid strength will enter in Lesson 6.
- Fig. 5.3: angle error against time after the 30 deg jump, for `zeta_pll` = 0.4, 0.707, 1.0 at fixed `omega_n_pll`. Must show the trade between speed and overshoot.

**Model limits.** Balanced, undistorted voltages; a stiff grid whose voltage the converter's current does not move (Lesson 6 removes this); no measurement filter. Unbalance puts a ripple at twice the grid frequency (100 Hz at 50 Hz) on `v_q`; named, not modelled.

**Exercises.**
1. *(Derivational)* Show that the three-phase instantaneous power in SI is `p = 1.5 (v_d i_d + v_q i_q)` with the amplitude-invariant transform, and that the factor 1.5 vanishes in per unit. **Target:** the per-unit bases absorb it.
2. *(Derivational)* Show that `K_pll = d(v_q)/d(theta_error)` at lock equals `V`.
3. *(Computational)* Add a 10 % negative-sequence component to the input and report the ripple on `v_q`. **Target:** a 100 Hz ripple; report its amplitude from the run.
4. *(Computational)* Retune for 20 Hz bandwidth and repeat the 30 deg jump. **Target:** `k_i_pll = 15791 1/s^2`, `k_p_pll = 177.7 1/s`; settling time about halves; report the measured value.
5. *(Conceptual)* Why does a frequency step leave zero steady angle error but a frequency ramp does not? **Target:** a type-2 loop tracks a ramp in angle (a frequency step) with zero error; a frequency ramp is a parabola in angle and needs a third integrator.

---

## Lesson 6 — Following on a weak grid: a current bound and a vanishing gain

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson6.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson6_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** A 200 MVA solar plant connects where the grid's short-circuit level is 300 MVA. Can it export its full rating at unity power factor with a standard grid-following controller? Answer computed by the lesson: no. The short-circuit ratio is 1.5, the terminal voltage sags to 0.745 pu, and this model's maximum power is 0.750 pu. The cited literature warns that the true limit is lower still [S07, S08 — verify].

**Learning goals.**
1. Define the short-circuit ratio `SCR = S_sc / S_rated` and, on the converter base with a purely inductive grid, `X_g = 1 / SCR`.
2. Model a grid-following converter as an ideal current source in its own phase-locked-loop frame behind `j X_g`.
3. Derive the loop equation `v_q = X_g I_d - V_g sin(theta_p)` and the existence bound: a steady state exists exactly when `X_g I_d <= V_g`, that is `I_d <= SCR V_g`. **The bound is on current, not power.**
4. Derive delivered power `P = (V_g^2 / (2 X_g)) sin(2 theta_0)`, which peaks at `SCR V_g^2 / 2` at `theta_0 = 45 deg`, and the loop gain `K_pll = V_g cos(theta_0)`, which equals the terminal voltage and goes to zero at the bound.
5. See non-existence in code: a root finder that finds no root, and a simulation whose angle runs away.

**Key derivation.** Grid source `V_g` at angle 0; converter current `I_d` on the phase-locked-loop d axis at angle `theta_p`; terminal voltage `V_g + j X_g I`. In the loop frame, `v_q = X_g I_d - V_g sin(theta_p)` and `v_d = V_g cos(theta_p)`. Lock needs `v_q = 0`: `sin(theta_0) = X_g I_d / V_g`, possible only when `X_g I_d <= V_g`. Linearise: `d(v_q)/d(theta_p) = -V_g cos(theta_0)`, so `K_pll = V_g cos(theta_0)`. Then with Lesson 5's gains: `omega_n_pll = sqrt(K_pll k_i_pll)`, `zeta_pll = K_pll k_p_pll / (2 omega_n_pll) = 0.7071 sqrt(K_pll)`. Compare explicitly with Lesson 2: `K_s = (E' V / X) cos(delta_0)` and `K_pll = V_g cos(theta_0)` have the same structure; both vanish at 90 deg. Numbers (Example 2.1 of P1): `SCR = 1.2`, `X_g = 0.8333`, `V_g = 1`, `I_d = 1`: `theta_0 = 56.44 deg`, terminal voltage `= K_pll = P = 0.5528 pu`, `P_max = 0.600 pu`; `omega_n_pll` falls from 62.83 to 46.71 rad/s (7.43 Hz) and `zeta_pll` from 0.707 to 0.526. The designer changed nothing; the grid moved the loop. Note for the draft: the P1 plan prints 46.72 rad/s and 7.44 Hz and `k_p_pll = 88.86`; the probe, with `k_i_pll = (2 pi 10)^2 = 3947.8` and `k_p_pll = 2 * 0.707 * 62.83 = 88.84`, gives 46.71 rad/s and 7.435 Hz; print the probe values and state the gains used. State the omission that matters most: no reactive support, so the terminal voltage falls to `V_g cos(theta_0)`; a plant that holds 1 pu with reactive current reaches the higher figure `P_max = SCR V_g |v|` quoted in the literature [S07, S08 — verify].

**Python snippet idea.** `lesson6_weak_grid.py`, about 50 lines, stdlib only. Part 1: for `SCR` in 10, 3, 2, 1.5, 1.2, 1.05, 0.95, solve `X_g I_d - V_g sin(theta) = 0` by bisection on [0, pi/2]; print `theta_0`, `K_pll`, `P`, `P_max`, `omega_n_pll`, `zeta_pll`, or "no steady state" for 0.95. Expected rows: `theta_0` = 5.74, 19.47, 30.00, 41.81, 56.44, 72.25 deg; `K_pll` = 0.9950, 0.9428, 0.8660, 0.7454, 0.5528, 0.3049; `zeta_pll` = 0.7052, 0.6865, 0.6579, 0.6104, 0.5256, 0.3904; `P_max` = 5.000, 1.500, 1.000, 0.750, 0.600, 0.525. Part 2: integrate the nonlinear loop `d(theta_p)/dt = k_p v_q + integral(k_i v_q)` with `v_q = X_g I_d - V_g sin(theta_p)` using RK4, at `SCR = 1.2` (locks, lightly damped) and at `SCR = 0.95` (`v_q > 0` for every angle, so `theta_p` grows without bound: loss of synchronism).

**Figures.**
- Fig. 6.1: phasor diagram at the point of connection for `SCR = 10` and `SCR = 1.2` side by side: `V_g`, `j X_g I`, terminal voltage, `theta_0`. Must show that on a weak grid the converter's own current sets most of the angle.
- Fig. 6.2: `K_pll` (equal to the terminal voltage and to `P` at `I_d = 1 pu`) and `P_max = SCR/2` against `SCR` from 1 to 10, with the `SCR = 1.2` point marked. Must show that `K_pll` collapses only near the bound.
- Fig. 6.3: `theta_p(t)` from Part 2 at `SCR = 1.2` and `SCR = 0.95`. Must show lock against runaway.
- Fig. 6.4: root locus of the linearised loop as `K_pll` falls from 1 to 0.1 with fixed gains. Must show the pair moving toward the origin, not into the right half-plane, so the static bound alone does not explain observed oscillatory instability; that comes from phase-locked-loop and current-loop interaction [S08 — verify], cited, not derived.

**Model limits.** Ideal current source (inner current loop infinitely fast), no reactive support, purely inductive grid, one converter. State that the observed instability arrives below the static bound (cited), and that a fleet of such converters adds no synchronizing coefficient and no inertia.

**Exercises.**
1. *(Conceptual)* The opening problem. **Target:** `SCR = 1.5`, `X_g = 0.6667`, `theta_0 = 41.81 deg`, terminal voltage and `K_pll` 0.7454 pu, `P = 0.7454 pu`, `P_max = 0.750 pu`: cannot export 1.0 pu without reactive support.
2. *(Derivational)* Show that all terms of `d(v_q)/d(theta_p)` except `-V_g cos(theta_0)` vanish at lock, so grid strength enters the loop through one scalar.
3. *(Computational)* Sweep `SCR` from 1.01 to 10 and find where `zeta_pll` first falls below 0.3. **Target:** analytically `K_pll = 0.180`, `theta_0 = 79.6 deg`, `SCR = 1.017`; report the value the sweep returns and its resolution.
4. *(Computational)* Retune so that `zeta_pll = 0.707` at `SCR = 1.2`, then run the retuned loop at `SCR = 10`. **Target:** `k_p_pll = 160.7`, `k_i_pll = 7142`; at `SCR = 10` the loop runs at `omega_n_pll = 84.3 rad/s`, `zeta_pll = 0.949`, faster than designed.
5. *(Conceptual)* Why does adding more grid-following plant not raise `SCR` for the plant already there? **Target:** `SCR` is set by the Thevenin sources behind the connection point; a current source adds no Thevenin voltage source and no short-circuit power.

---

## Lesson 7 — Forming instead of following: droop is a swing equation

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson7.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson7_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** A battery inverter has no rotor. A system operator asks it for inertia. Can code give it some, how much, and what backs it? The lesson answers in two parts. First, a droop controller with a power filter already behaves as a swing equation with `H_eq = 1 / (2 m_p omega_c)`: 1.59 s for 5 % droop and a 1 Hz filter. Second, the energy is not in the inverter: its DC capacitor holds 14.4 kJ per MVA, 243 times less than a 3.5 s machine, so the energy must come from the battery behind it.

**Learning goals.**
1. Define grid-forming control by terminal behaviour: a voltage source `E` behind an impedance, whose angle `theta` is an internal state and not a measurement.
2. Write P-f droop with a first-order power filter: `omega = omega_ref - m_p (P_f - P_ref)`, `d(P_f)/dt = omega_c (P - P_f)`.
3. Prove, by matching coefficients with the swing equation of Lesson 1, that `H_eq = 1 / (2 m_p omega_c)` and `K_D_eq = 1 / m_p`.
4. Show that a grid-forming converter against a grid restores a synchronizing coefficient `K_s = (E V / X) cos(delta_0)` of Lesson 2's form.
5. Compute matching control's `H_eq = 0.5 C_dc v_dc0^2 / S_base` and compare energies.

**Key derivation.** Define `dP = P_e - P_ref`. Differentiate the droop law and substitute the filter: `s dw = -omega_c dw - m_p omega_c dP`. The swing equation at constant `P_m` gives `s dw = -dP/(2H) - (K_D/(2H)) dw`. Match: `m_p omega_c = 1/(2H)` and `omega_c = K_D/(2H)`, so `H_eq = 1/(2 m_p omega_c)` and `K_D_eq = 1/m_p`. Exact when the filter is first order and the droop is linear. Numbers (Example 3.1 of P1): `m_p = 0.05`, `K_D_eq = 20 pu`; `omega_c = 2 pi 5` gives `H_eq = 0.318 s`, `omega_c = 2 pi 1` gives 1.592 s, `omega_c = 2 rad/s` gives 5.000 s; a 3.5 s equivalent needs `omega_c = 2.857 rad/s`, a filter time constant of 0.35 s. Against the Lesson 2 grid (`E = 1.1`, `V = 1`, `X = 0.65`, `P = 0.8`, 60 Hz) with `H_eq = 1.592 s`, `K_D_eq = 20`: `K_s = 1.4913 pu/rad`, `omega_n = 13.29 rad/s` (2.12 Hz), `zeta = 0.236`, eigenvalues `-3.142 +/- j12.91`; the real part equals `-omega_c/2`. The damping ratio is 14.8 times the machine's 0.0159. Matching control (Example 3.2 of P1): `C_dc = 20 mF`, `v_dc0 = 1200 V`, `S_base = 1 MVA`: 14.4 kJ, `H_eq = 0.0144 s`, ratio `3.5/0.0144 = 243`. An inertial response with `H_v = 5 s` on 100 MVA over 0.8 Hz at 50 Hz releases `2 H_v S df / f_0 = 16 MJ = 4.44 kWh`, 1111 times the capacitor store.

**Python snippet idea.** `lesson7_droop_vs_swing.py`, about 45 lines. Part 1: integrate the filtered droop law and the swing equation with `H_eq`, `K_D_eq` side by side under a 0.1 pu imbalance step; print the largest difference (about `3e-17` with Euler at `h = 1e-4`) and the final value `-0.005 pu` (`= -m_p * 0.1`). State plainly that this is an identity check of the algebra on one linear ODE, not an independent physics test. Part 2: put the droop converter against the Lesson 2 grid, `P_e = (E V / X) sin(theta)`, step `P_ref` from 0.8 to 0.85, integrate with RK4, and print the measured oscillation frequency and decay rate against `omega_d = 12.91 rad/s` and `sigma = -3.142 1/s`. Part 3: print the energy ratios 243 and 1111.

**Figures.**
- Fig. 7.1: grid-following and grid-forming block diagrams side by side, the same circuit beneath both. Must show that the difference is which variable is the input.
- Fig. 7.2: `H_eq` against `omega_c` for `m_p` = 0.02, 0.05, 0.10 on log axes, with a horizontal line at 3.5 s and the three Example 3.1 points. Must show the trade between filter speed and equivalent inertia.
- Fig. 7.3: log-scale bars of stored energy per MVA: machine at 3.5 s (3.5 MJ), the DC link (14.4 kJ), and the demand of the 16 MJ inertial response scaled per MVA (0.16 MJ). Must show the factor 243 (machine against DC link, both per MVA). Caution for the draft: the factor 1111 compares 16 MJ for a 100 MVA response against 14.4 kJ for a 1 MVA DC link, so it mixes ratings; per MVA the demand-to-DC-link ratio is `0.16 MJ / 14.4 kJ = 11.1`. Print both and say which ratings each compares.

**Model limits.** Linear droop about one operating point; current limit `I_max` ignored (a saturated converter is no longer a voltage source); ideal DC source behind the capacitor; virtual synchronous machine and dispatchable virtual oscillator control named, with the oscillator's global synchronization result cited [S11 — verify], not derived.

**Exercises.**
1. *(Derivational)* Derive `H_eq` and `K_D_eq` by coefficient matching. **Target:** as in the key derivation, with the assumption that makes the match exact.
2. *(Derivational)* Show that a virtual synchronous machine with `H_v`, `K_D_v` has the same steady-state droop as a droop controller with `m_p = 1/K_D_v`. **Target:** set derivatives to zero.
3. *(Computational)* Find the DC capacitance that gives `H_eq = 3.5 s` at 1200 V on 1 MVA. **Target:** `4.861 F`, 243 times 20 mF.
4. *(Conceptual)* Why can a converter be grid-forming and still unable to give an inertial response? **Target:** an internal angle fixes the control structure, not the energy store; energy reserve and `I_max` bound the response.
5. *(Conceptual)* A vendor says "5 seconds of inertia". Name the three numbers you need before the claim means anything. **Target:** the rating it refers to; the usable energy reserve; the current limit and the headroom kept below it.

---

## Lesson 8 — From one machine to a system: centre of inertia, nadir, and sizing

**House rules (short form of the Shared rules section).** Self-contained HTML `lesson8.html`, no external script, stylesheet, font or image, no MathJax; MathML or plain HTML maths; inline SVG figures drawn from computed numbers; dark palette `#0f172a` / `#1e293b` / `#e2e8f0` / `#cbd5e1` / `#94a3b8` / accents `#fb923c` `#2dd4bf` / borders `#334155` as `:root` variables with `<meta name="color-scheme" content="dark">`; no page scroll at 360 px. Python 3 stdlib only (numpy for eigenvalues in Lesson 8 only), PEP8, lines at most 79 chars, every listing runs and prints the quoted numbers; probe files named `lesson8_*.py`. Swing convention `2H d(dw)/dt = P_m - P_e - K_D dw`, `d(delta)/dt = omega_0 dw`, damping `K_D` never `D`. Park amplitude-invariant, d axis on measured voltage. Published numbers cited with S-identifiers of `../p1-textbook/book-plan.md` §5.2 and `— verify`; never print "ENTSO-E 1 Hz/s". Sections: opening problem, model, derivation, code, model limits, exercises with answer targets in `<details>`.

**Opening problem.** On 9 August 2019 Great Britain's frequency fell to 48.8 Hz and low-frequency demand disconnection shed about 931 MW, after a total infeed loss of about 1878 MW [S14 — verify]. For a 50 Hz grid that loses 1000 MW and gets 1000 MW of primary response ramped in over 10 s, what stored energy keeps the frequency above 48.8 Hz? Answer computed by the lesson: at least 104.2 GVA.s. At 100 GVA.s the nadir is 48.75 Hz, below the line.

**Learning goals.**
1. Write the swing equations of several machines coupled through a network, and define the centre-of-inertia frequency.
2. Build the state matrix for two machines and read two kinds of mode from its eigenvalues: the common mode (centre of inertia) and the relative mode (machines swinging against each other). Explain the zero eigenvalue.
3. Derive the initial rate of change of frequency `RoCoF_0 = f_0 dP / (2 E_kin_sys)` and the nadir `df_nadir = -f_0 dP T / (4 E_kin_sys)` under a linear primary-response ramp.
4. Size a grid-forming fleet to replace machine inertia against three separate constraints: energy, power headroom, current limit. Identify the binding one without adding unlike quantities.

**Key derivation.** Two units on a 1000 MVA base, taken from test system TS4 of P1: unit 1 400 MVA, `H = 4.0 s`; unit 2 300 MVA, `H = 3.0 s`; on the system base `M_i = 2 H_i S_i / S_sys` = 3.2 s and 1.8 s; `K_D` = 2 pu on own base, 0.8 and 0.6 on system base; `E_1 = E_2 = 1.05 pu`, tie reactance `X_12 = 2.0 pu`, transfer 0.2 pu (these coupling values are assumed for this lesson). Then `delta_12 = 21.27 deg`, `K_12 = (E_1 E_2 / X_12) cos(delta_12) = 0.5137 pu/rad`. State `x = (delta_1, delta_2, dw_1, dw_2)` at 50 Hz. Eigenvalues: `0` (absolute angle has no reference, not an instability), `-0.280 1/s` (common speed decays through total damping, `-(K_D1 + K_D2)/(M_1 + M_2)`), and `-0.1517 +/- j11.83 1/s`, a relative mode at 1.884 Hz with damping ratio 0.0128; check against `omega_n = sqrt(omega_0 K_12 (1/M_1 + 1/M_2)) = 11.84 rad/s`. Nadir: integrate `(2 E_kin_sys / f_0) d(df)/dt = -dP + dP t / T` from 0 to `T`; the nadir is at `t = T`, and the factor 4 is `2 * 2` from the two integrations. Numbers (Example 4.1 of P1, `E_kin_sys = 200 GVA.s` assumed or cited with year and `verify`): `RoCoF_0 = 0.125 Hz/s`, `f_nadir = 49.375 Hz`; at 300, 100, 50 GVA.s: 49.583, 48.75, 47.5 Hz. Floor for 48.8 Hz: `E_kin_sys >= f_0 dP T / (4 * 1.2) = 104.2 GVA.s`. Sizing (Example 4.2 of P1, a design case defined by the P1 book, not a published fleet; the project label "1.6 GW" is a 1.6 GVA rating): 8 synchronous condensers of 200 MVA, `H = 3.5 s` [assumed; cite a manufacturer figure with `verify` if one is used], `E_kin = 5.6 GVA.s`. Energy over 0.8 Hz at 50 Hz: `2 E_kin df / f_0 = 179.2 MJ = 49.8 kWh`; a 1.12 GVA, 1-hour battery fleet holds 22 500 times as much, so energy does not bind. Power at 1 Hz/s: `2 E_kin RoCoF / f_0 = 224 MW`; at `H_v = 5 s` a converter gives 0.20 pu of its rating, so 1120 MVA of grid-forming plant. Current: 0.20 pu on top of 1.0 pu dispatch uses all of `I_max = 1.2 pu`. Headroom and current limit bind together; energy does not.

**Python snippet idea.** Two listings. `lesson8_nadir.py` (stdlib, about 30 lines): RK4 on the aggregated model with the linear ramp, sweep `E_kin_sys` over 300, 200, 100, 50 GVA.s, print `RoCoF_0` and the nadir, then bisect for the smallest `E_kin_sys` that keeps the nadir at or above 48.8 Hz. Expected: 49.583, 49.375, 48.750, 47.500 Hz; floor 104.2 GVA.s. `lesson8_two_unit.py` (numpy allowed for `numpy.linalg.eigvals`, about 25 lines): build the 4-by-4 state matrix and print the eigenvalues and the relative-mode frequency and damping ratio. Expected: `0`, `-0.280`, `-0.1517 +/- j11.83`, 1.884 Hz, 0.0128.

**Figures.**
- Fig. 8.1: frequency against time for `E_kin_sys` = 300, 200, 100, 50 GVA.s with the nadir marked on each and a horizontal line at 48.8 Hz. Must show nadir depth scaling as `1/E_kin_sys`.
- Fig. 8.2: the two-unit eigenvalues in the complex plane with a sketch of the two mode shapes (both angles moving together; angles moving in opposition, weighted by `1/M_i`). Must show that one network has two different kinds of mode.
- Fig. 8.3: the three sizing constraints as three separate panels, each in its own unit (MJ, MW, pu current), with the fleet's capacity drawn against each. Must show that the constraints cannot be added and that energy is not the binding one.

**Model limits.** One aggregated mass for the nadir (all machines swing together); no load damping `D_load`; a linear ramp stands in for governor and converter response [S13 — verify]; two units stand in for a network; the current-limited converter is not proved stable while saturated at `I_max`, which is an open problem [S17, S18 — verify]. The two rate-of-change-of-frequency figures stay separate (shared rule 10).

**Exercises.**
1. *(Derivational)* Derive the nadir formula and locate the factor 4. **Target:** as in the key derivation.
2. *(Computational)* Sweep `T` over 5, 10, 20, 30 s at 200 GVA.s. **Target:** `df_nadir` = -0.3125, -0.625, -1.25, -1.875 Hz; report the run's values and tolerance.
3. *(Derivational)* Add load damping `D_load` (MW/Hz). Show the nadir is shallower and name the dimensionless group that decides when damping dominates the ramp. **Target:** `D_load T f_0 / (2 E_kin_sys)` much greater than 1 (MW/Hz, s, Hz, MJ); verify the grouping numerically before printing it.
4. *(Computational)* In the two-unit listing, raise `X_12` from 2.0 to 4.0 pu at the same transfer and report the relative-mode frequency. **Target:** report the run's value; it falls because `K_12` falls.
5. *(Conceptual)* State one change to the sizing case that makes energy the binding constraint. **Target:** a response held for minutes rather than seconds; a converter fleet without a long-duration store; or a requirement set by a deep, sustained frequency excursion rather than by rate of change.
6. *(Conceptual)* Why is the zero eigenvalue of the two-unit model not an instability? **Target:** shifting both angles by the same constant changes no power flow; only angle differences are physical.

---

## Handoff to the draft stage

Draft prompt, one per lesson: `Read p7-explainers/outline.md, section "Lesson N", and the "Shared rules" section. Write p7-explainers/lessonN.html per the rigorous-explainer skill, except that the page must not load MathJax or any external resource. Open with the lesson's opening problem and its number. Recompute every number in a probe named lessonN_*.py before printing it. Make every listing run as printed.`
