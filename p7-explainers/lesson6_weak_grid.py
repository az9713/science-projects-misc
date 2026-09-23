"""Weak-grid current-source PLL: existence bound and loop runaway.

Part 1: bisection for theta_0 over a range of SCR, plus PLL gain and
damping. Part 2: RK4 integration of the nonlinear PI-PLL loop, showing
lock at SCR = 1.2 and loss of synchronism at SCR = 0.95.

Swing/PLL convention matches Lesson 2/5: gains named k_p_pll, k_i_pll.
Stdlib only. Run: python lesson6_weak_grid.py
"""
import math

V_G = 1.0
I_D = 1.0
K_I_PLL = (2.0 * math.pi * 10.0) ** 2
K_P_PLL = 2.0 * 0.707 * (2.0 * math.pi * 10.0)


def v_q(theta_p, x_g):
    return x_g * I_D - V_G * math.sin(theta_p)


def bisect_theta0(x_g, lo=0.0, hi=math.pi / 2.0, tol=1e-10):
    if v_q(hi, x_g) > 0.0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if v_q(mid, x_g) > 0.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def part1():
    print("SCR    theta0(deg) K_pll   P       P_max   "
          "omega_n(rad/s) zeta")
    for scr in (10.0, 3.0, 2.0, 1.5, 1.2, 1.05, 0.95):
        x_g = 1.0 / scr
        theta0 = bisect_theta0(x_g)
        if theta0 is None:
            print("%5.2f  no steady state (X_g I_d=%.4f > V_g)"
                  % (scr, x_g * I_D))
            continue
        k_pll = V_G * math.cos(theta0)
        p = (V_G ** 2 / (2.0 * x_g)) * math.sin(2.0 * theta0)
        p_max = scr * V_G ** 2 / 2.0
        omega_n = math.sqrt(k_pll * K_I_PLL)
        zeta = k_pll * K_P_PLL / (2.0 * omega_n)
        print("%5.2f  %9.2f  %.4f  %.4f  %.3f   %7.2f       %.4f"
              % (scr, math.degrees(theta0), k_pll, p, p_max,
                 omega_n, zeta))


def rk4_step(state, dt, x_g):
    def deriv(s):
        theta_p, z = s
        vq = v_q(theta_p, x_g)
        return (K_P_PLL * vq + z, K_I_PLL * vq)

    k1 = deriv(state)
    s2 = tuple(state[i] + 0.5 * dt * k1[i] for i in range(2))
    k2 = deriv(s2)
    s3 = tuple(state[i] + 0.5 * dt * k2[i] for i in range(2))
    k3 = deriv(s3)
    s4 = tuple(state[i] + dt * k3[i] for i in range(2))
    k4 = deriv(s4)
    return tuple(state[i] + (dt / 6.0) * (k1[i] + 2 * k2[i]
                 + 2 * k3[i] + k4[i]) for i in range(2))


def simulate(scr, t_end=0.5, dt=1e-4):
    x_g = 1.0 / scr
    state = (0.0, 0.0)
    trace = [(0.0, 0.0)]
    t = 0.0
    n = int(t_end / dt)
    for _ in range(n):
        state = rk4_step(state, dt, x_g)
        t += dt
        trace.append((t, state[0]))
    return trace


def part2():
    for scr in (1.2, 0.95):
        trace = simulate(scr)
        t_end, theta_end = trace[-1]
        print("SCR=%.2f  theta_p(t=%.2fs)=%.4f rad (%.2f deg)"
              % (scr, t_end, theta_end, math.degrees(theta_end)))


if __name__ == "__main__":
    part1()
    print()
    print("k_p_pll=%.2f  k_i_pll=%.1f" % (K_P_PLL, K_I_PLL))
    print()
    part2()
