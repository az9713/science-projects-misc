"""P3 PDE bake-off: finite-difference method.

Benchmark (shared by all methods):
  u_t + u u_x = nu u_xx,  x in [0, 2pi] periodic,  t in [0, 0.5],  nu = 0.07
  phi(x,t) = exp(-(x-4t)^2/(4nu(t+1))) + exp(-(x-4t-2pi)^2/(4nu(t+1)))
  u(x,t)   = -2 nu phi_x/phi + 4      (Cole-Hopf)

Scheme: method of lines. Space: 2nd-order central differences, conservative
flux form (u^2/2)_x and 3-point Laplacian on a uniform periodic grid.
Time: classical RK4 with dt ~ dx^2, so the time error O(dt^4) = O(dx^8) is
far below the spatial error O(dx^2). Theoretical order = 2.
Error: discrete L2 norm sqrt(dx * sum(err^2)) at t = 0.5.
"""
import json
import time
from pathlib import Path

import numpy as np

NU = 0.07
T_END = 0.5
L = 2.0 * np.pi
GRIDS = [64, 128, 256, 512, 1024]
THEORETICAL_ORDER = 2.0


def exact(x, t, nu=NU):
    d = 4.0 * nu * (t + 1.0)
    a = x - 4.0 * t
    b = x - 4.0 * t - 2.0 * np.pi
    ea = np.exp(-a * a / d)
    eb = np.exp(-b * b / d)
    phi = ea + eb
    phi_x = -2.0 * a / d * ea - 2.0 * b / d * eb
    return -2.0 * nu * phi_x / phi + 4.0


def rhs(u, dx, nu=NU):
    f = 0.5 * u * u
    up = np.roll(u, -1)
    um = np.roll(u, 1)
    flux_x = (np.roll(f, -1) - np.roll(f, 1)) / (2.0 * dx)
    u_xx = (up - 2.0 * u + um) / (dx * dx)
    return -flux_x + nu * u_xx


def solve(n):
    dx = L / n
    x = np.arange(n) * dx
    u = exact(x, 0.0)
    umax = np.max(np.abs(u))
    dt_target = min(0.25 * dx * dx / NU, 0.25 * dx / umax)
    steps = int(np.ceil(T_END / dt_target))
    dt = T_END / steps
    for _ in range(steps):
        k1 = rhs(u, dx)
        k2 = rhs(u + 0.5 * dt * k1, dx)
        k3 = rhs(u + 0.5 * dt * k2, dx)
        k4 = rhs(u + dt * k3, dx)
        u = u + dt / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    err = u - exact(x, T_END)
    return float(np.sqrt(dx * np.sum(err * err))), steps


def main():
    t0 = time.perf_counter()
    errors, steps = [], []
    for n in GRIDS:
        e, s = solve(n)
        errors.append(e)
        steps.append(s)
        print(f"N={n:5d}  steps={s:7d}  L2 error={e:.6e}")

    h = L / np.array(GRIDS, dtype=float)
    err = np.array(errors)
    pairwise = [float(np.log(err[i] / err[i + 1]) / np.log(h[i] / h[i + 1]))
                for i in range(len(GRIDS) - 1)]
    # Least-squares fit of log(err) = p log(h) + c on the finest 3 grids
    # (the asymptotic range; the coarsest grid under-resolves the front).
    fit_idx = slice(-3, None)
    p_fit = float(np.polyfit(np.log(h[fit_idx]), np.log(err[fit_idx]), 1)[0])
    p_all = float(np.polyfit(np.log(h), np.log(err), 1)[0])
    runtime = time.perf_counter() - t0

    print("pairwise orders:", ", ".join(f"{p:.3f}" for p in pairwise))
    print(f"observed order (finest 3 grids): {p_fit:.4f}; all grids: {p_all:.4f}")
    print(f"runtime: {runtime:.2f} s")

    # Self-check.
    assert all(np.isfinite(err)), "non-finite error"
    assert all(err[i + 1] < err[i] for i in range(len(err) - 1)), "error not decreasing"
    assert abs(p_fit - THEORETICAL_ORDER) < 0.2, f"observed order {p_fit} not near 2"
    assert err[-1] < 5e-3, f"finest-grid error {err[-1]} too large"
    assert runtime < 300.0, "runtime over 5 minutes"
    passed = True

    out = {
        "method": "finite-difference",
        "scheme": "2nd-order central FD (conservative flux + 3-point Laplacian), RK4 time, dt ~ dx^2",
        "benchmark": "1D viscous Burgers, Cole-Hopf, nu=0.07, x in [0,2pi] periodic, t_end=0.5",
        "grids": GRIDS,
        "time_steps": steps,
        "errors": errors,
        "error_norm": "discrete L2: sqrt(dx*sum(err^2)) at t=0.5",
        "pairwise_orders": pairwise,
        "observed_order": p_fit,
        "observed_order_fit": "least squares on finest 3 grids",
        "observed_order_all_grids": p_all,
        "theoretical_order": THEORETICAL_ORDER,
        "runtime_s": runtime,
        "pass": passed,
    }
    path = Path(__file__).with_name("finite-difference-order.json")
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
