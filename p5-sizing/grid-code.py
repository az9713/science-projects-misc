"""P5 sizing study, scenario "grid-code".

Case: a grid-forming battery (BESS) replaces a 1.6 GVA synchronous condenser
fleet for frequency response. Method and reference numbers: p1-textbook/ch4.html,
section 4.5, Example 4.2 (R39), equations (4.11) to (4.13). Same base model as
inertia-constant.py, so the two scenarios are comparable: condenser fleet
8 x 200 MVA = 1.6 GVA, f0 = 50 Hz, H_v = 5.0 s, one-hour store. There the
inertia constant H varied; here H is held at its textbook value (3.5 s) and
the varied uncertainty is which grid code sets the RoCoF withstand
requirement and the frequency-excursion requirement that size the BESS.

Varied uncertainty: "grid-code" - a categorical draw over six representative
grid codes, each fixing (RoCoF requirement Hz/s, frequency-excursion
requirement Hz). Values are illustrative, drawn from the public shape of
real grid-code requirements, not audited against the current in-force text
of each code - "assumption, verify against the current code" on every row.

Run:  python grid-code.py      (writes grid-code.json next to it)
"""
import json
import os

import numpy as np

SEED = 20260922
N_SAMPLES = 10_000

# ---------------------------------------------------------------- fixed inputs
# All from ch4.html Example 4.1 / 4.2 unless marked "assumption". Same values
# as inertia-constant.py so the two scenarios are comparable.
F0_HZ = 50.0            # nominal frequency, ch4 Example 4.1 and 4.2
N_UNITS = 8             # condensers in the fleet, ch4 Example 4.2
S_UNIT_MVA = 200.0      # rating per condenser, ch4 Example 4.2 (8 x 200 = 1.6 GVA)
S_FLEET_MVA = N_UNITS * S_UNIT_MVA
H_S = 3.5               # condenser inertia constant, ch4 Example 4.2 textbook value; held fixed here
H_V_S = 5.0             # virtual inertia constant of the grid-forming BESS, ch4 eq (4.13), "assumed for this case"
STORE_HOURS = 1.0       # one-hour store, ch4 Constraint 1, "assumed for this case"
SYSTEM_EKIN_MJ = 200_000.0  # 200 GVA.s system, ch4 Example 4.1 (context only: fleet share)
LOSS_MW = 1000.0            # 1000 MW loss, ch4 Example 4.1 (context only)

# Cost inputs: assumption, NOT read from any source in this run. Same
# placeholders as inertia-constant.py so capex is comparable across scenarios.
COST_POWER_USD_PER_KVA = 200.0   # grid-forming converter + grid connection, assumption
COST_ENERGY_USD_PER_KWH = 250.0  # cells + racks + BMS, assumption

# ------------------------------------------------------ the varied uncertainty
# Six representative grid codes, each fixing a RoCoF withstand/design
# requirement (Hz/s) and a frequency-excursion requirement (Hz) used to size
# the BESS's power (eq 4.12) and energy (eq 4.11) response. Equal-probability
# categorical draw (1/6 each): a simplification of this study, not a market-
# share weighting of where a BESS of this kind would actually be built.
#
#   name                 rocof_hz_s  df_hz   source / assumption
#   GB (NGESO)            1.0        0.8     GB Grid Code / EFCC frequency-response design point,
#                                            same as ch4 Example 4.2's textbook figures - reproduced exactly below.
#   Continental Europe     2.0        0.8     ENTSO-E RfG (EU 2016/631), Type A/B RoCoF withstand
#                                            up to 2 Hz/s over 500 ms - assumption, verify against the
#                                            current national implementation, which can be lower.
#   Nordic synchronous area 1.0       0.5     Nordic System Operation Agreement design RoCoF ~1 Hz/s and a
#                                            narrower excursion band than GB/island codes - assumption,
#                                            verify against the current Nordic Grid Code / SOA text.
#   Ireland & N. Ireland    1.0       1.0     EirGrid/SONI DS3 programme raised the RoCoF withstand
#                                            standard to 1.0 Hz/s; wider excursion reflects a small,
#                                            weakly-interconnected island system - assumption, verify.
#   Australia (NEM)         1.0       0.5     AEMO NER RoCoF standard, raised from 0.25 to 1.0 Hz/s after the
#                                            2016 South Australia black system event - assumption, verify
#                                            against the current NER version.
#   Generic weak island grid 2.0      1.0     Illustrative small/weak island system (no single named code;
#                                            shape informed by IEC/IEEE microgrid guidance), standing in for
#                                            a grid with little synchronous inertia and wide tolerances -
#                                            assumption, not read from a specific code.
GRID_CODES = [
    {"name": "GB (NGESO)",              "rocof_hz_s": 1.0, "df_hz": 0.8},
    {"name": "Continental Europe (ENTSO-E RfG)", "rocof_hz_s": 2.0, "df_hz": 0.8},
    {"name": "Nordic synchronous area", "rocof_hz_s": 1.0, "df_hz": 0.5},
    {"name": "Ireland & N. Ireland (DS3)", "rocof_hz_s": 1.0, "df_hz": 1.0},
    {"name": "Australia (AEMO NER)",    "rocof_hz_s": 1.0, "df_hz": 0.5},
    {"name": "Generic weak island grid", "rocof_hz_s": 2.0, "df_hz": 1.0},
]
CODE_NAMES = [c["name"] for c in GRID_CODES]
ROCOF_BY_CODE = np.array([c["rocof_hz_s"] for c in GRID_CODES])
DF_BY_CODE = np.array([c["df_hz"] for c in GRID_CODES])


def size_for_code(rocof_hz_s, df_hz):
    """Return the sizing outputs for a given (RoCoF, df) grid-code requirement
    (arrays or floats). H = 3.5 s and H_v = 5.0 s are held fixed."""
    ekin_fleet_mj = H_S * S_FLEET_MVA                                    # eq (4.4) on the fleet, MJ = MVA.s (fixed: 5600 MJ)
    e_released_mj = 2.0 * ekin_fleet_mj * df_hz / F0_HZ                  # eq (4.11)
    p_headroom_mw = 2.0 * ekin_fleet_mj * rocof_hz_s / F0_HZ             # eq (4.12)
    p_inertial_pu = 2.0 * H_V_S * rocof_hz_s / F0_HZ                     # eq (4.13); scales with the code's RoCoF too
    s_gfm_mva = p_headroom_mw / p_inertial_pu                            # fleet rating
    e_required_mwh = e_released_mj / 3600.0                              # physical energy need
    e_store_mwh = s_gfm_mva * STORE_HOURS                                # textbook one-hour store
    capex_usd = (s_gfm_mva * 1e3 * COST_POWER_USD_PER_KVA
                 + e_store_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    capex_power_only_usd = (s_gfm_mva * 1e3 * COST_POWER_USD_PER_KVA
                            + e_required_mwh * 1e3 * COST_ENERGY_USD_PER_KWH)
    return {
        "grid_code_rocof_hz_s": np.broadcast_to(rocof_hz_s, np.shape(e_released_mj)) if np.ndim(e_released_mj) else rocof_hz_s,
        "grid_code_df_hz": np.broadcast_to(df_hz, np.shape(e_released_mj)) if np.ndim(e_released_mj) else df_hz,
        "fleet_stored_energy_MJ": ekin_fleet_mj if np.ndim(e_released_mj) == 0 else np.full_like(e_released_mj, ekin_fleet_mj),
        "bess_power_headroom_MW": p_headroom_mw,
        "bess_converter_rating_MVA": s_gfm_mva,
        "bess_energy_required_MWh": e_required_mwh,
        "bess_energy_one_hour_store_MWh": e_store_mwh,
        "capex_one_hour_store_MUSD": capex_usd / 1e6,
        "capex_min_energy_MUSD": capex_power_only_usd / 1e6,
    }


UNITS = {
    "grid_code_rocof_hz_s": "Hz/s",
    "grid_code_df_hz": "Hz",
    "fleet_stored_energy_MJ": "MJ",
    "bess_power_headroom_MW": "MW",
    "bess_converter_rating_MVA": "MVA",
    "bess_energy_required_MWh": "MWh",
    "bess_energy_one_hour_store_MWh": "MWh",
    "capex_one_hour_store_MUSD": "million USD",
    "capex_min_energy_MUSD": "million USD",
}

MEANING = {
    "grid_code_rocof_hz_s": "sampled grid code's RoCoF withstand/design requirement (part of the input)",
    "grid_code_df_hz": "sampled grid code's frequency-excursion requirement (part of the input)",
    "fleet_stored_energy_MJ": "condenser fleet kinetic energy at fixed H=3.5s, H x 1600 MVA (does not vary with grid code)",
    "bess_power_headroom_MW": "power above dispatch at the sampled RoCoF, eq (4.12); the required BESS response power",
    "bess_converter_rating_MVA": "grid-forming converter rating at H_v 5.0 s, eq (4.13); pu headroom itself scales with RoCoF",
    "bess_energy_required_MWh": "energy released over the sampled frequency excursion, eq (4.11); the physical energy need",
    "bess_energy_one_hour_store_MWh": "store size under the textbook one-hour assumption (a design choice, not a requirement)",
    "capex_one_hour_store_MUSD": "capex with the one-hour store, fixed placeholder unit costs",
    "capex_min_energy_MUSD": "capex with the store sized to the physical energy need only",
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(GRID_CODES), size=N_SAMPLES)  # equal-probability categorical draw
    rocof = ROCOF_BY_CODE[idx]
    df = DF_BY_CODE[idx]
    out = size_for_code(rocof, df)

    # ------------------------------------------------------------ self-checks
    # 1. Textbook reproduction at the GB (NGESO) code: RoCoF 1.0 Hz/s, df 0.8 Hz,
    #    H = 3.5 s -> same numbers as ch4 Example 4.2 / inertia-constant.py.
    ref = size_for_code(1.0, 0.8)
    assert abs(ref["fleet_stored_energy_MJ"] - 5600.0) < 1e-9
    assert abs(ref["fleet_stored_energy_MJ"] * 2 * 0.8 / F0_HZ - 179.2) < 1e-9
    assert abs(ref["bess_power_headroom_MW"] - 224.0) < 1e-9
    assert abs(ref["bess_converter_rating_MVA"] - 1120.0) < 1e-9
    assert abs(ref["bess_energy_one_hour_store_MWh"] - 1120.0) < 1e-9
    assert abs(ref["bess_energy_required_MWh"] - 179.2 / 3600.0) < 1e-12
    # 2. Sample count and category membership.
    assert rocof.size == N_SAMPLES == 10_000
    assert set(np.unique(idx)) <= set(range(len(GRID_CODES)))
    # 3. Each of the 6 codes drawn close to 1/6 of samples (equal-probability draw).
    counts = np.bincount(idx, minlength=len(GRID_CODES))
    assert np.all(np.abs(counts / N_SAMPLES - 1.0 / len(GRID_CODES)) < 0.02)
    # 4. bess_converter_rating_MVA depends only on df/rocof ratio (H_v pu term
    #    scales with rocof and cancels it out of the converter rating):
    #    S = p_headroom / p_inertial_pu = (2*Ekin*rocof/f0) / (2*H_v*rocof/f0)
    #      = Ekin / H_v  -> constant, independent of the grid code.
    assert np.allclose(out["bess_converter_rating_MVA"], 5600.0 / H_V_S)
    # 5. Physical energy need scales only with df (not with RoCoF).
    assert np.allclose(out["bess_energy_required_MWh"], 2 * 5600.0 * df / F0_HZ / 3600.0)
    # 6. Highest-severity code (Continental Europe or generic weak island,
    #    both RoCoF 2.0) gives double the GB power headroom.
    p_gb = size_for_code(1.0, 0.8)["bess_power_headroom_MW"]
    p_high = size_for_code(2.0, 0.8)["bess_power_headroom_MW"]
    assert abs(p_high - 2 * p_gb) < 1e-9

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
    # 7. Converter rating is the same at every percentile (constant, see check 4).
    assert abs(results["bess_converter_rating_MVA"]["p5"] - results["bess_converter_rating_MVA"]["p95"]) < 1e-6

    doc = {
        "scenario": "grid-code",
        "case": "grid-forming BESS replacing a 1.6 GVA synchronous condenser fleet for frequency response",
        "source_method": "p1-textbook/ch4.html section 4.5, Example 4.2 (R39), eqs (4.11)-(4.13); same base model as inertia-constant.py",
        "n_samples": N_SAMPLES,
        "seed": SEED,
        "varied_uncertainty": {
            "name": "grid code (sets the RoCoF withstand requirement and the frequency-excursion requirement)",
            "distribution": "categorical, 6 codes, equal probability 1/6 each",
            "categories": [
                {"name": c["name"], "rocof_hz_s": c["rocof_hz_s"], "df_hz": c["df_hz"]}
                for c in GRID_CODES
            ],
            "source": "illustrative values shaped on the public RoCoF/excursion figures of GB Grid Code/EFCC, ENTSO-E RfG (EU 2016/631) Type A/B, the Nordic System Operation Agreement, EirGrid/SONI DS3, AEMO NER, and a generic weak-island grid; not audited against the current in-force text of any of them - verify before quoting a specific jurisdiction",
        },
        "outputs": results,
        "textbook_reference_GB_code": {
            "fleet_stored_energy_MJ": 5600.0,
            "energy_released_0p8Hz_MJ": 179.2,
            "bess_power_headroom_MW": 224.0,
            "bess_converter_rating_MVA": 1120.0,
            "bess_energy_one_hour_store_MWh": 1120.0,
        },
        "context": {
            "system_stored_energy_MJ": SYSTEM_EKIN_MJ,
            "reference_loss_MW": LOSS_MW,
            "fleet_share_of_system_inertia_pct": round(5600.0 / SYSTEM_EKIN_MJ * 100, 4),
        },
        "findings": [
            "Required BESS power headroom scales 1:1 with the grid code's RoCoF requirement: GB and the two Australia/Nordic-style codes at 1.0 Hz/s give 224 MW; Continental Europe and the generic weak-island code at 2.0 Hz/s give 448 MW, exactly double.",
            "The converter rating (MVA) does NOT vary with the grid code in this model: it comes out to a constant 1120 MVA (=5600 MJ fleet energy / H_v 5.0 s) at every RoCoF, because the eq (4.13) headroom fraction scales with RoCoF the same way the power need does, cancelling RoCoF out of the ratio. Only the physical energy need and, through it, the one-hour store MWh vary, and only with the frequency-excursion requirement (df), not with RoCoF.",
            "Physical energy need ranges from 0.031 MWh (df 0.5 Hz: Nordic, Australia) to 0.062 MWh (df 1.0 Hz: Ireland/N. Ireland, generic weak island) - all far below the one-hour store size, so the one-hour store choice, not the grid code, still sets the energy rating.",
            "Capex with a one-hour store tracks the power headroom, so it doubles between the 1.0 Hz/s and 2.0 Hz/s RoCoF codes; the placeholder unit costs are not sourced.",
        ],
        "assumptions": [
            "Grid code ~ categorical over 6 representative codes, equal probability 1/6 each (a simplification of this study, not a market-share weighting): GB (NGESO) RoCoF 1.0 Hz/s, df 0.8 Hz; Continental Europe (ENTSO-E RfG) RoCoF 2.0 Hz/s, df 0.8 Hz; Nordic synchronous area RoCoF 1.0 Hz/s, df 0.5 Hz; Ireland & N. Ireland (DS3) RoCoF 1.0 Hz/s, df 1.0 Hz; Australia (AEMO NER) RoCoF 1.0 Hz/s, df 0.5 Hz; generic weak island grid RoCoF 2.0 Hz/s, df 1.0 Hz. All six rows are illustrative, shaped on public information about each regime, and not audited against the current in-force text - verify against the current code before quoting a specific jurisdiction.",
            "Condenser inertia constant H = 3.5 s, held fixed at the ch4 Example 4.2 textbook value ('assumed for this case - verify against a manufacturer figure'); the companion inertia-constant.py scenario varies H instead and holds the grid code fixed at GB.",
            "Fleet: 8 x 200 MVA = 1.6 GVA, ch4 Example 4.2 (the brief's '1.6 GW' is written as 1.6 GVA in the textbook).",
            "f0 = 50 Hz, ch4 Examples 4.1 and 4.2.",
            "BESS virtual inertia constant H_v = 5.0 s, ch4 eq (4.13), 'assumed for this case'; fixed across all grid codes.",
            "Terminal voltage 1.0 pu, unity power factor, current limit 1.2 pu at 1.0 pu dispatch, ch4 Constraint 3; converter rating = headroom / pu headroom fraction.",
            "One-hour store (MWh = MVA rating x 1 h), ch4 Constraint 1, 'assumed for this case'; reported separately from the physical energy need.",
            "Unit costs 200 USD/kVA (converter + connection) and 250 USD/kWh (energy), fixed placeholders, not from a source read in this run; the cost-curve scenario owns cost uncertainty.",
            "System context 200 GVA.s and 1000 MW loss from ch4 Example 4.1; used only for the fleet-share figure, not in the sizing.",
            "No current limiting beyond the 1.2 pu cap, no response delay, no degradation, no outage: other P5 scenarios cover those.",
        ],
    }
    with open(os.path.join(here, "grid-code.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")

    for key, r in results.items():
        print(f"{key:34s} p5 {r['p5']:12.4f}  p50 {r['p50']:12.4f}  p95 {r['p95']:12.4f}  {r['unit']}")
    print("self-check passed")


if __name__ == "__main__":
    main()
