"""Probes for Lesson 6 exercises 3 and 4 (weak-grid PLL retuning).

Stdlib only. Run: python lesson6_exercises.py
"""
import math

V_G = 1.0
I_D = 1.0
K_I_PLL = (2.0 * math.pi * 10.0) ** 2
K_P_PLL = 2.0 * 0.707 * (2.0 * math.pi * 10.0)


def theta0_of(scr):
    x_g = 1.0 / scr
    return math.asin(x_g * I_D / V_G)


def zeta_of(scr, k_p, k_i):
    theta0 = theta0_of(scr)
    k_pll = V_G * math.cos(theta0)
    omega_n = math.sqrt(k_pll * k_i)
    return k_pll * k_p / (2.0 * omega_n), k_pll, theta0


def exercise3():
    step = 0.001
    scr = 10.0
    found = None
    while scr >= 1.01:
        zeta, k_pll, theta0 = zeta_of(scr, K_P_PLL, K_I_PLL)
        if zeta < 0.3:
            found = (scr, zeta, k_pll, theta0)
            break
        scr -= step
    print("Exercise 3: sweep resolution d(SCR)=%.3f" % step)
    print("first SCR with zeta_pll < 0.3: SCR=%.3f  zeta=%.4f  "
          "K_pll=%.3f  theta0=%.1f deg"
          % (found[0], found[1], found[2], math.degrees(found[3])))
    analytic_scr = 1.0 / math.sin(math.radians(79.6))
    print("analytic check: zeta=0.300 at K_pll=0.180, "
          "theta0=79.6 deg, SCR=%.3f" % analytic_scr)


def exercise4():
    scr_tune = 1.2
    theta0 = theta0_of(scr_tune)
    k_pll_tune = V_G * math.cos(theta0)
    k_p_new = K_P_PLL / k_pll_tune
    k_i_new = K_I_PLL / k_pll_tune
    print()
    print("Exercise 4: retune at SCR=%.1f so zeta_pll=0.707"
          % scr_tune)
    print("k_p_pll=%.1f  k_i_pll=%.1f" % (k_p_new, k_i_new))
    zeta_10, k_pll_10, _ = zeta_of(10.0, k_p_new, k_i_new)
    omega_n_10 = math.sqrt(k_pll_10 * k_i_new)
    print("at SCR=10: omega_n_pll=%.1f rad/s  zeta_pll=%.3f"
          % (omega_n_10, zeta_10))


if __name__ == "__main__":
    exercise3()
    exercise4()
