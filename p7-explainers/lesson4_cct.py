"""Equal-area criterion and bisection for critical clearing time.

Swing convention: 2H d(dw)/dt = P_m - P_e - K_D dw
                   d(delta)/dt = omega_0 dw
Stdlib only. Run: python lesson4_cct.py
"""
import math

H = 3.5
OMEGA_0 = 2.0 * math.pi * 60.0
E_P = 1.1
V_INF = 1.0
X_PRE = 0.65
X_POST = 0.45 + 0.40
P_M = 0.8

P_MAX_PRE = E_P * V_INF / X_PRE
P_MAX_POST = E_P * V_INF / X_POST


def f(x, p_max, k_d):
    """State derivative. x = (delta, dw). p_max = 0 during the fault."""
    delta, dw = x
    ddelta = OMEGA_0 * dw
    ddw = (P_M - p_max * math.sin(delta) - k_d * dw) / (2.0 * H)
    return (ddelta, ddw)


def rk4_step(x, p_max, k_d, h):
    k1 = f(x, p_max, k_d)
    x2 = (x[0] + 0.5 * h * k1[0], x[1] + 0.5 * h * k1[1])
    k2 = f(x2, p_max, k_d)
    x3 = (x[0] + 0.5 * h * k2[0], x[1] + 0.5 * h * k2[1])
    k3 = f(x3, p_max, k_d)
    x4 = (x[0] + h * k3[0], x[1] + h * k3[1])
    k4 = f(x4, p_max, k_d)
    dd = (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
    dw = (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
    return (x[0] + h * dd, x[1] + h * dw)


def stable(t_clear, delta0, delta_max, k_d=0.0, h=0.5e-3, t_end=5.0):
    """True if delta never crosses delta_max after clearing at t_clear."""
    x = (delta0, 0.0)
    t = 0.0
    while t < t_clear - 1e-12:
        x = rk4_step(x, 0.0, k_d, h)
        t += h
    while t < t_end - 1e-12:
        x = rk4_step(x, P_MAX_POST, k_d, h)
        t += h
        if x[0] > delta_max:
            return False
    return True


def bisect_tcr(delta0, delta_max, k_d=0.0, lo=0.10, hi=0.25, tol=1e-3):
    """Bisection over t_clear; lo must be stable, hi must be unstable."""
    assert stable(lo, delta0, delta_max, k_d)
    assert not stable(hi, delta0, delta_max, k_d)
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if stable(mid, delta0, delta_max, k_d):
            lo = mid
        else:
            hi = mid
    return lo, hi


def main():
    delta0 = math.asin(P_M / P_MAX_PRE)
    delta_max = math.pi - math.asin(P_M / P_MAX_POST)
    num = P_M * (delta_max - delta0) + P_MAX_POST * math.cos(delta_max)
    cos_dcr = num / P_MAX_POST
    delta_cr = math.acos(cos_dcr)
    t_cr = math.sqrt(4.0 * H * (delta_cr - delta0) / (OMEGA_0 * P_M))

    print("=== Equal-area criterion (closed form) ===")
    print("P_max_pre  = %.4f pu" % P_MAX_PRE)
    print("P_max_post = %.4f pu" % P_MAX_POST)
    print("delta_0    = %.4f rad = %.4f deg" % (delta0, math.degrees(delta0)))
    print("delta_max  = %.4f rad = %.4f deg" %
          (delta_max, math.degrees(delta_max)))
    print("cos(delta_cr) = %.4f" % cos_dcr)
    print("delta_cr   = %.4f rad = %.4f deg" %
          (delta_cr, math.degrees(delta_cr)))
    print("t_cr       = %.4f s = %.2f cycles at 60 Hz" %
          (t_cr, t_cr * 60.0))

    print()
    print("=== Bisection over simulations (K_D = 0, h = 0.5 ms) ===")
    lo, hi = bisect_tcr(delta0, delta_max, k_d=0.0, tol=1e-3)
    print("bracket: [%.4f, %.4f] s, tol 1 ms" % (lo, hi))
    print("equal-area value t_cr = %.4f s falls in the bracket: %s" %
          (t_cr, lo <= t_cr <= hi))

    print()
    print("=== Exercise 2: tighter bisection, tol = 0.1 ms ===")
    lo2, hi2 = bisect_tcr(delta0, delta_max, k_d=0.0, tol=1e-4)
    print("bracket: [%.5f, %.5f] s, step h = 0.5 ms, tol 0.1 ms" %
          (lo2, hi2))

    print()
    print("=== Exercise 3: damped case, K_D = 2 pu ===")
    lo3, hi3 = bisect_tcr(delta0, delta_max, k_d=2.0, tol=1e-3)
    print("bracket: [%.4f, %.4f] s, tol 1 ms" % (lo3, hi3))
    print("longer than the undamped 0.1701 s: %s" % (lo3 > t_cr))

    print()
    print("=== Exercise 4: protection margin ===")
    t_protect = 5.0 / 60.0
    margin_ms = (t_cr - t_protect) * 1000.0
    print("protection clearing (5 cycles) = %.4f s = %.1f ms" %
          (t_protect, t_protect * 1000.0))
    print("t_cr = %.4f s = %.1f ms" % (t_cr, t_cr * 1000.0))
    print("margin = %.1f ms" % margin_ms)


if __name__ == "__main__":
    main()
