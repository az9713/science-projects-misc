"""P3 PDE bake-off: Fourier pseudo-spectral method.

Benchmark (shared by all methods):
  u_t + u u_x = nu u_xx,  x in [0, 2pi] periodic,  t in [0, 0.5],  nu = 0.07
  phi(x,t) = exp(-(x-4t)^2/(4nu(t+1))) + exp(-(x-4t-2pi)^2/(4nu(t+1)))
  u(x,t)   = -2 nu phi_x/phi + 4      (Cole-Hopf)

Scheme: Fourier Galerkin/collocation in space on N equispaced points.
  Nonlinear term -(u^2/2)_x is computed pseudo-spectrally with 3/2-rule
  zero padding (exact de-aliasing of the quadratic term).
  Diffusion nu u_xx is handled exactly by an integrating factor
  exp(-nu k^2 t), and the rest is advanced by classical RK4 (IF-RK4).
  dt is fixed small (DT_MAX) so the time error stays below the spatial error
  on every grid in the table.
Theoretical convergence: spectral, i.e. faster than any power of 1/N
(geometric/exponential in N for this analytic periodic solution).
Error: discrete L2 norm sqrt(dx * sum(err^2)) at t = 0.5 (same as other methods).

Note on the benchmark: the two-image phi is not exactly periodic. The missing
images are exp(-~43) relative at t = 0.5, so the exact solution is periodic
to about 1e-15 and does not limit the errors below.
"""
import json
import time
from pathlib import Path

import numpy as np

NU = 0.07
T_END = 0.5
L = 2.0 * np.pi
GRIDS = [64, 128, 192, 256, 320, 384]
DT_MAX = 1.0e-4
THEORETICAL_ORDER = None  # spectral: no finite algebraic order (see theoretical_order_note)


def exact(x, t, nu=NU):
    d = 4.0 * nu * (t + 1.0)
    a = x - 4.0 * t
    b = x - 4.0 * t - 2.0 * np.pi
    ea = np.exp(-a * a / d)
    eb = np.exp(-b * b / d)
    phi = ea + eb
    phi_x = -2.0 * a / d * ea - 2.0 * b / d * eb
    return -2.0 * nu * phi_x / phi + 4.0


def make_nonlinear(n):
    """Return f(uh) = FFT of -(u^2/2)_x, de-aliased with 3/2 zero padding."""
    k = np.fft.rfftfreq(n, d=1.0 / n)  # 0..n/2, integer wavenumbers on [0, 2pi]
    m = 3 * n // 2
    ik = 1j * k
    ik[-1] = 0.0  # Nyquist mode of an odd derivative is set to zero

    def nonlinear(uh):
        pad = np.zeros(m // 2 + 1, dtype=complex)
        pad[: n // 2 + 1] = uh
        pad[n // 2] = 0.0  # drop Nyquist before padding (keeps u real, symmetric)
        u_fine = np.fft.irfft(pad, n=m) * (m / n)
        w_hat = np.fft.rfft(0.5 * u_fine * u_fine)[: n // 2 + 1] * (n / m)
        return -ik * w_hat

    return k, nonlinear


def solve(n, dt_max=None):
    x = np.arange(n) * (L / n)
    k, nonlinear = make_nonlinear(n)
    steps = int(np.ceil(T_END / (dt_max or DT_MAX)))
    dt = T_END / steps
    lin = -NU * k * k
    e_half = np.exp(0.5 * dt * lin)
    e_full = np.exp(dt * lin)
    vh = np.fft.rfft(exact(x, 0.0))
    for _ in range(steps):
        # IF-RK4 on v = exp(-lin t) uh; written directly in uh variables.
        a = dt * nonlinear(vh)
        b = dt * nonlinear(e_half * (vh + 0.5 * a))
        c = dt * nonlinear(e_half * vh + 0.5 * b)
        d = dt * nonlinear(e_full * vh + e_half * c)
        vh = e_full * vh + (e_full * a + 2.0 * e_half * (b + c) + d) / 6.0
    u = np.fft.irfft(vh, n=n)
    err = u - exact(x, T_END)
    return float(np.sqrt((L / n) * np.sum(err * err))), steps


def main():
    t0 = time.perf_counter()
    errors, step_list = [], []
    for n in GRIDS:
        e, s = solve(n)
        errors.append(e)
        step_list.append(s)
        print(f"N={n:5d}  steps={s:5d}  L2 error={e:.3e}")
    # Time-error check: halve dt on the finest grid; the error must not move
    # by more than 1%, so the table measures spatial error only.
    e_half_dt, _ = solve(GRIDS[-1], dt_max=0.5 * DT_MAX)
    dt_sensitivity = abs(e_half_dt - errors[-1]) / errors[-1]
    print(f"finest grid with dt/2: L2 error={e_half_dt:.3e}  relative change={dt_sensitivity:.2e}")
    runtime = time.perf_counter() - t0

    ns = np.array(GRIDS, dtype=float)
    le = np.log(np.array(errors))
    # Algebraic slope p in err ~ C N^-p (pairwise and least squares on all grids).
    pairwise = [float(-(le[i + 1] - le[i]) / np.log(ns[i + 1] / ns[i]))
                for i in range(len(ns) - 1)]
    p_alg = float(-np.polyfit(np.log(ns), le, 1)[0])
    # Exponential rate c in err ~ C exp(-c N): least squares of log(err) vs N.
    c_exp = float(-np.polyfit(ns, le, 1)[0])

    # Self-check: errors fall on every refinement, the finest error is small,
    # and the algebraic slope keeps growing (spectral signature, no fixed order).
    monotone = all(errors[i + 1] < errors[i] for i in range(len(errors) - 1))
    pairwise_growing = all(pairwise[i + 1] > pairwise[i] for i in range(len(pairwise) - 1))
    ok = (monotone and errors[-1] < 1e-8 and pairwise_growing and c_exp > 0.03
          and dt_sensitivity < 0.01 and runtime < 300)

    out = {
        "method": "spectral",
        "scheme": "Fourier pseudo-spectral, 3/2-rule de-aliasing, integrating-factor RK4 (diffusion exact)",
        "benchmark": "1D viscous Burgers, Cole-Hopf, nu=0.07, x in [0,2pi] periodic, t_end=0.5",
        "grids": GRIDS,
        "time_steps": step_list,
        "dt": T_END / step_list[0],
        "errors": errors,
        "error_norm": "discrete L2: sqrt(dx*sum(err^2)) at t=0.5",
        "pairwise_orders": pairwise,
        "observed_order": p_alg,
        "observed_order_fit": "least-squares slope of log(err) vs log(N) on all grids; spectral convergence has no fixed algebraic order, so this slope depends on the grid range (see pairwise_orders, which grow)",
        "observed_exponential_rate": c_exp,
        "observed_exponential_rate_fit": "least-squares slope c of err ~ C exp(-c N) on all grids",
        "dt_halving_relative_change_finest": dt_sensitivity,
        "theoretical_order": THEORETICAL_ORDER,
        "theoretical_order_note": "spectral: faster than any fixed power of N (exponential in N for this analytic periodic solution); compare observed_exponential_rate, not observed_order",
        "runtime_s": runtime,
        "pass": bool(ok),
    }
    Path(__file__).with_name("spectral-order.json").write_text(json.dumps(out, indent=2), newline=chr(10))
    print(f"algebraic slope={p_alg:.2f}  pairwise={['%.2f' % p for p in pairwise]}")
    print(f"exp rate c={c_exp:.3f}  runtime={runtime:.2f}s  pass={ok}")
    assert ok, "spectral self-check failed"


if __name__ == "__main__":
    main()
