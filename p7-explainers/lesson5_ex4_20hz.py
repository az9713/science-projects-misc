"""Exercise 4: retune for 20 Hz bandwidth, repeat the 30 deg jump."""
import math
import lesson5_pll as m

WN20 = 2.0 * math.pi * 20.0
KP20 = 2.0 * m.ZETA * WN20 / m.V
KI20 = WN20 * WN20 / m.V

if __name__ == "__main__":
    t_hist, err = m.run(KP20, KI20, t_end=0.4)
    ts20 = m.settling_time(t_hist, err, 0.02, window_end=m.STEP_T)
    print("omega_n_pll (20 Hz) = %.4f rad/s" % WN20)
    print("k_p_pll = %.4f 1/s, k_i_pll = %.4f 1/s^2" % (KP20, KI20))
    print("settling time (2%% of 30 deg jump) = %.4f s" % ts20)
    t10, err10 = m.run(m.KP, m.KI, t_end=0.4)
    ts10 = m.settling_time(t10, err10, 0.02, window_end=m.STEP_T)
    print("ratio to 10 Hz settling time (%.4f s) = %.3f" %
          (ts10, ts20 / ts10))
