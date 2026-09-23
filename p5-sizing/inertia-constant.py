"""P5 sizing study, scenario "inertia-constant".

Case: a grid-forming battery (BESS) replaces a 1.6 GVA synchronous condenser
fleet for frequency response. Method and reference numbers: p1-textbook/ch4.html,
section 4.5, Example 4.2 (R39), equations (4.11) to (4.13).

Varied uncertainty: the inertia constant H of each condenser (textbook value
3.5 s, "assumed for this case - verify against a manufacturer figure").
Every other input is held at its textbook value, so the spread of the outputs
is the spread caused by H alone.

Run:  python inertia-constant.py      (writes inertia-constant.json next to it)
"""
import json
import os

import numpy as np

SEED = 20260922
N_SAMPLES = 10_000

# ---------------------------------------------------------------- fixed inputs
# All from ch4.html Example 4.1 / 4.2 unless marked "assumption".
F0_HZ = 50.0            # nominal frequency, ch4 Example 4.1 and 4.2
N_UNITS = 8             # condensers in the fleet, ch4 Example 4.2
S_UNIT_MVA = 200.0      # rating per condenser, ch4 Example 4.2 (8 x 200 = 1.6 GVA)
S_FLEET_MVA = N_UNITS * S_UNIT_MVA
ROCOF_HZ_S = 1.0        # design RoCoF, ch4 eq (4.12); DS3 / GB loss-of-mains figure [S16 - verify]
DF_EXCURSION_HZ = 0.8   # frequency excursion for the energy term, ch4 eq (4.11)
H_V_S = 5.0             # virtual inertia constant of the grid-forming BESS, ch4 eq (4.13), "assumed for this case"
STORE_HOURS = 1.0       # one-hour store, ch4 Constraint 1, "assumed for this case"
SYSTEM_EKIN_MJ = 200_000.0  # 200 GVA.s system, ch4 Example 4.1 (context only: fleet share)
LOSS_MW = 1000.0            # 1000 MW loss, ch4 Example 4.1 (context only)

# Cost inputs: assumption, NOT read from any source in this run. They are held
# fixed here; the separate "cost-curve" scenario owns cost uncertainty. Round
# placeholder figures so the memo can see how cost scales with H.
COST_POWER_USD_PER_KVA = 200.0   # grid-forming converter + grid connection, assumption
COST_ENERGY_USD_PER_KWH = 250.0  # cells + racks + BMS, assumption

# ------------------------------------------------------ the varied uncertainty
# H of each condenser, in seconds, including its flywheel.
# Distribution: triangular(min 2.0, mode 3.5, max 5.0).
#   - mode 3.5 s = the textbook value (ch4 Example 4.2), so the median sample
#     reproduces the textbook answer (224 MW, 1120 MVA).
#   - bounds 2.0 s and 5.0 s: assumption of this study, not read from a source.
#     Low end stands for a condenser with a small or no flywheel; high end for a
#     large flywheel. Verify against manufacturer data before quoting.
#   - one H per sample applied to all 8 units (fully correlated): the
#     uncertainty is in the design/manufacturer figure, which is common to a
#     fleet bought together. Independent draws per unit would narrow the spread
#     by about 1/sqrt(8) and understate it.
H_MIN_S, H_MODE_S, H_MAX_S = 2.0, 3.5, 5.0


def size_for_h(h_s):
    """Return the sizing outputs for condenser inertia constant h_s (array or float)."""
    ekin_fleet_mj = h_s * S_FLEET_MVA                                   # eq (4.4) on the fleet, MJ = MVA.s
    e_released_mj = 2.0 * ekin_fleet_mj * DF_EXCURSION_HZ / F0_HZ        # eq (4.11)
    p_headroom_mw = 2.0 * ekin_fleet_mj * ROCOF_HZ_S / F0_HZ             # eq (4.12)
    p_inertial_pu = 2.0 * H_V_S * ROCOF_HZ_S / F0_HZ                     # eq (4.13), 0.20 pu
    s_gfm_mva = p_headroom_mw / p_inertial_pu                            # fleet rating
    e_required_mwh = e_released_mj / 3600.0                              # physical energy need
    e_store_mwh = s_gfm_mva * STORE_HOURS                                # textbook one-hour store
    capex_usd = (s_gfm_mva * 1e3 * COST_POWER_USD_PER_KVA
                 + e_store_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    capex_power_only_usd = (s_gfm_mva * 1e3 * COST_POWER_USD_PER_KVA
                            + e_required_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    return {
        "condenser_H_s": h_s,
        "fleet_stored_energy_MJ": ekin_fleet_mj,
        "bess_power_headroom_MW": p_headroom_mw,
        "bess_converter_rating_MVA": s_gfm_mva,
        "bess_energy_required_MWh": e_required_mwh,
        "bess_energy_one_hour_store_MWh": e_store_mwh,
        "capex_one_hour_store_MUSD": capex_usd / 1e6,
        "capex_min_energy_MUSD": capex_power_only_usd / 1e6,
    }


UNITS = {
    "condenser_H_s": "s",
    "fleet_stored_energy_MJ": "MJ",
    "bess_power_headroom_MW": "MW",
    "bess_converter_rating_MVA": "MVA",
    "bess_energy_required_MWh": "MWh",
    "bess_energy_one_hour_store_MWh": "MWh",
    "capex_one_hour_store_MUSD": "million USD",
    "capex_min_energy_MUSD": "million USD",
}

MEANING = {
    "condenser_H_s": "sampled condenser inertia constant (the input)",
    "fleet_stored_energy_MJ": "condenser fleet kinetic energy the BESS must match, H x 1600 MVA",
    "bess_power_headroom_MW": "power above dispatch at RoCoF 1 Hz/s, eq (4.12); the required BESS response power",
    "bess_converter_rating_MVA": "grid-forming converter rating at H_v 5.0 s (0.20 pu headroom), eq (4.13)",
    "bess_energy_required_MWh": "energy released over a 0.8 Hz excursion, eq (4.11); the physical energy need",
    "bess_energy_one_hour_store_MWh": "store size under the textbook one-hour assumption (a design choice, not a requirement)",
    "capex_one_hour_store_MUSD": "capex with the one-hour store, fixed placeholder unit costs",
    "capex_min_energy_MUSD": "capex with the store sized to the physical energy need only",
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(SEED)
    h = rng.triangular(H_MIN_S, H_MODE_S, H_MAX_S, size=N_SAMPLES)
    out = size_for_h(h)

    # ------------------------------------------------------------ self-checks
    # 1. Textbook reproduction at H = 3.5 s (ch4 Example 4.2).
    ref = size_for_h(3.5)
    assert abs(ref["fleet_stored_energy_MJ"] - 5600.0) < 1e-9
    assert abs(ref["fleet_stored_energy_MJ"] * 2 * DF_EXCURSION_HZ / F0_HZ - 179.2) < 1e-9
    assert abs(ref["bess_power_headroom_MW"] - 224.0) < 1e-9
    assert abs(ref["bess_converter_rating_MVA"] - 1120.0) < 1e-9
    assert abs(ref["bess_energy_one_hour_store_MWh"] - 1120.0) < 1e-9
    assert abs(ref["bess_energy_required_MWh"] - 179.2 / 3600.0) < 1e-12
    # 2. Sample count and bounds.
    assert h.size == N_SAMPLES == 10_000
    assert h.min() >= H_MIN_S and h.max() <= H_MAX_S
    # 3. Power is linear in H: 2 x 1600 x 1.0 / 50 = 64 MW per second of H.
    assert np.allclose(out["bess_power_headroom_MW"] / h, 64.0)
    # 4. Energy-store-to-need ratio is 22 500 for every H (ch4 Constraint 1),
    #    so H does not change which constraint binds.
    ratio = out["bess_energy_one_hour_store_MWh"] / out["bess_energy_required_MWh"]
    assert np.allclose(ratio, 22_500.0)
    # 5. Sample percentiles of H against the analytic triangular quantiles.
    #    Lower tail: x = a + sqrt(q (b-a)(c-a)); upper tail by symmetry here.
    q5_exact = H_MIN_S + np.sqrt(0.05 * (H_MAX_S - H_MIN_S) * (H_MODE_S - H_MIN_S))
    q95_exact = H_MAX_S - np.sqrt(0.05 * (H_MAX_S - H_MIN_S) * (H_MAX_S - H_MODE_S))
    hp5, hp50, hp95 = np.percentile(h, [5, 50, 95])
    assert abs(hp5 - q5_exact) / q5_exact < 0.01
    assert abs(hp50 - H_MODE_S) / H_MODE_S < 0.01
    assert abs(hp95 - q95_exact) / q95_exact < 0.01

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
    # 6. Median power stays within 1 % of the textbook 224 MW.
    assert abs(results["bess_power_headroom_MW"]["p50"] - 224.0) / 224.0 < 0.01

    doc = {
        "scenario": "inertia-constant",
        "case": "grid-forming BESS replacing a 1.6 GVA synchronous condenser fleet for frequency response",
        "source_method": "p1-textbook/ch4.html section 4.5, Example 4.2 (R39), eqs (4.11)-(4.13)",
        "n_samples": N_SAMPLES,
        "seed": SEED,
        "varied_uncertainty": {
            "name": "condenser inertia constant H (s, including flywheel)",
            "distribution": f"triangular(min {H_MIN_S}, mode {H_MODE_S}, max {H_MAX_S})",
            "correlation": "one H per sample, applied to all 8 units",
        },
        "outputs": results,
        "textbook_reference_at_H_3p5": {
            "fleet_stored_energy_MJ": 5600.0,
            "energy_released_0p8Hz_MJ": 179.2,
            "bess_power_headroom_MW": 224.0,
            "bess_converter_rating_MVA": 1120.0,
            "bess_energy_one_hour_store_MWh": 1120.0,
            "store_to_need_ratio": 22500.0,
        },
        "context": {
            "system_stored_energy_MJ": SYSTEM_EKIN_MJ,
            "reference_loss_MW": LOSS_MW,
            "fleet_share_of_system_inertia_p5_p50_p95_pct": [
                round(float(v) / SYSTEM_EKIN_MJ * 100, 4)
                for v in np.percentile(out["fleet_stored_energy_MJ"], [5, 50, 95])
            ],
        },
        "findings": [
            "Required BESS power scales 1:1 with H: 64 MW per second of H, so the p5-p95 H range maps directly to the power range.",
            "The store-to-need energy ratio is 22 500 at every H, so power headroom (with the current limit) stays the binding constraint across the whole H range; energy never binds.",
            "Capex with a one-hour store is dominated by the store and scales linearly with H; the placeholder unit costs are not sourced.",
        ],
        "assumptions": [
            "Condenser H ~ triangular(2.0, 3.5, 5.0) s. Mode 3.5 s from ch4 Example 4.2 (itself 'assumed for this case - verify'). Bounds 2.0 s and 5.0 s are an assumption of this study, not read from a source.",
            "One H per sample for all 8 condensers (fully correlated). Independent per-unit draws would narrow the spread by about 1/sqrt(8).",
            "Fleet: 8 x 200 MVA = 1.6 GVA, ch4 Example 4.2 (the brief's '1.6 GW' is written as 1.6 GVA in the textbook).",
            "f0 = 50 Hz, ch4 Examples 4.1 and 4.2.",
            "Design RoCoF = 1.0 Hz/s, ch4 eq (4.12), DS3 / GB loss-of-mains figure [S16 - verify]; fixed.",
            "Energy term over a 0.8 Hz excursion, ch4 eq (4.11), linearised form (0.80 % above the exact form); fixed.",
            "BESS virtual inertia constant H_v = 5.0 s, so 0.20 pu headroom per unit rating, ch4 eq (4.13), 'assumed for this case'; fixed.",
            "Terminal voltage 1.0 pu, unity power factor, current limit 1.2 pu at 1.0 pu dispatch, ch4 Constraint 3; converter rating = headroom / 0.20.",
            "One-hour store (MWh = MVA rating x 1 h), ch4 Constraint 1, 'assumed for this case'; reported separately from the physical energy need.",
            "Unit costs 200 USD/kVA (converter + connection) and 250 USD/kWh (energy), fixed placeholders, not from a source read in this run; the cost-curve scenario owns cost uncertainty.",
            "System context 200 GVA.s and 1000 MW loss from ch4 Example 4.1; used only for the fleet-share figure, not in the sizing.",
            "No current limiting beyond the 1.2 pu cap, no response delay, no degradation, no outage: other P5 scenarios cover those.",
        ],
    }
    with open(os.path.join(here, "inertia-constant.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")

    for key, r in results.items():
        print(f"{key:34s} p5 {r['p5']:12.4f}  p50 {r['p50']:12.4f}  p95 {r['p95']:12.4f}  {r['unit']}")
    print("self-check passed")


if __name__ == "__main__":
    main()
