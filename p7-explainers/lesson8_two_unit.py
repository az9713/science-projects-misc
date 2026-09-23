"""Lesson 8: two-unit state matrix and its eigenvalues.

State x = (delta_1, delta_2, dw_1, dw_2). System base 1000 MVA, 50 Hz.
Swing convention: M_i d(dw_i)/dt = P_m - P_e - K_D dw_i,
                  M_i = 2 H_i S_i / S_sys (system base),
                  d(delta)/dt = omega_0 dw   (dw in pu, omega_0 = 2*pi*f0)
"""
import math
import numpy as np

F0 = 50.0
OMEGA0 = 2.0 * math.pi * F0

M1, M2 = 3.2, 1.8      # s, system-base inertia (2*H*S/S_sys)
KD1, KD2 = 0.8, 0.6     # pu on system base
E1, E2 = 1.05, 1.05
X12 = 2.0               # pu
P_TRANSFER = 0.2        # pu, pre-disturbance transfer


def build_state_matrix(delta12):
    """4x4 state matrix for x = (d1, d2, dw1, dw2), as nested lists."""
    k12 = (E1 * E2 / X12) * math.cos(delta12)  # pu/rad
    a = [
        [0.0, 0.0, OMEGA0, 0.0],
        [0.0, 0.0, 0.0, OMEGA0],
        [-k12 / M1, k12 / M1, -KD1 / M1, 0.0],
        [k12 / M2, -k12 / M2, 0.0, -KD2 / M2],
    ]
    return a, k12


def main():
    delta12 = math.asin(P_TRANSFER * X12 / (E1 * E2))
    print(f"delta_12 = {math.degrees(delta12):.2f} deg")

    a, k12 = build_state_matrix(delta12)
    print(f"K_12 = {k12:.4f} pu/rad")

    eigs = np.linalg.eigvals(a)
    eigs = sorted(eigs, key=lambda z: (abs(z.imag), z.real))
    print("Eigenvalues (1/s):")
    seen = set()
    for z in eigs:
        key = (round(z.real, 6), round(abs(z.imag), 6))
        if key in seen:
            continue
        seen.add(key)
        if abs(z.imag) < 1e-8:
            print(f"  {z.real:.4f}")
        else:
            print(f"  {z.real:.4f} +/- j{abs(z.imag):.2f}")

    common_expected = -(KD1 + KD2) / (M1 + M2)
    print(f"\nExpected common mode -(KD1+KD2)/(M1+M2) = "
          f"{common_expected:.4f} 1/s")

    omega_n = math.sqrt(OMEGA0 * k12 * (1.0 / M1 + 1.0 / M2))
    print(f"Check omega_n = sqrt(omega0*K12*(1/M1+1/M2)) = "
          f"{omega_n:.2f} rad/s")

    rel = [z for z in eigs if abs(z.imag) > 1e-8][0]
    f_rel = abs(rel.imag) / (2.0 * math.pi)
    zeta = -rel.real / abs(rel)
    print(f"Relative mode frequency = {f_rel:.3f} Hz")
    print(f"Relative mode damping ratio = {zeta:.4f}")


if __name__ == "__main__":
    main()
