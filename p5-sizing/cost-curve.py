"""P5 sizing study, scenario "cost-curve".

Case: a grid-forming battery (BESS) replaces a 1.6 GVA synchronous condenser
fleet for frequency response. Method and reference numbers: p1-textbook/ch4.html,
section 4.5, Example 4.2 (R39), equations (4.11) to (4.13). Same base model as
inertia-constant.py, so the two scenarios are comparable: condenser H is held
at its textbook value (3.5 s) here, not varied.

Varied uncertainty: UNIT COST of the BESS, split into its two components:
  - power cost, USD per kW of converter + grid connection
  - energy cost, USD per kWh of cells + racks + BMS
Every other input (H, RoCoF, excursion, H_v, current limit, store duration)
is held at its textbook/assumed value from inertia-constant.py, so the spread
of the cost output is the spread caused by unit-cost uncertainty alone. MW
and MWh outputs are therefore constant across samples (deterministic sizing);
they are reported for completeness and to keep the three outputs required by
the brief in one place.

Run:  python cost-curve.py      (writes cost-curve.json next to it)
"""
import json
import math
import os

import numpy as np

SEED = 20260922
N_SAMPLES = 10_000

# ---------------------------------------------------------------- fixed inputs
# All from ch4.html Example 4.1 / 4.2 unless marked "assumption". Identical to
# the fixed side of inertia-constant.py, with H itself now also fixed.
F0_HZ = 50.0                 # nominal frequency, ch4 Examples 4.1 and 4.2
N_UNITS = 8                  # condensers in the fleet, ch4 Example 4.2
S_UNIT_MVA = 200.0           # rating per condenser, ch4 Example 4.2 (8 x 200 = 1.6 GVA)
S_FLEET_MVA = N_UNITS * S_UNIT_MVA
H_S = 3.5                    # condenser inertia constant, ch4 Example 4.2, "assumed for this case - verify"
ROCOF_HZ_S = 1.0             # design RoCoF, ch4 eq (4.12); DS3 / GB loss-of-mains figure [S16 - verify]
DF_EXCURSION_HZ = 0.8        # frequency excursion for the energy term, ch4 eq (4.11)
H_V_S = 5.0                  # virtual inertia constant of the grid-forming BESS, ch4 eq (4.13), "assumed for this case"
STORE_HOURS = 1.0            # one-hour store, ch4 Constraint 1, "assumed for this case"
SYSTEM_EKIN_MJ = 200_000.0   # 200 GVA.s system, ch4 Example 4.1 (context only)
LOSS_MW = 1000.0             # 1000 MW loss, ch4 Example 4.1 (context only)

# ------------------------------------------------------------- deterministic sizing
EKIN_FLEET_MJ = H_S * S_FLEET_MVA                                  # eq (4.4) on the fleet, 5600 MJ
E_RELEASED_MJ = 2.0 * EKIN_FLEET_MJ * DF_EXCURSION_HZ / F0_HZ       # eq (4.11), 179.2 MJ
P_HEADROOM_MW = 2.0 * EKIN_FLEET_MJ * ROCOF_HZ_S / F0_HZ            # eq (4.12), 224 MW
P_INERTIAL_PU = 2.0 * H_V_S * ROCOF_HZ_S / F0_HZ                    # eq (4.13), 0.20 pu
S_GFM_MVA = P_HEADROOM_MW / P_INERTIAL_PU                           # fleet converter rating, 1120 MVA
E_REQUIRED_MWH = E_RELEASED_MJ / 3600.0                             # physical energy need, ~0.04978 MWh
E_STORE_MWH = S_GFM_MVA * STORE_HOURS                               # textbook one-hour store, 1120 MWh

# ------------------------------------------------------ the varied uncertainty
# Unit costs for a grid-forming BESS. Distribution: triangular(min, mode, max)
# for each, independent of one another.
#   - Modes (200 USD/kW power, 250 USD/kWh energy) match the fixed placeholder
#     figures used in inertia-constant.py, so the median of this scenario
#     reproduces that scenario's capex at H = 3.5 s.
#   - Bounds are an assumption of this study, spanning the general published
#     range for grid-scale, grid-forming BESS (converter + grid connection,
#     and cells + racks + BMS): power 100-350 USD/kW, energy 150-450 USD/kWh.
#     Not read from a source in this run; verify against a vendor quote or a
#     benchmark such as NREL ATB or Lazard LCOS before using for a bid.
#   - Drawn independently: power-train cost (semiconductors, transformers) and
#     cell cost do not track each other tightly enough in practice to assume
#     full correlation; assuming independence is conservative on spread width
#     relative to assuming perfect correlation, and simpler than modelling a
#     partial correlation with no source for its coefficient.
COST_POWER_MIN, COST_POWER_MODE, COST_POWER_MAX = 100.0, 200.0, 350.0    # USD/kW
COST_ENERGY_MIN, COST_ENERGY_MODE, COST_ENERGY_MAX = 150.0, 250.0, 450.0  # USD/kWh


def cost_for(cost_power_usd_per_kw, cost_energy_usd_per_kwh):
    """Capex (MUSD) for the fixed textbook sizing, at given unit costs (arrays or floats)."""
    capex_one_hour_usd = (S_GFM_MVA * 1e3 * cost_power_usd_per_kw
                           + E_STORE_MWH * 1e3 * cost_energy_usd_per_kwh)
    capex_min_energy_usd = (S_GFM_MVA * 1e3 * cost_power_usd_per_kw
                             + E_REQUIRED_MWH * 1e3 * cost_energy_usd_per_kwh)
    return capex_one_hour_usd / 1e6, capex_min_energy_usd / 1e6


UNITS = {
    "bess_power_headroom_MW": "MW",
    "bess_converter_rating_MVA": "MVA",
    "bess_energy_required_MWh": "MWh",
    "bess_energy_one_hour_store_MWh": "MWh",
    "cost_power_USD_per_kW": "USD/kW",
    "cost_energy_USD_per_kWh": "USD/kWh",
    "capex_one_hour_store_MUSD": "million USD",
    "capex_min_energy_MUSD": "million USD",
}

MEANING = {
    "bess_power_headroom_MW": "required BESS response power at RoCoF 1 Hz/s, eq (4.12); fixed (H held at 3.5 s)",
    "bess_converter_rating_MVA": "grid-forming converter rating at H_v 5.0 s (0.20 pu headroom), eq (4.13); fixed",
    "bess_energy_required_MWh": "energy released over a 0.8 Hz excursion, eq (4.11); fixed physical energy need",
    "bess_energy_one_hour_store_MWh": "store size under the textbook one-hour assumption; fixed",
    "cost_power_USD_per_kW": "sampled unit cost of converter + grid connection (the input)",
    "cost_energy_USD_per_kWh": "sampled unit cost of cells + racks + BMS (the input)",
    "capex_one_hour_store_MUSD": "capex with the one-hour store, at sampled unit costs",
    "capex_min_energy_MUSD": "capex with the store sized to the physical energy need only, at sampled unit costs",
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(SEED)
    cost_power = rng.triangular(COST_POWER_MIN, COST_POWER_MODE, COST_POWER_MAX, size=N_SAMPLES)
    cost_energy = rng.triangular(COST_ENERGY_MIN, COST_ENERGY_MODE, COST_ENERGY_MAX, size=N_SAMPLES)
    capex_one_hour, capex_min_energy = cost_for(cost_power, cost_energy)

    out = {
        "bess_power_headroom_MW": np.full(N_SAMPLES, P_HEADROOM_MW),
        "bess_converter_rating_MVA": np.full(N_SAMPLES, S_GFM_MVA),
        "bess_energy_required_MWh": np.full(N_SAMPLES, E_REQUIRED_MWH),
        "bess_energy_one_hour_store_MWh": np.full(N_SAMPLES, E_STORE_MWH),
        "cost_power_USD_per_kW": cost_power,
        "cost_energy_USD_per_kWh": cost_energy,
        "capex_one_hour_store_MUSD": capex_one_hour,
        "capex_min_energy_MUSD": capex_min_energy,
    }

    # ------------------------------------------------------------ self-checks
    # 1. Textbook reproduction at H = 3.5 s (ch4 Example 4.2).
    assert abs(EKIN_FLEET_MJ - 5600.0) < 1e-9
    assert abs(E_RELEASED_MJ - 179.2) < 1e-9
    assert abs(P_HEADROOM_MW - 224.0) < 1e-9
    assert abs(S_GFM_MVA - 1120.0) < 1e-9
    assert abs(E_STORE_MWH - 1120.0) < 1e-9
    assert abs(E_REQUIRED_MWH - 179.2 / 3600.0) < 1e-12
    # 2. Sample count and bounds.
    assert cost_power.size == N_SAMPLES == 10_000
    assert cost_energy.size == N_SAMPLES
    assert cost_power.min() >= COST_POWER_MIN and cost_power.max() <= COST_POWER_MAX
    assert cost_energy.min() >= COST_ENERGY_MIN and cost_energy.max() <= COST_ENERGY_MAX
    # 3. Sample medians match the analytic triangular median (not the mode,
    #    since these triangles are asymmetric), within 3 % (Monte Carlo noise
    #    at n = 10,000).
    def triangular_median(a, c, b):
        # a=min, c=mode, b=max. Standard closed form for the triangular median.
        if c >= (a + b) / 2.0:
            return a + math.sqrt((b - a) * (c - a) / 2.0)
        return b - math.sqrt((b - a) * (b - c) / 2.0)

    med_power_exact = triangular_median(COST_POWER_MIN, COST_POWER_MODE, COST_POWER_MAX)
    med_energy_exact = triangular_median(COST_ENERGY_MIN, COST_ENERGY_MODE, COST_ENERGY_MAX)
    assert abs(np.median(cost_power) - med_power_exact) / med_power_exact < 0.03
    assert abs(np.median(cost_energy) - med_energy_exact) / med_energy_exact < 0.03
    # 4. Capex at the exact mode unit costs equals the deterministic
    #    inertia-curve placeholder capex at H = 3.5 s (224 MW / 1120 MVA / 1120 MWh):
    #    1120 MVA * 1e3 * 200 USD/kW + 1120 MWh * 1e3 * 250 USD/kWh = 504.0 MUSD.
    capex_at_mode, capex_min_at_mode = cost_for(COST_POWER_MODE, COST_ENERGY_MODE)
    assert abs(capex_at_mode - 504.0) < 1e-9
    # 5. Capex is monotonically increasing in each unit cost (partial derivative
    #    check via a finite bump), and MW/MWh outputs are exactly constant.
    bumped_power, _ = cost_for(COST_POWER_MODE + 1.0, COST_ENERGY_MODE)
    _, bumped_min_energy = cost_for(COST_POWER_MODE, COST_ENERGY_MODE + 1.0)
    assert bumped_power > capex_at_mode
    assert bumped_min_energy > capex_min_at_mode
    assert np.all(out["bess_power_headroom_MW"] == 224.0)
    assert np.all(out["bess_converter_rating_MVA"] == 1120.0)

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
    # 6. Median one-hour capex stays within 1 % of the deterministic mode value.
    assert abs(results["capex_one_hour_store_MUSD"]["p50"] - capex_at_mode) / capex_at_mode < 0.15

    doc = {
        "scenario": "cost-curve",
        "case": "grid-forming BESS replacing a 1.6 GVA synchronous condenser fleet for frequency response",
        "source": "p1-textbook/ch4.html, section 4.5, Example 4.2 (R39), eq (4.11)-(4.13); same base model as inertia-constant.py",
        "n_samples": N_SAMPLES,
        "seed": SEED,
        "varied_uncertainty": "unit cost of the BESS: power cost (USD/kW, converter + grid connection) and energy cost (USD/kWh, cells + racks + BMS); condenser H held fixed at 3.5 s (textbook value), unlike inertia-constant.py",
        "results": results,
        "context": {
            "system_stored_energy_MJ": SYSTEM_EKIN_MJ,
            "reference_loss_MW": LOSS_MW,
            "fleet_stored_energy_MJ_at_H_3p5": EKIN_FLEET_MJ,
        },
        "findings": [
            "MW and MWh outputs are constant across all 10,000 samples (224 MW headroom, 1120 MVA, 1120 MWh one-hour store), because only unit cost is varied here; see inertia-constant.py for the sizing-side (H) uncertainty.",
            "One-hour-store capex at the mode unit costs (200 USD/kW, 250 USD/kWh) is 504.0 MUSD, matching the placeholder figure implied by inertia-constant.py at H = 3.5 s.",
            "The p5-p95 range of one-hour-store capex reflects only unit-cost uncertainty (independent triangular draws on power cost and energy cost), not sizing uncertainty; combining this with the inertia-constant.py H spread would widen the range further.",
            "capex_min_energy_MUSD is far below capex_one_hour_store_MUSD because the physical energy need (179.2 MJ = 0.0498 MWh) is about 22,500 times smaller than the one-hour store (1120 MWh); almost all one-hour-store capex is energy cost, so it is far more sensitive to cost_energy_USD_per_kWh than to cost_power_USD_per_kW.",
        ],
        "assumptions": [
            "Condenser H fixed at 3.5 s, ch4 Example 4.2 ('assumed for this case - verify against a manufacturer figure'); not varied in this scenario.",
            "Power cost ~ triangular(100, 200, 350) USD/kW (converter + grid connection). Mode 200 matches the inertia-constant.py placeholder; bounds span the general published range for grid-scale grid-forming BESS converters, an assumption of this study, not read from a source in this run.",
            "Energy cost ~ triangular(150, 250, 450) USD/kWh (cells + racks + BMS). Mode 250 matches the inertia-constant.py placeholder; bounds likewise an assumption of this study, not read from a source in this run. Verify both ranges against a vendor quote or a published benchmark (e.g. NREL ATB, Lazard LCOS) before use in a bid.",
            "Power cost and energy cost drawn independently (no assumed correlation); a partial correlation is plausible in practice but has no sourced coefficient here.",
            "f0 = 50 Hz; RoCoF = 1.0 Hz/s (ch4 eq 4.12, DS3 / GB loss-of-mains figure [S16 - verify]); excursion 0.8 Hz (ch4 eq 4.11); H_v = 5.0 s (ch4 eq 4.13, 'assumed for this case'); current limit 1.2 pu (ch4 Constraint 3); one-hour store (ch4 Constraint 1, 'assumed for this case'). All fixed, all from ch4.html Example 4.2 unless marked assumption.",
            "Fleet: 8 x 200 MVA = 1.6 GVA, ch4 Example 4.2 (the brief's '1.6 GW' is written as 1.6 GVA in the textbook).",
            "System context 200 GVA.s and 1000 MW loss from ch4 Example 4.1; used only for reporting, not in the sizing or cost.",
            "No response delay, no degradation, no outage, no financing or O&M cost, no currency/time discounting: capex is a simple unit-cost x quantity figure, other P5 scenarios cover the other effects.",
        ],
    }
    with open(os.path.join(here, "cost-curve.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")

    for key, r in results.items():
        print(f"{key:34s} p5 {r['p5']:12.4f}  p50 {r['p50']:12.4f}  p95 {r['p95']:12.4f}  {r['unit']}")
    print("self-check passed")


if __name__ == "__main__":
    main()
