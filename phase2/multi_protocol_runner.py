from copy import deepcopy

from defi_risk_agent.phase2.protocols import PROTOCOLS
from defi_risk_agent.stress.scenario_matrix import run_scenario_matrix
from defi_risk_agent.scoring.risk_surface import aggregate_risk_surface


def run_multi_protocol_analysis(base_strategy: dict):
    results = []

    for protocol in PROTOCOLS:
        strategy = deepcopy(base_strategy)
        strategy["protocol"] = protocol

        scenario_matrix = run_scenario_matrix(strategy)

        risk_surface = aggregate_risk_surface(
            scenario_matrix,
            protocol["liquidation_threshold"]
        )

        results.append({
            "protocol": protocol["name"],
            "liquidation_threshold": protocol["liquidation_threshold"],
            "summary": risk_surface["summary"]
        })

    return results
