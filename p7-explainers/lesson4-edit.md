# Lesson 4 — science-editor pass

File: `p7-explainers/lesson4.html` (line numbers refer to the file before fixes).
Script: `p7-explainers/lesson4_cct.py`, re-run on 2026-09-22. Its stdout matches the output block on the page, character for character.

## Verdict (before fixes)

**Revise before publication.** The main result is correct. I recomputed every value: delta_0 = 0.4924 rad, delta_max = 2.4752 rad, cos(delta_cr) = 0.4397, delta_cr = 1.1155 rad, t_cr = 0.17008 s, A_acc = A_dec = 0.49853. Two claims are false: the Exercise 2 bracket claim and the eigenvalue argument (Section 7, Exercise 5). There are also five moderate errors in definitions and physics, and six minor defects.

## Independent checks

- Closed form: A_acc = 0.8 x 0.6231 = 0.49853 and A_dec(delta_max) = 0.49853, so the areas are equal to 1e-15.
- t_cr unrounded = 0.170081 s. Margin at 5 cycles = 86.747 ms.
- Post-fault stable equilibrium delta_s,post = arcsin(0.8/1.2941) = 0.6664 rad = 38.18 deg. The page never states it.
- K_s,pre = 1.4913 pu/rad. With K_D = 2 pu: lambda_pre = -0.1429 +/- j8.9607.
- K_s,post = 1.0172 pu/rad. With K_D = 2 pu: lambda_post = -0.1429 +/- j7.400.
- Step quantization: `stable(0.16995)` = True, `stable(0.17002)` = False, `stable(0.1700)` = True, `stable(0.17005)` = False. At h = 0.05 ms with a 0.01 ms tolerance, the bracket is [0.170047, 0.170056] s.
- Fig. 4.3: the peak for clearing at 0.15 s is 106.706 deg. That matches the caption. The pixel mapping is linear, with the bottom edge at -15 deg.
- Fig. 4.1 and Fig. 4.2: every marked coordinate matches its computed angle and power to 0.1 px.

## Defects

### Blocking

**B1. Exercise 2 answer (l.903-905), Exercise 2 target (l.898-899), Section 6 closing paragraph (l.696-701).**
- Problem: the page says "The closed-form 0.1701 s sits inside this bracket" [0.16995, 0.17002]. That is false: 0.17008 > 0.17002.
- Problem: the page says the 0.1 ms run "shows the 1 ms bracket was already limited by the bisection tolerance, not by the integration step". That is the opposite of the truth.
- Cause: `stable()` steps while t < t_clear, so clearing happens at t_clear rounded up to a multiple of h = 0.5 ms. Any bisection tolerance below h adds no information.
- Fix: explain the rounding-up to the 0.5 ms grid. State the true information: the boundary lies between switching at 0.1700 s and 0.1705 s, and 0.17008 s is inside that interval. Report the h = 0.05 ms bracket as the correct way to resolve the boundary more finely. Rewrite the target text.

**B2. Section 7 eigenvalue paragraph (l.835-844) and Exercise 5 (l.951-968).**
- Problem: the page claims the linearised model is identical before and after clearing, "because both have the same local slope ... whenever the two equilibrium angles happen to coincide". The sentence contradicts itself in its own parenthesis.
- Problem: Exercise 5 asks the reader to explain why the eigenvalues are "the same ... before and after the fault is cleared". For this lesson's network, which loses a line, they are not the same. K_s falls from 1.4913 to 1.0172 pu/rad, and Im(lambda) falls from 8.961 to 7.400 rad/s.
- Problem: the page does not say that the Lesson 2 eigenvalues use K_D = 2 pu, but this lesson uses K_D = 0.
- Fix: state both eigenvalue pairs and state that both equilibria are small-signal stable. The point stays the same: neither eigenvalue pair tells whether the large excursion between the two equilibria returns. Rewrite the Exercise 5 question and answer to match.

### Moderate

**M1. Section 4 (l.399-403) and Exercise 1 (l.885-887).**
- Problem: the page says "As long as delta stays above delta_0 the post-fault curve delivers more than P_m". That is false. The post-fault P_e is less than P_m on 28.2 to 38.18 deg, and it is more than P_m only on 38.18 to 141.82 deg.
- Fix: state the band 38.18 deg to 141.82 deg. State that delta_cr = 63.9 deg lies inside it.

**M2. Section 4 (l.381-382).**
- Problem: the page says "The left side is (twice) the machine's kinetic energy". That is wrong. The left side is omega_0 x H dw^2, where H dw^2 is the deviation kinetic energy in pu-s.
- Fix: state the factor omega_0 and where it comes from (the integral is over angle in radians).

**M3. Opening (l.169-172, 177-179).**
- Problem: the page calls the 0.45 pu path "a transformer". The source (book-plan Example 1.1) defines 0.45 pu as X'_d + X_t, so the machine's own reactance disappears from the stated network.
- Fix: name it X'_d + X_t.

**M4. Section 3 (l.224-226).**
- Problem: the page says the classical model is "the model from Lesson 1's Park transformation in its amplitude-invariant form, with the direct axis defined on the measured terminal voltage". `lesson1.html` contains no Park transformation. A synchronous machine's d-axis sits on the rotor field axis, not on the terminal voltage.
- Fix: delete the clause. Define delta as the angle of E' relative to the infinite bus.

**M5. Section 3 (l.260-262).**
- Problem: the page says the post-fault curve is lower "because the remaining single line carries a larger share of the same reactance drop". That physics is wrong.
- Fix: X rises from 0.65 to 0.85 pu, so P_max = E'V/X falls by the ratio 0.765.

### Minor

**m1. Section 4 (l.454-457).** The page says "the delta_cr-independent terms cancel". In fact the +P_m delta_cr and -P_m delta_cr terms cancel. Fix: reword.

**m2. l.471.** cos(delta_max) = -0.78604, not -0.7859. Fix: write -0.7860.

**m3. l.250, l.359, l.577.** The page points to "Section 6" for the model assumptions, but they are in Section 7 (Section 6 is Code). Fix: change all three references to Section 7.

**m4. Fig. 4.1 (l.339-342).** The curve labels start at x = 580 in a 640-wide viewBox, so the labels are clipped. They also sit far from their curves. Fix: move them over the curve peaks.

**m5. Fig. 4.3 (l.712-713).** The "0" at the corner suggests delta = 0 at the bottom edge, but the bottom edge is -15 deg. Fix: move "0" under the t axis, add a 28.2 deg tick, and state the axis in the caption.

**m6. Fault location and P_e = 0 (l.173-176, 244-249).** The page says "essentially none" of the power reaches the bus, with the fault "at the machine's own terminals". The source puts the fault at the sending-end bus of line 2. There, P_e = 0 exactly in this model, because every path passes through a zero-voltage bus. Fix: use the sending-end bus and "exactly".

**m7. Damping explanation (l.793-795, Exercise 3 l.919-923).** The page says damping acts only "throughout the fault-on swing". Damping also adds deceleration after clearing. Fix: state both effects and give the size: dw(0.170 s) = 0.0194 pu, so the damping torque is about 0.039 pu.

**m8. l.666.** The page says "about 115 lines". The file has 120. Fix: write 120.

**m9. l.833, l.961.** The page gives Im(lambda) = 8.962. With K_D = 2, the damped value is 8.9607, and 8.962 is omega_n rounded. Fix: write 8.961 and note that book-plan prints 8.962.

**m10. Citation l.185-186, l.943-944.** "[S01 or S04 ... §5.2 — verify]" guesses a source. book-plan.md Example 1.2 gives the 4 to 6 cycle range with no S-identifier. Fix: mark it as unsourced, keep "verify", and name the two candidate sources.

## What already works

- The derivation chain works: swing equation, then energy balance, then the areas, then the closed form cos(delta_cr), then the quadratic fault-on trajectory, then t_cr. It is complete and algebraically correct.
- The code listing is the real file, and the output block is the real stdout.
- Figs. 4.1 and 4.2 are drawn to scale from computed values.
- The model-limits section names the right four assumptions.

## Fix log

All fixes were applied to `lesson4.html` in place on 2026-09-22. The original is backed up at scratchpad `p7_l4_edit_lesson4_orig.html`.

| ID | Status | Change made |
|----|--------|-------------|
| B1 | fixed | Section 6 paragraph rewritten to explain the rounding-up to the 0.5 ms grid and the true 0.1700-0.1705 s interval. Exercise 2 target and answer rewritten: the bracket does not contain 0.17008 s, the reason is given, and the h = 0.05 ms bracket [0.170047, 0.170056] s is added. |
| B2 | fixed | Section 7 paragraph now gives K_s,pre = 1.4913, K_s,post = 1.0172, lambda_pre = -0.1429 +/- j8.961 and lambda_post = -0.1429 +/- j7.400, notes K_D = 2 pu, and states that both equilibria are small-signal stable. Exercise 5 question and answer rewritten. |
| M1 | fixed | Section 4 and Exercise 1 now state the 38.18-141.82 deg band. Section 3 now defines delta_s,post = 0.6664 rad = 38.18 deg. |
| M2 | fixed | The left side is now explained as omega_0 x H dw^2, with the definition of H. |
| M3 | fixed | The opening names X'_d + X_t = 0.45 pu. |
| M4 | fixed | The Lesson 1 Park clause is deleted. delta is defined as the angle of E' relative to V_inf. |
| M5 | fixed | Reason replaced: X rises 0.65 to 0.85 pu, ratio 0.765. |
| m1 | fixed | Algebra step reworded. |
| m2 | fixed | -0.7859 changed to -0.7860. |
| m3 | fixed | Three "Section 6" references changed to Section 7. |
| m4 | fixed | Fig. 4.1 labels moved to x = 345 (middle-anchored) above each peak. |
| m5 | fixed | Fig. 4.3: "0" moved to the t axis, a 28.2 deg tick added, axis stated in the caption. |
| m6 | fixed | Opening and Section 3 use the sending-end bus and "P_e = 0 exactly". |
| m7 | fixed | Section 7 bullet and Exercise 3 answer rewritten, with the 0.0194 pu / 0.039 pu size estimate. |
| m8 | fixed | "about 115 lines" changed to "120 lines". |
| m9 | fixed | 8.962 changed to 8.961 in both places, with a note on the book-plan value. |
| m10 | partial | Citation marked unsourced, with the two candidate S-ids. The 4 to 6 cycle range is still unverified, because no source in the project states it. |

Checks after the fixes: tag balance is clean, the page has no external URLs, and the script output block is unchanged (it is still the real stdout).
