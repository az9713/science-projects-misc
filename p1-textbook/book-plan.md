# Book plan — Grid-Forming Inverters and Power-System Stability

Status: plan stage complete. Pre-approved by `../PLAN.md` section 6, block P1. The author approval gates A to D of the `stem-textbook` skill are set aside by the task. Four chapters. Customer-facing HTML output, dark mode.

Written 2026-09-22.

---

## 1. Book statement

### 1.1 The problem

A power system holds its frequency because synchronous machines store kinetic energy in steel and release it without being asked. The rotor of a generator is a mechanical integrator. Its angle moves when mechanical power in and electrical power out differ. This one fact produces the whole classical stability picture: the swing equation, the inertia constant H, the synchronizing torque coefficient, the equal-area criterion, and the small-signal eigenvalues of one machine against a stiff grid. Protection settings, reserve volumes, and grid codes in use today were all sized against that picture. An inverter has no rotor. A photovoltaic plant, a battery, or a wind turbine with a full converter stores energy of the order of tens of kilojoules in a DC capacitor, against hundreds of megajoules in a machine of the same rating (Example 3.2 computes the ratio: 243 to 1). The standard inverter control of the last three decades, grid-following control, does not try to be a machine. It measures the grid angle with a phase-locked loop and injects a commanded current. That control needs a grid angle that already exists. As machines retire, the angle it measures is set more and more by other converters that are also measuring it. The small-signal gain of the phase-locked loop falls as grid strength falls, the steady state ceases to exist above a current set by the short-circuit ratio, and the system loses stability by a mechanism the classical picture does not contain. Grid-forming control is the answer under test: control that makes the converter behave at its terminals as a voltage source behind an impedance, so that it sets an angle instead of following one. This book derives why the classical picture breaks, states exactly what grid-forming control restores, and states what it cannot restore, because a converter's inertia is bounded by its energy source and by its current limit in a way a rotor's is not.

### 1.2 Outcomes

After reading, the reader can do these four things.

1. **Derive and solve the classical stability models.** Write the swing equation in per unit from the rotor equation of motion, compute the synchronizing torque coefficient and the small-signal eigenvalues of one machine against an infinite bus, and find a critical clearing time by the equal-area criterion. Results R04, R06, R07, R09.
2. **Derive the low-short-circuit-ratio failure of grid-following control.** Build the dq-frame model of a converter with current control and a phase-locked loop, show that the steady state ceases to exist above a current set by the short-circuit ratio, and compute how the phase-locked-loop damping ratio and bandwidth fall as that bound is approached. Results R17, R18, R19.
3. **Map the four grid-forming control families onto one small-signal model.** Convert droop, virtual synchronous machine, matching, and dispatchable virtual oscillator control into a common angle model, then read off the equivalent inertia constant and equivalent damping of each. Results R26, R29, R32, R33.
4. **Size grid-forming plant for a system-level frequency requirement.** Compute system kinetic energy, initial rate of change of frequency, and frequency nadir for a mixed machine-and-converter grid, then size a grid-forming fleet against energy, power headroom, and current limit separately, so that the binding constraint is identified and not assumed. Results R34, R35, R36, R39.

### 1.3 Reader

A graduate engineer or physicist. Fluent in linear algebra, linear time-invariant systems, Laplace and frequency-domain analysis, complex numbers, and basic circuit theory: phasors, impedance, Kirchhoff's laws. Assumed to know nothing about power systems: not per unit, not the dq frame, not synchronous machines, not grid codes.

### 1.4 Out of scope

Electromagnetic transient modelling below the fundamental-frequency timescale; machine flux and excitation dynamics in detail; harmonic, subsynchronous and resonance stability; protection engineering; market design; semiconductor device physics. Each is named at the point where the book stops, with a source.

---

## 2. Result graph

Forty nodes. Identifiers are global and stable: `R01` to `R40`. A chapter prerequisite is cited by result identifier with no chapter prefix. Dependencies point backward only. There is no cycle and no forward edge.

Kinds: `def` definition, `model` derived model, `lem` lemma, `thm` theorem, `cor` corollary, `ex` worked numerical case, `cit` result carried from a source and not proved here.

| # | Ch | Kind | Result | Depends on |
|---|---|---|---|---|
| R01 | 1 | def | Per-unit system: base power S_base, base voltage V_base, derived I_base, Z_base, omega_base. Why per unit removes transformer ratios. | — |
| R02 | 1 | def | Rotor angle delta against a synchronous reference frame; per-unit speed deviation dw (omega-bar deviation); d(delta)/dt = omega_0 * dw. | R01 |
| R03 | 1 | def | Inertia constant H = (kinetic energy stored at rated speed) / S_base, unit second. Stored energy E_kin = H * S. | R01, R02 |
| R04 | 1 | model | Swing equation in per unit: 2H d(dw)/dt = P_m - P_e - K_D * dw. The rejected alternative convention (damping on speed in rad/s) is named and excluded. | R02, R03 |
| R05 | 1 | model | Classical machine model: constant emf E' behind transient reactance X_d'; P_e = (E' V / X) sin(delta). Omissions listed. | R01, R02 |
| R06 | 1 | lem | Synchronizing torque coefficient K_s = dP_e/d(delta) = (E' V / X) cos(delta_0). K_s > 0 exactly when abs(delta_0) < 90 degrees. | R05 |
| R07 | 1 | thm | Small-signal single-machine infinite-bus result: omega_n = sqrt(K_s * omega_0 / (2H)), zeta = K_D / (4 H omega_n). The equilibrium is asymptotically stable exactly when K_s > 0 and K_D > 0. | R04, R06 |
| R08 | 1 | ex | Example 1.1: numerical single-machine infinite-bus case. delta_0 = 28.2 deg, K_s = 1.49 pu/rad, omega_n = 8.96 rad/s = 1.43 Hz, zeta = 0.0159. | R07 |
| R09 | 1 | thm | Equal-area criterion. Critical clearing angle from equality of the accelerating and decelerating areas. | R04, R05 |
| R10 | 1 | ex | Example 1.2: critical clearing angle 63.9 deg, critical clearing time 0.170 s (10.2 cycles at 60 Hz). | R08, R09 |
| R11 | 1 | cit | Classification of power-system stability: rotor-angle, frequency, voltage. The 2021 revision adds converter-driven stability and resonance stability. | R07 |
| R12 | 2 | def | Clarke and Park transforms in amplitude-invariant form (factor 2/3). The dq frame. Convention: d axis on the measured voltage vector, so v_q = 0 when the loop is locked. | R01 |
| R13 | 2 | model | Averaged two-level voltage-source converter with L filter, written in dq with the omega*L cross-coupling terms. | R12 |
| R14 | 2 | model | Inner current control: proportional-integral control with decoupling; the closed loop approximated as first order with bandwidth alpha_c. Timescale separation from the outer loops. | R13 |
| R15 | 2 | def | Synchronous-reference-frame phase-locked loop: state equations driven by v_q, with gains k_p_pll and k_i_pll. | R12 |
| R16 | 2 | def | Short-circuit ratio SCR = S_sc / S_rated. On the converter base and for a purely inductive grid, SCR = 1 / X_g. Strength classes. | R01 |
| R17 | 2 | model | Grid-following converter as an ideal current source in its own phase-locked-loop frame, behind grid impedance j*X_g. Omissions listed, including the absence of reactive support, so the terminal voltage falls to V_g cos(theta_0); the omitted current-loop dynamics are repaid by R22. | R14, R15, R16 |
| R18 | 2 | thm | Existence bound: the loop equation is v_q = X_g I_d - V_g sin(theta_p), so a steady state exists exactly when X_g * I_d <= V_g, that is I_d <= SCR * V_g in per unit. The terminal voltage is then V_g cos(theta_0); delivered power is P = (V_g^2 / (2 X_g)) sin(2 theta_0), with maximum SCR * V_g^2 / 2 at theta_0 = 45 deg; and the phase-locked-loop small-signal gain K_pll = V_g cos(theta_0) reaches zero at the current bound. | R17 |
| R19 | 2 | thm | Linearised phase-locked loop: omega_n_pll = sqrt(K_pll * k_i_pll), zeta_pll = K_pll * k_p_pll / (2 * omega_n_pll). Both fall as SCR falls. K_pll is the only channel through which grid strength enters. | R15, R18 |
| R20 | 2 | ex | Example 2.1: SCR = 1.2, I_d = 1 pu, so theta_0 = 56.4 deg, terminal voltage 0.553 pu and P = 0.553 pu against P_max = 0.600 pu. K_pll = 0.553. A loop designed for 10 Hz and zeta = 0.707 at K_pll = 1 degrades to 7.44 Hz and zeta = 0.526. | R19 |
| R21 | 2 | ex | Example 2.2: sweep SCR over 10, 3, 2, 1.2, 1.05 against theta_0, K_pll, delivered power P at I_d = 1 pu, P_max = SCR/2, and zeta_pll. The table shows the decline is slow far from the bound and steep near it. | R20 |
| R22 | 2 | cit | Interaction between the phase-locked loop and the current loop produces oscillatory instability below the static bound of R18. Cited, not proved here. | R19 |
| R23 | 2 | cor | A fleet of grid-following converters contributes no synchronizing torque coefficient and no inertia. Compared with R06 and R07 term by term. | R07, R18 |
| R24 | 3 | def | Grid-forming control defined by terminal behaviour: a controlled voltage source behind an impedance, whose angle is an internal state and not a measurement. | R23 |
| R25 | 3 | model | Droop control: omega = omega_ref - m_p (P - P_ref), V = V_ref - n_q (Q - Q_ref), with a first-order power measurement filter of cutoff omega_c. | R24 |
| R26 | 3 | thm | Droop with a first-order filter is the swing equation of R04 with H_eq = 1 / (2 m_p omega_c) and K_D_eq = 1 / m_p. | R04, R25 |
| R27 | 3 | ex | Example 3.1: m_p = 0.05 pu. omega_c = 2*pi*5 rad/s gives H_eq = 0.318 s; omega_c = 2*pi*1 rad/s gives 1.59 s; H_eq = 5 s needs omega_c = 2 rad/s = 0.318 Hz. | R26 |
| R28 | 3 | model | Virtual synchronous machine: explicit integration of the swing equation with chosen H_v and K_D_v. What the free choice of H_v buys and what it costs. | R04, R24 |
| R29 | 3 | model | Matching control: d(theta)/dt = k_theta * v_dc. The DC capacitor takes the role of the rotor, so H_eq = 0.5 * C_dc * v_dc0^2 / S_base. | R24 |
| R30 | 3 | ex | Example 3.2: C_dc = 20 mF, v_dc0 = 1200 V, S_base = 1 MVA. Stored energy 14.4 kJ, H_eq = 0.0144 s, a factor 243 below H = 3.5 s. | R29 |
| R31 | 3 | model | Dispatchable virtual oscillator control: a harmonic oscillator with amplitude regulation and a rotation angle. The cited almost-global synchronization result. | R24 |
| R32 | 3 | thm | Unified small-signal model: all four families reduce to d(theta)/dt = omega plus a transfer function from power imbalance to frequency. Table of (H_eq, K_D_eq) per family. | R26, R28, R29, R31 |
| R33 | 3 | cor | A grid-forming converter restores K_s = (E V / X) cos(delta_0), and supplies inertia bounded by the DC energy reserve and by the current limit I_max. | R06, R32 |
| R34 | 4 | model | Multi-node network: bus admittance matrix, Kron reduction to internal nodes, centre of inertia, system stored energy E_kin_sys = sum over units of H_i * S_i. | R03, R05, R32 |
| R35 | 4 | thm | Initial rate of change of frequency after a loss of infeed: RoCoF_0 = f_0 * dP / (2 * E_kin_sys). | R34 |
| R36 | 4 | thm | Frequency nadir under a linear primary-response ramp delivered over time T, with no load damping: df_nadir = - f_0 * dP * T / (4 * E_kin_sys), reached at t = T. | R35 |
| R37 | 4 | ex | Example 4.1: 1000 MW loss, E_kin_sys = 200 GVA.s, f_0 = 50 Hz, T = 10 s. RoCoF_0 = 0.125 Hz/s, nadir 49.375 Hz. | R36 |
| R38 | 4 | cit | Great Britain, 9 August 2019: nadir 48.8 Hz; low-frequency demand disconnection at 48.8 Hz shed about 931 MW; total infeed loss about 1878 MW including embedded generation. | R36 |
| R39 | 4 | ex | Example 4.2: size a grid-forming fleet to replace a 1.6 GVA synchronous condenser fleet (8 x 200 MVA, H = 3.5 s, E_kin = 5.6 GVA.s) against three separate constraints. Energy 179 MJ, power headroom 224 MW at 1 Hz/s, current limit. Headroom binds; energy does not. | R33, R34, R35 |
| R40 | 4 | cit | Standards landscape and open problems: current limiting under large disturbances, fault current and protection, interoperability between grid-forming families, black start, model validation. | R33, R39 |

### 2.1 Graph checks

- **No cycle.** Every dependency carries a lower identifier than its node.
- **No forward edge.** Every cross-chapter dependency points backward: R23 to R07; R24 to R23; R26 to R04; R28 to R04; R33 to R06; R34 to R03 and R05.
- **Orphans.** Terminal nodes are R08, R10, R11, R20, R21, R22, R27, R30, R37, R38, R39, R40. Each is a worked case, a cited fact, or a closing survey. Each is named in an outcome or in the closing section of its chapter.
- **Outcome coverage.** Outcome 1: R04, R06, R07, R09. Outcome 2: R17, R18, R19. Outcome 3: R26, R29, R32, R33. Outcome 4: R34, R35, R36, R39.
- **Model omissions repaid.** R05 omits flux and excitation dynamics; repaid by R11 and by the scope note of Chapter 4. R17 omits current-loop dynamics; repaid by R22. R34 omits network electromagnetic transients; repaid by R40.

---

## 3. Book-wide notation table

One symbol has one meaning in the whole book. Search this table before you introduce a symbol. Scope `book` means the symbol keeps its meaning everywhere. Scope `ch N` means the symbol is local to chapter N and is redefined at first use there.

Bold upright capitals denote matrices. The damping coefficient of the swing equation is written `K_D`, never `D`, because `D` is reserved for the state-space feedthrough matrix and `D_load` for load damping. This is a deliberate departure from some textbooks; it is recorded here and stated in Chapter 1.

### 3.1 Base quantities and per unit

| Symbol | Meaning | Unit | Defined | Scope |
|---|---|---|---|---|
| S_base | three-phase base apparent power of a unit or system | VA (MVA) | Ch 1, §1.2 | book |
| V_base | line-to-line base voltage | V (kV) | Ch 1, §1.2 | book |
| I_base | base current, S_base / (sqrt(3) V_base) | A | Ch 1, §1.2 | book |
| Z_base | base impedance, V_base^2 / S_base | ohm | Ch 1, §1.2 | book |
| f_0 | rated system frequency, 50 or 60 Hz; each example states which | Hz | Ch 1, §1.2 | book |
| omega_0 | rated electrical angular frequency, 2 pi f_0 | rad/s | Ch 1, §1.2 | book |
| omega_base | base angular frequency; equal to omega_0 | rad/s | Ch 1, §1.2 | book |
| pu | per-unit value: quantity divided by its base | dimensionless | Ch 1, §1.2 | book |

### 3.2 Machine and swing dynamics (Chapter 1)

| Symbol | Meaning | Unit | Defined | Scope |
|---|---|---|---|---|
| delta | rotor angle against the synchronous reference frame | rad (printed in degrees where noted) | Ch 1, §1.3 | book |
| delta_0 | equilibrium value of delta | rad | Ch 1, §1.4 | book |
| delta_cr | critical clearing angle | rad | Ch 1, §1.6 | ch 1 |
| delta_max | largest angle with a decelerating area available after the fault | rad | Ch 1, §1.6 | ch 1 |
| omega | electrical angular frequency of the unit | rad/s | Ch 1, §1.3 | book |
| omega_m | mechanical angular speed of the rotor | rad/s | Ch 1, §1.3 | ch 1 |
| dw | per-unit speed deviation, (omega - omega_0) / omega_0 | dimensionless | Ch 1, §1.3 | book |
| J | rotor moment of inertia | kg m^2 | Ch 1, §1.3 | ch 1 |
| H | inertia constant, stored kinetic energy at rated speed divided by S_base | s | Ch 1, §1.3 | book |
| E_kin | kinetic energy stored by a unit, H * S_base | J (MJ) | Ch 1, §1.3 | book |
| K_D | damping coefficient in the per-unit swing equation, torque per unit speed deviation | pu | Ch 1, §1.3 | book |
| P_m | mechanical power input | pu | Ch 1, §1.3 | book |
| P_e | electrical power output | pu | Ch 1, §1.3 | book |
| T_m, T_e | mechanical and electrical torque | pu | Ch 1, §1.3 | ch 1 |
| E' | constant emf magnitude behind transient reactance | pu | Ch 1, §1.4 | book |
| X_d' | direct-axis transient reactance | pu | Ch 1, §1.4 | book |
| X_t | transformer reactance | pu | Ch 1, §1.4 | ch 1 |
| X_L | reactance of one transmission line | pu | Ch 1, §1.4 | ch 1 |
| X | total reactance between E' and the infinite bus | pu | Ch 1, §1.4 | book |
| V_inf | infinite-bus voltage magnitude | pu | Ch 1, §1.4 | ch 1 |
| K_s | synchronizing torque coefficient, dP_e/d(delta) at delta_0 | pu/rad | Ch 1, §1.5 | book |
| omega_n | undamped natural frequency of the linearised swing mode | rad/s | Ch 1, §1.5 | book |
| zeta | damping ratio of the linearised swing mode | dimensionless | Ch 1, §1.5 | book |
| t_cr | critical clearing time | s | Ch 1, §1.6 | ch 1 |
| A_acc, A_dec | accelerating and decelerating areas in the P-delta plane | pu rad | Ch 1, §1.6 | ch 1 |

### 3.3 Converter, dq frame and grid-following control (Chapter 2)

| Symbol | Meaning | Unit | Defined | Scope |
|---|---|---|---|---|
| a, b, c | three phase quantities in the stationary natural frame | pu | Ch 2, §2.1 | book |
| alpha, beta | stationary two-axis quantities after the Clarke transform | pu | Ch 2, §2.1 | book |
| T_C | Clarke transform matrix, amplitude-invariant, factor 2/3 | dimensionless | Ch 2, §2.1 | book |
| T_P(theta) | Park transform matrix, rotation by theta | dimensionless | Ch 2, §2.1 | book |
| d, q | direct and quadrature axes of the rotating frame; d on the measured voltage | — | Ch 2, §2.1 | book |
| v_d, v_q | converter terminal voltage components in the dq frame | pu | Ch 2, §2.1 | book |
| i_d, i_q | converter current components in the dq frame | pu | Ch 2, §2.1 | book |
| i_d_ref, i_q_ref | current references from the outer loop | pu | Ch 2, §2.3 | book |
| m_d, m_q | modulation index components | dimensionless | Ch 2, §2.2 | ch 2 |
| v_dc | DC-link voltage | V | Ch 2, §2.2 | book |
| v_dc0 | DC-link voltage at the operating point | V | Ch 2, §2.2 | book |
| C_dc | DC-link capacitance | F | Ch 2, §2.2 | book |
| L_f, R_f | converter filter inductance and resistance | H, ohm (also pu) | Ch 2, §2.2 | book |
| alpha_c | closed-loop bandwidth of the inner current control | rad/s | Ch 2, §2.3 | book |
| theta_pll | angle estimated by the phase-locked loop | rad | Ch 2, §2.4 | book |
| omega_pll | frequency estimated by the phase-locked loop | rad/s | Ch 2, §2.4 | book |
| k_p_pll, k_i_pll | proportional and integral gains of the phase-locked loop | 1/s, 1/s^2 | Ch 2, §2.4 | book |
| K_pll | small-signal gain from angle error to v_q, equal to V_g cos(theta_0) | pu | Ch 2, §2.5 | book |
| omega_n_pll | natural frequency of the linearised phase-locked loop | rad/s | Ch 2, §2.5 | book |
| zeta_pll | damping ratio of the linearised phase-locked loop | dimensionless | Ch 2, §2.5 | book |
| V_g | grid (Thevenin source) voltage magnitude | pu | Ch 2, §2.5 | book |
| X_g, R_g | grid Thevenin reactance and resistance on the converter base | pu | Ch 2, §2.5 | book |
| Z_g | grid Thevenin impedance magnitude | pu | Ch 2, §2.5 | book |
| S_sc | short-circuit apparent power at the point of connection | VA (MVA) | Ch 2, §2.5 | book |
| S_rated | rated apparent power of the converter | VA (MVA) | Ch 2, §2.5 | book |
| SCR | short-circuit ratio, S_sc / S_rated | dimensionless | Ch 2, §2.5 | book |
| theta_0 | steady-state angle of the point-of-connection voltage against the grid source | rad | Ch 2, §2.5 | book |
| P, Q | active and reactive power at the point of connection | pu | Ch 2, §2.3 | book |
| I_max | converter current limit, set by the semiconductor rating | pu | Ch 2, §2.3 | book |

### 3.4 Grid-forming control (Chapter 3)

| Symbol | Meaning | Unit | Defined | Scope |
|---|---|---|---|---|
| theta | internal angle state of a grid-forming converter | rad | Ch 3, §3.1 | book |
| E | internal voltage magnitude commanded by a grid-forming converter | pu | Ch 3, §3.1 | book |
| m_p | active-power droop gain, frequency change per unit power change | pu | Ch 3, §3.2 | book |
| n_q | reactive-power droop gain, voltage change per unit reactive power change | pu | Ch 3, §3.2 | book |
| omega_c | cutoff of the first-order power measurement filter | rad/s | Ch 3, §3.2 | book |
| omega_ref, V_ref | frequency and voltage set points | pu | Ch 3, §3.2 | book |
| P_ref, Q_ref | active and reactive power set points | pu | Ch 3, §3.2 | book |
| H_v | virtual inertia constant chosen in a virtual synchronous machine | s | Ch 3, §3.3 | book |
| K_D_v | virtual damping coefficient chosen in a virtual synchronous machine | pu | Ch 3, §3.3 | book |
| k_theta | matching-control gain from DC voltage to angular frequency | rad/(s V) | Ch 3, §3.4 | book |
| H_eq | inertia constant that a control law is equivalent to | s | Ch 3, §3.2 | book |
| K_D_eq | damping coefficient that a control law is equivalent to | pu | Ch 3, §3.2 | book |
| eta | dispatchable-virtual-oscillator gain | 1/s | Ch 3, §3.5 | ch 3 |
| kappa | dispatchable-virtual-oscillator rotation angle | rad | Ch 3, §3.5 | ch 3 |
| E_res | usable DC-side energy reserve of a converter | J (MJ) | Ch 3, §3.6 | book |

### 3.5 System level and small-signal analysis (Chapter 4)

| Symbol | Meaning | Unit | Defined | Scope |
|---|---|---|---|---|
| **Y** | bus admittance matrix | pu | Ch 4, §4.1 | book |
| **Y**_red | Kron-reduced admittance matrix at the internal nodes | pu | Ch 4, §4.1 | book |
| B_ij | susceptance of the reduced branch between nodes i and j | pu | Ch 4, §4.1 | book |
| delta_COI | centre-of-inertia angle, inertia-weighted mean of the unit angles | rad | Ch 4, §4.2 | book |
| omega_COI | centre-of-inertia frequency | rad/s | Ch 4, §4.2 | book |
| H_i, S_i | inertia constant and rating of unit i | s, VA | Ch 4, §4.2 | book |
| E_kin_sys | system stored kinetic energy, sum of H_i S_i over all units | J (GVA.s = GJ) | Ch 4, §4.2 | book |
| H_sys | system inertia constant on the system base, E_kin_sys / S_sys | s | Ch 4, §4.2 | book |
| S_sys | system base apparent power | VA (GVA) | Ch 4, §4.2 | book |
| dP | step loss of infeed | W (MW) | Ch 4, §4.3 | book |
| RoCoF | rate of change of frequency, df/dt | Hz/s | Ch 4, §4.3 | book |
| RoCoF_0 | initial rate of change of frequency, at the instant of the loss | Hz/s | Ch 4, §4.3 | book |
| f_nadir | lowest frequency reached after the loss | Hz | Ch 4, §4.4 | book |
| df_nadir | frequency deviation at the nadir, f_nadir - f_0 | Hz | Ch 4, §4.4 | book |
| T | time over which primary response is fully delivered | s | Ch 4, §4.4 | book |
| R_p | volume of primary response | W (MW) | Ch 4, §4.4 | book |
| D_load | load damping, change in demand per hertz of frequency deviation | MW/Hz | Ch 4, §4.4 | book |
| **x** | small-signal state vector | mixed | Ch 4, §4.2 | book |
| **u** | small-signal input vector | mixed | Ch 4, §4.2 | book |
| **y** | small-signal output vector | mixed | Ch 4, §4.2 | book |
| **A** | state matrix, d**x**/dt = **A x** + **B u** | 1/s | Ch 4, §4.2 | book |
| **B** | input matrix | mixed | Ch 4, §4.2 | book |
| **C** | output matrix | mixed | Ch 4, §4.2 | book |
| **D** | feedthrough matrix, **y** = **C x** + **D u** | mixed | Ch 4, §4.2 | book |
| lambda_i | eigenvalue i of **A**, lambda_i = sigma_i + j omega_d_i | 1/s | Ch 4, §4.2 | book |
| sigma_i | real part of lambda_i | 1/s | Ch 4, §4.2 | book |
| omega_d_i | damped angular frequency, imaginary part of lambda_i | rad/s | Ch 4, §4.2 | book |
| zeta_i | damping ratio of mode i, -sigma_i / sqrt(sigma_i^2 + omega_d_i^2) | dimensionless | Ch 4, §4.2 | book |
| p_ki | participation factor of state k in mode i | dimensionless | Ch 4, §4.2 | book |

### 3.6 Notation decisions recorded

1. `K_D` for swing damping, not `D`. `D` is the feedthrough matrix; `D_load` is load damping. Virtual and equivalent damping are `K_D_v` and `K_D_eq`, never `D_v` or `D_eq`. Stated in Chapter 1, §1.3.
2. Swing-equation convention: `2H d(dw)/dt = P_m - P_e - K_D dw` with `dw` in per unit, and `d(delta)/dt = omega_0 dw`. The alternative form, with damping acting on a speed deviation in rad/s and with `M = 2H/omega_0`, is named in Chapter 1, §1.3 and then not used. Mixing the two changes the numerical value of zeta by a factor of omega_0 and is the most common error in this material.
3. Park transform: amplitude-invariant, factor 2/3, d axis aligned with the measured voltage vector, so `v_q = 0` when the phase-locked loop is locked. In per unit, `P = v_d i_d + v_q i_q` with no factor 3/2. The factor 3/2 appears only in SI units. Stated in Chapter 2, §2.1.
4. `H` is a machine property. `H_v` is a chosen control parameter. `H_eq` is a property derived from a control law. The three are never interchanged.

---

## 4. Chapter specifications

Numbering of results inside a chapter follows the chapter-local scheme of §5.1. The global `R` identifiers of §2 are used only in plans, prerequisites, and acceptance checks; the chapter HTML carries the local numbers and states the `R` identifier in a data attribute so that later chapters can link to it.

### Chapter 1 — The classical picture: machines that swing

**Central result.** R07: the small-signal single-machine infinite-bus system has natural frequency `omega_n = sqrt(K_s omega_0 / (2H))` and damping ratio `zeta = K_D / (4 H omega_n)`, and the equilibrium is asymptotically stable exactly when `K_s > 0` and `K_D > 0`. Everything the rest of the book does is measured against these two numbers.

**Prerequisites.** None from earlier chapters. From the reader: linear time-invariant systems, eigenvalues, phasors.

**Sections.**

1. **1.1 The problem: why frequency is a shared variable.** Show that in an alternating-current grid every synchronous unit must run at the same average electrical frequency, so a power imbalance anywhere moves the speed of every rotor.
2. **1.2 Per unit and base quantities.** Define S_base, V_base, I_base, Z_base, omega_base, and show on a two-winding transformer why per unit removes the turns ratio from the equations (R01).
3. **1.3 The swing equation.** Derive `2H d(dw)/dt = P_m - P_e - K_D dw` from `J d(omega_m)/dt = T_m - T_e`, define H and show its unit is the second, and state the notation decision of §3.6 item 2 (R02, R03, R04).
4. **1.4 The classical machine against an infinite bus.** Introduce the constant-emf-behind-reactance model, derive `P_e = (E' V / X) sin(delta)`, and list what the model omits: flux decay, excitation control, saliency, stator resistance (R05).
5. **1.5 Small-signal stability of one machine.** Linearise, define `K_s`, derive the second-order characteristic polynomial, and compute the eigenvalues; interpret `K_s` as a spring constant and `K_D` as a dashpot (R06, R07, R08).
6. **1.6 Large-signal stability: the equal-area criterion.** Integrate the undamped swing equation once, derive the equal-area condition, and compute a critical clearing time; close with the stability classification and the fact that no term in this chapter survives if the rotor is removed (R09, R10, R11).

**Worked examples (concrete numbers to use).**

*Example 1.1 (R08) — small-signal.* A 60 Hz machine. `H = 3.5 s`, `K_D = 2 pu`, `E' = 1.1 pu`, `V_inf = 1.0 pu`, `P_m = 0.8 pu`. Network: `X_d' + X_t = 0.45 pu` and two parallel lines of `X_L = 0.40 pu` each, so `X = 0.45 + 0.20 = 0.65 pu`. Compute, in this order: `delta_0 = arcsin(P_m X / (E' V)) = arcsin(0.4727) = 28.2 deg = 0.4926 rad`; `K_s = (E' V / X) cos(delta_0) = 1.6923 * 0.8814 = 1.4915 pu/rad`; `omega_n = sqrt(K_s omega_0 / (2H)) = sqrt(1.4915 * 376.99 / 7) = 8.963 rad/s = 1.427 Hz`; `zeta = K_D / (4 H omega_n) = 2 / (4 * 3.5 * 8.963) = 0.01594`; eigenvalues `lambda = -0.1429 +/- j 8.962 1/s`. State that 1.43 Hz sits in the 0.7 Hz to 2 Hz band reported for local plant modes [S01, verify section] and that `zeta = 0.016` is why power system stabilisers exist.

*Example 1.2 (R10) — equal area.* Same machine and network. A three-phase fault at the sending-end bus of line 2 makes `P_e = 0` during the fault; the fault is cleared by tripping line 2, so `X_post = 0.45 + 0.40 = 0.85 pu`. Assume no damping during the swing. Compute: `P_max_pre = 1.6923 pu`, `P_max_post = 1.1/0.85 = 1.2941 pu`; `delta_max = pi - arcsin(P_m / P_max_post) = pi - 0.6666 = 2.4750 rad`; `cos(delta_cr) = [P_m (delta_max - delta_0) + P_max_post cos(delta_max)] / P_max_post = [1.5859 - 1.0164] / 1.2941 = 0.4401`, so `delta_cr = 63.9 deg = 1.1153 rad`; `t_cr = sqrt(4 H (delta_cr - delta_0) / (omega_0 P_m)) = sqrt(14 * 0.6227 / 301.6) = 0.170 s`, that is 10.2 cycles at 60 Hz. State that typical transmission protection clears a fault in 4 to 6 cycles, so this machine has margin.

**Figures.**

- **Fig. 1.1** Power-angle curve `P_e` against `delta` for the pre-fault, fault-on, and post-fault networks of Example 1.2, with `P_m = 0.8` drawn as a horizontal line and the three intersection angles marked. Must show that `P_max` falls when a line is lost.
- **Fig. 1.2** The same curve with the accelerating area and the decelerating area shaded and labelled, and `delta_0`, `delta_cr`, `delta_max` marked on the axis. Must show that equality of areas is what defines `delta_cr`.
- **Fig. 1.3** Time response of `delta(t)` from a numerical integration of the swing equation for clearing at 0.15 s (stable) and 0.19 s (unstable), on one axis. Must show that the boundary lies between them, near the computed 0.170 s.
- **Fig. 1.4** Eigenvalue plot in the complex plane for Example 1.1 with `K_D` swept over 0, 2, 10, 30 pu. Must show the pair moving left along a circle of radius `omega_n` while `omega_n` stays fixed.

**Exercises.**

1. *(Conceptual)* A machine has `delta_0 = 95 deg`. State whether it is small-signal stable and name the term that decides. **Target:** not stable; `K_s = (E'V/X) cos(95 deg) < 0`, so one eigenvalue is real and positive.
2. *(Derivational)* Derive `H` for a rotor of `J = 5000 kg m^2` on a 4-pole machine at 60 Hz rated `200 MVA`. **Target:** `omega_m = 2 pi 60 / 2 = 188.5 rad/s`; `E_kin = 0.5 J omega_m^2 = 88.8 MJ`; `H = 0.444 s`. Comment: this rotor alone is far below the 2 s to 8 s range, so the turbine mass dominates a real turbo-set.
3. *(Derivational)* Show that writing the damping term as `K_D' * (omega - omega_0)` with `omega` in rad/s, while keeping `2H d(dw)/dt` on the left, multiplies the computed `zeta` by `omega_0`. **Target:** `zeta` would be `376.99 * 0.01594 = 6.01` for Example 1.1, that is overdamped, which is why §3.6 item 2 fixes one convention.
4. *(Computational)* Integrate the swing equation of Example 1.2 and find the clearing time at which the machine first fails to return, to a resolution of 1 ms. **Target:** between 0.169 s and 0.171 s; the equal-area value 0.170 s is recovered because damping is neglected in both.
5. *(Computational)* Repeat Example 1.1 for `H` over 2, 3.5, 6, 8 s and plot `omega_n` and `zeta`. **Target:** `omega_n` = 11.86, 8.96, 6.84, 5.93 rad/s and `zeta` = 0.0211, 0.0159, 0.0122, 0.0105. Both scale as `H^-0.5`: `omega_n ~ H^-0.5` by its definition, and `zeta = K_D / (4 H omega_n) ~ H^-1 H^0.5 = H^-0.5`. Verify the exponent numerically before printing it.

**Definitions introduced.** Per unit and base quantities; rotor angle; per-unit speed deviation; inertia constant H; stored kinetic energy; damping coefficient K_D; swing equation; classical machine model; infinite bus; synchronizing torque coefficient; natural frequency and damping ratio of the swing mode; critical clearing angle and critical clearing time; the three classes of power-system stability.

**Length target.** 6500 words, plus 4 figures and 5 exercises. About 16 book pages, 3 lecture hours.

**Acceptance checks (editor).**

- Every symbol in §3.2 that appears in the chapter is defined in the prose before its first use, not only in the table.
- The swing-equation convention of §3.6 item 2 is stated in §1.3, and the alternative is named and excluded.
- Every number in Examples 1.1 and 1.2 is reproduced by the chapter's own arithmetic to the printed number of digits. Any typical-value claim (H of 2 s to 8 s, local mode 0.7 Hz to 2 Hz, 4 to 6 cycle clearing) carries a source identifier from §5.2 and a `verify` mark if unverified.
- Every claim is tied to a local result number, and every local result number is mapped to its `R` identifier.
- Figures 1.1 to 1.4 each use the numbers of Example 1.1 or 1.2, not invented ones.

---

### Chapter 2 — Inverter-based resources and the limit of following

**Central result.** R18 with R19: for a grid-following converter modelled as a current source behind `j X_g` at unity power factor, the loop equation is `v_q = X_g I_d - V_g sin(theta_p)`. A steady state therefore exists exactly when `X_g I_d <= V_g`, that is `I_d <= SCR * V_g` in per unit. This is a bound on current, not on power: delivered power is `P = (V_g^2 / (2 X_g)) sin(2 theta_0)`, which peaks at `SCR * V_g^2 / 2` at `theta_0 = 45 deg` and then falls back to zero at the current bound. At the operating point the terminal voltage magnitude and the phase-locked loop's small-signal gain are the same quantity, `K_pll = V_g cos(theta_0)`, and it goes to zero at that bound, taking the loop's bandwidth and damping ratio with it. This is the exact structural twin of `K_s = (E'V/X) cos(delta_0)` from Chapter 1, and the book's spine runs through that parallel.

**Prerequisites.** R01 (per unit), R06 (synchronizing coefficient, for the parallel), R07 (what stability looked like with a rotor).

**Sections.**

1. **2.1 The dq frame and the Park transform.** Define the Clarke and Park transforms in amplitude-invariant form, fix the convention that the d axis lies on the measured voltage, and show that a balanced sinusoidal set becomes two constants (R12).
2. **2.2 The averaged converter model.** Write the L-filter converter in dq with the `omega L` cross-coupling, and state the averaging assumption and the switching frequency below which it fails (R13).
3. **2.3 Inner current control.** Design the proportional-integral current controller with decoupling, derive the first-order closed loop of bandwidth `alpha_c`, and state the current limit `I_max` and why it exists (R14).
4. **2.4 The phase-locked loop.** Define the synchronous-reference-frame phase-locked loop, write its two states, and show that with a stiff grid the loop is a clean second-order system in the angle error (R15).
5. **2.5 Grid strength and the existence bound.** Define `SCR` and `X_g = 1/SCR`; build the current-source model; derive `v_q = X_g I_d - V_g sin(theta_p)`, the current existence bound, the power curve `P = (V_g^2/(2 X_g)) sin(2 theta_0)`, and `K_pll = V_g cos(theta_0)`; list what the model omits, reactive support first (R16, R17, R18).
6. **2.6 Why following fails on a weak grid.** Substitute `K_pll` into the linearised loop, derive `omega_n_pll` and `zeta_pll`, run the two worked examples, then state the cited result that the true instability arrives below the static bound, and close with the corollary that this fleet supplies neither `K_s` nor `H` (R19, R20, R21, R22, R23).

**Worked examples.**

*Example 2.1 (R20) — one weak-grid operating point.* `SCR = 1.2`, so `X_g = 1/1.2 = 0.8333 pu`. `V_g = 1.0 pu`, unity power factor, `I_d = 1.0 pu`, `I_q = 0`. Compute: `sin(theta_0) = X_g I_d / V_g = 0.8333`, so `theta_0 = 56.44 deg`; terminal voltage `v_d = V_g cos(theta_0) = 0.5528 pu`; delivered power `P = v_d I_d = 0.5528 pu`, against this model's maximum `P_max = SCR V_g^2 / 2 = 0.600 pu` at `theta_0 = 45 deg`; and `K_pll = V_g cos(theta_0) = 0.5528 pu`, which is the same number as the terminal voltage. Now take a phase-locked loop tuned on a stiff grid (`K_pll = 1`) for `omega_n_pll = 2 pi 10 = 62.83 rad/s` and `zeta_pll = 0.707`, which gives `k_i_pll = omega_n_pll^2 = 3948 1/s^2` and `k_p_pll = 2 zeta omega_n = 88.86 1/s`. At `K_pll = 0.5528` the same gains give `omega_n_pll = sqrt(0.5528 * 3948) = 46.72 rad/s = 7.44 Hz` and `zeta_pll = 0.5528 * 88.86 / (2 * 46.72) = 0.526`. State the conclusion in words: the designer changed nothing, and the grid moved the loop.

*Example 2.2 (R21) — the sweep.* For `V_g = 1.0 pu` and `I_d = 1.0 pu`, tabulate `SCR` over 10, 3, 2, 1.2, 1.05: `X_g` = 0.100, 0.3333, 0.500, 0.8333, 0.9524; `theta_0` = 5.74, 19.47, 30.00, 56.44, 72.25 deg; `K_pll` = 0.9950, 0.9428, 0.8660, 0.5528, 0.3047; `omega_n_pll` = 62.67, 61.01, 58.48, 46.72, 34.69 rad/s; `zeta_pll` = 0.7053, 0.6865, 0.6580, 0.5257, 0.3903. Add two power columns: delivered power at `I_d = 1 pu`, `P = V_g cos(theta_0) I_d` = 0.9950, 0.9428, 0.8660, 0.5528, 0.3047 pu, equal to `K_pll` because the terminal voltage and the loop gain are the same quantity; and `P_max = SCR V_g^2 / 2` = 5.000, 1.500, 1.000, 0.600, 0.525 pu. Point out that between `SCR = 10` and `SCR = 2` the damping ratio falls by 7 %, and between `SCR = 2` and `SCR = 1.05` it falls by 41 %. Recompute every row before printing.

**Figures.**

- **Fig. 2.1** Three balanced phase voltages against time, beside the same signal in the dq frame, showing the two constants after lock. Must show that a phase-locked loop turns a rotating problem into a stationary one.
- **Fig. 2.2** Phasor diagram at the point of connection: `V_g`, `j X_g I`, the resulting terminal voltage, and `theta_0`. Drawn for `SCR = 10` and `SCR = 1.2` side by side. Must show that the whole angle comes from the converter's own current when the grid is weak.
- **Fig. 2.3** `K_pll` (equal both to the terminal voltage and to `P` at `I_d = 1 pu`) and `P_max = SCR V_g^2 / 2` against `SCR` over 1 to 10, with the Example 2.1 point marked. Must show that `K_pll` collapses only near the bound, and that `P_max` is the binding constraint at low `SCR`.
- **Fig. 2.4** Root locus of the linearised phase-locked loop as `K_pll` falls from 1 to 0.1 with fixed gains, with constant-`zeta` lines drawn. Must show the pair sliding toward the origin, not into the right half-plane, so that the static bound alone does not explain the observed instability. This is the figure that motivates the cited result R22.

**Exercises.**

1. *(Conceptual)* A converter rated 200 MVA is connected where the short-circuit level is 300 MVA. State the short-circuit ratio and whether the plant can export its full rating at unity power factor under the model of §2.5. **Target:** `SCR = 1.5`, so `X_g = 0.6667 pu`. At `I_d = 1 pu`: `theta_0 = arcsin(0.6667) = 41.81 deg`, terminal voltage and `K_pll` both 0.7454 pu, and `P = 0.7454 pu`. This model's maximum is `P_max = SCR V_g^2 / 2 = 0.750 pu`, so the answer is no: the plant cannot export 1.0 pu without reactive support that holds the terminal voltage up. The cited result R22 warns that the true limit is lower still.
2. *(Derivational)* Derive `P = v_d i_d + v_q i_q` in per unit from the three-phase instantaneous power with the amplitude-invariant Park transform, and show where the factor 3/2 goes. **Target:** in SI, `p = 1.5 (v_d i_d + v_q i_q)`; the factor is absorbed by the per-unit bases.
3. *(Derivational)* Show that `K_pll` equals `dv_q/d(theta_error)` at the operating point, and explain why this makes grid strength enter the loop through exactly one scalar. **Target:** linearise `v_q` about the locked point; all other terms vanish at `v_q = 0`.
4. *(Computational)* Sweep `SCR` from 1.01 to 10 and find the `SCR` at which `zeta_pll` first falls below 0.3, for the gains of Example 2.1. **Target:** `zeta_pll = 0.7071 sqrt(K_pll)`, so `zeta_pll = 0.300` at `K_pll = 0.180`, `theta_0 = 79.6 deg` and `SCR = 1.017`; report the value the sweep returns, not this one, and state the resolution used.
5. *(Computational)* Retune `k_p_pll` and `k_i_pll` so that Example 2.1 recovers `zeta_pll = 0.707` at `SCR = 1.2`, then report what those gains do at `SCR = 10`. **Target:** divide both by `K_pll = 0.5528`, giving `k_p = 160.7` and `k_i = 7142`; at `SCR = 10` the loop then runs at `omega_n_pll = 84.3 rad/s` and `zeta = 0.948`, that is a loop far faster than designed, which is the trade the chapter is naming.
6. *(Conceptual)* State, in terms of R06 and R18, one sentence on why adding more grid-following plant does not raise `SCR` for the plant already there. **Target:** `SCR` is set by the Thevenin impedance of the sources behind the point of connection; a current source contributes no Thevenin voltage source, so it adds no short-circuit power.

**Definitions introduced.** Clarke transform; Park transform; dq frame; averaged converter model; modulation index; inner current control and its bandwidth; current limit; synchronous-reference-frame phase-locked loop; grid-following control; short-circuit ratio and grid strength classes; the phase-locked-loop small-signal gain `K_pll`.

**Length target.** 7500 words, plus 4 figures and 6 exercises. About 19 book pages, 4 lecture hours.

**Acceptance checks (editor).**

- The Park convention of §3.6 item 3 is stated in §2.1 before any dq quantity appears.
- The current-source model of §2.5 lists its omissions explicitly. It states that the bound of R18 is on current and that delivered power peaks at `SCR V_g^2 / 2`, and it records that a plant holding its terminal voltage at 1 pu with reactive support reaches the higher figure `P_max = SCR V_g |v|` quoted in the literature, cited [S07, S08 - verify]. Section 2.6 names R22 as the repayment of the omitted current-loop dynamics. No prose claims that the static bound explains an observed oscillation.
- Every number in Examples 2.1 and 2.2 is recomputed in the chapter. The SCR class boundaries carry a source identifier and a `verify` mark.
- The parallel between `K_s = (E'V/X) cos(delta_0)` and `K_pll = V_g cos(theta_0)` is stated explicitly and tied to result numbers R06 and R18.
- Every claim is tied to a local result number.

---

### Chapter 3 — Grid-forming control: what it restores

**Central result.** R32 with R33: droop with a measurement filter, a virtual synchronous machine, matching control, and dispatchable virtual oscillator control all reduce, to first order about a symmetric operating point, to the same angle model `d(theta)/dt = omega` driven by a transfer function from power imbalance to frequency; each family fixes a pair `(H_eq, K_D_eq)`; and each therefore restores a synchronizing torque coefficient `K_s = (E V / X) cos(delta_0)` of the same form as Chapter 1, with inertia bounded by the DC energy reserve and by `I_max`.

**Prerequisites.** R04 (swing equation), R06 (synchronizing coefficient), R23 (what grid-following does not supply), R12 to R14 (dq frame, converter model, current control).

**Sections.**

1. **3.1 The terminal definition.** Define grid-forming control by what the converter looks like from outside: a voltage source `E` behind an impedance, with `theta` an internal state. Contrast with R17 term by term, and warn that "grid-forming" is not defined by the inner control structure (R24).
2. **3.2 Droop control, and why it is a swing equation.** Write P-f and Q-V droop with the measurement filter, then prove `H_eq = 1/(2 m_p omega_c)` and `K_D_eq = 1/m_p` by matching coefficients with R04 (R25, R26, R27).
3. **3.3 The virtual synchronous machine.** Integrate the swing equation explicitly with chosen `H_v` and `K_D_v`; show what the free choice buys (an inertia number a system operator can contract for) and what it costs (the choice of `H_v` and the energy to back it are now separate decisions) (R28).
4. **3.4 Matching control.** Set `d(theta)/dt = k_theta v_dc` and show that the DC-link capacitor then plays the rotor's role exactly, giving `H_eq = 0.5 C_dc v_dc0^2 / S_base`; compute how small that is (R29, R30).
5. **3.5 Dispatchable virtual oscillator control.** Present the oscillator with amplitude regulation, state its almost-global synchronization property as a cited result with its hypotheses, and show that its small-signal reduction near the operating point matches droop (R31).
6. **3.6 One model, four families.** Put all four into `d(theta)/dt = omega`, tabulate `(H_eq, K_D_eq)`, and state what each family does that the others do not away from the operating point (R32).
7. **3.7 What is restored and what is not.** Recover `K_s` for a grid-forming converter, then bound the inertia response by the energy reserve `E_res` and by `I_max`, and state that these two bounds have no counterpart in Chapter 1 (R33).

**Worked examples.**

*Example 3.1 (R27) — droop is inertia you did not know you had.* `m_p = 0.05 pu` (5 % droop: full-range power change for a 5 % frequency change). Compute `H_eq = 1/(2 m_p omega_c)` and `K_D_eq = 1/m_p = 20 pu` for three filter cutoffs: `omega_c = 2 pi 5 = 31.42 rad/s` gives `H_eq = 0.3183 s`; `omega_c = 2 pi 1 = 6.283 rad/s` gives `H_eq = 1.592 s`; `omega_c = 2 rad/s = 0.3183 Hz` gives `H_eq = 5.000 s`. State the design consequence in one sentence: an inertia constant that matches a 3.5 s machine needs `omega_c = 2.857 rad/s`, that is a power measurement filter with a time constant of 0.35 s, which is slow enough to interact with the current loop of §2.3 and with protection.

*Example 3.2 (R30) — the capacitor is not a rotor.* `C_dc = 20 mF`, `v_dc0 = 1200 V`, `S_base = 1 MVA`. Compute stored energy `0.5 C_dc v_dc0^2 = 0.5 * 0.02 * 1.44e6 = 14.4 kJ`; `H_eq = 14400 / 1e6 = 0.0144 s`; ratio to a machine with `H = 3.5 s` is `3.5 / 0.0144 = 243`. Then compute the energy a real inertial response needs: for `H_v = 5 s` on `S = 100 MVA` and a frequency excursion `df = 0.8 Hz` at `f_0 = 50 Hz`, the released energy is `2 H_v S df / f_0 = 2 * 5 * 100e6 * 0.016 = 16 MJ = 4.44 kWh`. Compare: `16 MJ / 14.4 kJ = 1111`. Conclusion stated plainly: matching control gives the converter a rotor-like structure, not a rotor-like energy store; the energy must come from the DC source behind the capacitor.

**Figures.**

- **Fig. 3.1** Two block diagrams side by side: grid-following (measure angle, command current) and grid-forming (set angle, let current follow), with the same physical circuit drawn beneath both. Must show that the difference is which variable is the input.
- **Fig. 3.2** Block diagram of droop with the measurement filter, redrawn step by step into the swing-equation block diagram of Chapter 1, with `H_eq` and `K_D_eq` labelled at the end. Must show the equivalence as a picture, matching the proof of R26.
- **Fig. 3.3** `H_eq` against `omega_c` for `m_p` = 0.02, 0.05, 0.10 pu, on log axes, with the three points of Example 3.1 marked and a horizontal line at `H = 3.5 s`. Must show the trade between filter speed and equivalent inertia.
- **Fig. 3.4** Bar chart on a logarithmic axis of stored energy per MVA: synchronous machine at `H = 3.5 s`, the DC link of Example 3.2, and the energy demanded by Example 3.2's inertial response. Must show the 243 and 1111 factors.
- **Fig. 3.5** Frequency response from power imbalance to frequency for the four families with parameters chosen to give the same `H_eq`, showing where they differ (above `omega_c`, and in the amplitude channel). Must show that the families agree to first order and separate in bandwidth.

**Exercises.**

1. *(Conceptual)* State why a converter can be grid-forming and still be unable to supply an inertial response. **Target:** `theta` being an internal state fixes the control structure, not the energy store; R33 bounds the response by `E_res` and `I_max`.
2. *(Derivational)* Derive `H_eq = 1/(2 m_p omega_c)` from the filtered droop law by matching coefficients with R04, and state the assumption that makes the match exact. **Target:** define `dP = P_e - P_ref` once and use it in both lines. The filtered droop law gives `s dw = -omega_c dw - m_p omega_c dP`. The swing equation of R04 at constant `P_m` gives `s dw = -dP/(2H) - (K_D/(2H)) dw`. Matching coefficients: `m_p omega_c = 1/(2H)` and `omega_c = K_D/(2H)`. The match is exact when the filter is first order and the droop law is linear.
3. *(Derivational)* Show that a virtual synchronous machine with `H_v` and `K_D_v` has the same steady-state droop as a droop controller with `m_p = 1/K_D_v`. **Target:** set the derivative to zero in both laws.
4. *(Computational)* For Example 3.2's converter, compute the DC-link capacitance that would give `H_eq = 3.5 s` at `v_dc0 = 1200 V` and `S_base = 1 MVA`, then state its physical size in words. **Target:** `C_dc = 2 H_eq S_base / v_dc0^2 = 2 * 3.5 * 1e6 / 1.44e6 = 4.861 F`, that is 243 times the 20 mF of the example. Comment that capacitor banks of this size are not built for this purpose.
5. *(Computational)* Simulate the four families of §3.6 under a 0.1 pu power step with parameters tuned to a common `H_eq = 2 s`, and report the peak frequency deviation and settling time of each. **Target:** the four initial slopes agree to within the numerical tolerance of the run (state the tolerance); the peaks and settling times differ, and the difference is explained by the amplitude dynamics, not by the angle dynamics.
6. *(Conceptual)* A vendor states its product has "5 seconds of inertia". List the three further numbers you need before that claim means anything. **Target:** the rating it is referenced to; the usable energy reserve `E_res`; the current limit `I_max` and the headroom held below it.

**Definitions introduced.** Grid-forming control (terminal definition); active-power droop gain and reactive-power droop gain; power measurement filter cutoff; equivalent inertia constant and equivalent damping; virtual synchronous machine, virtual inertia constant and virtual damping; matching control and the matching gain; dispatchable virtual oscillator control, its gain and rotation angle; usable energy reserve; headroom.

**Length target.** 8000 words, plus 5 figures and 6 exercises. About 20 book pages, 4 lecture hours.

**Acceptance checks (editor).**

- The terminal definition of §3.1 is used consistently; no passage defines grid-forming by an inner control structure.
- R26 is proved by coefficient matching against the equation of R04 as it is written in §3.6 item 2, not against a different convention.
- Every one of the four families has its `(H_eq, K_D_eq)` entry in the §3.6 table, and each entry is either derived in the chapter or marked as cited with a source identifier.
- Every number in Examples 3.1 and 3.2 is recomputed in the chapter, including the ratios 243 and 1111.
- Claims about dispatchable virtual oscillator control's global behaviour carry the hypotheses of the cited theorem, and are labelled `cited`, not `proved here`.

---

### Chapter 4 — System-level stability and a sizing case

**Central result.** R36 applied through Example 4.2 (R39): for a mixed machine-and-converter grid, `RoCoF_0 = f_0 dP / (2 E_kin_sys)` and, under a linear primary-response ramp delivered over `T` with no load damping, `df_nadir = - f_0 dP T / (4 E_kin_sys)`; so replacing a synchronous condenser fleet with grid-forming converters is three separate sizing problems (energy, power headroom, current limit), and the binding one is power headroom, not energy.

**Prerequisites.** R03 (H), R04 (swing equation), R05 (network power flow), R32 and R33 (the unified grid-forming model and its bounds).

**Sections.**

1. **4.1 From one machine to a network.** Build the bus admittance matrix, perform Kron reduction to the internal nodes, and show that the multi-machine swing equations couple through `B_ij` terms (R34, part 1).
2. **4.2 The mixed grid in state-space form.** Assemble machines and grid-forming converters into `d**x**/dt = **A x** + **B u**`, define the centre of inertia and `E_kin_sys`, and read stability from the eigenvalues, damping ratios, and participation factors (R34, part 2).
3. **4.3 Rate of change of frequency.** Derive `RoCoF_0` from the aggregated swing equation, and state the two distinct roles the number plays: a protection setting and a measure of system strength (R35).
4. **4.4 The frequency nadir.** Derive `df_nadir` under the linear-ramp response model, state the assumptions that make it a lower bound in practice, and add load damping as a named extension (R36, R37).
5. **4.5 A sizing case: replacing a 1.6 GVA synchronous condenser fleet.** Work the three constraints separately and identify the binding one; compare with the Great Britain event of 9 August 2019 as a reality check on the model (R38, R39).
6. **4.6 What remains open.** Current limiting under large disturbances; fault current and protection with converter-dominated sources; interoperability between grid-forming families; black start; model validation and the gap between manufacturer models and measured plant. Each stated as a question with a source, not as a prediction (R40).

**Worked examples.**

*Example 4.1 (R37) — the textbook nadir.* A 50 Hz system. `E_kin_sys = 200 GVA.s` (mark `verify`; state the source and the year). Loss of infeed `dP = 1000 MW`. Primary response `R_p = 1000 MW` delivered as a linear ramp over `T = 10 s`. No load damping. Compute: `RoCoF_0 = f_0 dP / (2 E_kin_sys) = 50 * 1000 / (2 * 200000) = 0.125 Hz/s`; nadir at `t = T` with `df_nadir = - f_0 dP T / (4 E_kin_sys) = - 50 * 1000 * 10 / (4 * 200000) = -0.625 Hz`, so `f_nadir = 49.375 Hz`. Then repeat at half the inertia, `E_kin_sys = 100 GVA.s`: `RoCoF_0 = 0.25 Hz/s` and `f_nadir = 48.75 Hz`, which is below the 48.8 Hz at which Great Britain's low-frequency demand disconnection acted in 2019 [S14]. State the sensitivity plainly: nadir depth scales as `1/E_kin_sys`, so halving inertia doubles the deviation.

*Example 4.2 (R39) — sizing the replacement.* Define the fleet: this is a design case set by the project, not a published fleet. Take 8 synchronous condensers of 200 MVA each, so 1.6 GVA in total (the project brief labels it 1.6 GW; a condenser is rated in MVA, and the chapter says so), each with `H = 3.5 s` including its flywheel (mark `verify`; cite a manufacturer or standard figure or state it as an assumption). Then `E_kin_sys = 8 * 200 * 3.5 = 5600 MVA.s = 5.6 GVA.s`. Now size a grid-forming fleet against three constraints, separately.
  - **Energy.** Over a frequency excursion `df = 0.8 Hz` at `f_0 = 50 Hz`, the machines release `2 E_kin df / f_0 = 2 * 5600e6 * 0.016 = 179.2 MJ = 49.8 kWh`. A 1.12 GVA battery fleet with a 1 hour store holds 1.12 GWh, that is 22 500 times as much. Energy does not bind.
  - **Power headroom.** At `RoCoF = 1 Hz/s`, the machines deliver `2 E_kin RoCoF / f_0 = 2 * 5600 * 1 / 50 = 224 MW` instantaneously. A converter fleet must hold 224 MW of headroom above its dispatch to match it. Convert that to a fleet rating: at `H_v = 5 s` a converter's inertial power at `RoCoF = 1 Hz/s` is `2 H_v RoCoF / f_0 = 2 * 5 * 1 / 50 = 0.20 pu` of its own rating, so 224 MW of inertial power needs `224 / 0.20 = 1120 MVA` of grid-forming plant.
  - **Current limit.** 224 MW on 1120 MVA is 0.20 pu of extra current on top of dispatch. A converter with `I_max = 1.2 pu` running at 1.0 pu has exactly 0.2 pu left, and nothing left for a voltage-support current at the same instant. State the conclusion: headroom and current limit bind together; energy does not bind. Then state what the model does not answer: whether the converters remain stable while saturated at `I_max`, which is the first open problem of §4.6.

**Test system TS4 (used by Fig. 4.1, Fig. 4.2 and Exercise 4.5).** Fix these numbers once. Every figure and exercise in this chapter that needs a network uses them and introduces no others. 50 Hz. System base `S_sys = 1000 MVA`. Four sources feed one load bus L.

| Unit | Type | S (MVA) | H or H_eq (s) | K_D or K_D_eq (pu, own base) | Internal reactance (pu, own base) | Dispatch (pu, own base) | Reactance to bus L (pu, system base) |
|---|---|---|---|---|---|---|---|
| 1 | synchronous machine | 400 | 4.0 | 2 | 0.30 | 0.75 | 0.10 |
| 2 | synchronous machine | 300 | 3.0 | 2 | 0.35 | 0.60 | 0.12 |
| 3 | grid-forming converter | 200 | 2.0 | 20 | 0.20 | 0.50 | 0.08 |
| 4 | grid-forming converter | 100 | 2.0 | 20 | 0.20 | 0.50 | 0.15 |

Load at bus L: 630 MW and 120 Mvar, constant impedance. Generation sums to `400(0.75) + 300(0.60) + 200(0.50) + 100(0.50) = 630 MW`, so the case balances. Stored energy `E_kin_sys = 400(4.0) + 300(3.0) + 200(2.0) + 100(2.0) = 3100 MVA.s = 3.1 GVA.s`, that is `H_sys = 3.1 s` on the 1000 MVA base. The converter share is swept by moving rating and dispatch from units 1 and 2 to units 3 and 4 in steps of 20 % of total rating, holding total rating at 1000 MVA, total dispatch at 630 MW, and each unit's `H` or `H_eq` unchanged. Report `E_kin_sys` at every step; it falls, and that fall is the mechanism the figure shows.

**Figures.**

- **Fig. 4.1** One-line diagram of test system TS4, with every reactance marked, beside its Kron-reduced equivalent. Must show what reduction removes and what it keeps.
- **Fig. 4.2** Eigenvalues of TS4 as the converter share rises from 0 % to 100 % in 20 % steps, with constant-`zeta` lines. Must show which modes move and which do not, and must print `E_kin_sys` at each step.
- **Fig. 4.3** Frequency against time for Example 4.1 at `E_kin_sys` = 300, 200, 100, 50 GVA.s on one axis, with the nadir marked on each and a horizontal line at 48.8 Hz. Must show the `1/E_kin_sys` scaling of the nadir depth.
- **Fig. 4.4** The three constraints of Example 4.2 drawn as three bars against the same converter fleet rating, normalised so that the binding constraint is visibly the tallest. Must show that the constraints are of different kinds and cannot be added.
- **Fig. 4.5** Timeline of the Great Britain 9 August 2019 event from the source report: the two generation losses, the nadir at 48.8 Hz, and the demand disconnection. Every value labelled with its source and marked `verify`. Must show that the sequence, not one number, caused the outcome.

**Exercises.**

1. *(Conceptual)* Explain why `RoCoF` is a measure of system strength and also a protection setting, and why those two uses can conflict. **Target:** the same number bounds how fast frequency moves and decides whether embedded generation disconnects; raising the protection threshold permits lower inertia but widens the window in which a genuine islanding event is missed.
2. *(Derivational)* Derive `df_nadir = - f_0 dP T / (4 E_kin_sys)` from the aggregated swing equation with a linear-ramp response, and state where the factor 4 comes from. **Target:** integrate `2 E_kin_sys / f_0 * d(df)/dt = -dP + dP t/T` from 0 to `T`; the nadir is at `t = T` and the factor 4 is `2 * 2` from the two integrations.
3. *(Derivational)* Add load damping `D_load` in MW/Hz and show that the nadir is shallower; state the limit in which the damping term dominates the ramp. **Target:** the first-order term adds `-D_load df` to the right-hand side; damping dominates when the dimensionless group `D_load T f_0 / (2 E_kin_sys)` is much greater than 1, with `D_load` in MW/Hz, `T` in s, `f_0` in Hz and `E_kin_sys` in MJ. Verify the grouping and its units numerically before printing it.
4. *(Computational)* Integrate the Example 4.1 system with `T` swept over 5, 10, 20, 30 s and confirm the linear dependence of nadir depth on `T`. **Target:** `df_nadir` of -0.3125, -0.625, -1.25, -1.875 Hz; report the values the integration returns and the tolerance.
5. *(Computational)* For TS4, find the converter share at which the least-damped mode falls below `zeta = 0.05`, sweeping in 5 % steps. **Target:** report the value the sweep returns with the parameter set stated; do not quote a number from the literature.
6. *(Conceptual)* Example 4.2 concludes that power headroom binds and energy does not. State one change to the case that would reverse that conclusion. **Target:** any of: a much longer required response duration (minutes rather than seconds), a converter fleet without a long-duration store such as photovoltaic without a battery, or a requirement referenced to a deep and sustained frequency excursion rather than to `RoCoF`.

**Definitions introduced.** Bus admittance matrix; Kron reduction; centre of inertia; system kinetic energy and system inertia constant; small-signal state, input, output and feedthrough matrices; eigenvalue, damping ratio, damped frequency, participation factor; rate of change of frequency and initial rate of change of frequency; frequency nadir; primary response and its delivery time; load damping; low-frequency demand disconnection; synchronous condenser; headroom.

**Length target.** 7000 words, plus 5 figures and 6 exercises. About 18 book pages, 4 lecture hours.

**Acceptance checks (editor).**

- Every system-level number carries either a computation in the chapter or a source identifier from §5.2 with a page reference or a `verify` mark. `200 GVA.s`, `H = 3.5 s` for a condenser, the 2019 event values, and every rate-of-change-of-frequency threshold are all in the second class and must be marked.
- Example 4.2 states in its first sentence that the fleet is a design case defined by this book, and that "1.6 GW" is the project label for a 1.6 GVA rating.
- The three constraints of Example 4.2 are presented as three separate calculations with different units; no passage adds them or takes the maximum of unlike quantities.
- Section 4.6 states each open problem as a question with a source. No passage predicts a date or an outcome.
- Every claim is tied to a local result number, and every cross-chapter reference resolves to a result identifier from §2.

---

## 5. Cross-chapter rules

### 5.1 Numbering

- **Results.** Chapter-local, typed, and continuous within the chapter: `Definition 2.1`, `Lemma 1.2`, `Theorem 3.4`, `Corollary 2.5`, `Example 4.2`, `Remark 1.1`. One counter per chapter shared by definitions, models, lemmas, propositions, theorems and corollaries, so that `Theorem 3.4` cannot collide with `Definition 3.4`. `Model` is a numbered environment like the others: it states the model, lists its assumptions, and names its omissions. This plan names every central result by its `R` identifier only; the draft stage assigns the local numbers, because the shared counter fixes them only once the chapter is written. Examples and remarks carry their own counters.
- **Global identifiers.** Each chapter-local result also carries its `R` identifier from §2 as an HTML `data-rid` attribute on its container element, for example `<div class="thm" id="thm-3-4" data-rid="R32">`. Prerequisites and acceptance checks use the `R` identifier. Prose uses the local number.
- **Equations.** `(chapter.N)`, numbered continuously within the chapter: `(3.14)`. Number only equations that are referenced later. An unreferenced display equation carries no number.
- **Figures.** `Fig. chapter.N`: `Fig. 3.5`. The caption prefix carries the chapter number. If the template uses a CSS counter for figures, override the caption prefix per chapter file so that it reads `Fig. 3.` and not `Fig. `.
- **Sections.** `§chapter.N` and `§chapter.N.M`. Cross-references are always by number, never by "above", "below", "earlier" or "the following figure".
- **Cross-chapter links.** `<a href="ch1.html#thm-1-3">Theorem 1.3</a>`. Every link target is an `id` that exists. The plan-level check is `scripts/check_book_links.py`.

### 5.2 Citation rule for the draft stage

Every published number and every result not proved in the book carries an inline citation of the form:

> [S01, Kundur 1994, *Power System Stability and Control*, §3.9, Table 3.2 — verify]

The four required parts are: source identifier, author and year, title, and the location the number comes from (section, table, figure, or page). A trailing `— verify` is **required** whenever the draft agent has not read the source page itself. The draft stage cannot open these sources, so in practice every citation below carries `verify`. A number the book computes carries no citation; it carries the example number instead, for instance `(Example 1.1)`.

Never write a bare claim such as "typical values are 2 to 8 seconds" with no source identifier. Never remove a `verify` mark; only a human who has read the page removes it.

**Source list.** Identifiers are stable. Every entry is `verify` until a human checks it.

| Id | Source | Used for |
|---|---|---|
| S01 | Kundur, P. (1994). *Power System Stability and Control*. McGraw-Hill. | Swing equation; typical H of 2 s to 8 s; local plant mode band; small-signal single-machine infinite-bus analysis (Ch 1) |
| S02 | Kundur, P. et al. (2004). "Definition and Classification of Power System Stability." *IEEE Trans. Power Systems* 19(3), 1387–1401. | Stability classification (R11) |
| S03 | Hatziargyriou, N. et al. (2021). "Definition and Classification of Power System Stability — Revisited and Extended." *IEEE Trans. Power Systems* 36(4), 3271–3281. | Converter-driven and resonance stability classes (R11) |
| S04 | Anderson, P. M. and Fouad, A. A. (2003). *Power System Control and Stability*, 2nd ed. IEEE Press / Wiley. | Equal-area criterion; critical clearing time (R09, R10) |
| S05 | Machowski, J., Bialek, J. W. and Bumby, J. R. (2008). *Power System Dynamics: Stability and Control*, 2nd ed. Wiley. | Multi-machine network reduction; centre of inertia (R34) |
| S06 | Yazdani, A. and Iravani, R. (2010). *Voltage-Sourced Converters in Power Systems*. Wiley. | Park transform convention; current control design; phase-locked loop (R12–R15) |
| S07 | Zhang, L., Harnefors, L. and Nee, H.-P. (2010). "Power-Synchronization Control of Grid-Connected Voltage-Source Converters." *IEEE Trans. Power Systems* 25(2), 809–820. | Weak-grid limits of vector current control; the grid-forming alternative (R22, R24) |
| S08 | Zhou, J. Z., Ding, H., Fan, S., Zhang, Y. and Gole, A. M. (2014). "Impact of Short-Circuit Ratio and PLL Parameters on the Small-Signal Behavior of a VSC-HVDC Converter." *IEEE Trans. Power Delivery* 29(5), 2287–2296. | Phase-locked-loop and current-loop interaction below the static bound (R22) |
| S09 | D'Arco, S. and Suul, J. A. (2014). "Equivalence of Virtual Synchronous Machines and Frequency-Droops for Converter-Based Microgrids." *IEEE Trans. Smart Grid* 5(1), 394–395. | Droop-to-swing-equation equivalence (R26) |
| S10 | Arghir, C., Jouini, T. and Dörfler, F. (2018). "Grid-forming control for power converters based on matching of synchronous machines." *Automatica* 95, 273–282. | Matching control (R29) |
| S11 | Colombino, M., Groß, D., Brouillon, J.-S. and Dörfler, F. (2019). "Global Phase and Magnitude Synchronization of Coupled Oscillators with Application to the Control of Grid-Forming Power Inverters." *IEEE Trans. Automatic Control* 64(11), 4496–4511. | Dispatchable virtual oscillator control and its synchronization result (R31) |
| S12 | Tayyebi, A., Groß, D., Anta, A., Kupzog, F. and Dörfler, F. (2020). "Frequency Stability of Synchronous Machines and Grid-Forming Power Converters." *IEEE J. Emerging and Selected Topics in Power Electronics* 8(2), 1004–1018. | Side-by-side comparison of the four grid-forming families (R32) |
| S13 | Anderson, P. M. and Mirheydar, M. (1990). "A Low-Order System Frequency Response Model." *IEEE Trans. Power Systems* 5(3), 720–729. | Nadir model and its assumptions (R36) |
| S14 | National Grid ESO (2019). *Technical Report on the events of 9 August 2019*, 6 September 2019. | Nadir 48.8 Hz; low-frequency demand disconnection about 931 MW; total loss about 1878 MW (R38) |
| S15 | ENTSO-E (2018). *Rate of Change of Frequency (RoCoF) Withstand Capability — Guidance document for national implementation*. | Withstand requirement, reported as 2 Hz/s measured over 500 ms — **verify, and do not print 1 Hz/s against this source** |
| S16 | EirGrid and SONI, DS3 programme documentation. | The 1 Hz/s rate-of-change-of-frequency figure used in Ireland — verify which document and which year |
| S17 | National Grid ESO, Grid Code modification GC0137, *Minimum Specification Required for Provision of GB Grid Forming Capability*. | Grid-forming specification in Great Britain (R40) |
| S18 | IEEE Std 2800-2022, *Standard for Interconnection and Interoperability of Inverter-Based Resources Interconnecting with Associated Transmission Electric Power Systems*. | Inverter-based resource interconnection requirements (R40) |
| S19 | IEEE Std 1204-1997, *Guide for Planning DC Links Terminating at AC Locations Having Low Short-Circuit Capacities*. | Short-circuit ratio strength classes (R16) |
| S20 | ENTSO-E (2017). *High Penetration of Power Electronic Interfaced Power Sources (HPoPEIPS)*, IGD. | System-level consequences of converter penetration (R40) |

**Standing warning on one number.** The project brief names "ENTSO-E RoCoF limit 1 Hz/s". Two different figures circulate and must not be merged: the ENTSO-E withstand guidance value (reported as 2 Hz/s over 500 ms, S15) and the 1 Hz/s figure used in Ireland and in Great Britain loss-of-mains protection policy (S16). The draft stage prints both, each with its own source identifier and a `verify` mark. The draft stage never prints "ENTSO-E 1 Hz/s".

### 5.3 HTML template rule

Chapters are customer-facing. One self-contained file per chapter: `ch1.html`, `ch2.html`, `ch3.html`, `ch4.html`.

1. **No external resources.** No `<script src=...>`, no `<link rel="stylesheet">`, no web font, no content delivery network, no image file. All CSS is in one `<style>` block. This overrides the `stem-textbook` default of MathJax, which loads an external script.
2. **Mathematics.** MathML (`<math>` elements) for display and inline mathematics, or plain HTML with `<sub>`, `<sup>`, `<var>` and Unicode Greek letters where MathML is heavier than the expression deserves. Be consistent within a chapter. No LaTeX source left in the page.
3. **Figures.** Inline `<svg>` only. Every figure is drawn from numbers computed for that figure, stated in the caption or in a nearby table. Both theme colours must be legible on the dark background. No raster image, no `data:` image URI.
4. **Dark mode, per `~/.claude/CLAUDE.md`.** `<meta name="color-scheme" content="dark">`. Background `#0f172a`; card and panel `#1e293b`; body text `#e2e8f0`; secondary text `#cbd5e1`; muted `#94a3b8`; accents `#fb923c` and `#2dd4bf`; borders `#1e293b` and `#334155`. Define these as custom properties on `:root` and use the variables, not the literals, in the rules below `:root`.
5. **Structure.** One `<h1>` for the chapter title, `<h2>` per section, `<h3>` per subsection. Each result sits in a `<div>` with a class naming its kind (`def`, `model`, `lem`, `prop`, `thm`, `cor`, `ex`, `rem`), an `id` of the form `thm-3-4`, and the `data-rid` attribute of §5.1. Each exercise sits in a `<div class="exercise">` with its answer target in a `<details>` element.
6. **Width and reading.** Body text at a maximum measure of about 72 characters. Tables scroll horizontally on a narrow screen rather than overflowing the page. No horizontal page scroll at 360 px width.
7. **Self-check before handing off.** Open the file and confirm: no external request is made; every `id` referenced by an internal link exists; every figure caption carries its chapter-prefixed number; every symbol used appears in the chapter's own notation list.

### 5.4 Status label rule

Every result carries its epistemic status in the prose at the result, not only in a ledger: `proved here`, `proved in §1.5`, `cited [S07 — verify]`, `computed in Example 2.1`, or `assumed for this case`. A cited result is never written as though the book proved it. A number that no source and no computation supports does not go in the book; write `[NUMBER NOT YET COMPUTED]` instead.

---

## 6. Per-chapter draft prompts

One line each. The draft stage pastes the line, reads `book-plan.md`, and writes one chapter.

**Chapter 1.** `Read book-plan.md in this folder and draft Chapter 1 ("The classical picture: machines that swing") as ch1.html: six sections per §4, central result R07, both worked examples computed to the printed digits (Example 1.1: delta_0 28.2 deg, K_s 1.49 pu/rad, omega_n 8.96 rad/s, zeta 0.0159; Example 1.2: delta_cr 63.9 deg, t_cr 0.170 s), four inline-SVG figures, five exercises with answer targets, every symbol from §3.2 defined in prose before use, the §3.6 swing convention stated and the alternative excluded, every published value cited per §5.2 with "verify", and the §5.3 HTML rules obeyed exactly.`

**Chapter 2.** `Read book-plan.md in this folder and draft Chapter 2 ("Inverter-based resources and the limit of following") as ch2.html: six sections per §4, central results R18 and R19 derived in full from v_q = X_g I_d - V_g sin(theta_p) with the bound on CURRENT not power, both worked examples recomputed (Example 2.1: I_d = 1 pu, theta_0 56.44 deg, K_pll 0.5528 which equals both the terminal voltage and P, P_max = SCR/2 = 0.600 pu, omega_n_pll 46.72 rad/s, zeta_pll 0.526; Example 2.2: the five-row SCR sweep with both power columns), the parallel between K_s and K_pll stated explicitly with result numbers, R22 labelled cited not proved, four inline-SVG figures, six exercises, and the §5.2 and §5.3 rules obeyed exactly.`

**Chapter 3.** `Read book-plan.md in this folder and draft Chapter 3 ("Grid-forming control: what it restores") as ch3.html: seven sections per §4, central results R32 and R33, R26 proved by coefficient matching against the §3.6 swing convention, both worked examples recomputed (Example 3.1: H_eq 0.318 / 1.592 / 5.000 s; Example 3.2: 14.4 kJ, H_eq 0.0144 s, ratios 243 and 1111), the four-family (H_eq, K_D_eq) table complete with each entry derived or cited, five inline-SVG figures, six exercises, and the §5.2 and §5.3 rules obeyed exactly.`

**Chapter 4.** `Read book-plan.md in this folder and draft Chapter 4 ("System-level stability and a sizing case") as ch4.html: six sections per §4, central results R35 and R36 derived, both worked examples recomputed (Example 4.1: RoCoF_0 0.125 Hz/s, nadir 49.375 Hz, and the halved-inertia case; Example 4.2: E_kin 5.6 GVA.s, energy 179.2 MJ, headroom 224 MW at 1 Hz/s, 20 % of 1120 MVA, with the fleet declared a design case of this book), the two rate-of-change-of-frequency figures kept separate per the §5.2 standing warning, five inline-SVG figures, six exercises, §4.6 written as questions with sources, and the §5.2 and §5.3 rules obeyed exactly.`
