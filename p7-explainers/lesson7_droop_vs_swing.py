"""Droop-as-swing checks: algebra identity, RK4 vs eigenvalues, energy.

Swing convention: 2H d(dw)/dt = P_m - P_e - K_D dw
                   d(delta)/dt = omega_0 dw
Stdlib only. Run: python lesson7_droop_vs_swing.py
"""
import math

M_P = 0.05
OMEGA_C = 2.0 * math.pi * 1.0
H_EQ = 1.0 / (2.0 * M_P * OMEGA_C)
K_D_EQ = 1.0 / M_P
DP_STEP = 0.1
H_STEP = 1e-4
N_STEPS = 200000

# Part 1: filtered droop law vs its matched swing equation, same step.
dw_droop = 0.0
dw_swing = 0.0
max_diff = 0.0
for _ in range(N_STEPS):
    ddw_droop = -OMEGA_C * dw_droop - M_P * OMEGA_C * DP_STEP
    ddw_swing = (-DP_STEP - K_D_EQ * dw_swing) / (2.0 * H_EQ)
    dw_droop += H_STEP * ddw_droop
    dw_swing += H_STEP * ddw_swing
    diff = abs(dw_droop - dw_swing)
    if diff > max_diff:
        max_diff = diff
print("Part 1: identity check of the algebra, not a physics test")
print("H_eq = %.3f s, K_D_eq = %.1f pu" % (H_EQ, K_D_EQ))
print("largest |dw_droop - dw_swing| = %.1e pu" % max_diff)
print("dw_droop final = %.6f pu (-m_p * dP = %.6f)"
      % (dw_droop, -M_P * DP_STEP))

# Part 2: nonlinear droop converter against the Lesson 2 grid.
E, V, X = 1.1, 1.0, 0.65
OMEGA_0 = 2.0 * math.pi * 60.0
P_MAX = E * V / X
P_REF0, P_REF1 = 0.8, 0.85
THETA0 = math.asin(P_REF0 / P_MAX)
K_S = P_MAX * math.cos(THETA0)


def deriv(theta, p_f, p_ref):
    dw = -M_P * (p_f - p_ref)
    p_e = P_MAX * math.sin(theta)
    return OMEGA_0 * dw, OMEGA_C * (p_e - p_f)


def rk4(theta, p_f, p_ref, h):
    k1 = deriv(theta, p_f, p_ref)
    k2 = deriv(theta + 0.5 * h * k1[0], p_f + 0.5 * h * k1[1], p_ref)
    k3 = deriv(theta + 0.5 * h * k2[0], p_f + 0.5 * h * k2[1], p_ref)
    k4 = deriv(theta + h * k3[0], p_f + h * k3[1], p_ref)
    dtheta = (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
    dpf = (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
    return theta + h * dtheta, p_f + h * dpf


theta, p_f, t, h = THETA0, P_REF0, 0.0, 1e-4
theta_eq1 = math.asin(P_REF1 / P_MAX)
peaks = []
prev, prev2 = theta, theta
for i in range(300000):
    theta, p_f = rk4(theta, p_f, P_REF1, h)
    t += h
    err = theta - theta_eq1
    err_prev = prev - theta_eq1
    err_prev2 = prev2 - theta_eq1
    if err_prev > err and err_prev > err_prev2:
        peaks.append((t - h, err_prev))
    prev2, prev = prev, theta
sigma_meas = math.log(abs(peaks[0][1] / peaks[1][1])) / (peaks[1][0]
                                                           - peaks[0][0])
omega_d_meas = 2.0 * math.pi / (peaks[1][0] - peaks[0][0])
print("\nPart 2: RK4 on the nonlinear droop converter vs the L2 grid")
print("K_s = %.4f pu/rad" % K_S)
print("measured omega_d = %.2f rad/s (target 12.91)" % omega_d_meas)
print("measured sigma = %.3f 1/s (target -3.142)" % -sigma_meas)

# Part 3: stored-energy ratios.
C_DC, V_DC0, S_BASE = 0.020, 1200.0, 1.0e6
E_DC = 0.5 * C_DC * V_DC0 ** 2
H_MATCH = E_DC / S_BASE
H_MACHINE = 3.5
RATIO_MACHINE_DC = H_MACHINE / H_MATCH
E_INERTIAL_100MVA = 16.0e6
RATIO_MISMATCHED = E_INERTIAL_100MVA / E_DC
RATIO_PER_MVA = (E_INERTIAL_100MVA / 100.0) / E_DC
print("\nPart 3: stored energy ratios")
print("E_dc = %.1f kJ, H_eq(matching) = %.4f s" % (E_DC / 1e3, H_MATCH))
print("machine 3.5 s / DC link: ratio = %.0f" % RATIO_MACHINE_DC)
print("16 MJ (100 MVA) / 14.4 kJ (1 MVA), mismatched ratings: %.0f"
      % RATIO_MISMATCHED)
print("per-MVA: 0.16 MJ / 14.4 kJ = %.1f" % RATIO_PER_MVA)
