"""Largest Lyapunov exponent of the Lorenz system (sigma=10, rho=28, beta=8/3).

METHOD: Benettin renormalization on the tangent flow.
  The state (x, y, z) and one tangent (deviation) vector (a, b, c) are
  integrated together with a fixed-step classical RK4. The tangent obeys the
  linearized equations J(x,y,z) . (a,b,c):
      da/dt = sigma (b - a)
      db/dt = (rho - z) a - b - x c
      dc/dt = y a + x b - beta c
  Every RENORM_STEPS steps the tangent norm is recorded and the tangent is
  rescaled to unit length. lambda_1 of one trajectory is the sum of the
  recorded log norms divided by the measured time.

PUBLISHED VALUE: lambda_1 = 0.9056.
  Source: J. C. Sprott, "Chaos and Time-Series Analysis", Oxford University
  Press (2003), Lorenz spectrum (0.9056, 0, -14.5723). An independent,
  rigorously bounded computation, D. Viswanath, "Lyapunov exponents from
  random Fibonacci sequences to the Lorenz equations" (PhD thesis, Cornell,
  1998), is quoted in secondary sources as 0.90566 and as 0.905630; the primary
  was not checked. The published values differ by 3e-5 to 6e-5, depending on
  which Viswanath figure is right, which is folded into the method-bias
  allowance below.

KNOWN METHOD BIAS AND ITS EXPECTED SIZE
  1. Finite step size. RK4 is 4th order; at dt = 0.01 with Lorenz time scales
     of order 1 the per-step truncation error is ~1e-10 and the induced shift
     in lambda_1 is far below the statistical error. This is checked, not
     assumed: a second, independent ensemble is run at dt = 0.005 and the
     Richardson estimate of the dt-error of the coarse run, (|d_coarse -
     d_fine| + 2 sigma_diff) / (2^4 - 1), is used as the integrator part of
     the bias allowance. The 2 sigma_diff term makes this a 2-sigma upper
     bound, because the central difference d_coarse - d_fine is below its own
     statistical noise.
  2. Finite averaging time and imperfect initial alignment of the tangent
     vector. The expectation of the finite-time exponent carries an O(1/T)
     term from the tangent not starting along the leading Lyapunov direction.
     A transient of T_TRANSIENT = 100 time units is integrated (with
     renormalization) before any accumulation, which both relaxes the state
     onto the attractor and aligns the tangent; the residual O(1/T) term at
     T_MEASURE = 1500 is asserted to be well under 1e-4. It is not measured.
  3. Published-value rounding: 3e-5 to 6e-5, depending on which Viswanath
     figure is right. The 4-decimal value 0.9056 carries a rounding half-width
     of 5e-5.
  The bias allowance is max(Richardson 2-sigma bound, 1e-4). The floor is
  asserted, not measured. Items 2 and 3 together are 5e-5 (published rounding)
  plus an unmeasured O(1/T) term.

ERROR ESTIMATE: block averaging over independent trajectories.
  N_TRAJ = 1024 trajectories are started from independent random initial
  conditions and integrated separately, so each yields one lambda estimate and
  the estimates are statistically independent -- stronger than segments cut
  from a single trajectory, which share the attractor's autocorrelation across
  the cut. ERROR_ESTIMATE is the standard error of the mean,
  std(lambda_i, ddof=1) / sqrt(N_TRAJ).

TOLERANCE = 3 * ERROR_ESTIMATE + bias allowance, i.e. a 3-sigma statistical
  band plus the stated method bias. It is not a fixed loose number; it shrinks
  if the ensemble is enlarged.

SELF-CHECKS (run before the measurement, both assert):
  a. The analytic Jacobian action used by the tangent flow is compared against
     a central finite difference of the Lorenz field at random points on the
     attractor.
  b. The whole renormalize-and-accumulate machinery is run on a linear system
     with an exactly known exponent, dv/dt = A v with A = [[1, 2], [3, -4]],
     whose eigenvalues are exactly 2 and -5. The measured exponent must equal
     2 to 1e-8; the observed residual is -2.6e-9, which is exactly the RK4
     truncation of exp(lambda*dt), (lambda*dt)^5 / (120*dt) at lambda=2,
     dt=0.01. The same formula at the Lorenz value lambda=0.9 gives 4.9e-11,
     so this part of the step-size bias is negligible; the trajectory part is
     what the dt-halving ensemble checks.

Deterministic: one fixed seed, no other stochastic input. numpy only.
"""

import sys
import time
import numpy as np

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

SEED = 20260922
N_TRAJ = 1024            # independent trajectories (= independent blocks)
DT = 0.01                # main step size
DT_FINE = 0.005          # halved step size, convergence check
T_TRANSIENT = 100.0      # discarded: attractor relaxation + tangent alignment
T_MEASURE = 1500.0       # accumulated, main run
T_MEASURE_FINE = 750.0   # accumulated, halved-dt run (shorter: 2x cost/step)
RENORM_TIME = 1.0        # renormalize the tangent every 1.0 time units

PUBLISHED = 0.9056
BIAS_FLOOR = 1.0e-4      # alignment O(1/T), asserted; plus 3e-5 to 6e-5
                         # published rounding, depending on which Viswanath
                         # figure is right


def lorenz_rhs(s):
    """Lorenz field and its linearization, stacked as rows of a (6, N) array."""
    x, y, z, a, b, c = s
    return np.array([
        SIGMA * (y - x),
        x * (RHO - z) - y,
        x * y - BETA * z,
        SIGMA * (b - a),
        (RHO - z) * a - b - x * c,
        y * a + x * b - BETA * c,
    ])


def rk4(s, dt, rhs):
    k1 = rhs(s)
    k2 = rhs(s + 0.5 * dt * k1)
    k3 = rhs(s + 0.5 * dt * k2)
    k4 = rhs(s + dt * k3)
    return s + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def benettin(s, dt, total_time, renorm_steps, accumulate, rhs=lorenz_rhs):
    """Integrate, renormalizing the tangent; return (state, summed log norms).

    accumulate=False runs the same dynamics but discards the log norms, which
    is how the transient is handled.
    """
    n_steps = int(round(total_time / dt))
    assert n_steps % renorm_steps == 0
    log_sum = np.zeros(s.shape[1])
    for _ in range(n_steps // renorm_steps):
        for _ in range(renorm_steps):
            s = rk4(s, dt, rhs)
        norm = np.sqrt(s[3] ** 2 + s[4] ** 2 + s[5] ** 2)
        if accumulate:
            log_sum += np.log(norm)
        s = s.copy()
        s[3:] /= norm
    return s, log_sum


def check_jacobian(rng):
    """Analytic tangent field vs central finite difference of the Lorenz field."""
    pts = np.stack([rng.uniform(-18, 18, 8),
                    rng.uniform(-24, 24, 8),
                    rng.uniform(2, 45, 8)])
    tang = rng.normal(size=(3, 8))
    tang /= np.sqrt((tang ** 2).sum(axis=0))
    h = 1.0e-6
    zeros = np.zeros((3, 8))
    plus = lorenz_rhs(np.vstack([pts + h * tang, zeros]))[:3]
    minus = lorenz_rhs(np.vstack([pts - h * tang, zeros]))[:3]
    fd = (plus - minus) / (2.0 * h)
    analytic = lorenz_rhs(np.vstack([pts, tang]))[3:]
    err = np.abs(fd - analytic).max()
    assert err < 1.0e-5, "analytic tangent field disagrees with finite difference: %g" % err
    return err


def check_linear_system():
    """Run the full Benettin machinery on a linear flow of known exponent.

    dv/dt = A v with A = [[1, 2], [3, -4]] embedded in the 6-row layout; the
    largest Lyapunov exponent is the largest real part of the eigenvalues of A.
    """
    amat = np.array([[1.0, 2.0], [3.0, -4.0]])
    expected = np.max(np.linalg.eigvals(amat).real)

    def linear_rhs(s):
        out = np.zeros_like(s)
        out[3] = amat[0, 0] * s[3] + amat[0, 1] * s[4]
        out[4] = amat[1, 0] * s[3] + amat[1, 1] * s[4]
        return out

    s = np.zeros((6, 3))
    s[3] = np.array([1.0, 0.3, -0.7])
    s[4] = np.array([0.0, 0.9, 0.2])
    s, _ = benettin(s, 0.01, 20.0, 100, False, linear_rhs)   # alignment
    _, log_sum = benettin(s, 0.01, 200.0, 100, True, linear_rhs)
    measured = log_sum / 200.0
    err = np.abs(measured - expected).max()
    # RK4 truncates exp(lambda*dt) after the 4th term, so the recovered rate is
    # low by (lambda*dt)^5 / (120*dt) = 2.7e-9 here. The bound is that, x4.
    assert err < 1.0e-8, "linear-system self-check gave %s, expected %.12f" % (measured, expected)
    return expected, err


def run_ensemble(dt, t_measure, seed_offset):
    rng = np.random.default_rng(SEED + seed_offset)
    s = np.zeros((6, N_TRAJ))
    s[0] = rng.uniform(-15.0, 15.0, N_TRAJ)
    s[1] = rng.uniform(-20.0, 20.0, N_TRAJ)
    s[2] = rng.uniform(5.0, 40.0, N_TRAJ)
    tang = rng.normal(size=(3, N_TRAJ))
    s[3:] = tang / np.sqrt((tang ** 2).sum(axis=0))

    renorm_steps = int(round(RENORM_TIME / dt))
    s, _ = benettin(s, dt, T_TRANSIENT, renorm_steps, False)
    _, log_sum = benettin(s, dt, t_measure, renorm_steps, True)
    return log_sum / t_measure


def main():
    t_start = time.perf_counter()

    jac_err = check_jacobian(np.random.default_rng(SEED + 99))
    lin_expected, lin_err = check_linear_system()
    print("self-check: analytic tangent field vs finite difference, max err %.2e" % jac_err)
    print("self-check: linear flow exponent %.12f, machinery err %.2e"
          % (lin_expected, lin_err))

    lam = run_ensemble(DT, T_MEASURE, 0)
    measured = float(lam.mean())
    sem = float(lam.std(ddof=1) / np.sqrt(N_TRAJ))

    lam_fine = run_ensemble(DT_FINE, T_MEASURE_FINE, 1)
    measured_fine = float(lam_fine.mean())
    sem_fine = float(lam_fine.std(ddof=1) / np.sqrt(N_TRAJ))

    delta = measured - measured_fine
    delta_sem = float(np.hypot(sem, sem_fine))
    # RK4 is 4th order: (2^4 - 1). The central difference sits below its own
    # noise, so add 2 combined sems and read the result as an upper bound.
    richardson = (abs(delta) + 2.0 * delta_sem) / 15.0
    bias = max(richardson, BIAS_FLOOR)

    tolerance = 3.0 * sem + bias
    abs_diff = abs(measured - PUBLISHED)
    runtime = time.perf_counter() - t_start
    ok = abs_diff <= tolerance

    print()
    print("Benettin renormalization, %d independent trajectories" % N_TRAJ)
    print("  main run   : dt=%.4f  transient T=%.0f  measured T=%.0f" % (DT, T_TRANSIENT, T_MEASURE))
    print("    lambda_1 per trajectory: mean %.6f  std %.6f  min %.4f  max %.4f"
          % (measured, lam.std(ddof=1), lam.min(), lam.max()))
    print("    standard error of the mean: %.6f" % sem)
    print("  dt-halving : dt=%.4f  transient T=%.0f  measured T=%.0f" % (DT_FINE, T_TRANSIENT, T_MEASURE_FINE))
    print("    lambda_1 = %.6f  sem %.6f" % (measured_fine, sem_fine))
    print("    difference coarse - fine: %+.6f  (combined sem %.6f)" % (delta, delta_sem))
    print("    Richardson dt-error of the coarse run, 2-sigma upper bound: %.6f" % richardson)
    print("  bias allowance: %.6f  (max of Richardson and floor %.1e)" % (bias, BIAS_FLOOR))
    tol_nofloor = 3.0 * sem + richardson
    print("  tolerance without the 1e-4 floor: %.6f  -> %s"
          % (tol_nofloor, "PASS" if abs_diff <= tol_nofloor else "FAIL"))
    print()

    print("MEASURED=%.6f" % measured)
    print("PUBLISHED=%.6f" % PUBLISHED)
    print("ERROR_ESTIMATE=%.6f" % sem)
    print("TOLERANCE=%.6f" % tolerance)
    print("ABS_DIFF=%.6f" % abs_diff)
    print("RUNTIME_S=%.1f" % runtime)
    print("RESULT=%s" % ("PASS" if ok else "FAIL"))

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
