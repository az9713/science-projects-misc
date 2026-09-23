# Chapter 1 fix log

Applied to `ch1.html` from `ch1-edit.md`, bottom-up by content match (not line number,
since the editor's own line numbers were the drafted-file numbers and several had already
drifted by one or two lines from later edits; every change was matched on quoted text).

## Part 1 — Blocking defects

1. Applied. Mass-spring-dashpot triple corrected: dashpot is now K_D/ω0, derivation of Δδ
   written out.
2. Applied (all four sub-parts): Theorem 1.8 hypothesis (P_e = 0 during fault, δ_max
   defined) moved into the statement; A_acc/A_dec redefined as signed integrals with the
   rectangle special case named; change-of-variable validity argument added; Assumptions
   list gains (v) with the re-derivation note for a fault at a remote bus.
3. Applied (both sub-parts). Fig. 1.3 caption and Exercise 4 answer both rewritten to give
   the window-dependence of the bisection value (0.1703 s / 0.1701 s / 0.170085 s for
   1.2 s / 1.5 s / 3 s windows) instead of the unsupported single figure 0.17009 s.
4. Applied. E′ and X′_d defined in prose inside Model 1.5's statement.
5. Applied. "Synchronous generator" defined at first use in §1.1.
6. Applied. ζ introduced by name with a forward pointer to its §1.5 definition; "badly
   damped" replaced by the decay-time measurement (factor e in 7.0 s).
7. Applied. Citation date corrected: the 2004 classification, not the 1994 textbook.
8. Applied (all four sub-parts, recomputed and verified independently before writing):
   line 874-area product 14 × 0.623166 = 8.724324 (was printed 8.724319); line 876 sqrt
   argument matches; Exercise 3's 376.9911 × 0.0159407 = 6.0095 (was × 0.015941); Exercise
   5's log-ratio now uses the unrounded 0.0105438/0.0210875 and states the rounded-table
   value separately as −0.5003.

## Part 2 — Line-level rewrites

9. Applied. Derivation of (1.8) written out in four phasor-algebra lines; I and S
   introduced; the closing per-unit remark's bare `V` changed to `V_inf` for consistency
   with the "never bare V" rule.
10. Applied. E_kin now explicitly evaluated at the rated mechanical speed 2ω0/p.
11. Applied. Torque base defined; the "equal only at rated speed" line rewritten with the
    explicit 1 + Δω factor.
12. Applied. Step 2 rewritten to substitute the rated speed explicitly rather than silently.
13. Applied. Governor defined in a parenthetical at first use.
14. Applied. Damper windings defined; "a little" removed.
15. Applied. "Electrical energy is not stored in the network" softened to the accurate
    half-cycle-exchange statement.
16. Applied. "The only store large enough" now carries the 200 MVA / 700 MJ / 3.5 s numbers.
17. Applied. "Well under half" replaced by the 0.444 s / 22% measurement.
18. Applied. "A system operator will not accept..." replaced by the 36.8%-after-ten-swings
    measurement; S01 Ch. 12 citation kept.
19. Applied. "Completely" dropped from the chapter's opening claim.
20. Applied. "A sensible answer" replaced by "four assumptions, listed in Model 1.5."
21. Applied. "So much larger" replaced by "does not measurably move the system voltage or
    frequency," with the Chapter 4 pointer.
22. Applied (both sub-parts). "Round-rotor" and "salient-pole" defined in place.
23. Applied. Fault clarified as being at a bus, with the pure-reactance path stated as the
    reason P_e = 0.
24. Applied. Fig. 1.1 caption's δ_max forward-reference rewritten to describe the angle
    without naming it, deferring the name to §1.6 as before.
25. Applied (all three sub-parts). δ_0 now defined in §1.4 (new paragraph before Fig. 1.1);
    the §1.5 equilibrium paragraph rewritten to reference that definition; the notation
    table's δ_0 row moved to §1.4.
26. Applied. I and S added to the local notation list (also serves item 9's needs).
27. Applied. All 19 hex colour literals below `:root` (lines ~78, 88-102, 114 of the
    drafted file) replaced with `var(--bg)`, `var(--border2)`, `var(--accent)`,
    `var(--accent2)`, `var(--muted)`, `var(--text)` as appropriate. Zero hex literals now
    appear below the `:root` block (verified by regex scan after the edit).
28. Applied. `id="s1-8"` renamed to `id="s1-ex"` on the Exercises heading.
29. Applied (all three sub-parts). The two over-25-word sentences at the per-unit
    transformer section split into shorter ones; the Fig. 1.4 (now Fig. 1.2) axis-stretch
    sentence rewritten with the precise 10.2× figure in place of "about ten times."

## Part 3 — Structural notes (local to this chapter)

30. **Applied.** Figures renumbered to document order: old Fig. 1.4 (eigenvalues) -> new
    Fig. 1.2; old Fig. 1.2 (areas) -> new Fig. 1.3; old Fig. 1.3 (integration) -> new
    Fig. 1.4; Fig. 1.1 unchanged. Updated: 4 `<figure id>` values, 4 caption bold-prefixes,
    and the Exercise 4 in-prose reference to the integration figure (now "Fig. 1.4"). The
    two references that should stay as Fig. 1.1 ("Fig. 1.1 shows exactly that" and "The
    same curves as Fig. 1.1") were left untouched, as instructed. Not done: updating
    book-plan.md's figure list — that file is off-limits for this stage.
31. **Applied.** Moved the ~87-line notation block (book-wide table + local-symbol list)
    from before §1.2 to a new, unnumbered subsection "Notation of this chapter" (`id=
    "s1-notation"`) after §1.6.3 and before the Exercises. Left the one-sentence pointer
    at the old location, worded as instructed.
32. **Applied.** Added the "What you can now do" paragraph at the end of §1.6.2, before
    §1.6.3, exactly as given.
33. **No change made** (as instructed): the plan's rounded intermediates (K_s = 1.4915,
    ω_n = 8.963, cos δ_cr = 0.4401) are superseded by the chapter's exact values (1.4913,
    8.9618, 0.4397/0.439685), which are unchanged in this fix pass. Confirmed present:
    `1.4913` ×2, `8.9618` ×8, `0.439685` in Example 1.2.
34. **Overridden by the task's cross-chapter rule, not skipped.** ch1-edit.md's own
    recommendation was "do not change Chapter 1's glyph; resolve in Ch. 3/4 instead," but
    the fix-stage instructions for this run fix the book-wide glyph as Δω (no bar). All 40
    occurrences of `<var>Δω̄</var>` (34 original + 6 introduced by items 1/2/11/12/25 above)
    were changed to `<var>Δω</var>`. Two prose spots that described the bar were rewritten
    so the text stays true: the local-notation-list bullet at "Δ before any other symbol"
    (previously "the single symbol Δω̄, with a bar, is not a perturbation") and nothing
    else referenced the bar. The book-wide notation-table row and Definition 1.2 needed no
    further wording change beyond the symbol swap.
35. **No edit made** (as instructed — human citation check only, not a text fix). The six
    citations item 35 flags (lines ~330/379/1095 area for S01, plus 711, 1050, and the S04
    Ch. 2 fault-clearing-time citation) are unchanged; `verify` marks are all intact.
36. **Partly applied, partly overridden.** Renaming the file to `ch01.html` is overridden
    by this run's cross-chapter rule (chapter files stay `ch1.html`..`ch4.html`); kept
    `ch1.html`. The duplicate local-notation entry (D, D_load, D_v, D_eq, which repeated
    the §1.3 notation-decision box almost word for word) was shortened to a one-line
    pointer to that box, per the "cut one of the two" instruction. Word-count trim (8,310
    -> plan's 6,500 ± 20%) not pursued as a separate task; item 31's move does not remove
    words, as the editor noted, and no further trimming was requested by the fix-stage
    brief.
37. **Not run**, as instructed (task rule: parser check only, no browser render). A 360 px
    render check was not performed.

## Checks run

- Python `html.parser`-based tag-stack well-formedness check: no mismatched or unclosed
  tags after all edits (including the figure renumbering and the notation-block move).
- Zero-external-asset check (`https?://`, `<link`, `<script src=`, `@import`, `url(http`):
  no matches. The file is still fully self-contained.
- No `chNN.html`-style filename references exist inside `ch1.html` itself, so the
  "chapter files are ch1.html..ch4.html" cross-chapter rule needed no in-chapter edit.
- Recomputed independently before writing: 14×0.623166=8.724324; 376.9911×0.0159407=
  6.0095 (unrounded 6.00950...); log(0.0105438/0.0210875)/log(4)≈−0.499997 (≈−0.50000,
  matches the printed unrounded claim); log(0.01054/0.02109)/log(4)≈−0.50034 (matches the
  printed rounded-table claim).

## Not done / left for a later pass

- book-plan.md §5's figure list and §5.3's `ch01.html` filename are not updated — that
  file is out of scope for this fix stage.
- Item 35's six citation locations still need a human check against the actual sources
  (S01 chapter/section, S04 Ch. 2); no change made to any citation text.
- Item 37's 360 px browser render check was not performed (parser-only stage per brief).
