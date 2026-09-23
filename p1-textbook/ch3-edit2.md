# Chapter 3 EDIT2 (verification) — `ch3-edit2.md`

**ACCEPT**

Checked `ch3-edit.md`'s 9 blocking items (Part A) against `ch3-fix.md`'s fix log and the current `ch3.html`. All 9 are present and correct. Recomputed every worked-example number the blocking items and their surrounding passages depend on, in Python. Found no defect introduced by the fix pass.

## Item-by-item check (blocking items 1–9)

1. **Malformed `<sub>D</var>` tag (line 923 old).** Fixed at `ch3.html:1001-1003`: reads "Substitute (3.17), divide by `S`base, and match the result against the `K`<sub>D</sub> `δω` term of (3.3)." `html.parser` run over the full file: 0 errors (was 2 mismatched-tag errors before the fix).

2. **dVOC reduction dropping the ΔE coupling term.** Fixed at `ch3.html:1228-1249`. The deviation of (3.24) now shows both terms explicitly (the ΔP term and the 2ηP_ref/V_ref³·ΔE term), followed by a labeled "Assumption for the reduction" paragraph stating ΔE = 0 and tying it to Model 3.2 assumption (iv). Recomputed by hand: d/dE of η(P_ref/V_ref² − P/E²) at E = V_ref is 2ηP_ref/V_ref³, confirming the term the original draft silently dropped is real and only vanishes under the stated ΔE = 0 assumption. Correct.

3. **Wrong cross-reference "(3.22) gives".** Fixed at `ch3.html:1011`: now reads "(3.21) gives". Equation (3.21) at `ch3.html:1005-1007` is indeed the matching-control damping result `K_D,eq = k_dc·v_dc0²/S_base − P_0`, the equation the sentence is referring to. Correct target.

4. **Wrong "11 %" figure.** Fixed at `ch3.html:730-733`: now reads "9.1 % of a 3.5 s machine (0.3183 / 3.5 = 0.0909; the machine's constant is 11.0 times the converter's)." Recomputed: 0.3183 / 3.5 = 0.090943 → 9.1 %, and 3.5 / 0.3183 = 10.9959 → 11.0. Both numbers now correctly labeled and both shown. Correct.

5. **Unargued/reversed "interact with the current loop" claim.** Fixed at `ch3.html:696-716` (new paragraph "What that slowness touches, and what it does not"). Recomputed all four supporting numbers: α_c = 2π(500) = 3141.5927 rad/s (three decades above ω_c = 2.8571 rad/s, confirmed); ω_n = √(K_s·ω_0/(2H_eq)) = √(1.491 × 376.99 / 7) = 8.9610 rad/s (text: 8.96, matches); ζ = K_D,eq/(4H_eq·ω_n) = 20/(4×3.5×8.96) = 0.1594 (text: 0.159, matches); K_D,eq/(2H_eq) = 20/7 = 2.8571 rad/s (matches ω_c exactly, as claimed); breaker clearing 4–6 cycles at 60 Hz = 0.0667 s–0.100 s (matches); 1 − e^(−t/0.35) at those two times = 0.1734 and 0.2485, i.e. 17 %–25 % (text: "17 % to 25 %", matches with reasonable rounding). All five numbers check out.

6. **"Better conditioned as impedance rises" (wrong direction).** Fixed at `ch3.html:296-317`. Replacement instead argues via the network power limit E·V_g/X = SCR·E·V_g in per unit vs. the R18 model's SCR·V_g²/2. Recomputed: SCR × E × V_g = 1.2 × 1.1 × 1.0 = 1.32 pu; SCR × V_g²/2 = 1.2 × 1.0/2 = 0.600 pu; ratio 1.32/0.600 = 2.2. Text states "1.32 pu against the 0.600 pu of Example 2.1, a factor 2.2" — matches exactly.

7. **Undefined E_res before (3.30).** Fixed at `ch3.html:1514-1520`: E_res is now defined in prose ("the usable energy reserve of the converter: the energy, in joules, that the source behind the DC link can deliver...") immediately before its use in (3.30), with Δf also defined in the same passage. Correct, matches the plan's requirement that every symbol be defined in prose before first use.

8. **Undefined Q_f, δ, RoCoF, headroom; (3.31) scalar-addition condition.** (a) Fixed at `ch3.html:239-249`: all four terms now appear in the notation list — Q_f tied to (3.6), δ defined as the converter's lead angle with δ_0 as equilibrium, RoCoF defined as |df/dt| with the Chapter 4 forward-reference noted, headroom defined as I_max − i_0. (b) Fixed at `ch3.html:1524-1539`: RoCoF is defined again locally as a magnitude before (3.31), the scalar-addition condition ("both active currents, in phase with the terminal voltage") is now stated explicitly before the inequality, and a following sentence adds the reactive-current caveat ("the true headroom is larger than this difference, and (3.31) is conservative"). Recomputed the vector-vs-scalar claim structurally: since a vector sum of two currents of fixed magnitudes is always ≤ their scalar sum, the scalar bound (3.31) is indeed always conservative (never larger than the true headroom) — consistent with the editor's numerical check (0.200 pu scalar vs. 0.663 pu vector headroom at the stated test point). Correct.

9. **Great Britain loss-of-mains misattributed to S16.** Fixed at `ch3.html:1643-1648`: the Great Britain clause is removed from the S16 citation; the citation now covers only Ireland's DS3 programme, followed by "The book's source list holds no document for the Great Britain loss-of-mains setting, so this chapter makes no claim about it." Confirmed S16 is described elsewhere in the chapter's own source list as an EirGrid/SONI (Irish) document only. Correct.

## Other checks performed

- **HTML well-formedness:** `html.parser` over the full 1827+ line file — 0 errors.
- **Zero external assets:** no `<script>`, `<link>`, `<img>`, `http://`, `https://`, or `data:` anywhere in the file.
- **Hex-literal-to-var() fix (item 43a):** confirmed `--eqbg:#16213a` and `--thbg:#20304a` are declared once in `:root` (`ch3.html:12`) and all 8 other occurrences use `var(--eqbg)` / `var(--thbg)` (verified at lines 54, 68, 87, 353, 604, 636, 749, 1427). No literal `#16213a` or `#20304a` remains outside the `:root` declaration.
- **Result-div kind classes (item 43b):** all 8 target `<div class="res">` elements now carry a second kind class — `def` (Definition 3.1), `model` ×4 (Model 3.2, 3.4, 3.5, 3.6), `thm` ×2 (Theorem 3.3, 3.7), `cor` (Corollary 3.8) — alongside the pre-existing `ex` and `rem` kinds.
- **New §3.7.5 closing section (item 39):** confirmed inserted at `ch3.html:1684` ("3.7.5 What the reader can now do"), immediately before `<h2 id="ex">Exercises</h2>` at `ch3.html:1704`.
- **Worked-number spot checks beyond the blocking items** (sanity check against defects the fix pass might have introduced elsewhere): item 34's 100 MW × 1 h = 100 MWh = 3.6×10^11 J = 360 GJ, and 360 GJ / 16 MJ = 22,500 — recomputed, matches `ch3.html:1601`. Item 20's second-term-smallness check: K_D,v/(2ω_c) = 5/(2×31.4159) = 0.0796 s ≈ 0.080 s, and 0.080/2 = 4.0 % of H_v = 2 s — recomputed, matches `ch3.html:830-832`. Item 31's rolloff-curve ratios (1.11 at 10 rad/s, 1.013 at 30 rad/s) are present at `ch3.html:1475-1476`; not independently re-derived (would require reconstructing the full second-order transfer function used for Fig. 3.5, out of scope for this pass given no defect was suspected there).

## Residual items

None found. No new defect was introduced by the fix pass. Items 40–46 of `ch3-edit.md` were correctly left as no-action/skipped by `ch3-fix.md` (informational length note, two `book-plan.md`/`HANDOFF.md` corrections explicitly out of scope for a chapter-text edit, a file-naming confirmation, a low-severity SVG-literal note explicitly marked "fix if strictness is wanted," and a Chapter 4 figure-spec recommendation for the plan owner). None of these bear on Chapter 3's own correctness.

No small, certain defect was found in `ch3.html` during this verification pass, so no additional edit was made and no additional fix-log entry was needed.
