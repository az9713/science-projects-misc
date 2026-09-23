"""Synchronization threshold Kc of the Kuramoto model, Lorentzian frequencies (gamma=1).

MODEL: dtheta_i/dt = w_i + (K/N) sum_j sin(theta_j - theta_i)
  = w_i + K * Im( z * exp(-i theta_i) ),  z = r exp(i psi) = (1/N) sum_j exp(i theta_j).
  The mean field z makes the N-body sum an O(N) operation, so every oscillator and
  every coupling strength K is advanced in one vectorized numpy step.

METHOD: measure r above threshold and extrapolate to r = 0.
  For a Lorentzian g(w) = gamma / (pi (w^2 + gamma^2)) the stationary self-consistent
  order parameter is known in closed form, r = sqrt(1 - Kc/K) for K > Kc, so
  r^2 is exactly linear in x = 1/K:  r^2 = 1 - Kc x.
  We integrate 8 values of K in [2.4, 5.0], time-average r after a transient, fit
  r^2 = a + b x by unweighted least squares, and take the x-intercept:
  Kc_measured = 1 / (-a/b) = -b/a.  The intercept form (not the slope alone) is used
  on purpose - see the multiplicative bias below, which cancels exactly in -b/a.

PUBLISHED VALUE: Kc = 2 / (pi g(0)) = 2 gamma = 2 exactly.
  Kuramoto, "Self-entrainment of a population of coupled non-linear oscillators",
  Lecture Notes in Physics 39 (1975) 420; Strogatz, Physica D 143 (2000) 1,
  eqs. (1)-(8) (Kc = 2/(pi g(0)) and r = sqrt(1 - Kc/K) for the Lorentzian).

FREQUENCIES: deterministic Lorentzian quantiles w_i = tan(pi ((i+0.5)/N - 0.5)),
  i = 0..N-1. The set is exactly antisymmetric (sum w_i = 0), which removes the
  O(N^-1/2) sampling noise of random draws and pins the mean frequency at 0, so psi
  does not drift. The full (untruncated) Lorentzian is kept; the extreme tail is
  |w| up to about N/pi, and those oscillators are drifting, not locked.

INTEGRATOR: Strang-split exact drift / Heun coupling, timestep dt = 0.01.
  Each step applies half of the free rotation exactly (theta += w dt/2, pre-reduced
  modulo 2 pi so that float32 phases stay in [-pi, pi) and lose no precision), then
  a second-order Heun step on the coupling term, then the second half rotation. The
  mean field z is sampled at the step boundary, that is before the first half drift
  and after the previous step's second half drift, which is the symmetric point of
  the Strang step (see method bias 1). Phases are float32; the mean field is
  accumulated in float64.

KNOWN METHOD BIAS AND ITS EXPECTED SIZE
  1. Discretization, multiplicative. The sampling point of the mean field, not the
     splitting order, sets this term. If the mean field is sampled after the exact
     drift and before the coupling kick, each locked oscillator sits w dt/2 past its
     fixed point at that moment, so its in-phase contribution drops by
     w^2 dt / (2 K r). Summed over the Lorentzian and amplified by the
     self-consistency factor 1 / (1 - F'(r)), this gives a common factor
     lambda = 1 - O(dt): measured 0.990 at dt = 0.01 and 0.979 at dt = 0.02 with
     that sampling point. Sampling before the drift gives the opposite sign
     (+1.9 % at dt = 0.02). The derivation accounts for 85 % of it (predicted 0.0174
     against 0.0205 measured at dt = 0.02); the drifting population supplies the
     rest, and that part is not derived here.
     This script therefore samples z at the boundary of a Strang step, where the
     residual is O(dt^2): 1.4e-4 at dt = 0.01 and 5.6e-4 at dt = 0.02 (ratio 3.8),
     so lambda is about 0.99986 at dt = 0.01, not 0.990. A common factor scales a
     and b alike, so -b/a is unchanged; only the residual, K-dependent part of the
     deficit biases Kc. It is bounded here by rerunning at dt = 0.02 (delta_dt
     below), and all of delta_dt is charged to bias, which is conservative for an
     O(dt^2) residual.
  2. Finite N. With quantile sampling the locked-population sum is a midpoint rule
     whose error is O(N^-3/2), below 1e-5 here. What remains is the positive bias of
     |z| from the fluctuating drifting population, of order 1/(2 r N) ~ 1e-5 in r at
     N = 8000. It is bounded by rerunning at N = 4000 (delta_N below).
  3. Aliasing. Any fixed-step integrator folds |w| > pi/dt onto an effective
     frequency w_eff = ((w dt + pi) mod 2 pi - pi)/dt. An oscillator with |w| > K r
     but |w_eff| < K r can lock spuriously and add up to 1/N to r. The expected
     count is 2 K r N / (pi (pi/dt)^2) ~ 0.03 for these parameters; the script
     counts them exactly and prints the count instead of arguing about it.
  4. Finite averaging window. The slowest drifting oscillator sits just outside the
     locked band, with period 2 pi / sqrt(w^2 - (K r)^2) ~ 100 time units at
     N = 8000 and amplitude 1/N in r; T_meas = 200 leaves a residual below 1e-5.

ERROR ESTIMATE AND TOLERANCE
  sigma_fit : standard error of Kc = -b/a, from the least-squares covariance of
              (a, b) (numpy polyfit cov=True) propagated with
              d(Kc)/da = b/a^2, d(Kc)/db = -1/a, covariance term included.
  delta_T   : |Kc(first half of the measurement window) - Kc(second half)|,
              the statistical scatter of the time average.
  delta_N   : |Kc(N=8000) - Kc(N=4000)| at dt = 0.01, bias source 2.
  delta_dt  : |Kc(dt=0.01) - Kc(dt=0.02)| at N=4000, bias source 1. With boundary
              sampling this difference comes out below delta_T, so it is a
              noise-floor bound on the dt bias, not a resolved measurement of it.
  ERROR_ESTIMATE = sqrt(sigma_fit^2 + delta_T^2)          (statistical)
  TOLERANCE      = 3 * ERROR_ESTIMATE + (delta_N + delta_dt)   (3 sigma + measured
                   method-bias allowance; no free constant is added anywhere)
  MEASURED is the N = 8000, dt = 0.01 run.
"""

import sys
import time
import numpy as np

SEED = 20260922
TWO_PI = 2.0 * np.pi

KS = np.array([2.4, 2.7, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0])   # all above Kc = 2
GAMMA = 1.0
KC_PUBLISHED = 2.0 * GAMMA

N_MAIN = 8000        # oscillators, run that produces MEASURED
N_SMALL = 4000       # finite-N check
DT = 0.01            # timestep of the reported run
DT_COARSE = 0.02     # timestep of the discretization check
T_TRANS = 100.0      # discarded; Ott-Antonsen relaxation rate is (K - Kc)/2 >= 0.2,
                     # so 100 time units is at least 20 relaxation times
T_MEAS = 200.0       # averaged


def quantile_frequencies(n):
    """Deterministic Lorentzian (Cauchy) quantiles, gamma=1, exactly antisymmetric."""
    u = (np.arange(n) + 0.5) / n
    return GAMMA * np.tan(np.pi * (u - 0.5))


def simulate(n, dt, ks=KS, t_trans=T_TRANS, t_meas=T_MEAS, seed=SEED):
    """Integrate the model for every K at once.

    Returns (r_full, r_first_half, r_second_half, abs_mean_z, alias_count),
    each an array over ks.  r_* are time averages of r = |z|.
    """
    k_col = np.asarray(ks, dtype=np.float64).reshape(-1, 1)
    nk = k_col.size
    w = quantile_frequencies(n)

    # Exact free rotation in two half steps (Strang), each pre-reduced to [-pi, pi)
    # so float32 phases stay bounded.  Two half drifts sum to w*dt modulo 2 pi;
    # halving the already-reduced full drift would not, so the half step is reduced
    # on its own.
    dw_half64 = (((w * (0.5 * dt)) + np.pi) % TWO_PI) - np.pi
    dw_half = np.broadcast_to(dw_half64.astype(np.float32), (nk, n)).copy()
    half_dt_k = (0.5 * k_col * dt).astype(np.float32)

    rng = np.random.default_rng(seed)
    theta0 = rng.uniform(-0.5 * np.pi, 0.5 * np.pi, size=n).astype(np.float32)
    theta = np.broadcast_to(theta0, (nk, n)).copy()

    cos_t = np.empty_like(theta)
    sin_t = np.empty_like(theta)
    k1 = np.empty_like(theta)
    k2 = np.empty_like(theta)
    saved = np.empty_like(theta)

    def field(out):
        """out <- 0.5*dt*K*Im(z exp(-i theta)) at the current theta; return z."""
        np.cos(theta, out=cos_t)
        np.sin(theta, out=sin_t)
        c = cos_t.mean(axis=1, keepdims=True).astype(np.float64)
        s = sin_t.mean(axis=1, keepdims=True).astype(np.float64)
        np.multiply(cos_t, s.astype(np.float32), out=out)
        out -= c.astype(np.float32) * sin_t
        out *= half_dt_k
        return (c + 1j * s).ravel()

    def sample_z():
        """z = (1/N) sum_j exp(i theta_j) at the current theta, float64 mean."""
        np.cos(theta, out=cos_t)
        np.sin(theta, out=sin_t)
        c = cos_t.mean(axis=1, keepdims=True).astype(np.float64)
        s = sin_t.mean(axis=1, keepdims=True).astype(np.float64)
        return (c + 1j * s).ravel()

    r_sum = np.zeros((2, nk))          # two halves of the measurement window
    z_sum = np.zeros(nk, dtype=np.complex128)
    counts = np.zeros(2, dtype=np.int64)

    n_trans = int(round(t_trans / dt))
    n_meas = int(round(t_meas / dt))

    def step(bucket):
        if bucket >= 0:                        # sample at the Strang step boundary
            z = sample_z()
            r_sum[bucket] += np.abs(z)
            z_sum[:] += z
            counts[bucket] += 1
        np.add(theta, dw_half, out=theta)      # first half of the exact drift
        field(k1)                              # k1 holds 0.5*dt*f(theta)
        np.copyto(saved, theta)
        np.add(theta, k1, out=theta)           # Heun predictor: theta + dt*f
        np.add(theta, k1, out=theta)
        field(k2)
        np.add(saved, k1, out=theta)           # corrector: theta + dt*(f1+f2)/2
        np.add(theta, k2, out=theta)
        np.add(theta, dw_half, out=theta)      # second half of the exact drift
        np.subtract(theta, TWO_PI * np.floor((theta + np.pi) * (1.0 / TWO_PI)),
                    out=theta)

    for _ in range(n_trans):
        step(-1)
    for i in range(n_meas):
        step(0 if i < n_meas // 2 else 1)

    r_half = r_sum / counts.reshape(2, 1)
    r_full = r_sum.sum(axis=0) / counts.sum()
    abs_mean_z = np.abs(z_sum / counts.sum())

    # Aliased spurious locking (bias source 3), counted at the measured r.
    w_eff = ((((w * dt) + np.pi) % TWO_PI) - np.pi) / dt
    alias = np.empty(nk, dtype=np.int64)
    for j in range(nk):
        band = float(ks[j]) * r_full[j]
        alias[j] = int(np.count_nonzero((np.abs(w) > band) & (np.abs(w_eff) < band)))
    return r_full, r_half[0], r_half[1], abs_mean_z, alias


def fit_kc(ks, r):
    """Fit r^2 = a + b/K; return (Kc = -b/a, sigma_Kc, a, b)."""
    x = 1.0 / np.asarray(ks, dtype=np.float64)
    y = np.asarray(r, dtype=np.float64) ** 2
    (b, a), cov = np.polyfit(x, y, 1, cov=True)
    kc = -b / a
    d_da = b / a ** 2
    d_db = -1.0 / a
    var = (d_da ** 2 * cov[1, 1] + d_db ** 2 * cov[0, 0]
           + 2.0 * d_da * d_db * cov[0, 1])
    return kc, float(np.sqrt(max(var, 0.0))), a, b


def main():
    t_start = time.perf_counter()

    r_main, r_a, r_b, absz_main, alias_main = simulate(N_MAIN, DT)
    r_small, _, _, _, _ = simulate(N_SMALL, DT)
    r_coarse, _, _, _, _ = simulate(N_SMALL, DT_COARSE)

    kc_main, sigma_fit, a_fit, b_fit = fit_kc(KS, r_main)
    kc_a, _, _, _ = fit_kc(KS, r_a)
    kc_b, _, _, _ = fit_kc(KS, r_b)
    kc_small, _, _, _ = fit_kc(KS, r_small)
    kc_coarse, _, a_coarse, _ = fit_kc(KS, r_coarse)

    delta_t = abs(kc_a - kc_b)
    delta_n = abs(kc_main - kc_small)
    delta_dt = abs(kc_small - kc_coarse)

    error_estimate = float(np.sqrt(sigma_fit ** 2 + delta_t ** 2))
    bias_allow = delta_n + delta_dt
    tolerance = 3.0 * error_estimate + bias_allow
    abs_diff = abs(kc_main - KC_PUBLISHED)

    print("Kuramoto model, Lorentzian frequencies (gamma=%.1f), N=%d, dt=%.3f"
          % (GAMMA, N_MAIN, DT))
    print("  K      1/K      r        r^2       1-2/K     r^2/(1-2/K)  halves"
          "          |<z>|    aliased")
    for j, k in enumerate(KS):
        exact = 1.0 - KC_PUBLISHED / k
        print("  %.2f  %.5f  %.6f  %.6f  %.6f  %.6f    %.6f/%.6f  %.6f  %d"
              % (k, 1.0 / k, r_main[j], r_main[j] ** 2, exact,
                 r_main[j] ** 2 / exact, r_a[j], r_b[j], absz_main[j],
                 alias_main[j]))
    print()
    print("  fit r^2 = a + b/K :  a=%.6f  b=%.6f   (a is the dt scale factor"
          " lambda, expected 1-O(dt^2) with boundary sampling)" % (a_fit, b_fit))
    print("  lambda at dt=%.3f  : %.6f     lambda at dt=%.3f : %.6f"
          % (DT, a_fit, DT_COARSE, a_coarse))
    print("  Kc from -b/a      : %.6f" % kc_main)
    print("  window halves     : %.6f / %.6f   -> delta_T  = %.6f"
          % (kc_a, kc_b, delta_t))
    print("  N=%d, dt=%.3f   : %.6f             -> delta_N  = %.6f"
          % (N_SMALL, DT, kc_small, delta_n))
    print("  N=%d, dt=%.3f   : %.6f             -> delta_dt = %.6f"
          % (N_SMALL, DT_COARSE, kc_coarse, delta_dt))
    # Richardson extrapolation to dt -> 0 from the N=N_SMALL pair.  With boundary
    # sampling the leading sampling residual is O(dt^2) (1.4e-4 at dt=0.01 against
    # 5.6e-4 at dt=0.02, ratio 3.8), so the dt=0 estimate is
    # Kc(h) + (Kc(h) - Kc(2h)) / 3, and the statistical uncertainty of that
    # combination is sqrt((4/3)^2 + (1/3)^2) = 1.374 times the single-run error.
    kc_rich = kc_small + (kc_small - kc_coarse) / 3.0
    kc_rich_err = np.sqrt((4.0 / 3.0) ** 2 + (1.0 / 3.0) ** 2) * error_estimate
    signed_diff = kc_main - KC_PUBLISHED
    dt_bias = kc_small - kc_rich          # estimated dt bias of a dt=DT run
    stat_resid = signed_diff - dt_bias
    print("  fit standard err  : %.6f" % sigma_fit)
    print("  Richardson Kc(dt -> 0) from the N=%d pair, O(dt^2) form: %.6f"
          "  (uncertainty about %.1e)" % (N_SMALL, kc_rich, kc_rich_err))
    print("  summary: Kc = %.4f +/- %.1e (statistical) +/- %.1e (systematic);"
          " signed diff %+.1e = dt-bias %+.1e plus statistical residual %+.1e"
          % (kc_main, error_estimate, bias_allow, signed_diff, dt_bias,
             stat_resid))
    print("  spurious aliased locks, max over K : %d of %d oscillators"
          % (alias_main.max(), N_MAIN))
    print()

    runtime = time.perf_counter() - t_start
    result = "PASS" if abs_diff <= tolerance else "FAIL"
    print("MEASURED=%.6f" % kc_main)
    print("PUBLISHED=%.6f" % KC_PUBLISHED)
    print("ERROR_ESTIMATE=%.6f" % error_estimate)
    print("TOLERANCE=%.6f" % tolerance)
    print("ABS_DIFF=%.6f" % abs_diff)
    print("RUNTIME_S=%.1f" % runtime)
    print("RESULT=%s" % result)

    if result == "FAIL":
        print("Kc_measured %.6f differs from published %.6f by %.6f > tolerance"
              " %.6f" % (kc_main, KC_PUBLISHED, abs_diff, tolerance))
        sys.exit(1)


if __name__ == "__main__":
    main()
