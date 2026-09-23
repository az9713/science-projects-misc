"""Lesson 8: aggregated nadir model, RK4 integration, and inertia sizing.

Swing convention (system-wide, centre-of-inertia form):
    2 E_kin_sys / f_0 * d(df)/dt = dP(t)
State: df (Hz), integrated by RK4 on a linear primary-response ramp.
"""
import math

F0 = 50.0  # Hz, nominal frequency


def dp_ramp(t, dp0, ramp_t):
    """Net imbalance power (MW) at time t: loss dp0, ramped away by T."""
    if t >= ramp_t:
        return 0.0
    return -dp0 + dp0 * t / ramp_t


def rk4_nadir(e_kin_sys, dp0, ramp_t, dt=0.001, t_end=None):
    """Integrate d(df)/dt = f0 * dp(t) / (2 * e_kin_sys); return min df."""
    if t_end is None:
        t_end = ramp_t
    coef = F0 / (2.0 * e_kin_sys)

    def deriv(t):
        return coef * dp_ramp(t, dp0, ramp_t)

    t = 0.0
    df = 0.0
    df_min = 0.0
    n = int(round(t_end / dt))
    for i in range(n):
        k1 = deriv(t)
        k2 = deriv(t + dt / 2.0)
        k3 = deriv(t + dt / 2.0)
        k4 = deriv(t + dt)
        df = df + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + dt
        if df < df_min:
            df_min = df
    return df_min


def rocof0(e_kin_sys, dp0):
    return F0 * dp0 / (2.0 * e_kin_sys)


def bisect_floor(dp0, ramp_t, f_floor_drop, lo=10.0, hi=500.0, tol=1e-4):
    """Smallest E_kin_sys (GVA.s) keeping |nadir drop| <= f_floor_drop."""
    def drop_at(e):
        return -rk4_nadir(e * 1000.0, dp0, ramp_t)  # GVA.s -> MVA.s

    # drop_at is decreasing in e; find root drop_at(e) = f_floor_drop
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if drop_at(mid) > f_floor_drop:
            lo = mid
        else:
            hi = mid
    return hi


def main():
    dp0 = 1000.0  # MW
    ramp_t = 10.0  # s

    print("RoCoF_0 and nadir vs E_kin_sys (dP=1000 MW, T=10 s):")
    for e_gva in (300.0, 200.0, 100.0, 50.0):
        e_mva = e_gva * 1000.0  # GVA.s -> MVA.s
        rc0 = rocof0(e_mva, dp0)
        drop = rk4_nadir(e_mva, dp0, ramp_t)
        f_nadir = F0 + drop
        print(f"  E_kin_sys = {e_gva:6.1f} GVA.s  "
              f"RoCoF_0 = {rc0:.3f} Hz/s  "
              f"f_nadir = {f_nadir:.3f} Hz")

    # Floor for 48.8 Hz (drop of 1.2 Hz)
    floor = bisect_floor(dp0, ramp_t, 1.2)
    print(f"\nSmallest E_kin_sys keeping nadir >= 48.8 Hz: "
          f"{floor:.1f} GVA.s")

    # analytic check: E_floor = f0 dP T / (4 * 1.2)
    analytic = F0 * dp0 * ramp_t / (4.0 * 1.2) / 1000.0  # -> GVA.s
    print(f"Analytic formula f0 dP T / (4 * 1.2): {analytic:.1f} GVA.s")

    # check at 100 GVA.s directly
    drop100 = rk4_nadir(100.0 * 1000.0, dp0, ramp_t)
    print(f"\nCheck at 100 GVA.s: f_nadir = {F0 + drop100:.3f} Hz "
          f"(below 48.8 Hz line: {F0 + drop100 < 48.8})")

    # Exercise 2: sweep T at 200 GVA.s
    print("\nExercise 2: sweep T at E_kin_sys = 200 GVA.s")
    for t_ramp in (5.0, 10.0, 20.0, 30.0):
        drop = rk4_nadir(200.0 * 1000.0, dp0, t_ramp)
        print(f"  T = {t_ramp:4.1f} s  df_nadir = {drop:.4f} Hz")


if __name__ == "__main__":
    main()
