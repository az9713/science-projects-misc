"""P3 PDE bake-off, method: finite-element.

Benchmark: 1D viscous Burgers  u_t + u u_x = nu u_xx  on x in [0, 2pi], periodic,
nu = 0.07, t in [0, 0.5].  Analytic (Cole-Hopf) solution:
    phi(x,t) = exp(-(x-4t)^2/(4nu(t+1))) + exp(-(x-4t-2pi)^2/(4nu(t+1)))
    u(x,t)   = -2 nu phi_x/phi + 4

Discretization: continuous Galerkin, P1 (piecewise-linear) elements on a uniform
periodic mesh, consistent mass matrix, group finite-element form for the flux
(f = u^2/2 interpolated in the P1 space). Semi-discrete system
    M du/dt = -C f(u) - nu K u
integrated in time with classical RK4 and a step dt ~ h^2, so the time error
(O(dt^4)) is far below the spatial error. Theoretical L2 order for P1: 2.
L2 error at t = 0.5 uses 5-point Gauss quadrature on every element.
"""
import json
import os
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu

NU = 0.07
T_END = 0.5
L = 2.0 * np.pi
GRIDS = [40, 80, 160, 320, 640, 1280]  # number of elements (= nodes, periodic)
FIT_GRIDS = [320, 640, 1280]        # three finest grids (asymptotic range) for the order fit
THEORETICAL_ORDER = 2.0
HERE = os.path.dirname(os.path.abspath(__file__))


def u_exact(x, t, nu=NU):
    """Cole-Hopf solution exactly as specified by the benchmark."""
    s = 4.0 * nu * (t + 1.0)
    a = x - 4.0 * t
    b = x - 4.0 * t - L
    e1 = np.exp(-a * a / s)
    e2 = np.exp(-b * b / s)
    phi = e1 + e2
    phi_x = -2.0 * a / s * e1 - 2.0 * b / s * e2
    return -2.0 * nu * phi_x / phi + 4.0


def periodic_matrix(n, diag, off_lo, off_hi):
    """Circulant tridiagonal sparse matrix with periodic wrap."""
    i = np.arange(n)
    rows = np.concatenate([i, i, i])
    cols = np.concatenate([i, (i - 1) % n, (i + 1) % n])
    vals = np.concatenate([np.full(n, diag), np.full(n, off_lo), np.full(n, off_hi)])
    return sp.csc_matrix((vals, (rows, cols)), shape=(n, n))


def solve_fem(n):
    h = L / n
    x = np.arange(n) * h
    M = periodic_matrix(n, 4.0 * h / 6.0, h / 6.0, h / 6.0)     # int phi_i phi_j
    K = periodic_matrix(n, 2.0 / h, -1.0 / h, -1.0 / h)          # int phi_i' phi_j'
    C = periodic_matrix(n, 0.0, -0.5, 0.5)                       # int phi_i phi_j'
    lu = splu(M)

    def rhs(u):
        return lu.solve(-(C @ (0.5 * u * u)) - NU * (K @ u))

    umax = 8.0  # |u| <= 4 + pi/(t+1) < 8 for this benchmark
    dt_adv = 2.8 * h / (np.sqrt(3.0) * umax)   # consistent-mass advection bound
    dt_dif = 2.78 * h * h / (12.0 * NU)        # consistent-mass diffusion bound
    dt = 0.4 * min(dt_adv, dt_dif)
    nsteps = int(np.ceil(T_END / dt))
    dt = T_END / nsteps

    u = u_exact(x, 0.0)
    for _ in range(nsteps):
        k1 = rhs(u)
        k2 = rhs(u + 0.5 * dt * k1)
        k3 = rhs(u + 0.5 * dt * k2)
        k4 = rhs(u + dt * k3)
        u = u + dt / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return x, u, h, dt, nsteps


def l2_error(u_nodes, h, t):
    """||u_h - u||_{L2(0,2pi)} with 5-point Gauss quadrature per element."""
    n = u_nodes.size
    g, w = np.polynomial.legendre.leggauss(5)
    xi = 0.5 * (g + 1.0)                          # quadrature points on [0,1]
    left = np.arange(n) * h
    ul = u_nodes
    ur = np.roll(u_nodes, -1)                     # periodic right node
    xq = left[:, None] + h * xi[None, :]
    uh = ul[:, None] * (1.0 - xi[None, :]) + ur[:, None] * xi[None, :]
    err2 = (uh - u_exact(xq, t)) ** 2
    return float(np.sqrt(np.sum(err2 * (0.5 * h * w)[None, :])))


def main():
    t0 = time.perf_counter()
    # Periodicity check of the two-term benchmark formula (value mismatch at x=0 vs 2pi).
    per_gap = max(abs(u_exact(0.0, t) - u_exact(L, t)) for t in (0.0, T_END))

    errors, hs, dts = [], [], []
    for n in GRIDS:
        _, u, h, dt, nsteps = solve_fem(n)
        e = l2_error(u, h, T_END)
        errors.append(e)
        hs.append(h)
        dts.append(dt)
        print(f"N={n:5d}  h={h:.5f}  dt={dt:.3e}  steps={nsteps:6d}  L2 err={e:.4e}")

    idx = [GRIDS.index(n) for n in FIT_GRIDS]
    slope, _ = np.polyfit(np.log([hs[i] for i in idx]), np.log([errors[i] for i in idx]), 1)
    observed = float(slope)
    pair_orders = [float(np.log(errors[i] / errors[i + 1]) / np.log(hs[i] / hs[i + 1]))
                   for i in range(len(GRIDS) - 1)]
    runtime = time.perf_counter() - t0
    print(f"pairwise orders: {[round(p, 3) for p in pair_orders]}")
    print(f"observed order (LSQ fit on N={FIT_GRIDS}): {observed:.4f}  (theory {THEORETICAL_ORDER})")
    print(f"benchmark periodicity gap |u(0)-u(2pi)|: {per_gap:.2e}")
    print(f"runtime: {runtime:.2f} s")

    # Self-check.
    monotone = all(errors[i + 1] < errors[i] for i in range(len(errors) - 1))
    order_ok = abs(observed - THEORETICAL_ORDER) < 0.25
    passed = bool(monotone and order_ok and per_gap < 1e-8 and runtime < 300)

    out = {
        "method": "finite-element",
        "grids": GRIDS,
        "errors": errors,
        "observed_order": observed,
        "theoretical_order": THEORETICAL_ORDER,
        "runtime_s": round(runtime, 3),
        "pass": passed,
        "fit_grids": FIT_GRIDS,
        "pairwise_orders": pair_orders,
        "h": hs,
        "dt": dts,
        "discretization": "P1 continuous Galerkin, consistent mass, group FEM flux u^2/2, RK4, dt ~ h^2",
        "error_norm": "L2 over [0,2pi] at t=0.5, 5-pt Gauss per element, vs Cole-Hopf two-term formula",
        "benchmark": {"nu": NU, "t_end": T_END, "domain": [0.0, L], "periodicity_gap": per_gap},
    }
    with open(os.path.join(HERE, "finite-element-order.json"), "w") as f:
        json.dump(out, f, indent=2)

    assert monotone, f"errors not monotone decreasing: {errors}"
    assert order_ok, f"observed order {observed:.3f} not within 0.25 of {THEORETICAL_ORDER}"
    assert per_gap < 1e-8, f"benchmark not periodic to 1e-8: {per_gap}"
    assert runtime < 300, f"runtime {runtime:.1f}s exceeds 5 minutes"
    print("SELF-CHECK PASS")


if __name__ == "__main__":
    main()
