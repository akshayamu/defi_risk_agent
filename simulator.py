import yaml
from typing import Dict


# -----------------------------
# Load strategy configuration
# -----------------------------
def load_strategy(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


# -----------------------------
# Core financial logic
# -----------------------------
def compute_ltv(borrowed: float, collateral_value: float) -> float:
    return borrowed / collateral_value


def simulate_price_drop(
    collateral_amount: float,
    price: float,
    borrowed: float,
    liquidation_threshold: float,
    drop_pct: float,
) -> Dict:
    new_price = price * (1 - drop_pct)
    new_collateral_value = collateral_amount * new_price
    ltv = compute_ltv(borrowed, new_collateral_value)

    return {
        "price_drop_pct": drop_pct * 100,
        "new_price": round(new_price, 2),
        "ltv_pct": round(ltv * 100, 2),
        "liquidated": ltv > liquidation_threshold,
    }


# -----------------------------
# Risk report generation
# -----------------------------
def generate_risk_report(strategy: dict) -> Dict:
    collateral_amount = strategy["position"]["collateral_amount"]
    collateral_price = strategy["position"]["collateral_price"]
    borrowed = strategy["position"]["borrowed_amount"]
    liquidation_threshold = strategy["collateral"]["liquidation_threshold"]

    initial_value = collateral_amount * collateral_price
    initial_ltv = compute_ltv(borrowed, initial_value)

    scenarios = []
    liquidation_point = None

    for drop in [0.1, 0.2, 0.3, 0.4]:
        result = simulate_price_drop(
            collateral_amount,
            collateral_price,
            borrowed,
            liquidation_threshold,
            drop,
        )
        scenarios.append(result)

        if result["liquidated"] and liquidation_point is None:
            liquidation_point = result["price_drop_pct"]

    risk_level = (
        "LOW"
        if liquidation_point is None
        else "MEDIUM"
        if liquidation_point >= 30
        else "HIGH"
    )

    return {
        "protocol": strategy["protocol"],
        "current_ltv_pct": round(initial_ltv * 100, 2),
        "liquidation_threshold_pct": liquidation_threshold * 100,
        "liquidation_price_drop_pct": liquidation_point,
        "risk_level": risk_level,
        "stress_test_results": scenarios,
    }


def print_risk_report(report: Dict):
    print("\n=== Risk Report ===")
    print(f"Protocol: {report['protocol']}")
    print(f"Current LTV: {report['current_ltv_pct']}%")
    print(f"Liquidation Threshold: {report['liquidation_threshold_pct']}%")
    print(f"Risk Level: {report['risk_level']}")

    if report["liquidation_price_drop_pct"]:
        print(
            f"Liquidation occurs at ~{report['liquidation_price_drop_pct']}% price drop"
        )
    else:
        print("No liquidation observed in tested scenarios")

    print("\nStress Scenarios:")
    for s in report["stress_test_results"]:
        status = "LIQUIDATED" if s["liquidated"] else "SAFE"
        print(
            f"- {s['price_drop_pct']:>4.0f}% drop → "
            f"LTV {s['ltv_pct']:>6.2f}% → {status}"
        )


# -----------------------------
# Sensitivity analysis
# -----------------------------
def analyze_borrow_sensitivity(strategy: dict) -> Dict:
    collateral_amount = strategy["position"]["collateral_amount"]
    collateral_price = strategy["position"]["collateral_price"]
    liquidation_threshold = strategy["collateral"]["liquidation_threshold"]

    base_borrowed = strategy["position"]["borrowed_amount"]

    test_borrows = [
        base_borrowed * 0.7,
        base_borrowed * 0.8,
        base_borrowed,
        base_borrowed * 1.1,
    ]

    results = []

    for borrowed in test_borrows:
        collateral_value = collateral_amount * collateral_price
        ltv = compute_ltv(borrowed, collateral_value)

        results.append(
            {
                "borrowed_amount": round(borrowed, 2),
                "ltv_pct": round(ltv * 100, 2),
                "liquidation_buffer_pct": round(
                    (liquidation_threshold - ltv) * 100, 2
                ),
            }
        )

    return {
        "parameter": "borrowed_amount",
        "results": results,
    }


# -----------------------------
# Entry point
# -----------------------------
def main():
    strategy = load_strategy("strategy.yaml")

    report = generate_risk_report(strategy)
    print_risk_report(report)

    sensitivity = analyze_borrow_sensitivity(strategy)

    print("\n=== Sensitivity Analysis: Borrowed Amount ===")
    for r in sensitivity["results"]:
        print(
            f"- Borrowed ${r['borrowed_amount']:>8,.0f} → "
            f"LTV {r['ltv_pct']:>6.2f}% → "
            f"Buffer {r['liquidation_buffer_pct']:>6.2f}%"
        )


if __name__ == "__main__":
    main()
