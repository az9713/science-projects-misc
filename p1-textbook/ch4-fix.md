# ch4-fix.md — Fix-stage report for Chapter 4

Applied `ch4-edit.md` to `ch4.html` in place. Cross-chapter rules applied throughout: speed-deviation
glyph kept as Δω with no bar (ch1's Δω̄ noted for contrast only, in the notation-table
meaning cell); infinite-bus voltage rule is not applicable to this chapter (chapter 4 has
no infinite-bus references, only V_L at the load bus); chapter file names left as
`ch1.html`–`ch4.html` and all new cross-chapter links use those names; every hex colour
literal below `:root` replaced with `var(...)` (one instance, L18); ch1's exact example
numbers (1.4913 / 8.9618 / 0.4397) are not referenced anywhere in chapter 4, so no
occurrence needed changing.

## 1. Blocking defects

1. B1 — applied. Sweep definition (§4.2.4) rewritten as six numbered rules; rule 2 now
   states the common-dispatch-scaling factor explicitly, with the c = 20% worked check
   (0.9713 factor, unit 1 at 0.7285 pu).
2. B2 — applied. Added the four diagonal conductances G_11..G_44, the derivation of why
   diagonal susceptances drop out, the unit-1 self-term worked example (27% of dispatch),
   and the without-diagonal check (0.2193/0.1448/0.0537/0.0383 pu). Caption updated to name
   both transfer and self-conductances.
3. B3 — applied. Inserted the three-line derivation of Model 4.2 (current, complex power,
   real part) plus the sign convention for B_ij, between equation (4.2) and the
   Assumptions paragraph.
4. B4 — applied. Theorem 4.5 restated with three explicit numbered assumptions, an
   explicit definition of Δω_COI, a tightened proof, and a new "Where the hypotheses bind"
   paragraph. Added the Δω_COI bullet to the §4.2 local notation panel. Added the
   stays-connected sentence to Example 4.1's E_kin,sys line.
5. B5 — applied. Inserted the "Terms used in this chapter" panel (nine terms of art plus
   headroom) after the chapter notation table.
6. B6 — applied (primary fix, no renumbering, as the edit file allows). Example 4.1's
   citation of "Citation 4.7" before it exists is replaced with a self-contained figure
   and a forward pointer ("§4.5 restates it..."); same fix applied to the Fig. 4.3 caption.
7. B7 — applied. Removed the Great Britain attribution from the S16 (Ireland DS3) citation
   in both §4.3 and §4.5, in both places the figure is used, and added the sentence noting
   the book's source list has no Great Britain loss-of-mains entry. Exercise 4.1's answer
   text needed no change, as the edit file notes.
8. B8 — applied. Opening paragraph rewritten: synchronous condensers are now defined at
   first use, and the sentence "they do no useful work" (which contradicted §4.5
   Constraint 3) is removed.

## 2. Line-level rewrites

L1 applied · L2 applied · L3 applied · L4 applied (citation copied from `ch2.html:279`
Kundur 1994, verified present there) · L5 applied · L6 applied · L7 applied · L8(a)(b)(c)
applied (R28/R32 citation corrected to R33/Corollary 3.8, with R32 and R28 kept for the
virtual-synchronous-machine specialisation) · L9 applied · L10 applied · L11 applied ·
L12 applied · L13 applied · L14 applied · L15 applied · L16(a)(b)(c) applied (80–95%
sweep extension added to the §4.2.4 prose, Exercise 4.5 answer, and chapter summary) ·
L17(a)(b) applied (Fig. 4.5 order marked "as drawn ... not read from S14 — verify", box
label changed to "further loss + embedded", caption rewritten) · L18 applied ·
L19 — superseded by L27: L27's own replacement text already carries the corrected journal
name ("IEEE J. Emerging and Selected Topics in Power Electronics"), so applying L27 also
satisfies L19; no separate edit was needed or possible once L27 was applied, since the
quoted L19 text no longer exists after L27. L20 applied · L21 applied · L22 applied ·
L23 applied · L24 applied · L25 applied (sentence + table) · L26 applied · L27 applied ·
L28 applied · L29 applied · L30 — same item as L17(b), applied there.
L31 applied.

## 3. Structural notes

S1 — skipped. Cross-chapter rule for this fix pass fixes the glyph as Δω (no bar) rather
than Δω̄, which is the opposite resolution from the one S1 offers as its default ("if the
bar stays..."). The interim patch L21 already gives the correct chapter-4 wording under
the no-bar decision, so S1's own edit (adding bars throughout ch4) is not applied; this
is a deliberate cross-chapter decision, not an oversight.

S2 — applied. Every plain occurrence of R01, R03, R04, R05, R06, R11 (linking to
`ch1.html`) and R24, R25, R26, R28, R30, R32, R33 (linking to `ch3.html`) in the chapter's
prose is now an anchor link per the table in `ch4-edit.md`. Chapter 4's own results
(R34–R40) are left as plain text/local numbers, since S2's anchor map covers only
cross-chapter targets. File names kept as `ch1.html`–`ch4.html` per the note in S2 (using
the names on disk rather than renaming to `ch0N.html`); that is a plan-level naming
decision (plan §5.3), out of scope for a single-chapter fix.

S3 — applied. Added Remark 4.1 (R_p ≠ ΔP limit case) after Theorem 4.6, before §4.4.1.

S4 — no chapter change needed, as the edit file itself states: this is a note that the
departure from the plan (treating (4.10) as a screening formula, not a bound) should be
recorded in the plan's Chapter 4 spec. That is a `book-plan.md` edit, which this fix stage
is explicitly not to touch.

S5 — no chapter change needed beyond B7 (already applied). S5's own action item is a
plan-level fix (add a new source id S21 for the Great Britain loss-of-mains document to
`book-plan.md`); out of scope for this chapter-only pass.

S6 — skipped. The suggested cuts assume a book-wide front-matter section will absorb the
"How to read the results" box; no such front matter exists yet (each chapter currently
carries its own copy), and this fix pass touches only `ch4.html`. Deleting the box, or the
§4.6.1 recap, or the exercise-answer sentences, without a receiving home for that content
would remove material from the book rather than deduplicate it. Word-count is advisory
(19% over target), not a blocking defect, so it is left for a book-level pass that can
coordinate all four chapters and create the shared front matter. No chapter change made.

S7 — applied. Added the "reader can now do..." closing paragraph after the chapter
summary.

S8 — applied. Added the m_p = 0.05, ω_c = 5.0 rad/s (0.80 Hz) derivation after the TS4
description in §4.1.3, tying the converter H_eq/K_D,eq pair back to Chapter 3's droop law.

S9 — no chapter change needed, as the edit file itself states ("no chapter change" is in
S9's own heading). All three sub-items are `book-plan.md` edits (add `cit` to the plan's
result-class list; add "stated here" to the plan's status-word list; note on citation
locators), out of scope for a single-chapter fix.

## 4. Checks run

- Python `html.parser` well-formedness check: no tag mismatch, no unclosed tag, no
  duplicate `id` attribute. Stack empty at end of file.
- Zero-external-asset check: 0 `<script>`, 0 `<link>`, 0 `<img>`, 0 `src=`, 0 `data:` URI,
  0 `http://` or `https://` occurrences. 33 `<a href="...">` links, all internal
  same-book anchors (`ch1.html#...`, `ch3.html#...`, or `#...`); none external.
- Hex-colour-literal check: the only hex literals remaining in the `<style>` block are the
  eight `:root` custom-property definitions themselves; every use below `:root` is
  `var(...)`.

## Not done

Nothing from the numbered blocking defects or line-level rewrites was skipped. Three
structural notes (S1's own default resolution, S6, and part of S2's file-naming question)
were deliberately not applied, and S4/S5/S9 need `book-plan.md` changes that this
chapter-only fix stage does not make; reasons are given above under each item. No other
chapter was edited.
