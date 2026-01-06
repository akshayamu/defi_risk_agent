# Phase 2.2 — Governance Parameter Stress
# Explicit governance-driven parameter changes

GOVERNANCE_SHOCKS = [
    {
        "name": "baseline",
        "liquidation_threshold": 0.80
    },
    {
        "name": "minor_tightening",
        "liquidation_threshold": 0.78
    },
    {
        "name": "moderate_tightening",
        "liquidation_threshold": 0.75
    },
    {
        "name": "aggressive_tightening",
        "liquidation_threshold": 0.72
    }
]


from copy import deepcopy
from defi_risk_agent.stress.scenario_matrix import run_scenario_matrix
from defi_risk_agent.scoring.risk_surface import aggregate_risk_surface


def run_governance_stress(base_strategy: dict):
    """
    Apply governance-driven liquidation threshold changes
    to the same user position and measure risk surface shifts.
    """
    results = []

    for shock in GOVERNANCE_SHOCKS:
        strategy = deepcopy(base_strategy)

        # Apply governance change
        strategy["protocol"]["liquidation_threshold"] = shock["liquidation_threshold"]

        scenario_matrix = run_scenario_matrix(strategy)

        risk_surface = aggregate_risk_surface(
            scenario_matrix,
            shock["liquidation_threshold"]
        )

        results.append({
            "governance_scenario": shock["name"],
            "liquidation_threshold": shock["liquidation_threshold"],
            "risk_summary": risk_surface["summary"]
        })

    return results
