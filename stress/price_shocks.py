from simulator import simulate_price_drop

def run_price_shocks(strategy: dict):
    drops = [0.10, 0.20, 0.30, 0.40, 0.50]

    position = strategy["position"]
    market = strategy["market"]
    protocol = strategy["protocol"]

    results = []

    for d in drops:
        results.append(
            simulate_price_drop(
                collateral_amount=position["collateral_amount"],
                price=market["collateral_price"],
                borrowed=position["borrowed_amount"],
                liquidation_threshold=protocol["liquidation_threshold"],
                drop_pct=d,
            )
        )

    return results
