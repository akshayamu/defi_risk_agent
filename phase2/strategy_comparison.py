# Phase 2.3 — Strategy Comparison
# Compare user leverage strategies under identical conditions

STRATEGY_VARIANTS = [
    {
        "name": "conservative",
        "borrow_multiplier": 0.60
    },
    {
        "name": "moderate",
        "borrow_multiplier": 0.75
    },
    {
        "name": "aggressive",
        "borrow_multiplier": 0.90
    }
]

from copy import deepcopy

from defi_risk_agent.stress.scenario_matrix import run_scenario_matrix
from defi_risk_agent.scoring.risk_surface import aggregate_risk_surface


def run_strategy_comparison(
    base_strategy: dict,
    liquidation_threshold: float,
):
    """
    Compare leverage strategies under identical conditions.
    Only borrowed amount changes; everything else is fixed.
    """
    results = []

    base_borrowed = base_strategy["position"]["borrowed_amount"]

    for variant in STRATEGY_VARIANTS:
        strategy = deepcopy(base_strategy)

        # Apply strategy choice (user decision)
        strategy["position"]["borrowed_amount"] = (
            base_borrowed * variant["borrow_multiplier"]
        )

        # Keep protocol rule fixed
        strategy["protocol"]["liquidation_threshold"] = liquidation_threshold

        scenario_matrix = run_scenario_matrix(strategy)

        risk_surface = aggregate_risk_surface(
            scenario_matrix,
            liquidation_threshold
        )

        results.append({
            "strategy": variant["name"],
            "borrow_multiplier": variant["borrow_multiplier"],
            "risk_summary": risk_surface["summary"]
        })

    return results
