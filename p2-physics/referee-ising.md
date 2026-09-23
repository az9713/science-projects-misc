# Referee verdict: Ising Tc reproduction (`scripts/ising.py`, `results/ising.json`)

**Verdict: PASS WITH CAVEATS.** The physics is correct. The measured Tc sits 0.7 standard deviations from the exact value. The caveats are in the reporting: no error bar, six printed decimals with three supported, and a tolerance 20 times the statistical error.

## 1. Statistical validity: VALID, precision overstated

I re-ran the same checkerboard sweep at T = Tc (32 replicas, 20,000 sweeps) and measured autocorrelation times.

| L | tau_int(m^2) | tau_int(m) | script budget per T | N_eff per T |
|---|---|---|---|---|
| 16 | 9.4 sweeps | 240 sweeps | 4,000 sweeps x 128 replicas | ~27,000 |
| 32 | 34.9 sweeps | 726 sweeps | 4,000 sweeps x 64 replicas | ~3,700 |

Effective z from the m^2 ratio: log2(34.9/9.4) = 1.9 against 2.17.

- **Thermalization.** 1,000 sweeps = 29 tau_int(m^2) at L=32, sufficient for even moments. It is only 1.4 tau_int(m), but the sign mode does not enter m^2 or m^4. The halves agree at 0.002, so no drift remains.
- **Sampling interval.** 10 sweeps against tau_int(m^2) = 35 at L=32. Adjacent samples are correlated. This does not bias U4; it reduces N_eff, which the error below includes.
- **Error on U4.** From the printed halves: sigma(U16) = 0.0006, sigma(U32) = 0.0023. From replica scatter in my tau run, scaled to the script budget: 0.0008 and 0.0020.
- **Error on Tc.** Slope of D(T) = U16 - U32 at the root is 0.60 per unit T. A 20,000-draw noise Monte Carlo of the cubic-root procedure gives sigma(Tc) = 0.0026 (halves-based) and 0.0023 (tau-based). **Statistical error on Tc: 0.0025.**
- **Precision honesty.** Tc = 2.267460 supports three decimals. Honest form: Tc = 2.267 +/- 0.003. The JSON note "two runs gave bit-identical U4 tables" is a determinism check under a fixed seed, not a precision check.

## 2. Finite-size bias: MAGNITUDE BELOW NOISE, SIGN NOT RESOLVED

Scaling argument with nu = 1 and leading correction exponent omega = 2 for the torus (exponent from recall, not checked this session; U* = 0.61069 from Kamieniarz and Blöte 1993, verified):

U_L(T) = U* + a t L + c L^-2. Equating L and 2L gives t_cross = (3/4)(c/a) L^-3.

The crossing sits below Tc when U(Tc, L) approaches U* from above (c > 0, a < 0), and above Tc otherwise.

From this run, U16(Tc) = 0.6114 +/- 0.0006 by linear interpolation, so U16(Tc) - U* = 0.0007 +/- 0.0006. At central plus one sigma, c x 16^-2 <= 0.0013, so c <= 0.33. With a = -0.038 per unit L (measured slopes -0.615 and -1.175), **|t_cross| is below 0.0016**. The U32 route, -0.0009 +/- 0.0023, is uninformative.

- The observed deviation (measured minus exact) is -0.0017, which is 0.7 sigma. It is consistent with a bias up to 0.0016 plus noise.
- Sign: U16(Tc) sits above U* by 1.2 sigma, which points to c > 0 and a crossing below Tc, matching the observed direction. A hint, not a resolution. Not confirmed from a primary source.
- The docstring's "on the order of 0.005" is about 3 times the data bound. The JSON note calls 0.005 "smaller than the observed 0.0017". That comparison is inverted.

## 3. Method risks: NONE BLOCKING

- **Cubic fit, 7 points, 3 dof.** chi^2/dof = 0.19, residual rms 0.0007 against sigma(D) = 0.0024. A quadratic on the inner 5 points gives 2.2681, a 0.0006 shift, below sigma.
- **Single-root assertion.** 0 failures in 20,000 noise draws at the measured sigma. D(T) is monotonic. Line 92 crashes instead of reporting the root count.
- **Checkerboard update.** Spins of one colour are independent given the other, so each sublattice update satisfies detailed balance. The red-then-black composition preserves the Boltzmann measure (stationarity, not reversibility) and is ergodic at T > 0. The parity split needs even L across the periodic wrap; 16 and 32 are even.
- **Acceptance rule.** Line 58 accepts k <= 0 always, k = 2 with exp(-4/T), k = 4 with exp(-8/T). Correct.
- **Seeds.** SEED+16 and SEED+32 give independent PCG64 streams. Replicas and temperatures draw disjoint numbers. No correlation.

## 4. Tolerance: 0.05 IS NOT MEANINGFUL

- 0.05 / 0.0025 = 20 sigma. The pass band 2.219 to 2.319 contains 5 of the 7 grid temperatures.
- A 16/32 crossing supports 3 sigma = 0.0075 plus the 0.0016 bias bound, about 0.009.
- **Recommended tolerance: 0.01**, computed at run time from the halves.

## 5. Independent run: EXIT 0

`python ising.py` from the scripts folder: exit 0, Tc = 2.267460, U4 at crossing 0.6124. Runtime 93.0 s, which is 51.7 % of the 180 s bound, not "well under half".

## Concrete changes to the script

1. Compute sigma(U4) from the two halves, propagate to sigma(Tc) through the cubic root, print `Tc = 2.267 +/- 0.003`. Reason: six decimals with no error bar overstate precision by three decimals.
2. Set `TOL` to 0.01, or to 3 sigma(Tc) + 0.002 at run time. Reason: 0.05 is 20 sigma and cannot fail a wrong crossing inside the window.
3. Change the docstring bias figure from "on the order of 0.005" to "below about 0.0016, sign unresolved". Reason: the run's own U16(Tc) against U* bounds it.
4. Replace the line 92 assertion with a printed FAIL that reports the root count. Reason: a crash hides the diagnostic.
5. In `results/ising.json`, correct "smaller than the observed 0.0017" to "larger" and remove the determinism-as-precision sentence. Reason: both statements are wrong as written.
