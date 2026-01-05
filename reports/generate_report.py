import json
from pathlib import Path

from defi_risk_agent.simulator import load_strategy, generate_base_report
from defi_risk_agent.stress.price_shocks import run_price_shocks
from defi_risk_agent.stress.leverage_sensitivity import leverage_sensitivity
from defi_risk_agent.stress.regime_matrix import regime_matrix
from defi_risk_agent.stress.volatility_regimes import run_volatility_regime_stress
from defi_risk_agent.stress.scenario_matrix import run_scenario_matrix
from defi_risk_agent.scoring.risk_score import compute_risk_score
from defi_risk_agent.scoring.risk_surface import aggregate_risk_surface


# =========================================================
# Load strategy
# =========================================================

strategy = load_strategy("strategy.yaml")


# =========================================================
# Run analyses (Steps 0–12)
# =========================================================

base = generate_base_report(strategy)
price = run_price_shocks(strategy)
leverage = leverage_sensitivity(strategy)
regimes = regime_matrix(strategy)
volatility_regimes = run_volatility_regime_stress(strategy)
scenario_matrix = run_scenario_matrix(strategy)


# =========================================================
# Step 13 — Risk surface aggregation
# =========================================================

risk_surface = aggregate_risk_surface(
    scenario_matrix,
    strategy["protocol"]["liquidation_threshold"]
)


# =========================================================
# Risk score (summary scalar)
# =========================================================

liquidation_margin = 30
stress_survival = sum(not p["liquidated"] for p in price) / len(price)
avg_leverage_penalty = abs(leverage[-1]["safety_buffer_pct"])

risk_score = compute_risk_score(
    liquidation_margin,
    stress_survival,
    avg_leverage_penalty,
)


# =========================================================
# Assemble final report
# =========================================================

report = {
    "base": base,
    "price_shocks": price,
    "leverage_sensitivity": leverage,
    "regimes": regimes,
    "volatility_regimes": volatility_regimes,
    "scenario_matrix": scenario_matrix,
    "risk_surface": risk_surface,
    "risk_score": risk_score
}


# =========================================================
# Write output (package-relative)
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "latest.json"

with open(OUTPUT_PATH, "w") as f:
    json.dump(report, f, indent=2)

print("Risk report generated.")
