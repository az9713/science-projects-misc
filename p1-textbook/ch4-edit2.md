# ch4-edit2.md — EDIT2 verification of the ch4-fix.md pass

**ACCEPT**

Verified `ch4-fix.md` against `ch4-edit.md` (blocking items B1-B8, line-level rewrites
L1-L31, structural notes S1-S9) and the fixed `ch4.html`. Every blocking item and every
line-level rewrite checked in `ch4.html` is present, correctly worded, and numerically
exact. Independent Python recomputation of the chapter's key worked numbers — the sweep
scaling factor, the reduced-network conductance matrix, the four-mode eigenvalue sweep out
to 95%, the frequency-nadir RK4 check, and the sizing-case ratios — reproduces every
printed digit. No defect, of any size, was introduced by the fix. Nothing was changed in
`ch4.html` during this EDIT2 pass; none was needed.

## 1. Blocking items — item-by-item check

- **B1** (self-contradicting sweep definition, ch4.html:817-846). Fix replaces lines
  704-712 with the six-rule sweep definition, including the c = 20% worked check
  (unscaled sum 648.6 MW, factor 0.9713, unit 1 at 0.7285 pu). Recomputed independently in
  Python from the rating and dispatch rules: unscaled sum = 648.5714... MW ≈ 648.6,
  factor = 630/648.5714 = 0.971366 ≈ 0.9713, unit 1 pu = 0.75 × 0.971366 = 0.728524 ≈
  0.7285. Exact match. **Confirmed correct.**
- **B2** (unreproducible reduction check, ch4.html:443-478). Fix adds the four diagonal
  conductances G_11..G_44 and the with/without-diagonal check. Recomputed the full 5-node
  Ybus (four internal nodes + bus L with load admittance 0.6300 − j0.1200 pu), Kron-reduced
  to the 4×4 Y_red, and confirmed every printed value: off-diagonal B_12=0.2555,
  B_13=0.3043, B_14=0.1529, B_23=0.2011, B_24=0.1010, B_34=0.1203 pu; off-diagonal
  G_12=0.0465, G_13=0.0553, G_14=0.0278, G_23=0.0366, G_24=0.0184, G_34=0.0219 pu;
  diagonal G_11=0.0703, G_22=0.0307, G_33=0.0436, G_44=0.0110 pu. Substituting the printed
  equilibrium (E_i, δ_i) into (4.2) with the diagonal term returns P_e = 0.3000, 0.1800,
  0.1000, 0.0500 pu exactly (also cross-checked against direct S = V·conj(I) power flow,
  same result to 4 decimals); without the diagonal term it returns 0.2193, 0.1448, 0.0537,
  0.0383 pu exactly as printed. **Confirmed correct.**
- **B3** (Model 4.2 unproved, ch4.html:333-378). Derivation inserted between the equation
  and the Assumptions paragraph; present and reads correctly (three-line derivation plus
  the B_ij sign-convention note). **Confirmed present and correct.**
- **B4** (Theorem 4.5 imprecise, ch4.html:847+). Restated with the three numbered
  assumptions, the Δω_COI definition, tightened proof, and the "Where the hypotheses bind"
  paragraph — all present. Δω_COI bullet added to the §4.2 notation panel; the
  stays-connected sentence added to Example 4.1's E_kin,sys line. Recomputed the two
  Example 4.1 headline numbers this theorem feeds: RoCoF₀ = 50×1000/(2×200 000) = 0.250
  Hz/s and Δf_nadir = −50×1000×10/(4×200 000) = −500 000/800 000 = −0.625 Hz — both match.
  **Confirmed correct.**
- **B5** (nine undefined terms of art). "Terms used in this chapter" panel present after
  the chapter notation table, with all nine terms (synchronous condenser, infeed/loss of
  infeed, governor/deadband, primary response, headroom, low-frequency demand
  disconnection, embedded generation, loss-of-mains protection/islanding) defined.
  **Confirmed present.**
- **B6** (forward reference to Citation 4.7). Example 4.1's "Reading" paragraph
  (ch4.html:1245-1252) now reads "That is the frequency at which Great Britain's
  low-frequency demand disconnection acted on 9 August 2019 [S14 ...]. §4.5 restates it
  with the event's two other figures as Citation 4.7" — a forward pointer, not a premature
  use of an undefined citation. Citation 4.7 itself is first defined at line 1331, in
  §4.5, consistent with this being a pointer rather than a use. Fig. 4.3 caption fix also
  present. **Confirmed correct — the forward-reference defect is resolved.**
- **B7** (Great Britain figure wrongly attributed to Ireland's S16 source). Both instances
  (ch4.html:1063 area, and the ENTSO-E paragraph) now cite the 1 Hz/s figure to Ireland's
  DS3 programme only, and state "This book's source list has no entry for the
  corresponding Great Britain loss-of-mains setting, so no Great Britain value is printed
  here." **Confirmed present and correct.**
- **B8** (wrong opening sentence). Lines 129-138 now open with a correct definition of a
  synchronous condenser (supplies reactive power, short-circuit current, inertia; "on
  average it generates no active power") and no longer claim the machines "do no useful
  work," removing the contradiction with §4.5 Constraint 3. **Confirmed correct.**

## 2. Line-level rewrites — spot checks (representative sample plus every item touching a
number)

- **L1, L5, L23**: the sizing-case numbers in the new opening (§4.5) — 179.2 MJ, 4 032 000
  MJ, factor 22 500, 224 MW, 0.20 pu — all recomputed from the stated formulas
  (2×E_kin,fleet×Δf/f₀ etc.) and match to the printed digit, including 4 032 000/179.2 =
  22 500 exactly and 22 500 = 10^4.35 to two decimals (log₁₀22500 = 4.3522).
- **L16** (eigenvalue locus beyond 80%). This is the most demanding numerical claim in the
  fix. Built the full linearized 4-machine/converter small-signal model from the chapter's
  own TS4 data (ratings, H, K_D, reactances, the B1 sweep rule, and the Y_red from B2),
  linearized the power-angle Jacobian at each operating point, and computed eigenvalues at
  c = 20%, 80%, 85%, 90%, 95% in Python. Independent result: c=20% gives −2.2151+j17.3463
  (ζ=0.1267); c=80% gives −0.7671+j12.9359 (ζ=0.0592); c=85% gives −0.5839+j12.7436
  (ζ=0.0458); c=90% gives −0.4028+j12.6077 (ζ=0.0319); c=95% gives −0.2581+j12.5296
  (ζ=0.0206) — exact matches to the chapter and to the fix's added table, including the
  claim that this mode is never the least-damped one (the machine mode's ζ traces
  0.0136→0.0187→0.0203→0.0212→0.0185, staying below the tracked mode at 80-95%, and the
  crossing of ζ=0.05 between 80% and 85% is confirmed: 0.0592 → 0.0458).
- **L25** (RK4 numerical check table for damped ramp). Independently simulated the stated
  first-order ODE (2E_kin,sys/f₀)dΔf/dt = −ΔP+ΔPt/T−D_load·Δf by RK4 at step 1e-4 s for
  D_load = 0, 500, 1000, 2000 MW/Hz. Recomputed nadir/time pairs: (−0.6250, 10.000),
  (−0.4464, 7.768), (−0.3513, 6.487), (−0.2494, 5.011) — exact match to all four rows of
  the table the fix inserted.
- **L26**: 4 032 000/224 = 18 000 s = 5.0 h, and 3600/0.0144 = 250 000 — both recomputed
  and exact.
- **L4, L8, L9, L10-L15, L17-L22, L24, L27-L31**: read in place in `ch4.html`; wording
  matches the specified replacement text, citations point to real chapters/lines (L4's
  Kundur citation, L8's R33/Corollary 3.8 references), and no residual reference to the
  superseded R28/R32-only citation or the old JESTPE abbreviation (L19/L27) remains.

## 3. Structural notes — check

Matches the fix log's own accounting; nothing further to add:
- S1 — correctly left unresolved as a deliberate cross-chapter decision (no-bar glyph);
  L21's interim wording is present and consistent with that choice.
- S2 — anchor links present for cross-chapter R-numbers; sampled several (`ch1.html#def-1-1`
  style links) and found them well-formed and pointing at plausible ids.
- S3 — Remark 4.1 present after Theorem 4.6.
- S4, S5, S9 — correctly deferred as `book-plan.md`-level edits, out of scope for a
  chapter-only fix; ch4.html requires no in-chapter change for these.
- S6 — correctly left unresolved; the word-count item is advisory, not blocking, and
  cutting the box/recap without a receiving home would delete content rather than
  deduplicate it.
- S7 — closing "reader can now do..." paragraph present after the chapter summary.
- S8 — m_p = 0.05, ω_c = 5.0 rad/s (0.80 Hz) derivation present in §4.1.3; recomputed
  ω_c = 1/(2×0.05×2.0) = 5.0 rad/s exactly.

## 4. Defects introduced by the fix

None found. HTML re-checked with Python's `html.parser`: tag stack empty at end of file,
zero duplicate `id` attributes. Zero-external-asset re-check: 0 `<script>`, 0 `<link>`,
0 `<img>`, 0 `http://`/`https://`, 0 `data:` URIs. Hex-literal re-check: the only
remaining hex literals in the `<style>` block are the eight `:root` custom-property
definitions; L18's fix (`background:var(--bg)`) is present at line 93 and no
`background:#17233a` literal remains.

## 5. Residual items (not blocking, carried forward at book level)

Same three categories the fix log names, none of which is this chapter's to close:
1. **S1** — the book-wide Δω vs Δω̄ glyph decision is still open; chapter 4 keeps the
   no-bar convention documented in L21 until that book-level call is made.
2. **S4, S5, S9** — three `book-plan.md` edits (recording the (4.10) screening-formula
   departure, adding a Great Britain loss-of-mains source id, and two result-class/status
   vocabulary additions) remain to be made in the plan file, not in `ch4.html`.
3. **S6** — the word-count item (19% over target) and the "How to read" box duplication
   across chapters remain for a book-level pass once shared front matter exists; no
   single-chapter fix can resolve this without deleting content.

No new residual items were found during this verification pass.
