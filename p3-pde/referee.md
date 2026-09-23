# P3 PDE bake-off — referee notes

Benchmark check, method-by-method order analysis, and cause for every gap between
observed and theoretical order. Every number below is copied or computed directly
from the five `*-order.json` files; recomputed numbers are marked and the arithmetic
is shown.

## 1. Same benchmark, confirmed

All five scripts (`finite-difference.py`, `finite-element.py`, `finite-volume.py`,
`spectral.py`, `pinn.py`) solve the same problem: 1D viscous Burgers,
`u_t + u u_x = nu u_xx`, `nu = 0.07`, `x` in `[0, 2*pi]` periodic, `t_end = 0.5`,
against the same two-image Cole-Hopf analytic solution:

```
phi(x,t) = exp(-(x-4t)^2 / (4*nu*(t+1))) + exp(-(x-4t-2*pi)^2 / (4*nu*(t+1)))
u(x,t)   = -2*nu*phi_x/phi + 4
```

`finite-difference.py`, `spectral.py`, and `pinn.py` use this formula verbatim
(byte-identical `exact()`/`u_exact()` bodies). `finite-element.py` uses the same
formula with variable names `s`, `e1`, `e2`. `finite-volume.py` uses a
log-sum-exp (`np.logaddexp`) rewrite of the same formula for numerical stability
at small `nu*(t+1)`, and additionally compares **cell averages** of `u` (via the
closed-form `mean_cell(u) = 4 - 2*nu*[ln phi(b) - ln phi(a)]/h`) rather than point
values — the only benchmark-application difference across the five, and it is
appropriate for a finite-volume scheme. All five report a periodicity gap of the
two-image formula at `t=0.5` (finite-element: `5.77e-15`; finite-volume:
`6.22e-15` `analytic_periodicity_gap`; spectral notes the missing images are
`~exp(-43)` relative) — negligible next to every method's discretization error.
**Verdict: same benchmark, consistently applied.**

## 2. Observed vs theoretical order, per method

| Method | Theoretical order | Observed order (as reported) | Fit window used | Gap | Cause |
|---|---|---|---|---|---|
| finite-difference | 2.0 | 2.0039 | finest 3 grids (256,512,1024) | +0.004 (essentially exact) | None — coarsest pairwise order (64→128) is 1.764, below 2, because the diffusive boundary layer (`nu=0.07`) is under-resolved at 64 points; `observed_order_all_grids` = 1.946 confirms this pre-asymptotic drag. The finest-3 fit correctly isolates the asymptotic regime. |
| finite-element | 2.0 | 1.9874 | finest 3 grids (320,640,1280), per `fit_grids` | -0.013 | Same pre-asymptotic effect: pairwise order climbs monotonically from 1.549 (40→80) to 1.995 (640→1280) as `h` shrinks. P1 Galerkin with a consistent mass matrix is formally 2nd order; the fit on the three finest grids lands within 1% of theory. |
| finite-volume | 2.0 | 1.8199 | **all 5 grids** (128…2048) | -0.18 | This is a fit-window artifact, not a real accuracy shortfall. `finite-volume.py` line 91 fits `np.polyfit` over all 5 grids instead of the finest 3 that `finite-difference.py` and `finite-element.py` use. Recomputed on the finest 3 grids (512,1024,2048) with the same `np.polyfit(log h, log err)` the JSON errors give **1.9126** (verified: `python -c` recomputation from the JSON's own `grids`/`errors` arrays, not a re-run of the simulation) — in line with FD and FE. The reported pairwise order 1024→2048 is 1.9437, also consistent. **This is the one number in the five JSONs that is not apples-to-apples with FD/FE's `observed_order`; report.html flags it and shows the recomputed value alongside the reported one.** |
| pinn | none (no a-priori rate in `h`) | 1.3412 (least squares, all 3 sizes) | all 3 collocation-count levels | not applicable — no theory to gap against | `pinn.py` itself documents why: PINN error is bounded by optimization and network capacity, not by collocation density. The data show this directly: error goes 6.04 → 6.97 → 0.94 as `N_c` goes 2000 → 8000 → 32000 (non-monotonic — it gets *worse* at 8000 before improving at 32000), and `pairwise_orders` are `-0.205` then `2.887`. `residual_loss` also spikes at the middle size (73.1 vs 0.43 and 2.38 at the ends), and `lbfgs_hit_time_cap` is `true` for all three runs — L-BFGS never converged, it was cut off by a wall-clock cap every time. The width also increases with `N_c` (32→64→128, `params` 3329→12801→50177) so grid level and network capacity are confounded — this is not a controlled `h`-refinement study, it is three independent, undertrained fits. Cause of the gap is optimization failure (undertraining), not discretization; the JSON's own `pass: false` / `self_check_failures: ["largest-size error 0.9413210484124999 too large"]` agrees. |
| spectral | none (exponential in `N`, not a fixed algebraic order) | 9.1575 (algebraic slope, all 6 grids) — **not the right number to compare** | all 6 grids | not applicable | `spectral.py` documents this correctly: for an analytic periodic solution, Fourier spectral convergence is faster than any fixed power of `N`, so the algebraic slope keeps climbing with grid range (`pairwise_orders`: 4.73, 8.25, 11.83, 15.07, 18.41 — strictly increasing, exactly the exponential-convergence signature). The number that actually characterizes this method is `observed_exponential_rate = 0.05244` (least-squares slope of `err ~ C*exp(-c*N)`), and `dt_halving_relative_change_finest = 9.24e-4` confirms the fixed `dt=1e-4`, 5000-step RK4 (with the diffusion term treated exactly via integrating factor) is not the accuracy bottleneck at the finest grid — the spatial truncation still dominates. |

## 3. Runtime and verdict summary

| Method | Runtime (s) | `pass` (script's own check) | Referee verdict |
|---|---|---|---|
| finite-difference | 2.489 | true | **PASS** — order matches theory to 0.2%. |
| finite-element | 7.068 | true | **PASS** — order matches theory to 0.6%. |
| finite-volume | 6.199 | true | **PASS**, with a caveat — the scheme itself converges at the right rate (finest-pairwise 1.944; finest-3 refit 1.913), but the JSON's own `observed_order` (1.820) understates it because of the all-grid fit window discussed above. Treat 1.91–1.94, not 1.82, as this method's comparable number. |
| pinn | 241.328 | **false** | **FAIL**, correctly self-flagged. No accuracy claim should be drawn from `observed_order` = 1.34; the run is optimization-limited and non-monotonic, and the script's own `self_check_failures` already says so. |
| spectral | 12.261 | true | **PASS** — but judge it on `observed_exponential_rate` (0.0524), not `observed_order` (9.16), which is a fit-range artifact of the same kind (worse) as finite-volume's, just correctly labeled as such in the JSON. |

## 4. Caveats (carried into report.html)

1. **Fit-window inconsistency across scripts.** `finite-difference.py` and
   `finite-element.py` fit `observed_order` on the finest 3 grids; `finite-volume.py`
   fits on all 5; `pinn.py` fits on all 3; `spectral.py`'s algebraic slope uses all 6
   (but is explicitly disclaimed as not meaningful). This makes the raw
   `observed_order` field **not directly comparable** across FD/FE vs. FV/spectral
   without knowing which fit window produced it. The comparison table in
   report.html therefore shows both the reported number and, for finite-volume, the
   finest-3 recomputation (1.9126) alongside it.
2. **Error norms differ by construction, not by mistake.** FD and spectral compare
   point values on the grid; finite-element uses 5-point Gauss quadrature per
   element against the exact solution; finite-volume compares cell averages (the
   quantity a finite-volume scheme actually produces) via a closed-form exact
   cell-average integral. Comparing raw error *magnitudes* across methods at a
   nominally similar grid count is therefore an approximate comparison; comparing
   each method's own *order* (rate of decrease) is exact.
3. **PINN's `grids` field is not a physical grid.** It is `N_c`, the number of
   random space-time collocation points (`grids_meaning` in the JSON says so).
   `size_abscissa` converts it to a mean spacing `h = sqrt(2*pi*0.5/N_c)` for
   plotting only; comparing PINN's `h` to FD/FE/FV's mesh `h` is a rough proxy at
   best, since PINN error is dominated by training, not sampling density (see §2).
4. **PINN width is confounded with collocation count.** Network width scales
   32→64→128 alongside `N_c` 2000→8000→32000, so PINN's three data points vary two
   things at once (capacity and sampling). This is disclosed here, not hidden in
   the plot.
5. **Time-step counts reflect a CFL/diffusion crossover, not a bug.** In
   finite-difference and finite-volume, `time_steps` roughly doubles at coarse
   grids (advective CFL, `dt ~ h`) then roughly quadruples at fine grids (diffusive
   limit, `dt ~ h^2`) as `nu*dt/h^2` and `u*dt/h` trade off which constraint binds.
   Both scripts describe this with a `dt = min(...)` line; the "dt ~ dx^2" summary
   in the benchmark string is a simplification of that `min(...)`, not a
   discrepancy in the data.
6. **No script was re-run.** All numbers above came from reading the five
   `*-order.json` files and, for the one flagged recomputation (finite-volume
   finest-3 order), reapplying `np.polyfit` to that JSON's own `grids`/`errors`
   arrays — a check of the existing numbers, not a re-simulation.
