"""SRF-PLL: lock time after a phase jump, error after a freq step."""
import math

FS = 10000.0
DT = 1.0 / FS
OMEGA0 = 2.0 * math.pi * 50.0
V = 1.0
ZETA = 0.707
WN = 2.0 * math.pi * 10.0
KP = 2.0 * ZETA * WN / V
KI = WN * WN / V
JUMP_T, JUMP = 0.1, math.pi / 6
STEP_T, DHZ = 0.4, 0.5


def theta_grid(t):
    th = OMEGA0 * t
    if t >= JUMP_T:
        th += JUMP
    if t >= STEP_T:
        th += 2.0 * math.pi * DHZ * (t - STEP_T)
    return th


def clarke_park(va, vb, vc, theta_pll):
    valpha = (2.0 / 3.0) * (va - 0.5 * vb - 0.5 * vc)
    vbeta = (1.0 / math.sqrt(3.0)) * (vb - vc)
    vd = valpha * math.cos(theta_pll) + vbeta * math.sin(theta_pll)
    vq = -valpha * math.sin(theta_pll) + vbeta * math.cos(theta_pll)
    return vd, vq


def run(kp, ki, t_end=0.6):
    theta_pll, z = 0.0, 0.0
    n = int(round(t_end / DT))
    err, t_hist = [], []
    for k in range(1, n + 1):
        t = k * DT
        tg = theta_grid(t)
        va = V * math.cos(tg)
        vb = V * math.cos(tg - 2 * math.pi / 3)
        vc = V * math.cos(tg + 2 * math.pi / 3)
        vd, vq = clarke_park(va, vb, vc, theta_pll)
        z += DT * vq  # semi-implicit Euler: integral first, then angle
        omega_pll = OMEGA0 + kp * vq + ki * z
        theta_pll += DT * omega_pll
        e = math.atan2(math.sin(tg - theta_pll), math.cos(tg - theta_pll))
        err.append(e)
        t_hist.append(t)
    return t_hist, err


def settling_time(t_hist, err, band, window_end=STEP_T):
    band_abs = band * JUMP
    final_val = err[int(round(window_end / DT)) - 2]
    last_out = None
    for i, (t, e) in enumerate(zip(t_hist, err)):
        if JUMP_T <= t < window_end and abs(e - final_val) > band_abs:
            last_out = i
    return 0.0 if last_out is None else t_hist[last_out + 1] - JUMP_T


if __name__ == "__main__":
    t_hist, err = run(KP, KI)
    ts = settling_time(t_hist, err, 0.02)
    i1 = int(round((STEP_T - DT) / DT)) - 1
    i2 = int(round((0.6 - DT) / DT)) - 1
    print("omega_n_pll = %.4f rad/s" % WN)
    print("k_p_pll = %.4f 1/s, k_i_pll = %.4f 1/s^2" % (KP, KI))
    print("settling time (2%% of 30 deg jump) = %.4f s" % ts)
    print("angle error just before freq step = %.6f rad" % err[i1])
    print("angle error at end (after freq step)  = %.6f rad" % err[i2])
    w_new = OMEGA0 + 2.0 * math.pi * DHZ
    print("residual beyond -omega*DT bias: before = %.2e rad, "
          "after = %.2e rad" % (err[i1] + OMEGA0 * DT, err[i2] + w_new * DT))
