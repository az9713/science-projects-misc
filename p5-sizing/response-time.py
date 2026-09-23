"""P5 sizing study, scenario "response-time".

Case: a grid-forming battery (BESS) replaces a 1.6 GVA synchronous condenser
fleet for frequency response. Base method and reference numbers:
p1-textbook/ch4.html, section 4.5, Example 4.2 (R39), equations (4.11)-(4.13).
Same base model as inertia-constant.py, with H held fixed at the textbook
value 3.5 s (so this scenario isolates response time, not inertia spread).

Varied uncertainty: the BESS response time T_d (s) -- the delay between the
frequency-deviation trigger and full power delivery. Not given in ch4.html;
modelled here as an assumption of this study, order-of-magnitude anchored to
published fast-frequency-response products (e.g. National Grid ESO Dynamic
Containment, full delivery within about 1 s of the trigger) -- verify against
a specific product spec before quoting.

Model for the effect of T_d (assumption of this study, not from ch4.html):
- t_natural = DF_EXCURSION_HZ / ROCOF_HZ_S = 0.8 s: the time for frequency to
  reach the target 0.8 Hz excursion (ch4 eq 4.11) if wholly uncorrected.
- If the BESS needs T_d seconds to reach full power, only (t_natural - T_d)
  seconds remain to arrest the excursion at the same 0.8 Hz target, so the
  required power is scaled up by k = t_natural / (t_natural - T_d).
- k = 1 at T_d = 0, so the model reduces to the ch4 Example 4.2 numbers
  (224 MW, 1120 MVA) exactly at zero delay.
- The physical energy requirement (eq 4.11, a function of excursion depth
  only) is held fixed; only the required power/converter rating (and so
  capex) scale with k. T_d values are kept well below 0.8 s so k stays
  finite; this is a first-order approximation, not a full swing-dynamics
  simulation.

Run:  python response-time.py      (writes response-time.json next to it)
"""
import json
import os

import numpy as np

SEED = 20260922
N_SAMPLES = 10_000

# ---------------------------------------------------------------- fixed inputs
# All from ch4.html Example 4.1 / 4.2 unless marked "assumption". Same values
# as inertia-constant.py, with H fixed at its textbook mode (3.5 s).
F0_HZ = 50.0                 # nominal frequency, ch4 Example 4.1 and 4.2
N_UNITS = 8                  # condensers in the fleet, ch4 Example 4.2
S_UNIT_MVA = 200.0           # rating per condenser, ch4 Example 4.2 (8 x 200 = 1.6 GVA)
S_FLEET_MVA = N_UNITS * S_UNIT_MVA
H_S = 3.5                    # condenser inertia constant, ch4 Example 4.2, held fixed here
ROCOF_HZ_S = 1.0             # design RoCoF, ch4 eq (4.12); DS3 / GB loss-of-mains figure [S16 - verify]
DF_EXCURSION_HZ = 0.8        # frequency excursion target, ch4 eq (4.11)
H_V_S = 5.0                  # virtual inertia constant of the grid-forming BESS, ch4 eq (4.13), "assumed for this case"
STORE_HOURS = 1.0            # one-hour store, ch4 Constraint 1, "assumed for this case"
SYSTEM_EKIN_MJ = 200_000.0   # 200 GVA.s system, ch4 Example 4.1 (context only)
LOSS_MW = 1000.0             # 1000 MW loss, ch4 Example 4.1 (context only)
T_NATURAL_S = DF_EXCURSION_HZ / ROCOF_HZ_S  # 0.8 s, time to reach the target excursion uncorrected

# Cost inputs: assumption, NOT read from any source in this run. Held fixed
# here; the separate "cost-curve" scenario owns cost uncertainty.
COST_POWER_USD_PER_KVA = 200.0    # grid-forming converter + grid connection, assumption
COST_ENERGY_USD_PER_KWH = 250.0   # cells + racks + BMS, assumption

# ------------------------------------------------------ the varied uncertainty
# BESS response time T_d, in seconds (trigger to full power).
# Distribution: triangular(min 0.05, mode 0.15, max 0.30).
#   - Not in ch4.html. Order-of-magnitude assumption of this study, anchored
#     to published fast-frequency-response products (e.g. National Grid ESO
#     Dynamic Containment: full delivery within about 1 s of the trigger;
#     grid-forming inverter controller/comms delays typically sub-second).
#     Verify against a specific product spec before quoting.
#   - Bounds kept well under t_natural = 0.8 s so the amplification factor
#     k = t_natural / (t_natural - T_d) stays finite and moderate
#     (k in about 1.07-1.60 across the sampled range).
T_MIN_S, T_MODE_S, T_MAX_S = 0.05, 0.15, 0.30


def size_for_td(t_d_s):
    """Return the sizing outputs for BESS response time t_d_s (array or float)."""
    ekin_fleet_mj = H_S * S_FLEET_MVA                                    # eq (4.4) on the fleet, MJ = MVA.s, fixed
    e_released_mj = 2.0 * ekin_fleet_mj * DF_EXCURSION_HZ / F0_HZ         # eq (4.11), physical energy need, fixed
    p_headroom_base_mw = 2.0 * ekin_fleet_mj * ROCOF_HZ_S / F0_HZ         # eq (4.12) at T_d = 0 (224 MW)
    k = T_NATURAL_S / (T_NATURAL_S - t_d_s)                              # response-time amplification factor
    p_headroom_mw = p_headroom_base_mw * k                                # required power, scaled by delay
    p_inertial_pu = 2.0 * H_V_S * ROCOF_HZ_S / F0_HZ                      # eq (4.13), 0.20 pu
    s_gfm_mva = p_headroom_mw / p_inertial_pu                             # fleet converter rating
    e_required_mwh = np.broadcast_to(e_released_mj / 3600.0, np.shape(k)) if np.ndim(k) else e_released_mj / 3600.0  # physical energy need (fixed, broadcast to sample shape)
    e_store_mwh = s_gfm_mva * STORE_HOURS                                 # textbook one-hour store
    capex_usd = (s_gfm_mva * 1e3 * COST_POWER_USD_PER_KVA
                 + e_store_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    capex_power_only_usd = (s_gfm_mva * 1e3 * COST_POWER_USD_PER_KVA
                             + e_required_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    return {
        "response_time_s": np.broadcast_to(t_d_s, np.shape(p_headroom_mw)) if np.ndim(p_headroom_mw) else t_d_s,
        "amplification_factor": k,
        "bess_power_headroom_MW": p_headroom_mw,
        "bess_converter_rating_MVA": s_gfm_mva,
        "bess_energy_required_MWh": e_required_mwh,
        "bess_energy_one_hour_store_MWh": e_store_mwh,
        "capex_one_hour_store_MUSD": capex_usd / 1e6,
        "capex_min_energy_MUSD": capex_power_only_usd / 1e6,
    }


UNITS = {
    "response_time_s": "s",
    "amplification_factor": "dimensionless",
    "bess_power_headroom_MW": "MW",
    "bess_converter_rating_MVA": "MVA",
    "bess_energy_required_MWh": "MWh",
    "bess_energy_one_hour_store_MWh": "MWh",
    "capex_one_hour_store_MUSD": "million USD",
    "capex_min_energy_MUSD": "million USD",
}

MEANING = {
    "response_time_s": "sampled BESS trigger-to-full-power response time (the input)",
    "amplification_factor": "k = t_natural / (t_natural - T_d), t_natural = 0.8 s; power scale-up from the delay",
    "bess_power_headroom_MW": "power to still arrest the 0.8 Hz excursion given the delay; k x the 224 MW baseline",
    "bess_converter_rating_MVA": "grid-forming converter rating at H_v 5.0 s (0.20 pu headroom), eq (4.13)",
    "bess_energy_required_MWh": "energy released over the 0.8 Hz excursion, eq (4.11); unaffected by response time",
    "bess_energy_one_hour_store_MWh": "store size under the textbook one-hour assumption (a design choice, not a requirement)",
    "capex_one_hour_store_MUSD": "capex with the one-hour store, fixed placeholder unit costs",
    "capex_min_energy_MUSD": "capex with the store sized to the physical energy need only",
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(SEED)
    t_d = rng.triangular(T_MIN_S, T_MODE_S, T_MAX_S, size=N_SAMPLES)
    out = size_for_td(t_d)

    # ------------------------------------------------------------ self-checks
    # 1. Textbook reproduction at T_d = 0 (zero response delay).
    ref = size_for_td(0.0)
    assert abs(ref["amplification_factor"] - 1.0) < 1e-9
    assert abs(ref["bess_power_headroom_MW"] - 224.0) < 1e-9
    assert abs(ref["bess_converter_rating_MVA"] - 1120.0) < 1e-9
    assert abs(ref["bess_energy_one_hour_store_MWh"] - 1120.0) < 1e-9
    assert abs(ref["bess_energy_required_MWh"] - 179.2 / 3600.0) < 1e-12
    # 2. Sample count and bounds.
    assert t_d.size == N_SAMPLES == 10_000
    assert t_d.min() >= T_MIN_S and t_d.max() <= T_MAX_S
    assert t_d.max() < T_NATURAL_S, "response time must stay below t_natural or k is unbounded"
    # 3. Amplification factor matches the closed form and stays in the
    #    expected 1.07-1.60 window over the sampled range.
    k_check = T_NATURAL_S / (T_NATURAL_S - t_d)
    assert np.allclose(out["amplification_factor"], k_check)
    assert out["amplification_factor"].min() > 1.0
    assert out["amplification_factor"].max() < 1.7
    # 4. Power headroom is exactly 224 MW x k for every sample.
    assert np.allclose(out["bess_power_headroom_MW"], 224.0 * out["amplification_factor"])
    # 5. Energy required (physical need) is unaffected by response time.
    assert np.allclose(out["bess_energy_required_MWh"], 179.2 / 3600.0)
    # 6. Energy-store-to-need ratio is 22 500 x k: the store scales with the
    #    converter rating (which scales with k), but the physical energy need
    #    (eq 4.11) is fixed, so the ratio grows with response time.
    ratio = out["bess_energy_one_hour_store_MWh"] / out["bess_energy_required_MWh"]
    assert np.allclose(ratio, 22_500.0 * out["amplification_factor"])
    # 7. Sample percentiles of T_d against the analytic triangular quantiles.
    #    (This triangular is not symmetric -- c - a = 0.10, b - c = 0.15 --
    #    so the median is not the mode; use the general median formula.)
    q5_exact = T_MIN_S + np.sqrt(0.05 * (T_MAX_S - T_MIN_S) * (T_MODE_S - T_MIN_S))
    q95_exact = T_MAX_S - np.sqrt(0.05 * (T_MAX_S - T_MIN_S) * (T_MAX_S - T_MODE_S))
    if T_MODE_S >= (T_MIN_S + T_MAX_S) / 2:
        median_exact = T_MIN_S + np.sqrt((T_MAX_S - T_MIN_S) * (T_MODE_S - T_MIN_S) / 2)
    else:
        median_exact = T_MAX_S - np.sqrt((T_MAX_S - T_MIN_S) * (T_MAX_S - T_MODE_S) / 2)
    tp5, tp50, tp95 = np.percentile(t_d, [5, 50, 95])
    assert abs(tp5 - q5_exact) / q5_exact < 0.02
    assert abs(tp50 - median_exact) / median_exact < 0.02
    assert abs(tp95 - q95_exact) / q95_exact < 0.02

    results = {}
    for key, arr in out.items():
        p5, p50, p95 = (float(v) for v in np.percentile(arr, [5, 50, 95]))
        assert p5 <= p50 <= p95
        results[key] = {
            "unit": UNITS[key],
            "meaning": MEANING[key],
            "p5": round(p5, 6),
            "p50": round(p50, 6),
            "p95": round(p95, 6),
            "mean": round(float(arr.mean()), 6),
        }
    # 8. Median power stays above the zero-delay 224 MW baseline (delay only
    #    ever adds required power in this model).
    assert results["bess_power_headroom_MW"]["p50"] > 224.0

    doc = {
        "scenario": "response-time",
        "case": "grid-forming BESS replacing a 1.6 GVA synchronous condenser fleet for frequency response",
        "source_method": "p1-textbook/ch4.html section 4.5, Example 4.2 (R39), eqs (4.11)-(4.13); same base model as inertia-constant.py, H fixed at 3.5 s",
        "n_samples": N_SAMPLES,
        "seed": SEED,
        "varied_uncertainty": {
            "name": "BESS response time T_d (s), trigger to full power delivery",
            "distribution": f"triangular(min {T_MIN_S}, mode {T_MODE_S}, max {T_MAX_S})",
            "source": "Not in ch4.html. Assumption of this study, order-of-magnitude anchored to published fast-frequency-response products (e.g. National Grid ESO Dynamic Containment, full delivery within about 1 s of trigger); verify against a specific product spec before quoting.",
        },
        "effect_model": {
            "description": "k = t_natural / (t_natural - T_d), t_natural = DF_EXCURSION_HZ / ROCOF_HZ_S = 0.8 s; required power headroom = 224 MW (ch4 baseline) x k. Energy requirement (eq 4.11) held fixed; only power, converter rating, store size and capex scale with k.",
            "t_natural_s": T_NATURAL_S,
            "caveat": "First-order approximation (remaining-time scaling), not a full swing-equation/RoCoF-relay simulation. Assumption of this study, not from ch4.html.",
        },
        "outputs": results,
        "textbook_reference_at_Td_0": {
            "amplification_factor": 1.0,
            "bess_power_headroom_MW": 224.0,
            "bess_converter_rating_MVA": 1120.0,
            "bess_energy_one_hour_store_MWh": 1120.0,
            "bess_energy_required_MWh": 179.2 / 3600.0,
            "store_to_need_ratio": 22500.0,
        },
        "context": {
            "system_stored_energy_MJ": SYSTEM_EKIN_MJ,
            "reference_loss_MW": LOSS_MW,
            "condenser_H_s_fixed": H_S,
        },
        "findings": [
            "Required BESS power scales with the amplification factor k = 0.8 / (0.8 - T_d): from k = 1.12 at the p5 response time (0.086 s, 251 MW) to k = 1.47 at the p95 response time (0.257 s, 330 MW), against the zero-delay 224 MW baseline (median k = 1.26, 281 MW).",
            "The physical energy requirement (eq 4.11) does not change with response time in this model (fixed at 0.0498 MWh); only power, converter rating and capex scale with k, so response time drives a power/converter-sizing risk, not an energy-sizing risk.",
            "The energy-store-to-need ratio is 22 500 x k, so about 25 200 at p5 and about 33 100 at p95, rising with response time because the one-hour store scales with converter rating (k) while the physical energy need (eq 4.11) does not; power headroom remains the binding constraint throughout.",
        ],
        "assumptions": [
            "BESS response time T_d ~ triangular(0.05, 0.15, 0.30) s. Not read from ch4.html; order-of-magnitude assumption anchored to published fast-frequency-response products (e.g. National Grid ESO Dynamic Containment, full delivery within about 1 s); verify against a specific product spec.",
            "Effect model: required power scaled by k = t_natural/(t_natural - T_d), t_natural = 0.8 s (the time to reach the 0.8 Hz target excursion uncorrected). First-order remaining-time approximation, not a full dynamic simulation; assumption of this study.",
            "Condenser H held fixed at 3.5 s (ch4 Example 4.2 textbook value) so this scenario isolates response-time uncertainty; the inertia-constant scenario covers H uncertainty separately.",
            "Fleet: 8 x 200 MVA = 1.6 GVA, ch4 Example 4.2 (the brief's '1.6 GW' is written as 1.6 GVA in the textbook).",
            "f0 = 50 Hz, ch4 Examples 4.1 and 4.2.",
            "Design RoCoF = 1.0 Hz/s, ch4 eq (4.12), DS3 / GB loss-of-mains figure [S16 - verify]; fixed.",
            "Energy term over a 0.8 Hz excursion, ch4 eq (4.11), linearised form (0.80% above the exact form); fixed.",
            "BESS virtual inertia constant H_v = 5.0 s, so 0.20 pu headroom per unit rating, ch4 eq (4.13), 'assumed for this case'; fixed.",
            "Terminal voltage 1.0 pu, unity power factor, current limit 1.2 pu at 1.0 pu dispatch, ch4 Constraint 3; converter rating = headroom / 0.20.",
            "One-hour store (MWh = MVA rating x 1 h), ch4 Constraint 1, 'assumed for this case'; reported separately from the physical energy need.",
            "Unit costs 200 USD/kVA (converter + connection) and 250 USD/kWh (energy), fixed placeholders, not from a source read in this run; the cost-curve scenario owns cost uncertainty.",
            "System context 200 GVA.s and 1000 MW loss from ch4 Example 4.1; context only, not used in the sizing.",
            "No current limiting beyond the 1.2 pu cap, no degradation, no outage: other P5 scenarios cover those.",
        ],
    }
    with open(os.path.join(here, "response-time.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")

    for key, r in results.items():
        print(f"{key:34s} p5 {r['p5']:12.4f}  p50 {r['p50']:12.4f}  p95 {r['p95']:12.4f}  {r['unit']}")
    print("self-check passed")


if __name__ == "__main__":
    main()
