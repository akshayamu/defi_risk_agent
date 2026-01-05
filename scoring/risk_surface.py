def classify_risk_zone(ltv_pct: float, liquidation_threshold_pct: float) -> str:
    """
    Classify a scenario into SAFE / WARNING / LIQUIDATED
    based on distance to liquidation threshold.
    """
    buffer = liquidation_threshold_pct - ltv_pct

    if buffer >= 10:
        return "SAFE"
    elif buffer >= 0:
        return "WARNING"
    else:
        return "LIQUIDATED"


def aggregate_risk_surface(
    scenario_matrix: list,
    liquidation_threshold: float
) -> dict:
    """
    Enrich scenario matrix with risk zones and aggregate statistics.
    """
    threshold_pct = liquidation_threshold * 100

    enriched = []
    zone_counts = {"SAFE": 0, "WARNING": 0, "LIQUIDATED": 0}

    for row in scenario_matrix:
        zone = classify_risk_zone(row["ltv_pct"], threshold_pct)

        enriched_row = {
            **row,
            "risk_zone": zone
        }

        enriched.append(enriched_row)
        zone_counts[zone] += 1

    total = len(enriched)

    summary = {
        "total_scenarios": total,
        "zone_distribution": {
            k: {
                "count": v,
                "pct": round(v / total * 100, 2)
            }
            for k, v in zone_counts.items()
        }
    }

    return {
        "enriched_matrix": enriched,
        "summary": summary
    }
