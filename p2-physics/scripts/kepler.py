"""Energy behaviour of a symplectic vs a non-symplectic integrator on a Kepler orbit.

SYSTEM: planar two-body Kepler problem, GM = 1, semi-major axis a = 1,
  eccentricity e = 0.6, started at pericenter:
      r0 = a(1 - e)               = 0.4
      v0 = sqrt(GM (1+e) / (a(1-e))) = 2.0      (perpendicular to r0)
      E0 = -GM / (2a)             = -0.5        (exact, used as reference)
      L0 = r0 v0                  = 0.8
      T  = 2 pi a^(3/2)           = 2 pi
  Nothing in this script is stochastic. There is no Monte Carlo step, no random
  initial condition and no random number is drawn anywhere, so no seed is set;
  the output is bit-for-bit deterministic on one machine.

METHOD
  Integrator 1 (symplectic): Stormer-Verlet / leapfrog in kick-drift-kick
    (velocity Verlet) form. Position and velocity are synchronized at the end
    of every step, so the energy samples are taken at equal times.
  Integrator 2 (non-symplectic): classical explicit 4th-order Runge-Kutta,
    same fixed step, same initial condition.
  Both loops run on plain Python floats. The recurrence is sequential in time,
  so it cannot be vectorized over steps; at ~9e5 total steps a float loop is
  several times faster than the same loop written with numpy scalars, and the
  whole script runs in a few seconds. numpy is used only for the fits and the
  statistics. See "RUNTIME" below.

PUBLISHED VALUES AND SOURCE
  E. Hairer, C. Lubich, G. Wanner, "Geometric Numerical Integration:
  Structure-Preserving Algorithms for Ordinary Differential Equations",
  2nd ed., Springer (2006), chapter I. The Kepler problem with e = 0.6 is the
  worked example of I.2; Stormer-Verlet and the other basic schemes are
  introduced earlier in the same chapter. Only the chapter is cited here,
  because the task cites the chapter and an invented section number would be a
  checkable error that adds nothing. The two statements reproduced here are
    (a) Stormer-Verlet is a second-order method, so its energy error scales
        like h^2.  PUBLISHED = 2.
    (b) The energy error of a symplectic method on this problem stays bounded
        over very long times (no secular drift), while the energy error of
        explicit RK4 grows about linearly in t.  PUBLISHED_2 = 1, meaning the
        energy error late in a 1000-period run is the same size as early in
        the run.

QUANTITY (a): convergence order of the leapfrog energy error.
  err(h) = max over the sampled steps of |E(t) - E0| / |E0| during a
  10-period run, for 5 step sizes h = T/spp with spp = 200, 400, 800, 1600,
  3200. The 4 consecutive pairwise estimates p_i = log2(err_i / err_{i+1}) are
  averaged; MEASURED is that mean.

KNOWN METHOD BIAS FOR (a) AND ITS EXPECTED SIZE
  1. Higher-order terms. Verlet is a symmetric method, so its error expansion
     contains only even powers: err(h) = C h^2 (1 + (D/C) h^2 + ...). The
     induced shift in a pairwise log2 ratio between h and h/2 is
     log2((1 + q h^2) / (1 + q h^2 / 4)) ~= (3/(4 ln 2)) q h^2 ~= 1.08 q h^2,
     i.e. O(h^2), not O(h). This term is NOT covered by a fixed constant. The
     4 pairwise orders are a monotone sequence converging to the true order,
     and their excesses above the limit fall by about 4 per halving, so the
     run measures the term itself. Richardson on that sequence, with ratio 4
     for an h^2 term, gives
         p_inf = p_4 - (p_3 - p_4) / 3,
     and the bias allowance is BIAS_A = |mean(p) - p_inf|, the bias of the
     reported mean against that limit. The run gives p_inf = 2.0000 and
     BIAS_A = 0.0019.
  2. Sampling of the peak. err(h) is a maximum over a discrete time grid, and
     the true maximum sits at the pericenter spike. The sampled maximum
     therefore under-estimates the true one, and under-estimates it more at
     coarse h, which pushes the measured order slightly below 2. The spike is
     resolved by >= 25 samples even at spp = 200. This deficit is a smooth
     function of h, so the same Richardson limit absorbs it. It is not a
     separate allowance.
  An earlier version of this script used a constant BIAS_A = 0.02, fixed
  before the first run from item 1 alone. That constant was 72% of the
  tolerance and was asserted, not measured. It was replaced after referee
  review, because the run measures the same term and gets 0.0019, about one
  tenth of the asserted value.

ERROR ESTIMATE FOR (a): the sample standard deviation (ddof=1) of the 4
  pairwise order estimates. The 4 estimates are a deterministic converging
  sequence, not random draws, so this number is a spread and NOT a sigma.
  Multiplying it by 3 below is a convention of this project, not a confidence
  level. The spread is used rather than spread/sqrt(4) as the conservative
  choice.

TOLERANCE for (a) = 3 * ERROR_ESTIMATE + BIAS_A, with BIAS_A measured as
  above. State plainly what that test then is: ABS_DIFF = |mean(p) - 2| and
  BIAS_A = |mean(p) - p_inf|, so the comparison passes exactly when the
  Richardson limit p_inf lies within 3 * spread of the published order 2. The
  pass is a statement about p_inf, not about the mean of the 4 orders.

QUANTITY (b): boundedness of the leapfrog energy error over 1000 periods.
  One run of 1000 periods at spp = 400 (400000 steps) is cut into 100 windows
  of exactly 10 periods (4000 steps each). M_k is the maximum of
  |E - E0| / |E0| inside window k. MEASURED_2 = max(M_90..M_99) / M_0, the
  ratio of the largest late-run window maximum to the first-10-period
  maximum. A bounded error gives a ratio of order 1; an error growing like t
  would give about 100.

KNOWN METHOD BIAS FOR (b) AND ITS EXPECTED SIZE
  1. Extreme-value bias. The numerator is a maximum over 10 windows and the
     denominator is a single window, so even with a perfectly stationary
     envelope the ratio exceeds 1. For 10 draws the expected maximum sits
     about 1.54 standard deviations above the mean, so the expected excess is
     about 1.54 * sigma_rel, where sigma_rel = std(M)/mean(M) is the
     ERROR_ESTIMATE_2 below. This term is therefore computed from the run, not
     guessed.
  2. Peak sampling, again. Each M_k is a maximum over a discrete grid, and the
     grid phase relative to the pericenter passage drifts slowly because the
     numerical period differs from T by O(h^2). That drift is what makes the
     window maxima differ from window to window, and sigma_rel measures it
     over all 100 windows. It therefore needs no separate allowance. Roundoff
     is irrelevant here: a random walk over 400000 steps is about
     sqrt(N) * eps ~ 632 * 2.2e-16 = 1.4e-13 in relative energy, ten orders of
     magnitude below the h^2 signal.
  BIAS_B = 1.54 * ERROR_ESTIMATE_2, measured in the run.
  An earlier version of this script added a floor of 0.01 to BIAS_B, twice an
  asserted 0.5% peak-sampling bound. The floor was removed after referee
  review. It was 99.9% of TOLERANCE_2, and it blinded the test by a factor of
  about 1000: a method with a 1% secular energy drift over 1000 periods gives
  a ratio of 1.01, which passes the floored tolerance 0.010008 and fails the
  floor-free tolerance 7.9e-06.

ERROR ESTIMATE FOR (b): std(M_k, ddof=1) / mean(M_k) over all 100 windows,
  i.e. the relative wander of a bounded envelope from window to window. This
  is the natural scale against which an excess of the late-run maximum has to
  be judged. It is a deterministic spread, not a sigma.

TOLERANCE for (b) = 3 * ERROR_ESTIMATE_2 + BIAS_B, applied to
  ABS_DIFF_2 = |MEASURED_2 - 1|. Both terms are measured in the run. The
  task's own acceptance ceiling (the late maximum no larger than 3 times the
  early maximum) is printed as a diagnostic but is NOT used as the tolerance:
  asserting 3.0 here would be a band many thousand times wider than the
  measurement and would prove nothing.

INDEPENDENT CONTROL (the analogue of a positive control): the identical
  windowing is applied to explicit RK4 at the same step size. Its ratio must
  come out large (gate: > 10), because the published statement is a contrast
  between the two integrators, not a property of this particular orbit. A
  leapfrog ratio near 1 with an RK4 ratio also near 1 would mean the run is
  too short or the diagnostic is blind, not that RK4 conserves energy.

SELF-CHECKS (all run before the measurement, all hard-gated):
  1. The exact solution of the Kepler orbit (Newton solve of Kepler's
     equation) is checked to conserve E0 and L0 to 1e-13 on a grid of times.
  2. Global position error order against that exact solution: leapfrog must
     come out near 2 and RK4 near 4 (tolerance 0.15 each). This validates the
     force evaluation and both integrators independently of any energy
     statement. The step sizes used for this check are spp = 800, 1600, 3200,
     6400 because RK4 is still pre-asymptotic at coarse steps on an e = 0.6
     orbit: at spp = 100, 200, 400, 800 the same check returns 4.30, with the
     individual pairwise values 4.46, 4.28, 4.16 falling steadily towards 4;
     at spp = 400, 800, 1600, 3200 it returns 4.10. This is a calibration of
     the self-check range, not of any tolerance on a published quantity.
  3. Angular momentum in the long leapfrog run must be conserved to better
     than 1e-12 relative. Velocity Verlet conserves angular momentum exactly
     for a central force, so any larger drift means the implementation is
     wrong.

RUNTIME: the whole script is under 15 s on a 12-core laptop, well inside the
  180 s budget, so no size was traded away. RUNTIME_S and RUNTIME_S_2 both
  report the same total wall-clock time, because both quantities come from one
  execution of this script.
"""

import math
import sys
import time

import numpy as np

GM = 1.0
SMA = 1.0
ECC = 0.6
R0 = SMA * (1.0 - ECC)                                  # 0.4
V0 = math.sqrt(GM * (1.0 + ECC) / (SMA * (1.0 - ECC)))  # 2.0
E0 = -GM / (2.0 * SMA)                                  # -0.5
L0 = R0 * V0                                            # 0.8
PERIOD = 2.0 * math.pi * SMA ** 1.5                     # 2 pi

# Quantity (a)
SPPS_ORDER = (200, 400, 800, 1600, 3200)   # steps per period
N_PERIODS_ORDER = 10
PUBLISHED_A = 2.0
BIAS_A_PREREG = 0.02                       # superseded: now measured per run

# Quantity (b)
SPP_LONG = 400
N_PERIODS_LONG = 1000
WINDOW_PERIODS = 10
PUBLISHED_B = 1.0
EV_10 = 1.54                               # E[max of 10] - mean, in sigma
TASK_CEILING = 3.0                         # diagnostic only, never the tolerance
RK4_GATE = 10.0                            # control: RK4 ratio must exceed this

# Self-check settings
SPPS_SELF = (800, 1600, 3200, 6400)
ORDER_SELF_TOL = 0.15
L_DRIFT_TOL = 1e-12


def energy(x, y, vx, vy):
    return 0.5 * (vx * vx + vy * vy) - GM / math.sqrt(x * x + y * y)


def exact_state(t):
    """Exact Kepler orbit, pericenter at (+R0, 0) with velocity along +y."""
    m = 2.0 * math.pi * t / PERIOD
    m = math.fmod(m, 2.0 * math.pi)
    ecc_anom = m + ECC * math.sin(m)           # starting guess
    for _ in range(80):
        f = ecc_anom - ECC * math.sin(ecc_anom) - m
        fp = 1.0 - ECC * math.cos(ecc_anom)
        step = f / fp
        ecc_anom -= step
        if abs(step) < 1e-15:
            break
    b = SMA * math.sqrt(1.0 - ECC * ECC)
    x = SMA * (math.cos(ecc_anom) - ECC)
    y = b * math.sin(ecc_anom)
    r = SMA * (1.0 - ECC * math.cos(ecc_anom))
    edot = 2.0 * math.pi / PERIOD / (1.0 - ECC * math.cos(ecc_anom))
    vx = -SMA * math.sin(ecc_anom) * edot
    vy = b * math.cos(ecc_anom) * edot
    return x, y, vx, vy, r


def leapfrog(spp, n_periods, window_periods):
    """Velocity Verlet. Return (window maxima of |dE/E0|, max |dL/L0|, state)."""
    h = PERIOD / spp
    half = 0.5 * h
    x, y, vx, vy = R0, 0.0, 0.0, V0
    r2 = x * x + y * y
    inv = GM / (r2 * math.sqrt(r2))
    ax, ay = -inv * x, -inv * y
    wsteps = window_periods * spp
    n_steps = n_periods * spp
    maxima = []
    cur = 0.0
    l_drift = 0.0
    for i in range(n_steps):
        vxh = vx + half * ax
        vyh = vy + half * ay
        x += h * vxh
        y += h * vyh
        r2 = x * x + y * y
        rr = math.sqrt(r2)
        inv = GM / (r2 * rr)
        ax, ay = -inv * x, -inv * y
        vx = vxh + half * ax
        vy = vyh + half * ay
        d = abs((0.5 * (vx * vx + vy * vy) - GM / rr - E0) / E0)
        if d > cur:
            cur = d
        dl = abs((x * vy - y * vx - L0) / L0)
        if dl > l_drift:
            l_drift = dl
        if (i + 1) % wsteps == 0:
            maxima.append(cur)
            cur = 0.0
    return maxima, l_drift, (x, y, vx, vy)


def rk4(spp, n_periods, window_periods):
    """Classical explicit RK4. Return (window maxima of |dE/E0|, state)."""
    h = PERIOD / spp
    x, y, vx, vy = R0, 0.0, 0.0, V0
    wsteps = window_periods * spp
    n_steps = n_periods * spp
    maxima = []
    cur = 0.0

    def deriv(px, py, pvx, pvy):
        r2 = px * px + py * py
        inv = GM / (r2 * math.sqrt(r2))
        return pvx, pvy, -inv * px, -inv * py

    for i in range(n_steps):
        k1 = deriv(x, y, vx, vy)
        k2 = deriv(x + 0.5 * h * k1[0], y + 0.5 * h * k1[1],
                   vx + 0.5 * h * k1[2], vy + 0.5 * h * k1[3])
        k3 = deriv(x + 0.5 * h * k2[0], y + 0.5 * h * k2[1],
                   vx + 0.5 * h * k2[2], vy + 0.5 * h * k2[3])
        k4 = deriv(x + h * k3[0], y + h * k3[1],
                   vx + h * k3[2], vy + h * k3[3])
        x += h / 6.0 * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0])
        y += h / 6.0 * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1])
        vx += h / 6.0 * (k1[2] + 2.0 * k2[2] + 2.0 * k3[2] + k4[2])
        vy += h / 6.0 * (k1[3] + 2.0 * k2[3] + 2.0 * k3[3] + k4[3])
        d = abs((energy(x, y, vx, vy) - E0) / E0)
        if d > cur:
            cur = d
        if (i + 1) % wsteps == 0:
            maxima.append(cur)
            cur = 0.0
    return maxima, (x, y, vx, vy)


def pairwise_orders(errs):
    """log2 of consecutive error ratios for a step size halved each time."""
    return np.array([math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)])


def self_checks():
    print("self-checks")

    # 1. the exact solution conserves E0 and L0
    worst_e = 0.0
    worst_l = 0.0
    for k in range(101):
        t = PERIOD * k / 100.0
        x, y, vx, vy, _ = exact_state(t)
        worst_e = max(worst_e, abs((energy(x, y, vx, vy) - E0) / E0))
        worst_l = max(worst_l, abs((x * vy - y * vx - L0) / L0))
    print("  1. exact Kepler solution: max |dE/E0| %.2e, max |dL/L0| %.2e"
          % (worst_e, worst_l))
    if worst_e > 1e-13 or worst_l > 1e-13:
        print("     FAILED: analytic reference orbit is inconsistent")
        return False

    # 2. global position error order against the exact solution, 1 period
    xe, ye, _, _, _ = exact_state(PERIOD)
    lf_errs = []
    rk_errs = []
    for spp in SPPS_SELF:
        _, _, (x, y, _, _) = leapfrog(spp, 1, 1)
        lf_errs.append(math.hypot(x - xe, y - ye))
        _, (x, y, _, _) = rk4(spp, 1, 1)
        rk_errs.append(math.hypot(x - xe, y - ye))
    lf_order = float(np.mean(pairwise_orders(lf_errs)))
    rk_order = float(np.mean(pairwise_orders(rk_errs)))
    print("  2. position-error order over 1 period, spp=%s" % (SPPS_SELF,))
    print("       leapfrog errors %s -> order %.3f (expect 2)"
          % (" ".join("%.2e" % e for e in lf_errs), lf_order))
    print("       RK4      errors %s -> order %.3f (expect 4)"
          % (" ".join("%.2e" % e for e in rk_errs), rk_order))
    if abs(lf_order - 2.0) > ORDER_SELF_TOL or abs(rk_order - 4.0) > ORDER_SELF_TOL:
        print("     FAILED: an integrator does not show its nominal order")
        return False
    return True


def main():
    t_start = time.perf_counter()

    if not self_checks():
        runtime = time.perf_counter() - t_start
        for suffix in ("", "_2"):
            print()
            for key in ("MEASURED", "PUBLISHED", "ERROR_ESTIMATE",
                        "TOLERANCE", "ABS_DIFF"):
                print("%s%s=nan" % (key, suffix))
            print("RUNTIME_S%s=%.1f" % (suffix, runtime))
            print("RESULT%s=FAIL" % suffix)
        sys.exit(1)

    # ---- quantity (a): convergence order of the leapfrog energy error -------
    errs = []
    for spp in SPPS_ORDER:
        maxima, _, _ = leapfrog(spp, N_PERIODS_ORDER, N_PERIODS_ORDER)
        errs.append(maxima[0])
    orders = pairwise_orders(errs)
    measured_a = float(np.mean(orders))
    sigma_a = float(np.std(orders, ddof=1))
    p_inf = float(orders[-1] - (orders[-2] - orders[-1]) / 3.0)
    bias_a = abs(measured_a - p_inf)
    tol_a = 3.0 * sigma_a + bias_a
    diff_a = abs(measured_a - PUBLISHED_A)
    ok_a = diff_a <= tol_a

    # ---- quantity (b): boundedness over 1000 periods ------------------------
    lf_wins, l_drift, _ = leapfrog(SPP_LONG, N_PERIODS_LONG, WINDOW_PERIODS)
    rk_wins, _ = rk4(SPP_LONG, N_PERIODS_LONG, WINDOW_PERIODS)
    m = np.array(lf_wins)
    ratio_lf = float(m[-10:].max() / m[0])
    sigma_b = float(np.std(m, ddof=1) / np.mean(m))
    bias_b = EV_10 * sigma_b
    tol_b = 3.0 * sigma_b + bias_b
    diff_b = abs(ratio_lf - PUBLISHED_B)
    r = np.array(rk_wins)
    ratio_rk = float(r[-10:].max() / r[0])
    ok_b = (diff_b <= tol_b) and (ratio_rk > RK4_GATE) and (l_drift <= L_DRIFT_TOL)

    runtime = time.perf_counter() - t_start

    # ---- diagnostics --------------------------------------------------------
    print()
    print("(a) leapfrog energy-error convergence, %d periods per run"
          % N_PERIODS_ORDER)
    for spp, e in zip(SPPS_ORDER, errs):
        print("    spp=%4d  h=%.6f  max |dE/E0| = %.6e" % (spp, PERIOD / spp, e))
    print("    pairwise orders : %s" % " ".join("%.4f" % p for p in orders))
    print("    mean order      : %.4f" % measured_a)
    print("    spread (std,ddof=1) of the pairwise orders: %.4f"
          "  (spread of a converging sequence, not a sigma)" % sigma_a)
    print("    Richardson limit of the order sequence: p_inf = %.4f" % p_inf)
    print("    bias allowance  : %.4f  (measured: mean of the 4 orders minus"
          " the Richardson limit %.4f; pre-registered value was %.2f)"
          % (bias_a, p_inf, BIAS_A_PREREG))

    print()
    print("(b) leapfrog over %d periods at spp=%d, %d windows of %d periods"
          % (N_PERIODS_LONG, SPP_LONG, len(lf_wins), WINDOW_PERIODS))
    print("    window 0 max |dE/E0|            : %.6e" % m[0])
    print("    max over windows 90..99         : %.6e" % m[-10:].max())
    print("    mean / std over all 100 windows : %.6e / %.3e"
          % (m.mean(), m.std(ddof=1)))
    print("    late/early ratio (leapfrog)     : %.9f  (ratio - 1 = %+.3e)"
          % (ratio_lf, ratio_lf - 1.0))
    print("    task ceiling on that ratio      : %.1f  -> %s"
          % (TASK_CEILING, "satisfied" if ratio_lf <= TASK_CEILING else "violated"))
    print("    bias allowance                  : %.3e  (%.2f x the window-to-"
          "window wander: extreme-value shift of a max of 10)"
          % (bias_b, EV_10))
    print("    tolerance                       : %.3e  (no floor; the 0.01"
          " floor of the earlier version is removed)" % tol_b)
    print("    a 1 % secular drift (ratio 1.01) would fail this tolerance")
    print("  control, identical windowing applied to explicit RK4:")
    print("    window 0 max |dE/E0|            : %.6e" % r[0])
    print("    max over windows 90..99         : %.6e" % r[-10:].max())
    print("    late/early ratio (RK4)          : %.3f   (gate > %.0f -> %s)"
          % (ratio_rk, RK4_GATE, "ok" if ratio_rk > RK4_GATE else "FAILED"))
    print("  angular momentum drift in the long leapfrog run: %.2e"
          " (gate <= %.0e -> %s)"
          % (l_drift, L_DRIFT_TOL, "ok" if l_drift <= L_DRIFT_TOL else "FAILED"))

    # ---- parseable blocks ---------------------------------------------------
    print()
    print("MEASURED=%.6f" % measured_a)
    print("PUBLISHED=%.6f" % PUBLISHED_A)
    print("ERROR_ESTIMATE=%.6f" % sigma_a)
    print("TOLERANCE=%.6f" % tol_a)
    print("ABS_DIFF=%.6f" % diff_a)
    print("RUNTIME_S=%.1f" % runtime)
    print("RESULT=%s" % ("PASS" if ok_a else "FAIL"))
    print()
    print("MEASURED_2=%.6f" % ratio_lf)
    print("PUBLISHED_2=%.6f" % PUBLISHED_B)
    print("ERROR_ESTIMATE_2=%.3e" % sigma_b)
    print("TOLERANCE_2=%.3e" % tol_b)
    print("ABS_DIFF_2=%.3e" % diff_b)
    print("RUNTIME_S_2=%.1f" % runtime)
    print("RESULT_2=%s" % ("PASS" if ok_b else "FAIL"))

    if not (ok_a and ok_b):
        sys.exit(1)


if __name__ == "__main__":
    main()
