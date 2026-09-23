# Chapter 3 fix log — `ch3-fix.md`

One line per `ch3-edit.md` item number. All edits applied bottom-of-file-upward, matched on quoted text (not line number alone), verified by unique-substring match before write.

1. Applied — malformed `<sub>D</var>` tag fixed; parses clean.
2. Applied — dVOC reduction rewritten with ΔE = 0 stated as an explicit assumption; second (dropped) term shown and justified.
3. Applied — "(3.22) gives" corrected to "(3.21) gives".
4. Applied — "11 %" corrected to "9.1 %", with both ratios (0.0909 and 11.0) shown.
5. Applied — "interact with the current loop" replaced with the swing-mode/protection-timing argument, sourced to R14, R07, R08, Example 1.2.
6. Applied — "better conditioned as impedance rises" replaced with the terminal-magnitude/network-limit argument (R06, R18, Example 2.1).
7. Applied — E_res defined in prose before first use in (3.30).
8. Applied — two-part fix: (a) Q_f, δ, RoCoF, headroom added to the notation list; (b) (3.31) rewritten with the active-current condition stated and a vector-addition caveat added.
9. Applied — Great Britain loss-of-mains clause removed from the S16 (Ireland-only) citation; note added that the book's source list holds no GB document.
10. Applied — SVG label "(3.8) and (3.8)" corrected to "(3.8) and (3.9)".
11. Applied — "global convergence proof" softened to "cited almost-global synchronization proof (Remark 3.3)".
12. Applied — same overstatement corrected in §3.5 opening; sentence also split.
13. Applied — "vendor data sheets" claim narrowed to grid codes and sourced to S17.
14. Applied — the 1111 ratio given its two ratings (1 MVA / 100 MVA) at first mention.
15. Applied — Remark 3.1 rewritten: unsourced "published designs use all three" cut; S07 claim narrowed to what a design paper can carry.
16. Applied — 33-word sentence split into three.
17. Applied — Fig. 3.1 caption split; 38-word sentence broken up.
18. Applied — "published as a short note ... that is why" (asserted motive) replaced with the factual "two-page letter".
19. Applied — "ten times as damped" corrected to a coefficient statement (20 pu vs 2 pu), with ζ's dependence on H and ω_n stated separately.
20. Applied — Model 3.4 assumptions paragraph rewritten with the second-order loop shown and the "filter fast" condition quantified (4.0% at the stated numbers).
21. Applied — "built on exactly this" (48-word sentence) split and de-flourished.
22. Applied — Δf given an explicit unit/definition pointer at first prose use.
23. Applied — per-unit vs watts distinction for P and ΔP in (3.14)/(3.18) stated once.
24. Applied — "That is the whole trick" replaced with a content sentence naming the mechanism.
25. Applied — (3.19) reframed as one modeled operating mode, not a universal claim about devices.
26. Applied — Remark 3.3 closing sentence split into two reasons.
27. Applied — "(3.24) to (3.27) are proved here" now carries "under ΔE = 0".
28. Applied — Theorem 3.7: "symmetric operating point" given its own defining sentence; ΔE = 0 inheritance stated.
29. Applied — Table 3.1 dVOC row: ΔE = 0 assumption added to the cell.
30. Applied — Fig. 3.5 caption: matching-control tuning flagged as a thought experiment with the 2.78 F / 139× figures shown; sentence also de-conflated.
31. Applied — "merge above about 10 rad/s" replaced with the actual ratios (1.11 at 10 rad/s, 1.013 at 30 rad/s).
32. Applied — Corollary 3.8 statement: three background assumptions (pure reactance Z_f, ΔE = 0, δ definition) stated explicitly.
33. Applied — Corollary 3.8(b) proof: sign convention for a falling frequency (δω negative, energy is the magnitude) made explicit.
34. Applied — "thousands of times more" replaced with a worked number (100 MW × 1 h = 100 MWh = 360 GJ = 22,500× the 16 MJ).
35. Applied — "the bound that usually binds" tied to the Chapter 4 sizing case (R39) instead of left as an unsupported claim.
36. Applied — Exercise 3.5 statement: the four tunings that give H_eq = 2 s spelled out (droop, VSM, matching-control thought experiment, dVOC).
37. Applied — Exercise 3.5 answer: 67-word/six-number sentence split into four shorter sentences.
38. Applied — "against a real fleet" corrected to "a design fleet that Chapter 4 defines, not a published one", matching the Chapter 4 plan spec.
39. Applied — inserted new §3.7.5 "What the reader can now do" closing section immediately before the Exercises `<hr>`, per the plan's Outcome 3.
40. No action — length is informational only ("Not blocking"); no cut requested.
41. Skipped — plan correction targeting `book-plan.md` Example 3.1 spec wording. Out of scope: task instructions say do not edit `book-plan.md`. No chapter text depends on this; item 5's replacement already carries the corrected physics independent of the plan wording.
42. Skipped — plan correction targeting `book-plan.md` §5.2 / `HANDOFF.md` source attribution. Out of scope: do not edit `book-plan.md`. The chapter-side fix is item 9, which is applied.
43. Applied (both parts) — (a) non-palette hex literals `#16213a` and `#20304a` replaced with new `var(--eqbg)` / `var(--thbg)` custom properties (added to `:root`) at all 8 occurrences (lines were in the main `<style>`, notation-card CSS, and five SVG `<style>`/attribute spots), satisfying the cross-chapter rule "replace hex colour literals below :root with var()". (b) added a second, kind-naming class (`def`, `model`, `thm`, `cor`) to the 8 result `<div>` elements that only carried `class="res"` (definition, three models, two theorems, the corollary); `ex` and `rem` kinds already had their class. Left unfixed: the ~76 remaining hex literals inside the five SVG `<style>` blocks that repeat the chapter's own palette values (e.g. `#334155` = `--bd2`, `#1e293b` = `--card`/`--bd1`) — the editor's note explicitly marks this "low severity" / "fix if strictness is wanted", and `--card` and `--bd1` share one hex value, so a blanket substitution would require guessing which variable each SVG shape means; left as literals to avoid introducing a wrong semantic mapping, consistent with the rest of the book's diagrams.
44. Skipped — recommends the plan owner add `stated here` to `book-plan.md` §5.4's status-label list; explicitly "Recommend that the plan owner add ... rather than change the chapter." No chapter edit implied.
45. No action — file-naming note; confirms chapter already uses `ch1.html`–`ch4.html` convention and contains no cross-chapter `href` to break. Matches the cross-chapter rule as given.
46. Skipped — recommendation for the plan owner's Chapter 4 figure spec (Fig. 3.4 per-MVA vs absolute bar chart); not a Chapter 3 chapter-text edit.

## Cross-chapter rules (applied within this chapter only)

- Speed-deviation glyph: chapter already uses `&Delta;&omega;`/`&delta;&omega;` (Δω / δω) with no overline throughout; no bar-glyph instances found, no change needed.
- Infinite-bus voltage: chapter has no "bare V" standing for an infinite-bus voltage (only `V_g`, grid source voltage in a finite-network model, and one unrelated `&infin;` limit in §3.5); no change needed.
- Chapter file names `ch1.html`–`ch4.html`: chapter contains no cross-chapter `href`; already compliant (see item 45).
- Hex colour literals below `:root` replaced with `var()`: done, see item 43(a).
- Ch1 exact example numbers 1.4913 / 8.9618 / 0.4397: not restated at that precision anywhere in Chapter 3 (the chapter's own convention, already verified correct by the editor in item 50/98/99, quotes K_s as 1.491 pu/rad and δ0 as 0.4924 rad); no ch1.html edit made (out of scope) and no ch3.html contradiction found.

## Verification

- `html.parser` well-formedness check: 0 errors (was 1, from item 1, now fixed).
- Zero-external-asset check: no `<script>`, `<link>`, `<img>`, `http(s)://`, or `data:` anywhere in the file — 0 matches on every check.
- Spot recompute of item 4: 0.3183 / 3.5 = 0.0909 → 9.1 %, matches the applied replacement text.
