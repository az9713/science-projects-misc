"""Forward Euler, semi-implicit Euler, and RK4 on the SMIB swing
equation: which one lies about stability at h = 10 ms?

Swing convention: 2H d(dw)/dt = P_m - P_e - K_D dw
                   d(delta)/dt = omega_0 dw
Stdlib only. Run: python lesson3_euler_drift.py
"""
import cmath
import math

H = 3.5
K_D = 2.0
OMEGA_0 = 2.0 * math.pi * 60.0
P_MAX = 1.1 * 1.0 / 0.65


def f(x, p_m, k_d=K_D):
    delta, dw = x
    ddelta = OMEGA_0 * dw
    ddw = (p_m - P_MAX * math.sin(delta) - k_d * dw) / (2.0 * H)
    return (ddelta, ddw)


def equilibrium(p_m):
    delta = math.asin(p_m / P_MAX)
    k_s = P_MAX * math.cos(delta)
    a10, a11 = -k_s / (2.0 * H), -K_D / (2.0 * H)
    disc = cmath.sqrt(a11 * a11 + 4.0 * a10 * OMEGA_0)
    return delta, (a11 + disc) / 2.0


def euler_step(x, p_m, h):
    dx = f(x, p_m)
    return (x[0] + h * dx[0], x[1] + h * dx[1])


def semi_implicit_step(x, p_m, h):
    delta, dw = x
    ddw = (p_m - P_MAX * math.sin(delta) - K_D * dw) / (2.0 * H)
    dw_new = dw + h * ddw
    return (delta + h * OMEGA_0 * dw_new, dw_new)


def rk4_step(x, p_m, h):
    k1 = f(x, p_m)
    x2 = (x[0] + 0.5*h*k1[0], x[1] + 0.5*h*k1[1])
    k2 = f(x2, p_m)
    x3 = (x[0] + 0.5*h*k2[0], x[1] + 0.5*h*k2[1])
    k3 = f(x3, p_m)
    x4 = (x[0] + h*k3[0], x[1] + h*k3[1])
    k4 = f(x4, p_m)
    dd = (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6.0
    dw = (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6.0
    return (x[0] + h*dd, x[1] + h*dw)


def late_amplitude(step_fn, delta0, delta_new, p_m, h, t_end):
    x = (delta0, 0.0)
    n = int(round(t_end / h))
    amp = 0.0
    for i in range(n):
        x = step_fn(x, p_m, h)
        t = (i + 1) * h
        if 8.0 <= t <= 10.0:
            amp = max(amp, abs(x[0] - delta_new))
    return math.degrees(amp)


def slip_time(delta0, p_m, h, t_end):
    x = (delta0, 0.0)
    n = int(round(t_end / h))
    for i in range(n):
        x = euler_step(x, p_m, h)
        if abs(x[0]) > math.pi:
            return (i + 1) * h
    return None


def main():
    delta0, lam = equilibrium(0.8)
    sigma, omega_d = lam.real, lam.imag
    print("lambda = %.4f %+.4fj 1/s (sigma, omega_d)" % (sigma, omega_d))

    h = 0.01
    mag = abs(1.0 + h * lam)
    growth = math.log(mag) / h
    print("h = %.3f s: |1 + h*lambda| = %.5f" % (h, mag))
    print("Euler growth rate  = %+.3f 1/s (physical = %+.3f 1/s)" %
          (growth, sigma))
    print("Euler amplitude x10s  = %.3f" % (mag ** (10.0 / h)))
    print("True amplitude x10s   = %.3f" % math.exp(sigma * 10.0))

    h_crit = -2.0 * sigma / (sigma * sigma + omega_d * omega_d)
    print("h_crit (formula) = %.5f s = %.2f ms" % (h_crit, h_crit * 1000))

    lo, hi = 0.0001, 0.02
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if abs(1.0 + mid * lam) < 1.0:
            lo = mid
        else:
            hi = mid
    print("h_crit (bisection) = %.5f s = %.2f ms" % (lo, lo * 1000))

    h1 = 0.001
    mag1 = abs(1.0 + h1 * lam)
    print("h = %.3f s: Euler amplitude x10s = %.3f" %
          (h1, mag1 ** (10.0 / h1)))

    p_m_new = 0.85
    delta_new, _ = equilibrium(p_m_new)
    amp0 = math.degrees(delta_new - delta0)
    print("\nInitial amplitude |delta_new - delta0| = %.2f deg" % amp0)
    for name, step_fn in (("forward Euler", euler_step),
                           ("semi-implicit Euler", semi_implicit_step),
                           ("RK4", rk4_step)):
        amp = late_amplitude(step_fn, delta0, delta_new, p_m_new, 0.01, 10.0)
        print("%-20s late amplitude (8-10 s) = %.3f deg" % (name, amp))

    t_slip = slip_time(delta0, p_m_new, 0.01, 60.0)
    print("\nForward Euler, h = 10 ms, run to 60 s:")
    print("slip time (|delta| > 180 deg) = %.2f s" % t_slip)


if __name__ == "__main__":
    main()
