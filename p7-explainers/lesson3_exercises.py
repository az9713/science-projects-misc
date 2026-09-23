"""Answers for Lesson 3 exercises 1, 3, and 5.

Swing convention: 2H d(dw)/dt = P_m - P_e - K_D dw
                   d(delta)/dt = omega_0 dw
Stdlib only. Run: python lesson3_exercises.py
"""
import math
from lesson3_euler_drift import (equilibrium, rk4_step, euler_step)

delta0, lam = equilibrium(0.8)
p_m_new = 0.85
delta_new, _ = equilibrium(p_m_new)


def rk4_amplitude(h, t_end=10.0):
    x = (delta0, 0.0)
    n = int(round(t_end / h))
    amp = 0.0
    for i in range(n):
        x = rk4_step(x, p_m_new, h)
        t = (i + 1) * h
        if t_end - 2.0 <= t <= t_end:
            amp = max(amp, abs(x[0] - delta_new))
    return math.degrees(amp)


print("Exercise 1: bisection for the largest decaying Euler step")
lo, hi = 0.0001, 0.02
for _ in range(60):
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if abs(1.0 + mid * lam) < 1.0 else (lo, mid)
print("  h_crit = %.5f s = %.2f ms" % (lo, lo * 1000))

print("\nExercise 3: RK4 late amplitude for larger steps")
for h in (0.1, 0.2, 0.3, 0.35):
    amp = rk4_amplitude(h, t_end=max(10.0, 6.0 / h))
    print("  h = %.2f s: late amplitude = %.4f deg" % (h, amp))

print("\nExercise 5: forward-Euler amplitude x10s vs h")
prev_h, prev_mag = None, None
for i in range(1, 11):
    h = i * 0.001
    mag = abs(1.0 + h * lam) ** (10.0 / h)
    flag = " <-- crosses 0.240 here" if prev_mag is not None and (
        prev_mag - 0.240) * (mag - 0.240) < 0 else ""
    print("  h = %d ms: amplitude x10s = %.3f%s" % (i, mag, flag))
    prev_h, prev_mag = h, mag
