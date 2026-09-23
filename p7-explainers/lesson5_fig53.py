"""Fig. 5.3 data: angle error after the 30 deg jump for three zeta
values at fixed omega_n_pll, plus each case's settling time.
"""
import math
import lesson5_pll as m


def gains(zeta, wn=m.WN, k=m.V):
    return 2.0 * zeta * wn / k, wn * wn / k


def sample(zeta, t0=0.1, t1=0.3, n=120):
    kp, ki = gains(zeta)
    t_hist, err = m.run(kp, ki, t_end=t1)
    # settling and overshoot use the same 0.1-0.4 s window as the main
    # listing; a 0.3 s window cuts off the zeta = 0.4 tail
    t_l, err_l = m.run(kp, ki, t_end=m.STEP_T)
    ts = m.settling_time(t_l, err_l, 0.02, window_end=m.STEP_T)
    final = err_l[int(round(m.STEP_T / m.DT)) - 2]
    over = (-min(err_l), final - min(err_l))
    idx0 = int(round(t0 / m.DT)) - 1
    step = max(1, (len(t_hist) - idx0) // n)
    pts = [(t_hist[i] - t0, err[i]) for i in range(idx0, len(t_hist),
                                                     step)]
    return kp, ki, ts, pts, over


if __name__ == "__main__":
    for zeta in (0.4, 0.707, 1.0):
        kp, ki, ts, pts, over = sample(zeta)
        print("zeta=%.3f kp=%.4f ki=%.4f settle=%.4f s" %
              (zeta, kp, ki, ts))
        print("  overshoot past zero = %.4f rad (%.1f%%), past final "
              "value = %.4f rad (%.1f%%)" %
              (over[0], 100 * over[0] / m.JUMP, over[1],
               100 * over[1] / m.JUMP))
