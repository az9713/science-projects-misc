# science-projects-misc

Seven science and mathematics projects, each built end to end by a fleet of Claude Code subagents. A single orchestrating session planned each project, split it into stages, and handed every unit of work (one chapter, one physics target, one theorem, one lesson) to its own subagent. About 125 subagents ran in total, across all seven projects.

The projects are independent. Each one has its own folder and its own final deliverable, which is a self-contained HTML page or a set of pages.

| Folder | Project | Final deliverable | Subagents |
|---|---|---|---|
| `p1-textbook/` | Graduate textbook: grid-forming inverters and power-system stability | `ch1.html` to `ch4.html` | 17 |
| `p2-physics/` | Reproduction of eight published physics results | `report.html` | about 33 |
| `p3-pde/` | Bake-off of five PDE methods on viscous Burgers | `report.html` | 11 |
| `p4-proofs/` | Proof arena: ten graduate theorems, proved and refereed | `t1-proof.md` to `t10-proof.md`, verdicts | 22 |
| `p5-sizing/` | Monte Carlo sizing study: battery storage replacing a synchronous condenser fleet | `design-memo.html` | 10 |
| `p6-blindspot/` | Blind-spot sweep of numerical linear algebra | `index.html` | 15 |
| `p7-explainers/` | Explainer series: power-system dynamics for programmers | `index.html`, `lesson1.html` to `lesson8.html` | 19 |

## Live pages

Every HTML deliverable is served by GitHub Pages. Click a link to open the rendered page.

| Project | Live pages |
|---|---|
| P1 textbook | [Ch 1: Machines that swing](https://az9713.github.io/science-projects-misc/p1-textbook/ch1.html) · [Ch 2: The limit of following](https://az9713.github.io/science-projects-misc/p1-textbook/ch2.html) · [Ch 3: Grid-forming control](https://az9713.github.io/science-projects-misc/p1-textbook/ch3.html) · [Ch 4: System stability and sizing](https://az9713.github.io/science-projects-misc/p1-textbook/ch4.html) |
| P2 physics | [Reproduction report](https://az9713.github.io/science-projects-misc/p2-physics/report.html) |
| P3 PDE | [Bake-off report](https://az9713.github.io/science-projects-misc/p3-pde/report.html) |
| P5 sizing | [BESS design memo](https://az9713.github.io/science-projects-misc/p5-sizing/design-memo.html) |
| P6 blind spots | [Numerical linear algebra index](https://az9713.github.io/science-projects-misc/p6-blindspot/index.html) |
| P7 explainers | [Series index](https://az9713.github.io/science-projects-misc/p7-explainers/index.html) · [1](https://az9713.github.io/science-projects-misc/p7-explainers/lesson1.html) · [2](https://az9713.github.io/science-projects-misc/p7-explainers/lesson2.html) · [3](https://az9713.github.io/science-projects-misc/p7-explainers/lesson3.html) · [4](https://az9713.github.io/science-projects-misc/p7-explainers/lesson4.html) · [5](https://az9713.github.io/science-projects-misc/p7-explainers/lesson5.html) · [6](https://az9713.github.io/science-projects-misc/p7-explainers/lesson6.html) · [7](https://az9713.github.io/science-projects-misc/p7-explainers/lesson7.html) · [8](https://az9713.github.io/science-projects-misc/p7-explainers/lesson8.html) |

P4 proofs are Markdown. GitHub renders them in the repository view: [theorems.md](p4-proofs/theorems.md).

## How the agent fleet works

Every project follows the same pattern. Claude Code's Workflow tool ran each stage as a script of `agent()` calls:

1. **One subagent per unit of work.** A chapter, a physics target, a PDE method, a theorem, a scenario, a subtopic, or a lesson each gets its own agent. The agent reads only its own inputs and writes only its own output files.
2. **Pipelines, not batches.** Each unit moves through its stages on its own, for example draft, then edit, then fix. Unit A can be in the edit stage while unit B is still in the draft stage. A barrier is used only where a stage needs all the earlier results together, for example a referee that compares all five PDE methods.
3. **Different roles for different models.** Drafting and code agents make the work. Separate judge agents (editors, referees, attackers, red teams) check it, and the judge is never the agent that wrote the work. Fix agents apply the judge's numbered findings. Cheap models do mechanical checks such as re-running scripts or building index pages.
4. **Structured returns.** Every agent returns a JSON object (status, files written, verdict, summary, skipped items with reasons). The orchestrator uses these to decide the next stage.
5. **Isolation between concurrent agents.** Up to about a dozen agents ran at once. Each agent got a unique prefix for its scratch files, so concurrent agents could not overwrite each other's work.
6. **Resumable prompts.** Every agent first checks whether its output already exists and is complete. If it does, the agent returns at once. This makes an interrupted run safe to relaunch.
7. **Computed, not asserted.** Agents ran every number they print. Scripts end with `assert`-based self-checks. Judges recompute the numbers and do not accept a drafter's claims without a check.

Models used: Claude Opus 5.5, Claude Sonnet 5, Claude Fable 5.1 and Claude Haiku 4.5, assigned by role as the tables below show.

---

## P1 — Graduate textbook: grid-forming inverters and power-system stability

**Folder:** `p1-textbook/`

A four-chapter graduate textbook. It starts with classical synchronous machines and ends with a system-level sizing case:

1. *The classical picture: machines that swing* — swing equation, synchronizing torque, equal-area criterion, critical clearing time.
2. *Inverter-based resources and the limit of following* — grid-following control, the phase-locked loop, and the short-circuit-ratio limit on weak grids.
3. *Grid-forming control: what it restores* — droop, virtual synchronous machines, dVOC, and DC-link sizing.
4. *System-level stability and a sizing case* — RoCoF, frequency nadir, and replacing a 1.6 GVA condenser fleet.

`book-plan.md` holds the specification: a graph of 40 results (R01 to R40, no forward references), a notation table of 106 symbols, per-chapter specifications with fixed worked-example numbers, and 20 sources. Every citation is marked "verify" until a human checks the primary source.

**Agent fleet (17 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| plan | 1 | Opus | Wrote the book plan, result graph and notation table |
| draft | 4, one per chapter, in 2 parallel lanes | Opus | Wrote each chapter as self-contained HTML with inline SVG figures and Python-checked worked examples (34,081 words in total) |
| edit | 4, one per chapter | Fable | Senior science editor (`science-editor` skill): blocking defects as `file:line` with replacement text, line rewrites, and a table of recomputed numbers (709 numbers checked) |
| fix | 4, one per chapter | Sonnet | Applied every numbered editor item and logged each one as applied or skipped (`ch<N>-fix.md`) |
| edit2 | 4, one per chapter | Sonnet | Checked each blocking fix item by item and recomputed the worked examples (`ch<N>-edit2.md`) |

Result: all four first edits gave ACCEPT WITH CHANGES. After the fixes, all four edit2 checks gave ACCEPT.

## P2 — Reproduction of eight published physics results

**Folder:** `p2-physics/`

Eight classic computational-physics results, each reproduced from scratch and compared with the published value within a stated tolerance:

| Target | Quantity |
|---|---|
| 2D Ising model | Critical temperature T_c, from a Binder-cumulant crossing (published 2.2692) |
| Lorenz system | Largest Lyapunov exponent |
| Kuramoto model | Synchronization threshold K_c, for Lorentzian frequencies |
| Three-body figure-eight | Orbit period |
| Fermi–Pasta–Ulam chain | Recurrence time |
| Logistic map | Feigenbaum constant δ |
| Kepler orbit | Integrator convergence order and long-term energy drift (leapfrog against RK4) |
| Poisson equation | Convergence order of the 5-point finite-difference solver |

`scripts/` holds one script per target, and `results/` holds one JSON per target with the measured value, published value, tolerance and pass flag.

**Agent fleet (about 33 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| draft | 8, one per target, up to 3 in parallel | Opus | Wrote each simulation with an `assert` self-check |
| verify | 8, one per target | Sonnet | Re-ran each script independently, checked it is deterministic, and wrote the results JSON |
| referee | 2 | Fable | Judged every result and its tolerance, ran their own probes, and listed 26 required changes (`referee.md`, `referee-ising.md`) |
| fix | 7, one per target | Opus | Applied the referee's changes |
| verify2 | 7, in 4 lanes | Sonnet | Re-verified every patched target |
| report | 1 | Sonnet | Built `report.html` and cross-checked every row against the JSON |

Result: 8 of 8 targets pass.

## P3 — PDE method bake-off: viscous Burgers equation

**Folder:** `p3-pde/`

Five numerical methods solve the same benchmark: the 1D viscous Burgers equation on a periodic domain [0, 2π], with ν = 0.07 up to t = 0.5, checked against the Cole–Hopf analytic solution. Each method runs on three resolutions, and its observed convergence order is fitted and compared with theory.

| Method | Observed order | Theoretical order |
|---|---|---|
| Finite difference | 2.00 | 2 |
| Finite element | 1.99 | 2 |
| Finite volume | 1.82 | 2 |
| Spectral | 9.16 (a slope fitted to exponential convergence) | spectral |
| Physics-informed neural network | 1.34 | none (does not pass) |

**Agent fleet (11 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| draft | 5, one per method, in parallel | Opus | Wrote each solver, ran the convergence study, wrote `<method>-order.json` |
| complete and verify | 5, one per method | Sonnet | Checked each result and finished the PINN run |
| referee and report | 1 | Sonnet | Confirmed all five use the same benchmark, explained each gap between observed and theoretical order (`referee.md`), and built `report.html` with log-log convergence plots |

## P4 — Proof arena: ten graduate theorems

**Folder:** `p4-proofs/`

Ten theorems from ten areas, each proved in full and then attacked by an independent referee:

Arzelà–Ascoli · Sylow theorems · Urysohn's lemma · strong law of large numbers (Etemadi) · spectral theorem for normal operators · Hall's marriage theorem · quadratic reciprocity · uniform boundedness principle · Radon–Nikodym · Picard–Lindelöf.

**Agent fleet (22 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| list | 1 | Opus | Chose the ten theorems and wrote precise statements with all hypotheses (`theorems.md`) |
| read | 1 | Haiku | Passed the statements to the pipeline |
| prove | 10, one per theorem, in parallel | Sonnet | Wrote a complete proof (`t<N>-proof.md`) |
| attack and referee | 10, one per theorem | Opus | Acted as a hostile referee: checked every step for gaps, unjustified steps and missing hypotheses, and gave a verdict of VALID or GAP (`t<N>-verdict.md`) |
| reprove | 0 of 10 needed | Sonnet | Runs only when a referee returns GAP |

Result: all ten proofs VALID.

## P5 — Sizing study: battery storage replacing a synchronous condenser fleet

**Folder:** `p5-sizing/`

A Monte Carlo sizing study for grid-forming battery storage (BESS) that takes over frequency response from a 1.6 GVA synchronous condenser fleet (179.2 MJ stored, 224 MW response, for a 1,000 MW loss on a 200 GVA·s system). Six scenarios each vary one uncertainty over 10,000 samples and report p5, p50 and p95:

inertia constant · response time · outage rate · cost curve · battery degradation over 15 years · grid code (RoCoF limit).

`design-memo.html` combines the scenarios into one recommendation: **1,840 MW / 2,135 MWh installed**, with a range of 1,176 MW / 1,348 MWh to 2,400 MW / 2,912 MWh. Response time drives the power rating, and degradation drives the energy rating. The memo lists its open caveats. One example: `grid-code.py` does not apply the 1.2 pu current limit, and with that limit a 2.0 Hz/s grid code would need 2,240 MVA.

**Agent fleet (10 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| model and run | 8 for 6 scenarios, in parallel (the degradation scenario needed two reruns) | Opus and Sonnet | Wrote each Monte Carlo model with stated distributions and sources, ran it with a fixed seed, and wrote `<scenario>.json` |
| memo | 1 | Opus | Checked the scenarios for conflicting assumptions and wrote the design memo, tracing every number to a JSON |
| memo update | 1 | Opus | Added the degradation scenario and revised the recommendation |

## P6 — Blind-spot sweep: numerical linear algebra

**Folder:** `p6-blindspot/`

A map of the unknown unknowns in numerical linear algebra for a graduate reader, across twelve subtopics:

floating point and conditioning · LU and pivoting · QR and least squares · SVD · eigenvalue algorithms · Krylov methods · preconditioning · sparse direct methods · randomized NLA · structured matrices · mixed precision · matrix functions.

Each pass (`<subtopic>.md`) gives the topic stack, unknown unknowns, common misconceptions with the correct statement and a numpy check, rat-holes, and study prompts. `index.html` has one card per subtopic and a table of concepts that appear across subtopics.

**Agent fleet (15 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| split | 1 | Opus | Divided the field into twelve subtopics (`subtopics.md`) |
| read | 1 | Haiku | Passed the subtopics to the pipeline |
| pass | 12, one per subtopic, in parallel | Sonnet | Ran a blind-spot pass (`blind-spot-pass` method), including small numpy experiments |
| index | 1 | Sonnet | Built `index.html` and the cross-topic concept table |

## P7 — Explainer series: power-system dynamics for programmers

**Folder:** `p7-explainers/`

Eight code-first lessons. Each one opens with one consequential problem, derives the physics under stated assumptions, and runs a plain-Python simulation. The Python files next to each lesson are the scripts the lesson prints output from.

1. Frequency is shared state
2. One machine on a stiff grid
3. When the integrator lies
4. Equal-area criterion
5. Rotating frames: the Park transform and the PLL
6. Following on a weak grid
7. Forming instead of following
8. One machine to a system

**Agent fleet (19 subagents):**

| Stage | Agents | Model | Role |
|---|---|---|---|
| outline | 1 | Opus | Wrote the eight lesson specifications (`outline.md`) |
| read | 1 | Sonnet | Passed the specifications to the pipeline |
| draft | 8, one per lesson, in parallel | Sonnet | Wrote each lesson (`rigorous-explainer` method) with a snippet it actually ran and inline SVG figures |
| edit and fix | 8, one per lesson | Opus | Re-ran the code, recomputed every number, logged each defect (`lesson<N>-edit.md`), then applied the fixes |
| red team | 1 | Sonnet | Found the strongest attack on each lesson and on the series (`redteam.md`), and built `index.html` |

The editors found real defects before the fixes. Two examples: a figure trace in lesson 6 that did not match the simulation output, and a false claim in lesson 4 that the eigenvalues are the same before and after clearing (they are −0.1429 ± j8.961 before and −0.1429 ± j7.400 after).

---

## Viewing the output

Every HTML page is self-contained: dark mode, inline SVG, and no external scripts or stylesheets. Open any page directly in a browser. The Python scripts need `numpy` and `scipy`. The PINN solver uses `torch` if it is installed, and a small numpy network if not.

## Caveats

- Every citation in P1 is marked "verify". No human has checked the sources yet.
- P3's PINN does not converge at a clean order. Its result is reported as a failure, not tuned away.
- The P5 memo lists open model defects and assumed distributions (for example the battery fade curves). Treat its numbers as a study, not an engineering design.
- Agents wrote all of this content, and other agents reviewed it. A domain expert has not reviewed it.
