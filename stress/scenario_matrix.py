from itertools import product
from defi_risk_agent.simulator import compute_ltv

PRICE_SHOCKS = [0.10, 0.20, 0.30, 0.40, 0.50]
BORROW_MULTIPLIERS = [0.8, 1.0, 1.2]

VOLATILITY_REGIMES = {
    "calm": 0.7,
    "normal": 1.0,
    "turbulent": 1.5,
    "crisis": 2.0,
}

MAX_DROP_CAP = 0.95


def run_scenario_matrix(strategy: dict):
    position = strategy["position"]
    market = strategy["market"]
    protocol = strategy["protocol"]

    base_borrowed = position["borrowed_amount"]
    collateral_amount = position["collateral_amount"]
    price = market["collateral_price"]
    liquidation_threshold = protocol["liquidation_threshold"]

    results = []

    for price_shock, borrow_mult, (regime, vol_mult) in product(
        PRICE_SHOCKS, BORROW_MULTIPLIERS, VOLATILITY_REGIMES.items()
    ):
        borrowed = base_borrowed * borrow_mult
        effective_drop = min(price_shock * vol_mult, MAX_DROP_CAP)

        new_price = price * (1 - effective_drop)
        new_collateral_value = collateral_amount * new_price
        ltv = compute_ltv(borrowed, new_collateral_value)

        results.append({
            "price_shock_pct": round(price_shock * 100, 1),
            "borrow_multiplier": borrow_mult,
            "volatility_regime": regime,
            "volatility_multiplier": vol_mult,
            "effective_drop_pct": round(effective_drop * 100, 1),
            "ltv_pct": round(ltv * 100, 2),
            "liquidated": ltv > liquidation_threshold,
        })

    return results
