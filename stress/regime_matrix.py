def regime_matrix(strategy: dict):
    regimes = {
        "low": 0.15,
        "medium": 0.30,
        "high": 0.50,
    }

    borrowed = strategy["position"]["borrowed_amount"]
    collateral_value = (
        strategy["position"]["collateral_amount"]
        * strategy["market"]["collateral_price"]
    )

    results = {}

    for name, drop in regimes.items():
        ltv = borrowed / (collateral_value * (1 - drop))
        results[name] = {
            "assumed_drop_pct": drop * 100,
            "ltv_pct": round(ltv * 100, 2),
            "liquidated": ltv > strategy["protocol"]["liquidation_threshold"],
        }

    return results
