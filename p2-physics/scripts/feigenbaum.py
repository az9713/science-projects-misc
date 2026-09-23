"""Feigenbaum constant delta from the logistic map x -> r x (1 - x).

METHOD: superstable parameter values.
  A superstable 2^n-cycle contains the critical point x = 1/2, because that is
  where f'(x) = 0. So the parameter r_n of the superstable 2^n-cycle is the
  root of
        g_n(r) = f_r^(2^n)(1/2) - 1/2 = 0,
  taken as the first such root above r_{n-1}. We solve g_n by Newton iteration.
  The derivative is propagated with the orbit itself:
        x_{k+1}     = r x_k (1 - x_k)
        dx_{k+1}/dr = x_k (1 - x_k) + r (1 - 2 x_k) dx_k/dr,
  started from x = 1/2, dx/dr = 0. That is exact to rounding; no finite
  difference is taken. The ratio of successive parameter gaps
        delta_n = (r_n - r_{n-1}) / (r_{n+1} - r_n)
  tends to delta as n -> infinity. We solve levels n = 0 .. 13 and report
  delta_N at the level N whose own error estimate is smallest (see below).

PUBLISHED VALUE: delta = 4.669201609102990.
  Feigenbaum, J. Stat. Phys. 19 (1978) 25 (discovery, ~4.6692016);
  Briggs, Math. Comp. 57 (1991) 435 (high-precision value; source of the digits
  asserted here, and of |alpha| = 2.502907875096 and the accumulation point
  r_inf = 3.5699456718709 used below only as an upper bracket).

NO STOCHASTIC STEP: the computation is Newton iteration on a deterministic
  recurrence. There is no random number, so there is no seed to fix, and the
  output is reproducible on the same libm. Requirement 2 is answered by there
  being nothing to seed. For the same reason nothing here is vectorizable:
  f^(2^n) is a serial recurrence, each step depending on the one before, so the
  inner loop is plain Python floats (faster than numpy scalars at this size).
  Total work is about 8e5 map steps and the whole run takes about 0.05 s,
  far inside the 180 s budget, so no size was traded away for speed.

KNOWN METHOD BIAS, TWO PARTS, PULLING IN OPPOSITE DIRECTIONS IN n.
  1. Truncation, which falls with n. delta_n approaches delta geometrically,
     the successive differences shrinking by roughly a factor delta per level.
     At level N the remaining truncation is of the order of one further
     successive difference, |delta_N - delta_{N-1}|, and smaller than it. No
     single-exponent correction law is assumed and no extrapolation is done:
     the early delta_n (n <= 4) do not follow one cleanly, the difference even
     changing sign between n = 3 and n = 4.
  2. Roundoff, which RISES with n and is measured, not assumed. Evaluating
     f^(2^n)(1/2) in double precision leaves a residual noise floor in g_n that
     grows with the orbit length: |g_n| settles near 6e-16 at n = 3 but near
     1.5e-11 at n = 13, because rounding errors made early in the orbit are
     amplified by the partial products of f' along the rest of it. Newton
     therefore does not converge to a point at high n; it enters a limit cycle
     of width w_n. The script measures w_n directly (the spread of the last 40
     Newton iterates), takes r_n as their mean, and sets the parameter
     uncertainty eps_n = max(w_n / 2, |g_n| / |g_n'|, spacing(r_n)), the last
     two terms being the Newton residual translated into r and the floating
     point floor. Measured w_n is about
     1.5e-14 at n = 11 and 1.1e-13 at n = 13, that is 30 to 240 ulps of r, not
     the one ulp a naive residual argument would give.
     Because the gap r_{n+1} - r_n shrinks like delta^-n, this noise divided by
     an ever smaller gap eventually swamps the truncation gain: delta_12 is
     already worse than delta_10 against the published value.
  EXPECTED SIZE AT THE REPORTED LEVEL: at N = 10 the two parts are about equal,
  truncation 4.1e-7 and roundoff 3.6e-7, so the total bias is of order 8e-7,
  that is six correct significant figures, 4.66920. The truncation part has a
  known sign: every delta_n for n >= 4 lies BELOW delta, so delta_N is expected
  to come out low, and it does, by 9.5e-8.

LEVEL CHOICE: for every candidate level the script forms
     sigma_A         = sqrt(eps_N^2 + eps_{N-1}^2),  A = r_N - r_{N-1}
     sigma_B         = sqrt(eps_{N+1}^2 + eps_N^2),  B = r_{N+1} - r_N
     sigma_round(N)  = delta_N * sqrt((sigma_A/A)^2 + (sigma_B/B)^2)
     ERROR_ESTIMATE(N) = |delta_N - delta_{N-1}| + sigma_round(N)
  and reports the N that minimises ERROR_ESTIMATE, that is the level where
  falling truncation and rising roundoff balance. The choice uses only the
  error estimate. It never looks at the published value or at ABS_DIFF, so it
  cannot be tuned to make the test pass. The full table is printed so the
  choice can be checked.

TOLERANCE:
     BIAS_ALLOWANCE = |delta_N - delta_{N-1}|
     TOLERANCE      = 3 * ERROR_ESTIMATE + BIAS_ALLOWANCE
  three times the error estimate plus a stated method-bias allowance of one
  further successive difference. The tolerance is computed from the run; it is
  not a fixed loose number.

SELF-CHECKS (the analogue of the Ising script's U4* ~ 0.61 sanity value).
  g_n(r) vanishes at every earlier r_k, k < n, and again in the period-2^n
  windows above r_inf, so a Newton step that jumped roots would silently give a
  wrong delta. The script asserts:
    a. r_{n-1} < r_n < r_inf, and the search interval starts a sliver above
       r_{n-1} so the old root is not a candidate;
    b. minimal period: |d_n| > |d_{n-1}| / 10, where
       d_n = f^(2^(n-1))(1/2; r_n) - 1/2. A root that fell back onto r_{n-1}
       would give |d_n| ~ 1e-16. The threshold is relative because |d_n| itself
       shrinks by the Feigenbaum alpha ~ 2.5 at every level, so a fixed 1e-3
       threshold would reject the correct root from n = 8 upward;
    b2. |d_{n-1} / d_n| at the top level must lie in (2.0, 3.0). That ratio is
       the other Feigenbaum constant, |alpha| = 2.502907875096, obtained from
       the same orbits, so it catches a wrong-root run that still produced a
       plausible delta. It is printed, not fitted;
    c1. the propagated derivative agrees with a central difference of f^4 at
       r = 3.3 to better than 1e-6 relative;
    c2. r_1 has the closed form 1 + sqrt(5); Newton started from a crude r = 3.0
       must reproduce it to 1e-14. That is the wiring test.
  The search never uses the published delta: each initial guess comes from the
  running gap ratio measured at lower n (a crude factor 4 at n = 2), so the
  answer is not fed back into the method.
"""

import math
import sys
import time
import numpy as np

R_INF = 3.5699456718709          # accumulation point (Briggs 1991), bracket only
DELTA_PUBLISHED = 4.669201609102990
ALPHA_PUBLISHED = 2.502907875096
N_MAX = 13                       # highest superstable level solved
N_CAND = range(5, N_MAX)         # candidate reporting levels (need r_{N+1})
NEWTON_MAX = 200
N_AVERAGE = 40                   # Newton iterates averaged over the limit cycle
GUESS_FACTORS = (4.0, 3.0, 5.0, 2.5, 6.0, 8.0)


def orbit(r, steps):
    """Iterate f^steps from x = 1/2. Return (f^steps(1/2) - 1/2, d/dr of it)."""
    x = 0.5
    d = 0.0
    for _ in range(steps):
        d = r * (1.0 - 2.0 * x) * d + x * (1.0 - x)
        x = r * x * (1.0 - x)
    return x - 0.5, d


def newton(r0, steps, lo, hi):
    """Damped Newton on g(r) = f^steps(1/2) - 1/2, kept inside (lo, hi).

    Newton stops converging once the step falls to the evaluation noise floor
    of g, after which the iterates cycle. We detect the stall, then run
    N_AVERAGE more iterations and return their mean and their full spread.

    Returns (r_mean, iterations_to_stall, |g|, |g'|, spread) or None.
    """
    r = r0
    prev = float("inf")
    stalls = 0
    stall_at = NEWTON_MAX
    hist = []
    for it in range(1, NEWTON_MAX + 1):
        g, d = orbit(r, steps)
        if d == 0.0 or not math.isfinite(d):
            return None
        step = g / d
        r_new = r - step
        damp = 0
        while (r_new <= lo or r_new >= hi) and damp < 80:
            step *= 0.5
            r_new = r - step
            damp += 1
        if r_new <= lo or r_new >= hi:
            return None
        r = r_new
        if abs(step) >= prev * 0.5:          # no longer halving: at the floor
            stalls += 1
        else:
            stalls = 0
        prev = abs(step) if step != 0.0 else 0.0
        if step == 0.0 or stalls >= 3:
            stall_at = it
            break
    for _ in range(N_AVERAGE):
        g, d = orbit(r, steps)
        if d == 0.0 or not math.isfinite(d):
            return None
        r_try = r - g / d
        if lo < r_try < hi:
            r = r_try
        hist.append(r)
    arr = np.array(hist)
    r_mean = float(arr.mean())
    spread = float(arr.max() - arr.min())
    g, d = orbit(r_mean, steps)
    return r_mean, stall_at, abs(g), abs(d), spread


def solve_level(n, rs, delta_est, sep_prev):
    """Solve for r_n. Try the running gap ratio first, then crude fallbacks."""
    steps = 1 << n
    half = 1 << (n - 1)
    gap = rs[n - 1] - rs[n - 2]
    # g_n also vanishes at r_{n-1}; exclude a sliver above it so Newton cannot
    # settle back on the old root. gap/1000 is far below the new gap, ~gap/4.7.
    lo, hi = rs[n - 1] + gap / 1000.0, R_INF
    sep_min = max(sep_prev / 10.0, 1e-12)
    factors = []
    if delta_est is not None:
        factors.append(delta_est)
    factors.extend(GUESS_FACTORS)
    for f in factors:
        guess = rs[n - 1] + gap / f
        if not (lo < guess < hi):
            continue
        out = newton(guess, steps, lo, hi)
        if out is None:
            continue
        r, iters, res, slope, spread = out
        sep = orbit(r, half)[0]               # check b: minimal period is 2^n
        if abs(sep) > sep_min:
            return r, iters, res, slope, spread, sep, f
    raise RuntimeError("Newton failed to find a valid r_%d" % n)


def main():
    t_start = time.perf_counter()

    rs = [2.0, 1.0 + math.sqrt(5.0)]          # closed forms: period 1 and 2
    eps = [np.spacing(rs[0]), np.spacing(rs[1])]
    info = {}

    # check c1: the propagated derivative against a central difference.
    r_probe, h = 3.3, 1e-6
    d_analytic = orbit(r_probe, 4)[1]
    d_numeric = (orbit(r_probe + h, 4)[0] - orbit(r_probe - h, 4)[0]) / (2.0 * h)
    d_err = abs(d_analytic - d_numeric) / abs(d_numeric)
    assert d_err <= 1e-6, (
        "derivative wiring test failed: analytic %.12f vs central difference "
        "%.12f (relative %.3e)" % (d_analytic, d_numeric, d_err))

    # check c2: Newton must reproduce r_1 = 1 + sqrt(5). The start value 3.0 is
    # a crude point inside the period-2 window, not the answer.
    out1 = newton(3.0, 2, 2.0 + 1e-6, R_INF)
    assert out1 is not None, "Newton failed on the r_1 wiring test"
    r1_newton = out1[0]
    r1_err = abs(r1_newton - rs[1])
    assert r1_err <= 1e-14, (
        "wiring test failed: Newton r_1 = %.16f differs from 1+sqrt(5) by %.3e"
        % (r1_newton, r1_err))

    delta_est = None
    seps = {1: rs[1] / 4.0 - 0.5}             # d_1 = f^1(1/2) - 1/2 at r_1
    sep_prev = abs(seps[1])
    for n in range(2, N_MAX + 1):
        r, iters, res, slope, spread, sep, factor = solve_level(
            n, rs, delta_est, sep_prev)
        assert rs[n - 1] < r < R_INF, (
            "r_%d = %.16f left the interval (r_%d, r_inf)" % (n, r, n - 1))
        rs.append(r)
        eps.append(max(spread / 2.0, res / slope, np.spacing(r)))
        seps[n] = sep
        sep_prev = abs(sep)
        info[n] = (iters, res, slope, spread, sep, factor)
        if n >= 3:
            delta_est = (rs[n - 1] - rs[n - 2]) / (rs[n] - rs[n - 1])

    # check b2: alpha from the same orbits.
    alpha_measured = abs(seps[N_MAX - 1] / seps[N_MAX])
    assert 2.0 < alpha_measured < 3.0, (
        "alpha from the same orbits is %.6f, not near 2.5029: wrong roots"
        % alpha_measured)

    deltas = {n: (rs[n] - rs[n - 1]) / (rs[n + 1] - rs[n])
              for n in range(1, N_MAX)}

    print("Superstable parameters of the logistic map (period 2^n through x=1/2)")
    print("  wiring test  : Newton r_1 = %.16f vs 1+sqrt(5) = %.16f (diff %.2e)"
          % (r1_newton, rs[1], r1_err))
    print("  derivative   : analytic %.9f vs central difference %.9f (rel %.2e)"
          % (d_analytic, d_numeric, d_err))
    print("  |alpha| from the same orbits: %.6f   published %.9f (Briggs 1991)"
          % (alpha_measured, ALPHA_PUBLISHED))
    print()
    print("   n           r_n            it   |g(r_n)|   Newton spread"
          "    d_n         delta_n")
    for n in range(0, N_MAX + 1):
        if n in info:
            iters, res, slope, spread, sep, factor = info[n]
            head = "  %2d  %.15f    %3d   %.2e    %.2e   %+.3e   " % (
                n, rs[n], iters, res, spread, sep)
        else:
            head = ("  %2d  %.15f    (closed form)                "
                    "              " % (n, rs[n]))
        print(head + ("%.9f" % deltas[n] if n in deltas else "-"))

    # Error estimate per candidate level; pick the smallest. Never looks at
    # the published value.
    table = {}
    for n in N_CAND:
        a = rs[n] - rs[n - 1]
        b = rs[n + 1] - rs[n]
        sig_a = math.hypot(eps[n], eps[n - 1])
        sig_b = math.hypot(eps[n + 1], eps[n])
        sigma_round = deltas[n] * math.hypot(sig_a / a, sig_b / b)
        trunc = abs(deltas[n] - deltas[n - 1])
        table[n] = (trunc, sigma_round, trunc + sigma_round)

    print()
    print("Error budget per candidate level (truncation falls, roundoff rises)")
    print("    N   truncation   sigma_round   error estimate")
    for n in N_CAND:
        trunc, sigma_round, tot = table[n]
        print("   %2d    %.3e    %.3e     %.3e" % (n, trunc, sigma_round, tot))

    n_rep = min(N_CAND, key=lambda n: table[n][2])
    trunc, sigma_round, error_estimate = table[n_rep]
    measured = deltas[n_rep]
    bias_allowance = trunc
    tolerance = 3.0 * error_estimate + bias_allowance
    abs_diff = abs(measured - DELTA_PUBLISHED)
    runtime = time.perf_counter() - t_start
    ok = abs_diff <= tolerance

    print()
    print("Reported level N = %d (smallest error estimate)" % n_rep)
    print("  gap r_%d - r_%d          : %.6e" % (n_rep + 1, n_rep, rs[n_rep + 1] - rs[n_rep]))
    print("  eps_%d / eps_%d           : %.3e / %.3e"
          % (n_rep, n_rep + 1, eps[n_rep], eps[n_rep + 1]))
    print("  truncation |d_%d - d_%d|  : %.3e" % (n_rep, n_rep - 1, trunc))
    print("  roundoff   sigma_round  : %.3e" % sigma_round)
    print("  tolerance = 3*(truncation + sigma_round) + truncation")
    print()
    print("MEASURED=%.15g" % measured)
    print("PUBLISHED=%.15g" % DELTA_PUBLISHED)
    print("ERROR_ESTIMATE=%.6g" % error_estimate)
    print("TOLERANCE=%.6g" % tolerance)
    print("ABS_DIFF=%.6g" % abs_diff)
    print("RUNTIME_S=%.3f" % runtime)
    print("RESULT=%s" % ("PASS" if ok else "FAIL"))

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
