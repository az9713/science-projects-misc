"""P3 PDE bake-off: finite-volume solver for 1D viscous Burgers.

u_t + u u_x = nu u_xx on [0, 2pi], periodic, nu = 0.07, t in [0, 0.5].
Analytic (Cole-Hopf) solution:
    phi(x,t) = exp(-(x-4t)^2/(4nu(t+1))) + exp(-(x-4t-2pi)^2/(4nu(t+1)))
    u = -2 nu phi_x / phi + 4

Scheme: cell-average finite volume, unlimited linear (Fromm) reconstruction,
Rusanov (local Lax-Friedrichs) convective flux, central 2nd-order viscous
flux, SSP-RK3 time stepping. Theoretical spatial order 2.
Initial data and reference are EXACT cell averages:
    mean_cell(u) = 4 - 2 nu [ln phi(b) - ln phi(a)] / h
Error: discrete L2 norm sqrt(h * sum (U - Uexact)^2) at t = 0.5.
"""
import json
import os
import time

import numpy as np

NU = 0.07
T_END = 0.5
L = 2.0 * np.pi
GRIDS = [128, 256, 512, 1024, 2048]
THEORETICAL_ORDER = 2.0


def log_phi(x, t):
    s = 4.0 * NU * (t + 1.0)
    a = -((x - 4.0 * t) ** 2) / s
    b = -((x - 4.0 * t - 2.0 * np.pi) ** 2) / s
    return np.logaddexp(a, b)


def u_exact(x, t):
    s = 4.0 * NU * (t + 1.0)
    a = -((x - 4.0 * t) ** 2) / s
    b = -((x - 4.0 * t - 2.0 * np.pi) ** 2) / s
    m = np.maximum(a, b)
    ea, eb = np.exp(a - m), np.exp(b - m)
    dphi = ea * (-2.0 * (x - 4.0 * t) / s) + eb * (-2.0 * (x - 4.0 * t - 2.0 * np.pi) / s)
    return -2.0 * NU * dphi / (ea + eb) + 4.0


def cell_averages(n, t):
    edges = np.linspace(0.0, L, n + 1)
    h = L / n
    lp = log_phi(edges, t)
    return 4.0 - 2.0 * NU * np.diff(lp) / h


def rhs(U, h):
    # Fromm slope (unlimited, centered) -> 2nd order for smooth data
    slope = 0.5 * (np.roll(U, -1) - np.roll(U, 1))
    uL = U + 0.5 * slope                      # left state at face i+1/2
    uR = np.roll(U - 0.5 * slope, -1)         # right state at face i+1/2
    a = np.maximum(np.abs(uL), np.abs(uR))
    fconv = 0.25 * (uL ** 2 + uR ** 2) - 0.5 * a * (uR - uL)
    fvisc = -NU * (np.roll(U, -1) - U) / h
    F = fconv + fvisc                         # flux at face i+1/2
    return -(F - np.roll(F, 1)) / h


def solve(n):
    h = L / n
    U = cell_averages(n, 0.0)
    umax = np.max(np.abs(U))
    dt = min(0.4 * h / umax, 0.25 * h * h / NU)
    nsteps = int(np.ceil(T_END / dt))
    dt = T_END / nsteps
    for _ in range(nsteps):
        U1 = U + dt * rhs(U, h)
        U2 = 0.75 * U + 0.25 * (U1 + dt * rhs(U1, h))
        U = U / 3.0 + 2.0 / 3.0 * (U2 + dt * rhs(U2, h))
    return U, nsteps


def main():
    t0 = time.perf_counter()
    # Periodicity check of the 2-image Cole-Hopf formula (it is not exactly periodic)
    per_gap = max(abs(u_exact(0.0, t) - u_exact(L, t)) for t in (0.0, T_END))
    errors, steps = [], []
    for n in GRIDS:
        U, ns = solve(n)
        h = L / n
        e = np.sqrt(h * np.sum((U - cell_averages(n, T_END)) ** 2))
        errors.append(float(e))
        steps.append(ns)
        print(f"N={n:4d} steps={ns:5d} L2={e:.3e}")
    hs = np.array([L / n for n in GRIDS])
    observed = float(np.polyfit(np.log(hs), np.log(errors), 1)[0])
    pair = [float(np.log2(errors[i] / errors[i + 1])) for i in range(len(GRIDS) - 1)]
    runtime = time.perf_counter() - t0
    ok = bool(abs(observed - THEORETICAL_ORDER) < 0.3 and errors[-1] < errors[0]
              and all(np.isfinite(errors)) and runtime < 300)
    print(f"pairwise orders={['%.3f' % p for p in pair]}  fitted={observed:.3f}")
    print(f"periodicity gap of analytic formula={per_gap:.2e}  runtime={runtime:.2f}s")
    out = {
        "method": "finite-volume",
        "scheme": "Fromm (unlimited MUSCL) + Rusanov flux, central viscous flux, SSP-RK3",
        "benchmark": "1D viscous Burgers, nu=0.07, x in [0,2pi] periodic, t_end=0.5, Cole-Hopf 2-image phi, u=-2nu phi_x/phi+4",
        "grids": GRIDS,
        "time_steps": steps,
        "errors": errors,
        "error_norm": "discrete L2 of cell averages vs exact cell averages, sqrt(h*sum e^2)",
        "pairwise_orders": pair,
        "observed_order": observed,
        "theoretical_order": THEORETICAL_ORDER,
        "analytic_periodicity_gap": float(per_gap),
        "runtime_s": runtime,
        "pass": ok,
    }
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finite-volume-order.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    assert ok, f"self-check failed: observed order {observed:.3f} vs {THEORETICAL_ORDER}"
    print("self-check PASS")


if __name__ == "__main__":
    main()
