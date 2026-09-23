"""SMIB classical model: equilibrium, linearisation, eigenvalues, RK4.

Swing convention: 2H d(dw)/dt = P_m - P_e - K_D dw
                   d(delta)/dt = omega_0 dw
Stdlib only. Run: python lesson2_smib.py
"""
import cmath
import math

H = 3.5
K_D = 2.0
E_P = 1.1
V_INF = 1.0
X = 0.65
OMEGA_0 = 2.0 * math.pi * 60.0
P_MAX = E_P * V_INF / X


def f(x, p_m):
    """State derivative. x = (delta, dw)."""
    delta, dw = x
    ddelta = OMEGA_0 * dw
    ddw = (p_m - P_MAX * math.sin(delta) - K_D * dw) / (2.0 * H)
    return (ddelta, ddw)


def analytic_jacobian(delta0):
    k_s = P_MAX * math.cos(delta0)
    return ((0.0, OMEGA_0),
            (-k_s / (2.0 * H), -K_D / (2.0 * H)))


def fd_jacobian(x0, p_m, step=1e-6):
    n = len(x0)
    jac = [[0.0] * n for _ in range(n)]
    f0 = f(x0, p_m)
    for j in range(n):
        xp = list(x0)
        xp[j] += step
        fp = f(tuple(xp), p_m)
        for i in range(n):
            jac[i][j] = (fp[i] - f0[i]) / step
    return jac


def eigenvalues_2x2(a):
    tr = a[0][0] + a[1][1]
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    disc = cmath.sqrt(tr * tr - 4.0 * det)
    return ((tr + disc) / 2.0, (tr - disc) / 2.0)


def rk4_step(x, p_m, h):
    k1 = f(x, p_m)
    x2 = (x[0] + 0.5 * h * k1[0], x[1] + 0.5 * h * k1[1])
    k2 = f(x2, p_m)
    x3 = (x[0] + 0.5 * h * k2[0], x[1] + 0.5 * h * k2[1])
    k3 = f(x3, p_m)
    x4 = (x[0] + h * k3[0], x[1] + h * k3[1])
    k4 = f(x4, p_m)
    dd = (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
    dw = (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
    return (x[0] + h * dd, x[1] + h * dw)


def main():
    p_m0 = 0.8
    delta0 = math.asin(p_m0 / P_MAX)
    k_s = P_MAX * math.cos(delta0)
    omega_n = math.sqrt(k_s * OMEGA_0 / (2.0 * H))
    zeta = K_D / (4.0 * H * omega_n)

    print("=== Base equilibrium (P_m = 0.8 pu) ===")
    print("P_max   = %.4f pu" % P_MAX)
    print("delta_0 = %.4f rad = %.4f deg" % (delta0, math.degrees(delta0)))
    print("K_s     = %.4f pu/rad" % k_s)
    print("omega_n = %.4f rad/s = %.4f Hz" %
          (omega_n, omega_n / (2 * math.pi)))
    print("zeta    = %.5f" % zeta)

    a_analytic = analytic_jacobian(delta0)
    a_fd = fd_jacobian((delta0, 0.0), p_m0)
    print("\n=== Jacobian check at base equilibrium ===")
    print("Analytic A =", a_analytic)
    print("Finite-diff A =", ((a_fd[0][0], a_fd[0][1]),
                               (a_fd[1][0], a_fd[1][1])))
    for i in range(2):
        for j in range(2):
            diff = abs(a_analytic[i][j] - a_fd[i][j])
            print("  |A[%d][%d] diff| = %.3e" % (i, j, diff))

    eig1, eig2 = eigenvalues_2x2(a_analytic)
    print("\nEigenvalues (base) = %.4f %+.4fj, %.4f %+.4fj" %
          (eig1.real, eig1.imag, eig2.real, eig2.imag))

    print("\n=== Step P_m: 0.8 -> 0.85 pu, RK4 h=0.001 s, 10 s ===")
    p_m_new = 0.85
    delta_new = math.asin(p_m_new / P_MAX)
    k_s_new = P_MAX * math.cos(delta_new)
    omega_n_new = math.sqrt(k_s_new * OMEGA_0 / (2.0 * H))
    zeta_new = K_D / (4.0 * H * omega_n_new)
    print("New equilibrium delta_new = %.4f rad = %.4f deg" %
          (delta_new, math.degrees(delta_new)))
    print("New K_s = %.4f pu/rad, omega_n = %.4f rad/s = %.4f Hz, "
          "zeta = %.5f" % (k_s_new, omega_n_new,
                            omega_n_new / (2 * math.pi), zeta_new))

    h = 0.001
    n_steps = int(10.0 / h)
    x = (delta0, 0.0)
    t = 0.0
    prev_g = x[0] - delta_new
    crossings = []
    history = [(t, x[0])]
    for _ in range(n_steps):
        x = rk4_step(x, p_m_new, h)
        t += h
        g = x[0] - delta_new
        if prev_g < 0.0 <= g or prev_g > 0.0 >= g:
            t_cross = t - h * g / (g - prev_g)
            crossings.append(t_cross)
        prev_g = g
        history.append((t, x[0]))

    periods = [crossings[i + 2] - crossings[i]
               for i in range(len(crossings) - 2)]
    if periods:
        avg_period = sum(periods) / len(periods)
        freq_zc = 1.0 / avg_period
    else:
        freq_zc = float("nan")
    print("Zero crossings found: %d" % len(crossings))
    print("Zero-crossing oscillation frequency = %.4f Hz" % freq_zc)
    print("Linearised frequency at new point   = %.4f Hz" %
          (omega_n_new / (2 * math.pi)))

    print("\n=== Eigenvalue sweep over K_D (Fig. 2.3 data) ===")
    for kd_sweep in (0.0, 2.0, 10.0, 30.0):
        a_sweep = ((0.0, OMEGA_0), (-k_s / (2.0 * H), -kd_sweep / (2.0 * H)))
        e1, e2 = eigenvalues_2x2(a_sweep)
        print("  K_D=%5.1f: %.4f %+.4fj, %.4f %+.4fj  |eig|=%.4f" %
              (kd_sweep, e1.real, e1.imag, e2.real, e2.imag, abs(e1)))

    print("\n=== H sweep (Exercise 3) ===")
    for h_sweep in (2.0, 3.5, 6.0, 8.0):
        omega_n_h = math.sqrt(k_s * OMEGA_0 / (2.0 * h_sweep))
        zeta_h = K_D / (4.0 * h_sweep * omega_n_h)
        print("  H=%.1f s: omega_n=%.2f rad/s, zeta=%.4f" %
              (h_sweep, omega_n_h, zeta_h))

    print("\n=== Finite-difference step-size sweep (Exercise 4) ===")
    best_step = None
    best_err = None
    for exp in range(-2, -13, -1):
        step = 10.0 ** exp
        a_fd_s = fd_jacobian((delta0, 0.0), p_m0, step=step)
        err = abs(a_analytic[1][0] - a_fd_s[1][0])
        print("  step=%.0e: A[1][0]=%.10f, |error|=%.3e" %
              (step, a_fd_s[1][0], err))
        if best_err is None or err < best_err:
            best_err = err
            best_step = step
    print("Smallest error at step = %.0e (error = %.3e)" %
          (best_step, best_err))


if __name__ == "__main__":
    main()
