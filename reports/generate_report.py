import json
from simulator import load_strategy, generate_base_report
from stress.price_shocks import run_price_shocks
from stress.leverage_sensitivity import leverage_sensitivity
from stress.regime_matrix import regime_matrix
from scoring.risk_score import compute_risk_score

strategy = load_strategy("strategy.yaml")

base = generate_base_report(strategy)
price = run_price_shocks(strategy)
leverage = leverage_sensitivity(strategy)
regimes = regime_matrix(strategy)

liquidation_margin = 30
stress_survival = sum(not p["liquidated"] for p in price) / len(price)
avg_leverage_penalty = abs(leverage[-1]["safety_buffer_pct"])

risk_score = compute_risk_score(
    liquidation_margin,
    stress_survival,
    avg_leverage_penalty,
)

report = {
    "base": base,
    "price_shocks": price,
    "leverage_sensitivity": leverage,
    "regimes": regimes,
    "risk_score": risk_score,
}

with open("reports/latest.json", "w") as f:
    json.dump(report, f, indent=2)

print("Risk report generated.")
