"""P5 sizing study, scenario "outage-rate".

Case: a grid-forming battery fleet (BESS) replaces the 1.6 GVA synchronous
condenser fleet of p1-textbook/ch4.html, Example 4.2, for frequency response.

Varied uncertainty: the FORCED OUTAGE RATE (FOR) of one BESS block, that is,
the probability that a block is unavailable at the instant of a disturbance.
This is the only stochastic input. Every other input is fixed at the value in
ch4.html so that this scenario is comparable with the other P5 scenarios.

Alternative reading NOT modelled here: "outage rate" as the rate of
loss-of-infeed events per year. That rate changes cycling and throughput, not
the MW headroom, so it does not change the installed rating in this model.

Method (one sample):
  1. Draw FOR q from the distribution below.
  2. Find the smallest number of blocks n such that
         P(at least N_REQ of n blocks are available) >= RELIABILITY_TARGET,
     with block outages independent Bernoulli(q). The block-state randomness
     is integrated exactly with the binomial tail, so only q is sampled.
  3. Installed power = n * BLOCK_MVA (unity power factor, so MVA = MW).
     Installed energy = installed power * STORE_HOURS.
     Cost = power * $/kW + energy * $/kWh (fixed unit costs).

Run:  python outage-rate.py   (writes outage-rate.json next to this file)
Only the Python standard library is used. Output text is ASCII only.
"""

import json
import math
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixed inputs from p1-textbook/ch4.html (Example 4.2 unless stated)
# ---------------------------------------------------------------------------
F0_HZ = 50.0                 # nominal frequency, ch4 Example 4.1/4.2
N_CONDENSERS = 8             # ch4 Example 4.2: 8 condensers ...
CONDENSER_MVA = 200.0        # ... of 200 MVA each = 1.6 GVA
H_CONDENSER_S = 3.5          # ch4 Example 4.2, "assumed for this case - verify"
DELTA_F_HZ = 0.8             # ch4 Example 4.2, excursion for Constraint 1
ROCOF_DESIGN_HZ_S = 1.0      # ch4 Example 4.2, design RoCoF (DS3 / GB LoM figure)
H_V_S = 5.0                  # ch4 Example 4.2, virtual inertia constant, assumed
I_MAX_PU = 1.2               # ch4 Example 4.2, converter current limit, assumed
STORE_HOURS = 1.0            # ch4 Example 4.2, "a one-hour store", assumed

# Reference context from ch4 Example 4.1. NOT an input to the sizing: the
# 224 MW headroom is set at the design RoCoF of 1 Hz/s, not at the 0.125 Hz/s
# that this event gives. Used only in a self-check.
REF_LOSS_MW = 1000.0         # ch4 Example 4.1, loss of infeed
REF_E_KIN_SYS_MJ = 200000.0  # ch4 Example 4.1, 200 GVA.s, "verify"

# Derived deterministic quantities (ch4 eq. 4.4, 4.11, 4.12, 4.13)
E_KIN_FLEET_MJ = N_CONDENSERS * CONDENSER_MVA * H_CONDENSER_S          # 5600 MJ
E_RELEASED_MJ = 2.0 * E_KIN_FLEET_MJ * DELTA_F_HZ / F0_HZ              # 179.2 MJ
E_RELEASED_MWH = E_RELEASED_MJ / 3600.0                                # 0.0498 MWh
P_HEADROOM_MW = 2.0 * E_KIN_FLEET_MJ * ROCOF_DESIGN_HZ_S / F0_HZ       # 224 MW
P_INERTIAL_PU = 2.0 * H_V_S * ROCOF_DESIGN_HZ_S / F0_HZ                # 0.20 pu
S_REQ_MVA = P_HEADROOM_MW / P_INERTIAL_PU                              # 1120 MVA
REF_ROCOF0_HZ_S = F0_HZ * REF_LOSS_MW / (2.0 * REF_E_KIN_SYS_MJ)       # 0.125 Hz/s

# ---------------------------------------------------------------------------
# Model assumptions of this scenario (not from ch4; all "assumed - verify")
# ---------------------------------------------------------------------------
BLOCK_MVA = 40.0             # assumed block size; 1120/40 = 28 blocks exactly
N_REQ = int(round(S_REQ_MVA / BLOCK_MVA))                              # 28 blocks
RELIABILITY_TARGET = 0.999   # assumed: P(available >= 1120 MVA) at a random instant
# Uncertain input: FOR q ~ Beta(A, B). Mean A/(A+B) = 0.04, sd about 0.0195,
# central 90% about 0.013 to 0.077. ASSUMPTION: chosen to span a block
# availability of roughly 92% to 99%. It is not read from a published
# availability dataset. Verify against operator data (e.g. NERC GADS or
# vendor availability guarantees) before quoting.
FOR_BETA_A = 4.0
FOR_BETA_B = 96.0
# Unit costs, FIXED (not sampled, so only the outage rate varies).
# ASSUMPTION: order of recent utility-scale BESS estimates, with a premium for
# grid-forming converters. Not read from a source. Verify (e.g. NREL ATB).
COST_USD_PER_KW = 250.0      # power-related (converter, grid connection)
COST_USD_PER_KWH = 300.0     # energy-related (cells, racks, BoP)

N_SAMPLES = 10000
SEED = 20260922
N_SEARCH_MAX = 200           # hard cap on blocks searched per sample


def prob_at_least(k_req, n, p_avail):
    """P(X >= k_req) for X ~ Binomial(n, p_avail). Exact sum, n <= 200."""
    total = 0.0
    q = 1.0 - p_avail
    for k in range(k_req, n + 1):
        total += math.comb(n, k) * p_avail ** k * q ** (n - k)
    return total


def blocks_needed(q):
    """Smallest n >= N_REQ with P(avail blocks >= N_REQ) >= RELIABILITY_TARGET."""
    for n in range(N_REQ, N_SEARCH_MAX + 1):
        if prob_at_least(N_REQ, n, 1.0 - q) >= RELIABILITY_TARGET:
            return n
    raise RuntimeError("no block count up to %d meets the target at FOR=%.4f"
                       % (N_SEARCH_MAX, q))


def percentile(sorted_vals, pct):
    """Linear interpolation between closest ranks (numpy 'linear' method)."""
    pos = (len(sorted_vals) - 1) * pct / 100.0
    lo = math.floor(pos)
    hi = math.ceil(pos)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def run(seed=SEED, n_samples=N_SAMPLES):
    rng = random.Random(seed)
    cache = {}
    rows = {"for": [], "n_blocks": [], "power_mw": [], "energy_mwh": [],
            "cost_musd": []}
    for _ in range(n_samples):
        q = rng.betavariate(FOR_BETA_A, FOR_BETA_B)
        # n is a step function of q; cache on q rounded to 1e-6 is exact
        # enough and only speeds the run (the search is monotone in q).
        key = round(q, 6)
        if key not in cache:
            cache[key] = blocks_needed(q)
        n = cache[key]
        power = n * BLOCK_MVA                       # MW at unity power factor
        energy = power * STORE_HOURS                # MWh
        cost = (power * 1000.0 * COST_USD_PER_KW
                + energy * 1000.0 * COST_USD_PER_KWH) / 1e6
        rows["for"].append(q)
        rows["n_blocks"].append(n)
        rows["power_mw"].append(power)
        rows["energy_mwh"].append(energy)
        rows["cost_musd"].append(cost)
    return rows


def summarize(vals):
    s = sorted(vals)
    return {"p5": percentile(s, 5), "p50": percentile(s, 50),
            "p95": percentile(s, 95)}


def self_check(rows, rows_again):
    # Deterministic re-derivation of the ch4 numbers
    assert abs(E_KIN_FLEET_MJ - 5600.0) < 1e-9
    assert abs(E_RELEASED_MJ - 179.2) < 1e-9
    assert abs(P_HEADROOM_MW - 224.0) < 1e-9
    assert abs(P_INERTIAL_PU - 0.20) < 1e-12
    assert abs(S_REQ_MVA - 1120.0) < 1e-9
    assert abs(REF_ROCOF0_HZ_S - 0.125) < 1e-12
    assert abs(S_REQ_MVA * H_V_S - E_KIN_FLEET_MJ) < 1e-9   # H*S matched
    assert abs(I_MAX_PU - 1.0 - P_INERTIAL_PU) < 1e-12      # 0.00 pu margin
    assert N_REQ * BLOCK_MVA == S_REQ_MVA
    # Limit cases of the reliability search
    assert blocks_needed(0.0) == N_REQ
    assert blocks_needed(0.01) <= blocks_needed(0.05) <= blocks_needed(0.10)
    # Sample shape and reproducibility
    assert all(len(v) == N_SAMPLES for v in rows.values())
    assert rows == rows_again, "same seed must give identical samples"
    assert all(0.0 < q < 1.0 for q in rows["for"])
    assert min(rows["power_mw"]) >= S_REQ_MVA
    # Monotone: a higher FOR never needs fewer blocks
    pairs = sorted(zip(rows["for"], rows["n_blocks"]))
    assert all(pairs[i][1] <= pairs[i + 1][1] for i in range(len(pairs) - 1))
    # Stored energy is not binding (ch4 Constraint 1)
    assert min(rows["energy_mwh"]) > 1000.0 * E_RELEASED_MWH
    for key in ("for", "power_mw", "energy_mwh", "cost_musd"):
        st = summarize(rows[key])
        assert st["p5"] <= st["p50"] <= st["p95"], key
    # Sample mean FOR close to the Beta mean A/(A+B)
    mean_q = sum(rows["for"]) / N_SAMPLES
    assert abs(mean_q - FOR_BETA_A / (FOR_BETA_A + FOR_BETA_B)) < 0.002


def main():
    rows = run()
    rows_again = run()
    self_check(rows, rows_again)

    out = {
        "scenario": "outage-rate",
        "varied_uncertainty": "forced outage rate (FOR) of one BESS block",
        "n_samples": N_SAMPLES,
        "seed": SEED,
        "percentile_method": "sorted samples, linear interpolation between "
                             "closest ranks (numpy 'linear')",
        "outputs": {
            "forced_outage_rate": summarize(rows["for"]),
            "bess_power_mw": summarize(rows["power_mw"]),
            "bess_energy_mwh": summarize(rows["energy_mwh"]),
            "bess_cost_musd": summarize(rows["cost_musd"]),
            "n_blocks": summarize(rows["n_blocks"]),
        },
        "deterministic_reference": {
            "condenser_fleet_stored_energy_mj": E_KIN_FLEET_MJ,
            "energy_released_0p8hz_mj": E_RELEASED_MJ,
            "energy_released_0p8hz_mwh": round(E_RELEASED_MWH, 6),
            "power_headroom_at_1hz_per_s_mw": P_HEADROOM_MW,
            "converter_inertial_pu_at_hv5": P_INERTIAL_PU,
            "required_available_rating_mva": S_REQ_MVA,
            "bess_power_mw_at_for_zero": N_REQ * BLOCK_MVA,
            "bess_energy_mwh_at_for_zero": N_REQ * BLOCK_MVA * STORE_HOURS,
        },
        "reference_context_not_inputs": {
            "loss_of_infeed_mw": REF_LOSS_MW,
            "system_stored_energy_gva_s": REF_E_KIN_SYS_MJ / 1000.0,
            "rocof0_hz_per_s": REF_ROCOF0_HZ_S,
            "note": "ch4 Example 4.1 event. The 224 MW headroom uses the "
                    "1 Hz/s design RoCoF, not this 0.125 Hz/s.",
        },
        "assumptions": [
            "Only the block forced outage rate is sampled; all other inputs "
            "are fixed at p1-textbook/ch4.html Example 4.2 values.",
            "FOR ~ Beta(4, 96): mean 0.04, central 90% about 0.013 to 0.077. "
            "Assumed, not read from a dataset - verify.",
            "Block outages are independent Bernoulli(FOR); no common-mode "
            "failure (control software, grid connection, site event). "
            "Common-mode outages would raise the required rating.",
            "Sizing criterion: P(available rating >= 1120 MVA) >= 0.999 at "
            "the instant of a disturbance. Target assumed - verify.",
            "Block size 40 MVA, 40 MWh (1120 MVA = 28 blocks). Assumed.",
            "Required available rating 1120 MVA = 224 MW / 0.20 pu, from "
            "2*5600 MJ*1 Hz/s/50 Hz and H_v = 5.0 s (ch4 eq. 4.12, 4.13).",
            "Unity power factor and 1.0 pu terminal voltage, so MVA = MW "
            "(ch4 Example 4.2, Constraint 3).",
            "One-hour store per block, so MWh = MW x 1 h (ch4 Example 4.2 "
            "assumption). Energy is set by this duration, not by the "
            "179.2 MJ (0.0498 MWh) inertial release, which does not bind.",
            "Current limit 1.2 pu at 1.0 pu dispatch leaves 0.00 pu margin "
            "(ch4 Constraint 3); this model does not add rating for voltage "
            "support or fault current.",
            "Cost = MW x 250 USD/kW + MWh x 300 USD/kWh, fixed. Assumed, not "
            "read from a source - verify (e.g. NREL ATB). Excludes O&M, "
            "degradation, land, financing.",
            "Condenser fleet availability is not credited: the target is the "
            "full 224 MW headroom, not the condensers' availability-weighted "
            "headroom.",
        ],
    }
    path = Path(__file__).resolve().parent / "outage-rate.json"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    o = out["outputs"]
    for key in ("forced_outage_rate", "bess_power_mw", "bess_energy_mwh",
                "bess_cost_musd", "n_blocks"):
        print("%-20s p5=%10.4f p50=%10.4f p95=%10.4f"
              % (key, o[key]["p5"], o[key]["p50"], o[key]["p95"]))
    print("self-check passed; wrote %s" % path)


if __name__ == "__main__":
    main()
