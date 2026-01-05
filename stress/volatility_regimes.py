from defi_risk_agent.simulator import simulate_price_drop

VOLATILITY_REGIMES = {
    "calm": 0.7,
    "normal": 1.0,
    "turbulent": 1.5,
    "crisis": 2.0,
}

BASE_PRICE_DROP = 0.20  # 20%

def run_volatility_regime_stress(strategy: dict):
    position = strategy["position"]
    market = strategy["market"]
    protocol = strategy["protocol"]

    results = []

    for regime, multiplier in VOLATILITY_REGIMES.items():
        effective_drop = min(BASE_PRICE_DROP * multiplier, 0.95)

        outcome = simulate_price_drop(
            collateral_amount=position["collateral_amount"],
            price=market["collateral_price"],
            borrowed=position["borrowed_amount"],
            liquidation_threshold=protocol["liquidation_threshold"],
            drop_pct=effective_drop,
        )

        results.append({
            "regime": regime,
            "volatility_multiplier": multiplier,
            "effective_price_drop_pct": round(effective_drop * 100, 2),
            "ltv_pct": outcome["ltv_pct"],
            "liquidated": outcome["liquidated"],
        })

    return results
