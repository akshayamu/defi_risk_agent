from simulator import compute_ltv

def leverage_sensitivity(strategy: dict):
    borrowed_levels = [7000, 8000, 9000, 10000, 11000]

    position = strategy["position"]
    market = strategy["market"]
    protocol = strategy["protocol"]

    collateral_value = (
        position["collateral_amount"] * market["collateral_price"]
    )

    results = []

    for borrowed in borrowed_levels:
        ltv = compute_ltv(borrowed, collateral_value)
        buffer = protocol["liquidation_threshold"] - ltv

        results.append({
            "borrowed": borrowed,
            "ltv_pct": round(ltv * 100, 2),
            "safety_buffer_pct": round(buffer * 100, 2),
            "liquidated": ltv > protocol["liquidation_threshold"],
        })

    return results
