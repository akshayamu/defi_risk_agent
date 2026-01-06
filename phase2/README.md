# Phase 2 — Protocol, Governance, and Strategy Risk

Phase 2 extends the deterministic DeFi risk engine built in Phase 1.
The goal is to move beyond single-position risk and analyze how
**protocol design**, **governance decisions**, and **user strategies**
shape liquidation outcomes.

This phase remains fully deterministic, simulation-first, and explainable.

No ML. No randomness. No blockchain calls.

---

## Scope of Phase 2

Phase 2 answers three distinct questions:

1. How does the **same user position** behave across different protocol designs?
2. How do **governance parameter changes** affect users already in position?
3. Which **leverage strategies** are robust versus fragile under stress?

Each question is isolated into a clean sub-phase.

---

## Phase 2.1 — Multi-Protocol Modeling

**Question:**  
How does protocol design affect user liquidation risk?

**Method:**  
- Same position
- Same market
- Same stress scenarios
- Different liquidation thresholds

**Insight:**  
Protocol rules materially change the size of SAFE, WARNING, and LIQUIDATED regions.
Risk is not only experienced by users — it is designed by protocols.

---

## Phase 2.2 — Governance Parameter Stress

**Question:**  
What happens when governance tightens liquidation rules after users are positioned?

**Method:**  
- Fix user and market
- Apply deterministic liquidation threshold changes
- Recompute full risk surface

**Insight:**  
Even without price movement, governance decisions can push large portions of user
states from SAFE into LIQUIDATED.

Governance risk is real, immediate, and measurable.

---

## Phase 2.3 — Strategy Comparison

**Question:**  
Which leverage strategies are robust under worst-case conditions?

**Method:**  
- Fix protocol and governance
- Compare conservative, moderate, and aggressive leverage strategies
- Measure dominance and fragility across identical stress grids

**Insight:**  
Higher leverage consistently collapses the SAFE region and expands liquidation risk.
User decisions dominate outcomes even under the same protocol.

---

## Design Principles (Unchanged from Phase 1)

- Deterministic simulations only
- Explicit assumptions
- Pure functions
- Single source of truth
- Read-only analysis layers

Each sub-phase is isolated and frozen once validated.

---

## Status

✔ Phase 2.1 — Complete  
✔ Phase 2.2 — Complete  
✔ Phase 2.3 — Complete  

**Phase 2 is fully complete and frozen.**

---

## Disclaimer

This project is for research and educational purposes only.
It does not constitute financial advice.
