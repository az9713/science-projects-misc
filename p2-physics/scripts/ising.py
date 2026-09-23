"""Critical temperature of the 2D square-lattice Ising model (J=1, k_B=1, h=0).

METHOD: Binder-cumulant crossing.
  U4(T, L) = 1 - <m^4> / (3 <m^2>^2), m = (1/N) sum_i s_i.
  U4 is dimensionless at the critical point, so curves for two lattice sizes
  cross at T ~ Tc. We simulate L=16 and L=32, fit the difference
  D(T) = U4(T,16) - U4(T,32) with a cubic over a 7-point temperature window,
  and take its single root as Tc_measured.

KNOWN FINITE-SIZE BIAS: the crossing of a finite pair (L, 2L) does not sit
  exactly at Tc. The shift decays like L^-(1/nu + omega) with corrections to
  scaling, so it is not removed by using only two sizes. The run's own U16(Tc)
  against U* = 0.61069 bounds the shift below about 0.0016; the sign is not
  resolved. The value of U4 at the crossing is also an independent check on
  correctness: for the square lattice with periodic boundaries it must come
  out near 0.61. A run that lands on Tc but reports U4* far from 0.61 is wrong
  by luck, not right.

ERROR AND TOLERANCE: the measurement is stochastic, so the error estimate is a
  statistical sigma. Each lattice size gives two independent half-window
  estimates of U4(T); sigma(U4, L) is the root-mean-square over the 7 window
  temperatures of |U4_first_half - U4_second_half| / 2. That per-point noise is
  pushed through the same cubic-root procedure by a 2000-draw Monte Carlo,
  which gives sigma(Tc). The tolerance is set at run time:
      tol = 3 * sigma(Tc) + 0.002,
  where 0.002 is the finite-size bound above, rounded up. Expect tol ~ 0.010.
  No fixed tolerance constant is used.

DYNAMICS: single-spin-flip Metropolis, checkerboard (red/black) sublattice
  update. All spins of one color are conditionally independent given the other
  color, so a whole sublattice is updated in one vectorized numpy step. The
  temperature axis and an ensemble of independent replicas are stacked into the
  same array, so one numpy call advances every replica at every temperature.
"""

import sys
import time
import numpy as np

SEED = 20260922
TEMPS = np.linspace(2.22, 2.34, 7)          # window straddling Tc = 2.269185
SIZES = {16: 128, 32: 64}                   # lattice size -> replicas
N_THERM = 1000                              # sweeps discarded
N_MEAS = 4000                               # sweeps measured
MEAS_EVERY = 10                             # sweeps between samples
TC_EXACT = 2.0 / np.log(1.0 + np.sqrt(2.0))
N_MC = 2000                                 # noise draws for sigma(Tc)
FINITE_SIZE_BOUND = 0.002                   # bound on the 16/32 crossing shift

NT = TEMPS.size
# Metropolis acceptance for dE > 0. With k = s_i * (sum of 4 neighbours),
# dE = 2k and k is in {-4,-2,0,2,4}. Only k=2 and k=4 can be rejected.
EXP4 = np.exp(-4.0 / TEMPS).astype(np.float32).reshape(NT, 1, 1, 1)   # dE=4
EXP8 = np.exp(-8.0 / TEMPS).astype(np.float32).reshape(NT, 1, 1, 1)   # dE=8


def binder(L, replicas, rng):
    """Return (U4 over all samples, U4 of first half, U4 of second half)."""
    spins = (rng.integers(0, 2, size=(NT, replicas, L, L), dtype=np.int8) * 2 - 1)
    row, col = np.indices((L, L))
    red = ((row + col) % 2 == 0)
    black = ~red

    def sweep(s):
        for color in (red, black):
            nb = (np.roll(s, 1, 2) + np.roll(s, -1, 2)
                  + np.roll(s, 1, 3) + np.roll(s, -1, 3))
            k = s * nb
            u = rng.random(s.shape, dtype=np.float32)
            accept = color & ((k <= 0) | (u < EXP8) | ((k == 2) & (u < EXP4)))
            s = np.where(accept, -s, s)
        return s

    for _ in range(N_THERM):
        spins = sweep(spins)

    halves = []
    for _ in range(2):
        m2 = np.zeros(NT)
        m4 = np.zeros(NT)
        n = 0
        for step in range(N_MEAS // 2):
            spins = sweep(spins)
            if step % MEAS_EVERY == 0:
                m = spins.mean(axis=(2, 3), dtype=np.float64)   # (NT, replicas)
                m2 += (m ** 2).sum(axis=1)
                m4 += (m ** 4).sum(axis=1)
                n += m.shape[1]
        halves.append((m2 / n, m4 / n))

    (a2, a4), (b2, b4) = halves
    u_all = 1.0 - (a4 + b4) / (3.0 * ((a2 + b2) / 2.0) ** 2) / 2.0
    u_a = 1.0 - a4 / (3.0 * a2 ** 2)
    u_b = 1.0 - b4 / (3.0 * b2 ** 2)
    return u_all, u_a, u_b


def crossing(temps, diff, strict=True):
    """Root of the cubic fit of diff(T).

    With strict=True a root count other than 1 prints RESULT=FAIL and exits 1.
    With strict=False the same case returns (None, coeffs), which lets the
    noise Monte Carlo discard that draw instead of stopping the run.
    """
    coeffs = np.polyfit(temps, diff, 3)
    grid = np.linspace(temps[0], temps[-1], 20001)
    vals = np.polyval(coeffs, grid)
    sign_change = np.nonzero(np.signbit(vals[:-1]) != np.signbit(vals[1:]))[0]
    if sign_change.size != 1:
        if strict:
            print("RESULT=FAIL  (expected exactly one U4 crossing, found %d)"
                  % sign_change.size)
            sys.exit(1)
        return None, coeffs
    i = sign_change[0]
    t0, t1 = grid[i], grid[i + 1]
    v0, v1 = vals[i], vals[i + 1]
    return t0 - v0 * (t1 - t0) / (v1 - v0), coeffs


def half_sigma(u_a, u_b):
    """sigma of U4 from two independent half-window estimates.

    For two samples the standard error of their mean is |a - b| / 2. The
    root-mean-square over the 7 window temperatures gives one number per
    lattice size with 7 contributions instead of 1.
    """
    return float(np.sqrt(np.mean(((u_a - u_b) / 2.0) ** 2)))


def sigma_tc_monte_carlo(temps, diff, sigma_diff, rng, ndraw=N_MC):
    """Push per-point U4 noise through the cubic-root procedure."""
    roots = []
    for _ in range(ndraw):
        noisy = diff + rng.normal(0.0, sigma_diff, size=diff.shape)
        root, _ = crossing(temps, noisy, strict=False)
        if root is not None:
            roots.append(root)
    return float(np.std(roots, ddof=1)), len(roots)


def main():
    t_start = time.perf_counter()
    results = {}
    for L, replicas in SIZES.items():
        rng = np.random.default_rng(SEED + L)
        results[L] = binder(L, replicas, rng)
        u_all, u_a, u_b = results[L]
        print("L=%2d  replicas=%3d" % (L, replicas))
        for i, T in enumerate(TEMPS):
            print("   T=%.3f  U4=%.4f   (halves %.4f / %.4f)"
                  % (T, u_all[i], u_a[i], u_b[i]))

    u16, u16_a, u16_b = results[16]
    u32, u32_a, u32_b = results[32]
    tc_measured, coeffs = crossing(TEMPS, u16 - u32)

    # Statistical error: sigma(U4) per size from the halves, propagated to
    # sigma(Tc) by a noise Monte Carlo of the same cubic-root procedure.
    sig16 = half_sigma(u16_a, u16_b)
    sig32 = half_sigma(u32_a, u32_b)
    sigma_diff = float(np.hypot(sig16, sig32))
    rng_mc = np.random.default_rng(SEED + 999)
    sigma_tc, n_ok = sigma_tc_monte_carlo(TEMPS, u16 - u32, sigma_diff, rng_mc)
    tol = 3.0 * sigma_tc + FINITE_SIZE_BOUND

    # U4 at the crossing, from a cubic fit of each size's curve.
    u_star = 0.5 * (np.polyval(np.polyfit(TEMPS, u16, 3), tc_measured)
                    + np.polyval(np.polyfit(TEMPS, u32, 3), tc_measured))

    runtime = time.perf_counter() - t_start
    diff = abs(tc_measured - TC_EXACT)
    ok = diff <= tol
    print()
    print("Binder crossing of L=16 and L=32 (cubic fit of U4_16 - U4_32)")
    print("  U4 at the crossing : %.4f   (square lattice, PBC: expect ~0.61)" % u_star)
    print("  Tc = %.3f +/- %.3f   (statistical sigma, from the two halves)"
          % (tc_measured, sigma_tc))
    print("  Tc published       : %.6f   (2 / ln(1 + sqrt(2)))" % TC_EXACT)
    print("  sigma(U4)          : L=16 %.4f, L=32 %.4f   (|first half - second half| / 2, rms over the 7 temperatures)"
          % (sig16, sig32))
    print("  sigma(Tc)          : %.4f  (%d-draw noise Monte Carlo of the cubic root; %d draws gave exactly one root)"
          % (sigma_tc, N_MC, n_ok))
    print("  absolute difference: %.6f   (%.2f sigma)" % (diff, diff / sigma_tc))
    print("  tolerance          : %.4f  (3 sigma + %.3f finite-size bound)"
          % (tol, FINITE_SIZE_BOUND))
    print("  pass on 3 sigma alone: %s   (3 sigma = %.4f)"
          % ("yes" if diff <= 3.0 * sigma_tc else "no", 3.0 * sigma_tc))
    print("  wall-clock runtime : %.1f s" % runtime)
    print()
    print("MEASURED=%.4f" % tc_measured)
    print("PUBLISHED=%.6f" % TC_EXACT)
    print("ERROR_ESTIMATE=%.4f" % sigma_tc)
    print("TOLERANCE=%.4f" % tol)
    print("ABS_DIFF=%.4f" % diff)
    print("RUNTIME_S=%.1f" % runtime)
    print("RESULT=%s" % ("PASS" if ok else "FAIL"))

    # Exit on the same boolean that printed RESULT=. A NaN tolerance would
    # make `diff > tol` False and hide a printed FAIL behind exit 0.
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
