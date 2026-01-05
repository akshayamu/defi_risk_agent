import json
from pathlib import Path


# =========================================================
# Load report (READ-ONLY)
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = BASE_DIR / "reports" / "latest.json"

with open(REPORT_PATH, "r") as f:
    report = json.load(f)


# =========================================================
# Explanation helpers
# =========================================================

def explain_base_risk(base: dict) -> str:
    return (
        f"The current position has a loan-to-value (LTV) of "
        f"{base['current_ltv_pct']}%, against a liquidation threshold of "
        f"{base['liquidation_threshold_pct']}%. "
        f"This indicates the position is initially solvent but exposed to price declines."
    )


def explain_price_risk(price_shocks: list) -> str:
    for p in price_shocks:
        if p["liquidated"]:
            return (
                f"Liquidation first occurs at approximately a "
                f"{p['price_drop_pct']}% price drop, "
                f"indicating a relatively narrow safety margin."
            )
    return (
        "No liquidation was observed under the tested price shock scenarios, "
        "indicating strong resilience to direct price declines."
    )


def explain_volatility(volatility_regimes: list) -> str:
    risky = [r for r in volatility_regimes if r["liquidated"]]

    if not risky:
        return (
            "Across all tested volatility regimes, the position remains solvent, "
            "suggesting limited sensitivity to market turbulence."
        )

    first = risky[0]
    return (
        f"Under the '{first['regime']}' volatility regime, liquidation occurs "
        f"at an effective price drop of approximately "
        f"{first['effective_price_drop_pct']}%. "
        f"This shows that volatility materially amplifies liquidation risk."
    )


def explain_surface(summary: dict) -> str:
    zones = summary["zone_distribution"]

    return (
        f"Out of {summary['total_scenarios']} simulated scenarios, "
        f"{zones['SAFE']['pct']}% are classified as SAFE, "
        f"{zones['WARNING']['pct']}% fall into a WARNING zone, "
        f"and {zones['LIQUIDATED']['pct']}% result in liquidation. "
        f"This distribution highlights the balance between stability and tail risk."
    )


def explain_dominant_risk() -> str:
    return (
        "The dominant risk driver for this position is the interaction between "
        "leverage and market volatility. While moderate price declines are survivable "
        "in calm conditions, elevated volatility rapidly erodes the safety buffer "
        "and leads to liquidation."
    )


# =========================================================
# Generate explanation
# =========================================================

explanation = {
    "base_risk": explain_base_risk(report["base"]),
    "price_risk": explain_price_risk(report["price_shocks"]),
    "volatility_risk": explain_volatility(report["volatility_regimes"]),
    "risk_surface": explain_surface(report["risk_surface"]["summary"]),
    "dominant_risk_driver": explain_dominant_risk(),
}


# =========================================================
# Output (read-only narrative)
# =========================================================

for section, text in explanation.items():
    print(f"\n--- {section.replace('_', ' ').upper()} ---")
    print(text)
