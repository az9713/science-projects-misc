# Chapter 2 fix log

File edited: `ch2.html`. Edit source: `ch2-edit.md`. Cross-chapter items consulted: HANDOFF.md "Cross-chapter items" paragraph and the computed-task cross-chapter rules for this chapter.

One line per edit item. "Applied" means the exact change (or the described fix, where no literal replacement text was given) is now in `ch2.html`.

## Blocking defects

- B1 (equation (2.13) derivation, θ_p link to θ_pll/θ_g, assumption 5, status line) — applied.
- B2 (θ_p tied to θ_pll and ω_0; notation entries, stiff-grid derivation, Theorem 2.8 opening and statement) — applied.
- B3 (Definition 2.5: S_sc at nominal voltage, not at V_g; X_g = 1/SCR holds for symbolic V_g) — applied.
- B4 (bare V split into V_m for the §2.1 peak amplitude and V_inf for the Chapter 1 K_s formula; two notation entries added) — applied at all 7 locations (lines with v_a, v_d=V, V=1pu, and the four K_s formula instances at the summary card, prerequisites [via R13], Table 2.1, Exercise 6).
- B5 (Corollary 2.10 timescale hypothesis: PLL settling time vs. swing period, R08 citation) — applied.
- B6 ("every weak-grid symptom falls out of K_pll" corrected to exclude the oscillatory instability; §2.6.3 pointer added) — applied.
- B7 (fault-current ratio range 0.157–0.260, not 0.220/0.186) — applied.
- B8 (S07 citation completed with title and location) — applied.
- B9 (two "symbols defined below" pointer sentences, in the summary card and before the problem-statement paragraph) — applied.
- B10 (Fig. 2.4 caption: cite S08 for the oscillatory-instability claim instead of an unsupported field-evidence claim) — applied.
- B11 (bandwidth/damping fall as √K_pll, not the same fraction as voltage/power; both instances, §2.6.2 reading and closing summary) — applied.

## Line-level rewrites

- R1 (§2.1 lede: replace universal claim with measured claim) — applied.
- R2 ("obvious" → "one control input on each axis") — applied.
- R3 ("well before" → exact current 0.707·bound) — applied.
- R4 ("well below" → "against", redundant hedge removed) — applied.
- R5 (superseded by B11) — applied via B11.
- R6 ("uncomfortable" → "limits its reach") — applied.
- R7 (current-controller gain units derived: Ω and Ω/s in SI, pu/pu·s in per unit) — applied.
- R8 (per-unit converter voltage formula made executable) — applied.
- R9 ("microseconds" ×2 replaced with "fraction of one/a cycle", device physics marked out of scope) — applied.
- R10 (Exercise 2 answer: correct attribution, bases formula spelled out) — applied.
- R11 (38-word sentence split in two) — applied.
- R12 (55-word sentence split into four) — applied.
- R13 (line 118 prerequisites rewritten; carries the B4 V_inf fix for this location) — applied.
- R14 ("simply given" → "a given constant") — applied.
- R15 (superseded by B2's replacement text, which already opens "Take the stiff-grid case first") — applied via B2.
- R16 (four notation entries added: j, t, superscript T, V_pk,base) — applied.
- R17 (hex literals below `:root` replaced with `var()`: added `--card2`, `--eqbg`; `.ex` and `.eqn` now reference them) — applied. This also satisfies the cross-chapter rule on hex literals below `:root`.
- R18 (K_pll/K_s unit note — plan-level table change was out of scope since book-plan.md may not be touched; applied the fallback one-sentence clarification instead, in Theorem 2.7's proof) — applied via fallback, as the edit doc allows.
- R19 (S01 locator marked doubtful) — applied.
- R20 (S18 doubtful-source note added) — applied.
- R21 (S06 1.5-sample-period locator marked "location unconfirmed") — applied.
- R22 (S19 strength-classification citation) — no change, as the edit doc specifies.
- R23 (Rendering-convention paragraph moved out of the notation card into the closing conventions paragraph) — applied.

## Structural notes

- S1 (file name ch2.html vs. plan's ch02.html) — resolved by the cross-chapter rule for this run: chapter files are ch1.html..ch4.html; no rename needed.
- S2 (cross-chapter hyperlinks) — applied: every `<span class="rid">R0n</span>` for R01, R03, R04, R06, R07, R08 is now wrapped in `<a href="ch1.html#...">`, matched against ch1.html's actual anchor ids (def-1-1, def-1-3, model-1-4, lem-1-6, thm-1-7, ex-1-1). The closing cross-reference paragraph is updated to say which identifiers are linked and which (R24, R32, R33, R39, R40, in Chapters 3/4) are not yet, since those chapters' anchors don't exist and this run may not touch other chapters.
- S3 (local notation card moved above the §2.1 heading, right after the chapter's problem-statement paragraphs) — applied.
- S4 (promote §2.6.5 "what this chapter does not cover" to an unnumbered closing section after the exercises) — **skipped**. Reason: this is a larger structural move (relocating a whole subsection past the exercises and the ledger) with a real risk of breaking heading numbering or figure/exercise ordering, and the edit doc itself frames it as available room ("the plan fixes six sections, so keep the count") rather than a required fix; given the finish-by-8:30pm/usage-budget constraint, the higher-value blocking defects and rewrites were prioritized. The content is unchanged and correctly labelled where it sits.
- S5 (optional two-line identity added to Exercise 2's answer) — **skipped**, as the edit doc marks it optional ("if space allows") and the existing answer is already judged acceptable for a graduate reader.
- S6 (word count) — noted, not actioned: the edit doc anticipated the chapter would land about 2% over the 6,000–9,000 target band after B1/B2/B5, and accepted that overrun as an option. No cuts were made.
- S7 (Model 2.6 ledger status "derived in §2.5") — already correct after B1; no action needed.
- S8 (Fig. 2.1 "locked" caption) — already correct; no action needed.

## Numbers recomputed (edit-table corrections)

All 4 numbers the edit table marked wrong are now fixed in `ch2.html`:
1. Fault-current ratio range: 0.220/0.186 → 0.157 (1.1/7) and 0.260 (1.3/5) — via B7.
2. Exercise 5: 0.5528 × 7141.82 = 3947.99 → printed as 3948.00.
3. Exercise 5: √(0.9950/0.5528) = √1.8001 → printed as √1.8000 (exact value is 1.8000; root 1.3416 unaffected).
4. Exercise 5: ω_n,pll = 62.83 × 1.3416 = 84.29 rad/s → printed as 84.30 rad/s (and the derived 84.30/(2π) = 13.42 Hz).

## Checks run

- Python `html.parser` well-formedness check: tag stack balances to empty, zero errors.
- Zero-external-asset check: 0 `<script>`, 0 `<link>`, 0 `<img>`, 0 `http://`/`https://`, 0 `data:` URIs; one inline `<style>`; `color-scheme: dark` present; all hex color literals confined to the `:root` block.
- Equations (2.1) through (2.19) present, continuous, no gaps.
- 14 internal `<a href="ch1.html#...">` links added (S2), all pointing at ids confirmed present in `ch1.html`.
- No cross-chapter rule violation: Δω glyph rule does not apply to this chapter (ch2 has no speed-deviation Δω; that quantity belongs to the swing-equation chapters). V_inf used (matching ch1.html's actual `<var>V</var><sub>inf</sub>` rendering) everywhere the infinite-bus voltage appears; bare V eliminated. Chapter file references use ch1.html/ch2.html/ch3.html/ch4.html throughout. ch1's exact example numbers (1.4913 / 8.9618 / 0.4397) do not appear in ch2.html (not applicable to this chapter's content) and were left untouched.
- `book-plan.md` and other chapter files (ch1.html, ch3.html, ch4.html) were not modified.
