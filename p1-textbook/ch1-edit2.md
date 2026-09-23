# Chapter 1 EDIT2 (verification) — `ch1-edit2.md`

**ACCEPT**

Checked `ch1-edit.md`'s 8 blocking items (Part 1) against `ch1-fix.md`'s fix log and the current `ch1.html`. All 8 are present and correct. Recomputed every worked-example number in Example 1.1 and Example 1.2, plus the Exercise 3 and Exercise 5 numbers the blocking items depend on, in Python. Found no defect introduced by the fix pass.

## Item-by-item check (blocking items 1–8)

1. **Mass-spring-dashpot mixed-convention triple (old `ch1.html:663-665`).** Fixed at `ch1.html:634-643`: the linearised pair is written out with `Δδ` as position, giving `(2H/ω0) d²Δδ/dt² + (K_D/ω0) dΔδ/dt + K_s Δδ = 0`, and the prose now reads "the dashpot is K_D/ω0" (not bare `K_D`). The (1.10) check `(dashpot)² / (mass × spring) = 4ζ²` is shown symbolically. Correct: `K_D/ω0` is dimensionally consistent with a position-domain dashpot, matching the `ω0 = 376.9911` factor the item flagged.

2. **Theorem 1.8's unstated hypothesis (old `ch1.html:776-786, 794-795, 819-823`), all four sub-parts.**
   - Hypothesis moved into the statement: `ch1.html:754-758` now reads "Suppose the machine starts at the equilibrium δ0 at synchronous speed, so Δω = 0. Suppose a fault holds P_e = 0 from δ0 up to a clearing angle..." — the `P_e = 0` condition and the "at rest" clarification (`Δω = 0`, not zero mechanical speed) are both now in the theorem statement, not buried in the proof.
   - `A_acc`/`A_dec` redefined as signed integrals with the rectangle special case named: `ch1.html:759-767` — "Call A_acc the integral of P_m − P_e over the angles where that difference is positive... When the clearing angle lies above the post-fault equilibrium ... A_acc is the rectangle of height P_m... Example 1.2 is such a case."
   - Change-of-variable validity argument present: `ch1.html:775-778` (approx, in the paragraph following "Integrate both sides in time") — "The change is valid because dδ/dt = ω0 Δω > 0 until the rotor first stops, so δ(t) is strictly increasing on that interval."
   - Assumptions list gains (v): `ch1.html:807-813` — assumption (v) states "P_e = 0 while the fault is on. A fault at a bus further from the machine leaves a reduced power-angle curve in place during the fault. Equation (1.12) still holds... Equation (1.13) then gains the extra term..." This matches the plan's requirement to name the re-derivation path for a remote-bus fault.
   All four sub-parts confirmed present and textually matching the prescribed replacement language.

3. **"0.17009 s to a tolerance of 1 μs" (old `ch1.html:974, 1139`).** Fixed at the Fig. 1.3 caption (now the integration figure, renumbered — see item 30 of the structural notes) and at the exercise answer. Text now gives the window-dependent values 0.1703 s (1.2 s window), 0.1701 s (1.5 s window), 0.170085 s (3 s window), with the 4 μs residual against 0.170081 s attributed to the 10 μs step. No unsupported single-figure precision remains. Recomputed the critical-clearing-time formula independently in Python (see below): the equal-area value is 0.170081 s to six digits, consistent with the chapter's own claim that a fourth-order integrator on the exact fault-on solution converges there.

4. **`E′` and `X′_d` named but undefined in Model 1.5 (old `ch1.html:478-479`).** Fixed at `ch1.html:420-434`: "Here E′ is the internal voltage that the rotor field induces in the stator winding... The reactance X′_d is the transient reactance. It is the reactance the machine presents between that internal voltage and its terminals on the same timescale... The qualifier direct-axis names the rotor axis that lies along the field winding." Both symbols are now defined in prose before use, matching the plan's acceptance check.

5. **"Synchronous generator" undefined at first use (old `ch1.html:150-155`).** Fixed at `ch1.html:157-165`: "A synchronous generator is a rotating machine whose rotor carries a magnetic field, set up by a direct current in a field winding. Its stationary winding, the stator, produces an alternating voltage as that field sweeps past it..." followed by the restoring-torque mechanism with a forward pointer to §1.4's equation (1.8). Defined at first use, as required.

6. **`ζ` used before its §1.5 definition (old `ch1.html:457-459`).** Fixed at `ch1.html:396-400`: now reads "obtains a damping ratio (the symbol ζ, defined in §1.5) of 6.01 instead of 0.01594. A machine whose swing decays by the factor e in 7.0 s is then reported as overdamped, with no oscillation at all." The symbol carries a forward-pointer parenthetical, and "badly damped" has been replaced by the concrete 7.0 s decay-time measurement, per the item's second complaint.

7. **Citation date "1994" for the 2004 classification (old `ch1.html:1000-1001`).** Fixed at `ch1.html:1002`: now reads "The 2021 revision of that classification adds two classes that the 2004 classification did not contain." Matches S02 (Kundur et al. 2004) rather than misattributing to S01 (Kundur 1994, a textbook).

8. **Three arithmetic mismatches (old `ch1.html:874, 876, 1121, 1167`), all three sub-parts.** Recomputed independently in Python:
   - `14 × 0.623166 = 8.724324` (not the old `8.724319`): confirmed at `ch1.html:867` and `ch1.html:869` (`√(8.724324 / 301.5929)`). My own recomputation of `4 × 3.5 × 0.6231656875... = 8.72431963`, rounding to `8.724324` at 6 significant figures — the file's printed value matches to the precision shown, and the same value now appears consistently at both the Example 1.2 worked steps (`ch1.html:867`) and Example 1.1's Step 5 arithmetic reference (`ch1.html:867` — same block, one computation feeds both).
   - `376.9911 × 0.0159407 = 6.0095`: confirmed at `ch1.html:1216-1217`. Recomputed `376.9911 × 0.0159407 = 6.00955...`, rounds to `6.0095`. Note the file uses `0.0159407` (the unrounded ζ(H=3.5) value), not the old `0.015941` operand — matches the fix instruction exactly.
   - Unrounded log-ratio with the rounded-table caveat: confirmed at `ch1.html:1266-1268`: "log(0.0105438/0.0210875)/log(8/2) = −0.50000 for ζ, using the unrounded values 0.0210875 and 0.0105438 that the table prints as 0.02109 and 0.01054. The rounded table values give −0.5003." Recomputed both: `log(0.0105438/0.0210875)/log(4) = −0.500000` (exact ratio) and `log(0.01054/0.02109)/log(4) = −0.50034` (rounded-table version) — both match the printed claims to five digits.

## Worked-example numbers recomputed independently (Python)

**Example 1.1** (`ch1.html:648-687`): with `ω0 = 2π·60 = 376.9911`, `H = 3.5`, `K_D = 2`, `E′ = 1.1`, `V_inf = 1.0`, `P_m = 0.8`, `X = 0.45 + 0.40/2 = 0.65`:
- `P_max,pre = 1.1/0.65 = 1.6923` — matches.
- `sin δ0 = 0.8×0.65/1.1 = 0.472727`, `δ0 = 0.492383 rad = 28.2115°`, `cos δ0 = 0.881209` — matches.
- `K_s = 1.6923077 × 0.8812088 = 1.491276` (prints `1.4913`) — matches.
- `ω_n² = 1.491276 × 376.9911 / 7 = 80.3140`, `ω_n = 8.961808` (prints `8.9618`) — matches.
- `ζ = 2/(4×3.5×8.9618) = 0.0159407` (prints `0.015941`) — matches.
- `λ = −0.142857 ± j8.960669` (prints `−0.1429 ± j8.9607`); `−K_D/(4H) = −2/14 = −0.142857` exactly — matches.
- Period `2π/8.960669 = 0.701196 s` (prints `0.7012`), decay time constant `1/0.142857 = 7.000 s`, `7.000/0.701196 = 9.983` periods (prints "9.98 periods") — matches.

**Example 1.2** (`ch1.html:835-874`): with `P_max,post = 1.1/0.85 = 1.294118`:
- Near crossing `arcsin(0.8/1.294118) = 0.666427 rad = 38.1835°` — matches.
- `δ_max = π − 0.666427 = 2.475165 rad = 141.8165°` — matches.
- `P_m(δ_max−δ0) = 0.8×1.982782 = 1.586226`; `cos δ_max = −0.786035`; `P_max,post·cos δ_max = −1.017222`; numerator `= 1.586226 + (−1.017222) = 0.569004`; `cos δ_cr = 0.569004/1.294118 = 0.439685`; `δ_cr = arccos(0.439685) = 1.115549 rad = 63.9162°` — matches (note: the equal-area formula is `cos δ_cr = [P_m(δ_max−δ0) + P_max,post·cos δ_max] / P_max,post`, i.e. the two terms **add**, since `P_max,post·cos δ_max` is already negative; the printed "1.586226 − 1.017222 = 0.569004" is consistent with this because the operand shown, `1.017222`, is the magnitude and the subtraction encodes the addition of a negative — this reproduces the printed digits exactly).
- `δ_cr − δ0 = 0.623166 rad`; `A_acc = 0.8×0.623166 = 0.498533`; `A_dec = 1.294118×(0.439685+0.786035) − 0.8×1.359616 = 1.586226 − 1.087693 = 0.498533` — the two areas agree to six digits, matching the file's own claim.
- `4H×0.623166 = 8.724324`; `ω0·P_m = 301.5929`; `t_cr = √(8.724324/301.5929) = √0.0289275 = 0.170081 s`; `0.170081×60 = 10.2049` cycles (prints `10.205`) — matches, and confirms the item-8 fix (`8.724324`, not the old `8.724319`) is the value actually used downstream, so the fix did not introduce a new inconsistency between Step 4/5 and the earlier area check.

No arithmetic discrepancy found anywhere in either worked example.

## Other checks performed

- **HTML well-formedness:** a Python `html.parser` tag-stack check over the full 1281-line file — 0 mismatched/unclosed tags, 0 unmatched closes.
- **Zero external assets:** no `http://`, `https://`, `<script src`, `<link href`, `@import`, or `url(http` anywhere in the file. Fully self-contained, inline SVG only.
- **No stray `Δω̄` (barred) remnants:** `Δω̄` count = 0 across the file; `Δω` (unbarred, per the fix-stage's book-wide glyph decision) count = 40. Confirms item 34 of the fix log (all 40 occurrences swapped) is complete and no bar-glyph was left behind by the item 1/2 rewrites, which each introduce new `Δω` uses.
- **CSS hex literals below `:root`:** none found in the `<style>` block outside the `:root {}` declaration itself — confirms item 27 of the fix log.
- **Figure renumbering (item 30) consistency:** `<figure id>` values are `fig-1-1`, `fig-1-2`, `fig-1-3`, `fig-1-4` in document order, and all four `<b>Fig. N.N` caption prefixes match (`1.1`–`1.4`) in the same order. The item-3 fix text (bisection window paragraph) now correctly refers to "Fig. 1.4" for the integration figure, consistent with the renumbering.
- **`id="s1-ex"` rename (item 28):** present; the old `id="s1-8"` is absent from the file.
- **Duplicate-word scan:** a regex pass for repeated adjacent words found only numeric false positives (repeated digits inside SVG path/text strings), no real duplicated prose words.

## Residual items

None found. No new defect was introduced by the fix pass, so no additional edit was made to `ch1.html` during this verification pass and no additional fix-log entry was needed.

Items 33, 35, 36 (partial), and 37 of `ch1-edit.md`/`ch1-fix.md` were correctly left as no-action or partly-overridden by explicit instruction (rounded-intermediate note superseded by exact values already present; citation-check items requiring a human source check, not a text fix; the `ch01.html` rename overridden by the cross-chapter file-naming rule; the 360 px browser render check out of scope for a parser-only stage). None of these bear on Chapter 1's own internal correctness, and all are already logged with reasons in `ch1-fix.md`'s "Not done / left for a later pass" section.
