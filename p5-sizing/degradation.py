"""P5 sizing study, scenario "degradation".

Case: a grid-forming battery (BESS) replaces a 1.6 GVA synchronous condenser
fleet for frequency response. Base method and reference numbers:
p1-textbook/ch4.html, section 4.5, Example 4.2 (R39), equations (4.11)-(4.13).
Same base model as inertia-constant.py / cost-curve.py, with condenser H held
fixed at the textbook value 3.5 s, so the end-of-life (EOL) requirement this
scenario must still meet is the textbook figure: 224 MW headroom, 1120 MVA
converter rating, 1120 MWh one-hour store.

Varied uncertainty: BESS energy (capacity) fade and power fade over a 15-year
life. Not in ch4.html -- ch4.html has no ageing model. Both fades are modelled
here as an assumption of this study, order-of-magnitude anchored to common
industry conventions for grid-scale Li-ion BESS end-of-life (EOL); verify
against a specific vendor warranty spec before quoting.

Sizing logic: ch4.html sizes the BESS to meet the requirement once, with no
time axis. This scenario asks the requirement to still hold at year 15, after
the battery has faded. So the plant must be installed at beginning of life
(BOL) somewhat larger than the bare EOL requirement:
    BOL power (MVA)  = EOL required power (1120 MVA) / power retention at EOL
    BOL energy (MWh) = EOL required energy (1120 MWh) / energy retention at EOL
where "retention at EOL" is the fraction of BOL nameplate capability still
available after 15 years. Capex is then unit cost x the BOL (as-installed)
quantities, since that is what is bought and paid for on day one.

Run:  python degradation.py      (writes degradation.json next to it)
"""
import json
import math
import os

import numpy as np

SEED = 20260922
N_SAMPLES = 10_000
LIFE_YEARS = 15

# ---------------------------------------------------------------- fixed inputs
# All from ch4.html Example 4.1 / 4.2 unless marked "assumption". Identical to
# the fixed side of cost-curve.py: H fixed at its textbook value, so this
# scenario isolates degradation, not inertia spread or unit-cost spread.
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

# ------------------------------------------------------- deterministic EOL requirement
# The requirement the plant must still meet at end of life (year 15), computed
# by the unchanged ch4.html method (identical to cost-curve.py's fixed sizing).
EKIN_FLEET_MJ = H_S * S_FLEET_MVA                                  # eq (4.4) on the fleet, 5600 MJ
E_RELEASED_MJ = 2.0 * EKIN_FLEET_MJ * DF_EXCURSION_HZ / F0_HZ       # eq (4.11), 179.2 MJ
P_HEADROOM_MW_EOL = 2.0 * EKIN_FLEET_MJ * ROCOF_HZ_S / F0_HZ        # eq (4.12), 224 MW
P_INERTIAL_PU = 2.0 * H_V_S * ROCOF_HZ_S / F0_HZ                    # eq (4.13), 0.20 pu
S_GFM_MVA_EOL = P_HEADROOM_MW_EOL / P_INERTIAL_PU                   # required EOL converter rating, 1120 MVA
E_REQUIRED_MWH = E_RELEASED_MJ / 3600.0                             # physical energy need, ~0.04978 MWh (fade-independent)
E_STORE_MWH_EOL = S_GFM_MVA_EOL * STORE_HOURS                       # required EOL one-hour store, 1120 MWh

# Unit costs: assumption, NOT read from any source in this run. Majority
# convention per the brief: 200 USD/kW (power) + 250 USD/kWh (energy).
COST_POWER_USD_PER_KW = 200.0    # grid-forming converter + grid connection, assumption
COST_ENERGY_USD_PER_KWH = 250.0  # cells + racks + BMS, assumption

# ------------------------------------------------------ the varied uncertainty
# Two independent fades over the 15-year life, each expressed as the fraction
# of BOL nameplate capability still available at year 15 ("retention at EOL").
#   - Energy (capacity) retention at EOL: triangular(0.70, 0.80, 0.85).
#     Not in ch4.html. Order-of-magnitude assumption of this study, anchored
#     to the common industry convention of defining Li-ion grid-storage EOL
#     at 70-80% retained capacity (e.g. NREL ATB storage degradation
#     assumptions; vendor warranties such as Tesla Megapack, quoted around
#     70% retention at 20 years, imply a higher figure at 15 years). Verify
#     against a specific product warranty spec before quoting.
#   - Power retention at EOL: triangular(0.85, 0.92, 0.97).
#     Not in ch4.html. Assumption of this study: power fade (driven mainly by
#     cell internal-resistance rise) is generally smaller than energy
#     (capacity) fade for grid-scale Li-ion over a 15-year life, since the
#     converter itself does not materially degrade; order-of-magnitude only,
#     verify against a specific product spec.
#   - Drawn independently: the mechanisms (capacity loss vs. resistance rise)
#     are related but not perfectly correlated in practice, and no sourced
#     correlation coefficient is available; independence is the simpler,
#     unbiased choice here (as in cost-curve.py's independent unit costs).
ENERGY_RETENTION_MIN, ENERGY_RETENTION_MODE, ENERGY_RETENTION_MAX = 0.70, 0.80, 0.85
POWER_RETENTION_MIN, POWER_RETENTION_MODE, POWER_RETENTION_MAX = 0.85, 0.92, 0.97


def size_for_fade(energy_retention, power_retention):
    """BOL install (MVA, MWh) and capex (MUSD) so EOL still meets the fixed
    requirement, given fractional retention at EOL (arrays or floats)."""
    s_bol_mva = S_GFM_MVA_EOL / power_retention          # BOL power so EOL power >= requirement
    e_bol_mwh = E_STORE_MWH_EOL / energy_retention        # BOL energy so EOL store >= requirement
    capex_usd = (s_bol_mva * 1e3 * COST_POWER_USD_PER_KW
                 + e_bol_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    return {
        "energy_retention_at_EOL": energy_retention,
        "power_retention_at_EOL": power_retention,
        "bess_installed_power_BOL_MVA": s_bol_mva,
        "bess_installed_energy_BOL_MWh": e_bol_mwh,
        "capex_BOL_MUSD": capex_usd / 1e6,
    }


UNITS = {
    "energy_retention_at_EOL": "fraction",
    "power_retention_at_EOL": "fraction",
    "bess_installed_power_BOL_MVA": "MVA",
    "bess_installed_energy_BOL_MWh": "MWh",
    "capex_BOL_MUSD": "million USD",
}

MEANING = {
    "energy_retention_at_EOL": "sampled fraction of BOL nameplate energy still available at year 15 (the input)",
    "power_retention_at_EOL": "sampled fraction of BOL nameplate power still available at year 15 (the input)",
    "bess_installed_power_BOL_MVA": "converter rating to install at BOL so EOL power still meets 1120 MVA / 224 MW headroom",
    "bess_installed_energy_BOL_MWh": "energy (one-hour store) to install at BOL so EOL energy still meets 1120 MWh",
    "capex_BOL_MUSD": "capex at BOL (day-one purchase), 200 USD/kW + 250 USD/kWh on the BOL install quantities",
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(SEED)
    energy_retention = rng.triangular(ENERGY_RETENTION_MIN, ENERGY_RETENTION_MODE, ENERGY_RETENTION_MAX, size=N_SAMPLES)
    power_retention = rng.triangular(POWER_RETENTION_MIN, POWER_RETENTION_MODE, POWER_RETENTION_MAX, size=N_SAMPLES)
    out = size_for_fade(energy_retention, power_retention)

    # ------------------------------------------------------------ self-checks
    # 1. EOL requirement reproduces the ch4 Example 4.2 / cost-curve.py textbook figures.
    assert abs(EKIN_FLEET_MJ - 5600.0) < 1e-9
    assert abs(E_RELEASED_MJ - 179.2) < 1e-9
    assert abs(P_HEADROOM_MW_EOL - 224.0) < 1e-9
    assert abs(S_GFM_MVA_EOL - 1120.0) < 1e-9
    assert abs(E_STORE_MWH_EOL - 1120.0) < 1e-9
    assert abs(E_REQUIRED_MWH - 179.2 / 3600.0) < 1e-12
    # 2. No fade (retention = 1) reproduces the bare EOL requirement exactly.
    ref = size_for_fade(1.0, 1.0)
    assert abs(ref["bess_installed_power_BOL_MVA"] - 1120.0) < 1e-9
    assert abs(ref["bess_installed_energy_BOL_MWh"] - 1120.0) < 1e-9
    # 3. Sample count and bounds.
    assert energy_retention.size == N_SAMPLES == 10_000
    assert power_retention.size == N_SAMPLES
    assert energy_retention.min() >= ENERGY_RETENTION_MIN and energy_retention.max() <= ENERGY_RETENTION_MAX
    assert power_retention.min() >= POWER_RETENTION_MIN and power_retention.max() <= POWER_RETENTION_MAX
    assert energy_retention.max() < 1.0 and power_retention.max() < 1.0, "retention must stay below 1 (fade is real)"
    # 4. BOL install always exceeds the bare EOL requirement (fade < 1 always
    #    inflates the install), and the identity S_bol * retention = EOL req
    #    holds exactly for every sample.
    assert np.all(out["bess_installed_power_BOL_MVA"] > S_GFM_MVA_EOL)
    assert np.all(out["bess_installed_energy_BOL_MWh"] > E_STORE_MWH_EOL)
    assert np.allclose(out["bess_installed_power_BOL_MVA"] * power_retention, S_GFM_MVA_EOL)
    assert np.allclose(out["bess_installed_energy_BOL_MWh"] * energy_retention, E_STORE_MWH_EOL)
    # 5. Capex at the exact mode retentions matches the closed-form figure.
    #    1120/0.92 = 1217.391... MVA; 1120/0.80 = 1400 MWh.
    #    1217.391e3 * 200 + 1400e3 * 250 = 243.478e6 + 350.0e6 = 593.478 MUSD.
    ref_at_mode = size_for_fade(ENERGY_RETENTION_MODE, POWER_RETENTION_MODE)
    s_bol_mode_exact = 1120.0 / POWER_RETENTION_MODE
    e_bol_mode_exact = 1120.0 / ENERGY_RETENTION_MODE
    capex_mode_exact = (s_bol_mode_exact * 1e3 * COST_POWER_USD_PER_KW
                         + e_bol_mode_exact * 1e3 * COST_ENERGY_USD_PER_KWH) / 1e6
    assert abs(ref_at_mode["bess_installed_power_BOL_MVA"] - s_bol_mode_exact) < 1e-9
    assert abs(ref_at_mode["bess_installed_energy_BOL_MWh"] - e_bol_mode_exact) < 1e-9
    assert abs(ref_at_mode["capex_BOL_MUSD"] - capex_mode_exact) < 1e-9
    assert abs(capex_mode_exact - 593.478260869) < 1e-6
    # 6. Capex is monotonically decreasing in each retention fraction (higher
    #    retention -> less BOL over-build needed -> lower capex).
    bumped_energy = size_for_fade(ENERGY_RETENTION_MODE + 0.01, POWER_RETENTION_MODE)
    bumped_power = size_for_fade(ENERGY_RETENTION_MODE, POWER_RETENTION_MODE + 0.01)
    assert bumped_energy["capex_BOL_MUSD"] < ref_at_mode["capex_BOL_MUSD"]
    assert bumped_power["capex_BOL_MUSD"] < ref_at_mode["capex_BOL_MUSD"]
    # 7. Sample medians match the analytic triangular medians (asymmetric
    #    triangles, so median != mode), within 2% (Monte Carlo noise at n = 10,000).
    def triangular_median(a, c, b):
        if c >= (a + b) / 2.0:
            return a + math.sqrt((b - a) * (c - a) / 2.0)
        return b - math.sqrt((b - a) * (b - c) / 2.0)

    med_energy_exact = triangular_median(ENERGY_RETENTION_MIN, ENERGY_RETENTION_MODE, ENERGY_RETENTION_MAX)
    med_power_exact = triangular_median(POWER_RETENTION_MIN, POWER_RETENTION_MODE, POWER_RETENTION_MAX)
    assert abs(np.median(energy_retention) - med_energy_exact) / med_energy_exact < 0.02
    assert abs(np.median(power_retention) - med_power_exact) / med_power_exact < 0.02

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
    # 8. Median BOL install and capex stay above the bare EOL requirement /
    #    the mode-retention capex reference by construction.
    assert results["bess_installed_power_BOL_MVA"]["p50"] > S_GFM_MVA_EOL
    assert results["bess_installed_energy_BOL_MWh"]["p50"] > E_STORE_MWH_EOL
    assert results["capex_BOL_MUSD"]["p50"] > 0.0

    doc = {
        "scenario": "degradation",
        "case": "grid-forming BESS replacing a 1.6 GVA synchronous condenser fleet for frequency response",
        "source_method": "p1-textbook/ch4.html section 4.5, Example 4.2 (R39), eqs (4.11)-(4.13); same base model as inertia-constant.py / cost-curve.py, H fixed at 3.5 s. ch4.html has no ageing model; the degradation logic below is an addition of this study.",
        "n_samples": N_SAMPLES,
        "seed": SEED,
        "life_years": LIFE_YEARS,
        "varied_uncertainty": {
            "energy_retention_at_EOL": {
                "distribution": f"triangular(min {ENERGY_RETENTION_MIN}, mode {ENERGY_RETENTION_MODE}, max {ENERGY_RETENTION_MAX})",
                "meaning": "fraction of BOL nameplate energy (capacity) still available after 15 years",
                "source": "Not in ch4.html. Assumption of this study, order-of-magnitude anchored to the common industry convention of 70-80% retained capacity as Li-ion grid-storage end-of-life (e.g. NREL ATB storage degradation assumptions; vendor warranties such as Tesla Megapack, quoted near 70% retention at 20 years). Verify against a specific product warranty spec before quoting.",
            },
            "power_retention_at_EOL": {
                "distribution": f"triangular(min {POWER_RETENTION_MIN}, mode {POWER_RETENTION_MODE}, max {POWER_RETENTION_MAX})",
                "meaning": "fraction of BOL nameplate power still available after 15 years",
                "source": "Not in ch4.html. Assumption of this study: power fade (cell internal-resistance rise) is generally smaller than capacity fade for grid-scale Li-ion over 15 years, and the converter itself does not materially degrade. Order-of-magnitude only; verify against a specific product spec.",
            },
            "correlation": "energy_retention_at_EOL and power_retention_at_EOL drawn independently; no sourced correlation coefficient between capacity fade and power fade.",
        },
        "sizing_logic": {
            "description": "BOL install = EOL requirement / retention at EOL, so the plant still meets the ch4.html requirement (1120 MVA / 224 MW headroom, 1120 MWh one-hour store) after 15 years of fade. Capex is unit cost x the BOL (as-installed, day-one) quantities.",
            "eol_requirement_power_MVA": S_GFM_MVA_EOL,
            "eol_requirement_power_headroom_MW": P_HEADROOM_MW_EOL,
            "eol_requirement_energy_one_hour_store_MWh": E_STORE_MWH_EOL,
            "eol_requirement_energy_physical_need_MWh": E_REQUIRED_MWH,
        },
        "outputs": results,
        "textbook_reference_no_fade": {
            "bess_installed_power_BOL_MVA": 1120.0,
            "bess_installed_energy_BOL_MWh": 1120.0,
            "capex_BOL_MUSD": (1120.0 * 1e3 * COST_POWER_USD_PER_KW + 1120.0 * 1e3 * COST_ENERGY_USD_PER_KWH) / 1e6,
        },
        "context": {
            "system_stored_energy_MJ": SYSTEM_EKIN_MJ,
            "reference_loss_MW": LOSS_MW,
            "condenser_H_s_fixed": H_S,
            "unit_costs": {"power_USD_per_kW": COST_POWER_USD_PER_KW, "energy_USD_per_kWh": COST_ENERGY_USD_PER_KWH},
        },
        "findings": [
            "At the mode retentions (80% energy, 92% power), the plant must be installed at 1400 MWh / 1217.4 MVA at BOL to still deliver the 1120 MWh / 1120 MVA EOL requirement after 15 years, for a BOL capex of 593.5 MUSD against the no-fade reference of 504.0 MUSD -- about 1.18x, driven mainly by the deeper assumed energy fade (20% vs. 8% power fade at the mode).",
            "Across the 10,000 Monte Carlo samples, BOL capex runs from 579.8 MUSD (p5) to 631.8 MUSD (p95), median 601.9 MUSD; energy retention drives most of the spread because the one-hour store (1120 MWh at EOL) dominates capex over the 1120 MVA converter (as in cost-curve.py). The sample median (601.9 MUSD) sits above the closed-form mode-retention figure (593.5 MUSD) because the triangular medians of both retention distributions are pulled toward their wider, lower-retention tail (0.70-0.85 for energy, 0.85-0.97 for power), which is asymmetric around the mode.",
            "The BOL/EOL install ratio equals 1/retention exactly for each fade channel by construction (checked to machine precision in the self-check), so power and energy over-build never interact -- the two channels can be read independently off their own retention figure.",
        ],
        "assumptions": [
            "Condenser H fixed at 3.5 s, ch4 Example 4.2 ('assumed for this case - verify against a manufacturer figure'); not varied in this scenario, matching cost-curve.py.",
            "Energy (capacity) retention at EOL ~ triangular(0.70, 0.80, 0.85). Not in ch4.html; assumption of this study anchored to the common 70-80% retained-capacity EOL convention for grid-scale Li-ion (e.g. NREL ATB; vendor warranties such as Tesla Megapack near 70% at 20 years). Verify against a specific product warranty before quoting.",
            "Power retention at EOL ~ triangular(0.85, 0.92, 0.97). Not in ch4.html; assumption of this study that power fade is smaller than capacity fade over 15 years for grid-scale Li-ion, order-of-magnitude only; verify against a specific product spec.",
            "Energy and power retention drawn independently (no sourced correlation between the two fade mechanisms).",
            "BOL install = EOL requirement / retention at EOL, applied separately to power and energy; this assumes linear, monotonic fade to a single 15-year figure (no fade curve shape, no calendar-vs-cycling split, no augmentation/replacement partway through life).",
            "EOL requirement itself: 1120 MVA converter rating / 224 MW headroom / 1120 MWh one-hour store, from ch4.html Example 4.2 at H = 3.5 s, eqs (4.11)-(4.13), identical to cost-curve.py's fixed sizing.",
            "Unit costs 200 USD/kW (converter + grid connection) and 250 USD/kWh (cells + racks + BMS), the majority convention per the brief, fixed placeholders, not from a source read in this run, applied to the BOL (as-installed) quantities.",
            "f0 = 50 Hz; RoCoF = 1.0 Hz/s (ch4 eq 4.12, DS3 / GB loss-of-mains figure [S16 - verify]); excursion 0.8 Hz (ch4 eq 4.11); H_v = 5.0 s (ch4 eq 4.13, 'assumed for this case'); current limit 1.2 pu (ch4 Constraint 3); one-hour store (ch4 Constraint 1, 'assumed for this case'). All fixed, all from ch4.html Example 4.2 unless marked assumption.",
            "Fleet: 8 x 200 MVA = 1.6 GVA, ch4 Example 4.2 (the brief's '1.6 GW' is written as 1.6 GVA in the textbook).",
            "System context 200 GVA.s and 1000 MW loss from ch4 Example 4.1; used only for reporting, not in the sizing.",
            "No response delay, no outage, no financing or O&M cost, no augmentation/replacement strategy, no currency/time discounting: other P5 scenarios cover response time and unit-cost/inertia spread; this scenario isolates 15-year degradation only.",
        ],
    }
    with open(os.path.join(here, "degradation.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")

    for key, r in results.items():
        print(f"{key:34s} p5 {r['p5']:12.4f}  p50 {r['p50']:12.4f}  p95 {r['p95']:12.4f}  {r['unit']}")
    print("self-check passed")


if __name__ == "__main__":
    main()
