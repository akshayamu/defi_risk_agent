def compute_risk_score(
    liquidation_margin_pct: float,
    stress_survival_ratio: float,
    leverage_sensitivity_pct: float,
):
    score = 100

    score -= max(0, 30 - liquidation_margin_pct)
    score -= (1 - stress_survival_ratio) * 40
    score -= leverage_sensitivity_pct * 0.3

    return round(max(score, 0), 2)
