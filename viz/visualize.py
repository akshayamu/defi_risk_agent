import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# =========================================================
# Load data (read-only)
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = BASE_DIR / "reports" / "latest.json"

with open(REPORT_PATH, "r") as f:
    report = json.load(f)

matrix = report["risk_surface"]["enriched_matrix"]
threshold_pct = report["base"]["liquidation_threshold_pct"]


df = pd.DataFrame(matrix)


# =========================================================
# Helper: map risk zone to numeric for heatmap
# =========================================================

ZONE_MAP = {"SAFE": 0, "WARNING": 1, "LIQUIDATED": 2}
df["zone_num"] = df["risk_zone"].map(ZONE_MAP)


# =========================================================
# 1. Heatmaps (one per volatility regime)
# =========================================================

for regime in df["volatility_regime"].unique():
    subset = df[df["volatility_regime"] == regime]

    pivot = subset.pivot(
        index="price_shock_pct",
        columns="borrow_multiplier",
        values="zone_num",
    )

    plt.figure()
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(ticks=[0, 1, 2])
    plt.clim(0, 2)

    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)

    plt.xlabel("Borrow Multiplier")
    plt.ylabel("Price Shock (%)")
    plt.title(f"Risk Heatmap — {regime.capitalize()} Regime")

    plt.show()


# =========================================================
# 2. Cliff plot (LTV vs effective drop)
# =========================================================

plt.figure()

for regime in df["volatility_regime"].unique():
    subset = df[df["volatility_regime"] == regime]
    plt.plot(
        subset["effective_drop_pct"],
        subset["ltv_pct"],
        marker="o",
        linestyle="",
        label=regime,
    )

plt.axhline(
    y=threshold_pct,
    linestyle="--",
    label="Liquidation Threshold",
)

plt.xlabel("Effective Price Drop (%)")
plt.ylabel("LTV (%)")
plt.title("Liquidation Cliff")
plt.legend()

plt.show()
