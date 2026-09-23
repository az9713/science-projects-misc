ACCEPT

# Chapter 2 EDIT2 (verification) — Inverter-based resources and the limit of following

File verified: `p1-textbook/ch2.html`. Inputs read: `ch2-edit.md` (the 11 blocking items, B1–B11), `ch2-fix.md` (the fix log), and the current `ch2.html`. Verifier: Fable, `science-editor` skill, EDIT2 pass. Written 2026-09-22.

## 1. Blocking-item check (B1–B11)

Each item: confirmed present in `ch2.html` and matches the fix log's claim.

- **B1** (equation (2.13) derivation) — present. `ch2.html` now carries the three-line derivation ("Derivation of the point-of-connection voltage": complex Park form, grid source in the loop frame, Kirchhoff's law across X_g) between Model 2.6 and equation (2.13). Correct.
- **B2** (θ_p tied to θ_pll and ω_0) — present. The local-notation card (lines 144–158) defines θ_g and θ_p = θ_pll − θ_g explicitly, with dθ_p/dt = ω_pll − ω_0 stated. The stiff-grid derivation and Theorem 2.8 use this definition consistently. Correct.
- **B3** (Definition 2.5 fixes V_g = 1 pu only for X_g = 1/SCR; Theorem 2.7 keeps V_g symbolic) — present, at lines 318–326: equation (2.9) is shown at V_g = 1 pu for the gain-design step, with a following paragraph warning that V_g is not 1 on a weak grid and "cannot be forgotten." Correct.
- **B4** (bare V split into V_m and V_inf) — present at all 7 locations the fix log names. V_m used at lines 151, 190, 192, 196 (§2.1/Fig. 2.1 peak amplitude); V_inf used at lines 114, 119, 444, 717 (all four K_s-formula instances: summary card, prerequisites, Table 2.1, Exercise 6). No bare, unsubscripted V with an ambiguous meaning remains (`grep` for a lone `>V<` found none). Correct.
- **B5** (Corollary 2.10's timescale hypothesis) — present at lines 631–643. The proof states the settling-time-vs-swing-period comparison explicitly and gives numbers. I recomputed them: 4/(0.7071·62.83) = 0.0900 s (stiff grid) and 4/(0.5257·46.71) = 0.1629 s (SCR = 1.2), against a swing period 1/1.43 Hz = 0.6993 s — both match the printed 0.090 s, 0.163 s, 0.70 s. The R08 citation to Example 1.1 is present and links correctly. Correct.
- **B6** ("every weak-grid symptom falls out of K_pll" no longer includes the oscillatory instability) — present at line 137: the sentence now explicitly carves out "One symptom is not among these: the oscillatory instability that a fuller model predicts," with a pointer to §2.6.3. Correct.
- **B7** (fault-current ratio range) — present at line 288: "between 0.157 (1.1/7) and 0.260 (1.3/5)." I recomputed: 1.1/7 = 0.15714… → 0.157; 1.3/5 = 0.260 exactly. The old wrong figures (0.220, 0.186) do not appear anywhere in the file. Correct.
- **B8** (S07 citation completed) — present at lines 359, 623, 654, 744: "S07, Zhang, Harnefors and Nee 2010, 'Power-Synchronization Control of Grid-Connected Voltage-Source Converters,' IEEE Trans. Power Systems 25(2), 809–820, weak-grid limit section." Title, journal, volume/issue/pages and locator are all present, matching the plan's four-part citation rule. Correct.
- **B9** (two "symbols defined below" pointer sentences) — present. Line 108: "This card summarises the results proved below. Its symbols are defined in §2.1 to §2.5." Line 135: "The symbols in the next paragraph are defined in §2.4 and §2.5." Both inserted at the locations the edit doc specifies (after line 106 and after line 132 of the original). Correct.
- **B10** (Fig. 2.4 caption cites S08 instead of an unsupported field-evidence claim) — present at line 617: the caption now attributes the oscillatory-instability claim to "Cited Result 2.9" and the S08 citation, not to unattributed field evidence. Correct.
- **B11** (bandwidth/damping fall as √K_pll, not the same fraction) — present at both locations the edit doc names. Line 526 (§2.6.2 reading): "loses loop bandwidth and damping ratio at the same moment, by the square root of the same factor, equation (2.19)... down 25.7 % (1 − √0.5528 = 1 − 0.7435)." Line 727 (closing summary): "It loses loop bandwidth and damping ratio at the same moment, as √K_pll (equation (2.19))... down 44.7 %... 25.7 %." I recomputed: √0.552771 = 0.74349, 1 − 0.74349 = 0.2565 → 25.7 %; 1 − 0.552771 = 0.4472 → 44.7 %. Both printed percentages match. The phrase "same fraction" no longer occurs anywhere in the file. Correct.

All 11 blocking items are applied and correct. No blocking item was left half-done or applied in a way that contradicts its own numbers.

## 2. Worked-example numbers recomputed (Python, full precision)

I recomputed the full Exercise 5 retuning chain and the Example 2.1 / Corollary 2.10 numbers independently in Python, carrying unrounded intermediates:

- k_i,pll = (2π·10)² = 3947.8418 → prints as 3948 (correct rounding).
- k_p,pll = 2·0.7071·62.8319 = 88.8577 → prints as 88.86 (correct).
- K_pll at SCR = 1.2: cos(arcsin(0.8333)) = 0.552771 → prints as 0.5528 (correct).
- K_pll at SCR = 10: cos(arcsin(0.1)) = 0.994987 → prints as 0.9950 (correct).
- Exercise 5 retuned gains: k_p,pll,new = 88.86/0.5528 = 160.75 → prints as 160.7; k_i,pll,new = 3948/0.5528 = 7141.91 → prints as 7142. Both correct.
- Check equation: 0.5528 × 7141.82 = 3947.998 → √3947.998 = 62.833 → prints as √3948.00 = 62.83. Correct (the fix log's item 1 is confirmed).
- Ratio at SCR = 10: using full-precision K_pll values, 0.994987/0.552771 = 1.80000 exactly → √1.8000 = 1.34164 → prints as √1.8000 = 1.3416. Confirmed: with rounded 4-digit inputs (0.9950/0.5528 = 1.79993) the ratio is not exactly 1.8000, but with the unrounded K_pll values it is exactly 1.8000 to 5 significant figures — the fix log's note that "the exact value is 1.8000" is correct (fix-log item 3 confirmed).
- ω_n,pll at SCR = 10: 62.83 × 1.3416 = 84.295 → prints as 84.30 rad/s; 84.30/(2π) = 13.42 Hz. Both confirmed (fix-log item 4).
- ζ_pll at SCR = 10: 0.7071 × 1.3416 = 0.9487. Confirmed.
- Corollary 2.10 settling times: 4/(0.7071·62.83) = 0.0900 s, 4/(0.5257·46.71) = 0.1629 s, swing period 1/1.43 = 0.6993 s. All three match the printed 0.090 s, 0.163 s, 0.70 s.
- Fault-current ratio: 1.1/7 = 0.157, 1.3/5 = 0.260. Confirmed.
- B11 percentages: 1 − 0.5528 = 44.7 %, 1 − √0.5528 = 25.7 %. Confirmed.
- Fig. 2.1 numeric check (equation (2.3) at f0 = 50 Hz): at t = 4 ms, ω0t = 72°, v_a = cos 72° = 0.3090, v_b = cos(72°−120°) = 0.6691, v_c = cos(72°−240°) = −0.9781; at t = 8 ms, ω0t = 144°, v_a = −0.8090, v_b = 0.9135, v_c = −0.1045. All match the printed values.

No arithmetic defect found anywhere I recomputed. The four corrections the fix log claims (fault-current range; 3948.00; √1.8000; 84.30 rad/s / 13.42 Hz) are all present and are all correct.

## 3. Defects introduced by the fix — none found

- HTML well-formedness: parsed the full file with Python's `html.parser`, tracking the open-tag stack. Zero mismatched or unclosed tags; stack empty at end of document.
- Self-contained/dark-mode rule: 0 `<script>`, 0 `<link>`, 0 `<img>`, 0 `http://`/`https://` references, 0 stray `data:` URIs; `color-scheme` present. No external asset was introduced by the fix.
- Cross-chapter links (S2): all 6 anchor ids the fix wired to ch1.html (`def-1-1`, `def-1-3`, `model-1-4`, `lem-1-6`, `thm-1-7`, `ex-1-1`) exist exactly once each in `ch1.html`; all 17 `href="ch1.html#..."` occurrences in `ch2.html` resolve to a real anchor. No dangling link.
- Hex-below-`:root` rule (R17): `var(--card2)` and `var(--eqbg)` are both used in the stylesheet as the fix log claims; no raw hex literal found outside `:root`.
- I re-checked the two B9 sentences, the B4 seven locations, and the B11 two locations by direct grep against the exact text the fix log describes (not just its summary) — all match the file, not just the log's own account of itself.

I found no small, certain defect to fix during this pass. No edit was made to `ch2.html` in this stage.

## 4. Residual items (carried from ch2-edit.md, not re-opened)

These are the fix log's own honest skips, unchanged from `ch2-fix.md`, and I concur with leaving them as recorded:

- **S4** — promoting §2.6.5 to an unnumbered closing section after the exercises: skipped in the fix as a larger structural move with real risk to heading/figure/exercise numbering, and the edit doc treats it as optional headroom, not a required fix. Content is present and correctly labelled where it sits; no reader-facing defect.
- **S5** — optional two-line identity in Exercise 2's answer: skipped, marked optional ("if space allows") by the edit doc; the existing answer is acceptable.
- **S6** — chapter is noted as landing about 2% over the 6,000–9,000 word target band after B1/B2/B5; the edit doc accepted this overrun as an option. Not a correctness defect.
- **R18** — the plan-level K_pll/K_s unit-note table change was out of scope (book-plan.md not to be touched this run); the fallback one-sentence clarification was applied in Theorem 2.7's proof instead, as the edit doc allows.
- **R22 / S19** — no citation-strength change made, as the edit doc specifies no change here.
- Doubtful-citation locators (R19 S01, R20 S18, R21 S06) remain marked "verify"/"locator doubtful"/"location unconfirmed" in the text, per the edit doc's own instruction that these are human-verification items, not defects to silently resolve.

None of these residual items is a blocking defect, a wrong number, or a broken tag. All are scope or judgement calls the fix log already recorded and justified.

## Verdict

**ACCEPT.** All 11 blocking items (B1–B11) are present in `ch2.html` and independently verified correct, including recomputation of every worked-example number they touch. The four numeric corrections the fix log claims are confirmed correct in full-precision Python. No arithmetic, HTML, cross-reference, or asset defect was introduced by the fix. No new defect was found to correct in this pass; `ch2.html` was not modified during EDIT2.
