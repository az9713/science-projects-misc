"""Exercise 3: 10% negative-sequence voltage -> ripple on v_q.

A negative-sequence set rotates at -theta_g. In the frame that
rotates at +theta_pll (near +theta_g once locked), it appears at
-2*theta_g, so it lands on v_q as a component at twice grid
frequency (100 Hz at 50 Hz).
"""
import math
import lesson5_pll as m

NEG = 0.10


def abc_with_negseq(theta_g, neg_frac):
    va = m.V * math.cos(theta_g) + neg_frac * m.V * math.cos(-theta_g)
    vb = (m.V * math.cos(theta_g - 2 * math.pi / 3) +
          neg_frac * m.V * math.cos(-theta_g - 2 * math.pi / 3))
    vc = (m.V * math.cos(theta_g + 2 * math.pi / 3) +
          neg_frac * m.V * math.cos(-theta_g + 2 * math.pi / 3))
    return va, vb, vc


def run_negseq(kp, ki, neg_frac, t_end=0.3):
    theta_pll, z = 0.0, 0.0
    n = int(round(t_end / m.DT))
    vq_hist, t_hist = [], []
    for k in range(1, n + 1):
        t = k * m.DT
        tg = m.OMEGA0 * t
        va, vb, vc = abc_with_negseq(tg, neg_frac)
        vd, vq = m.clarke_park(va, vb, vc, theta_pll)
        z += m.DT * vq
        omega_pll = m.OMEGA0 + kp * vq + ki * z
        theta_pll += m.DT * omega_pll
        vq_hist.append(vq)
        t_hist.append(t)
    return t_hist, vq_hist


if __name__ == "__main__":
    t_hist, vq_hist = run_negseq(m.KP, m.KI, NEG)
    tail = vq_hist[len(vq_hist) // 2:]
    ripple_amp = 0.5 * (max(tail) - min(tail))
    mean_vq = sum(tail) / len(tail)
    print("negative-sequence fraction = %.2f" % NEG)
    print("v_q ripple amplitude = %.5f pu (predicted %.5f pu)" %
          (ripple_amp, NEG * m.V))
    print("mean v_q over tail = %.6f pu" % mean_vq)
