# DeFi Risk Agent (v0)

A **read-only, simulation-first engine** for analyzing DeFi strategy risk and parameter sensitivity.

This project focuses on understanding *how and why* DeFi positions fail under stress, rather than executing trades or optimizing yield.

---

## Why This Exists

Many DeFi losses occur not because smart contracts are incorrect, but because **risk parameters interact poorly under adverse conditions**.

Dashboards often show current metrics (e.g., LTV), but fail to answer:
- What happens under sudden price shocks?
- How sensitive is this position to leverage changes?
- Which parameter actually drives liquidation risk?

This project addresses those questions through deterministic simulation.

---

## Design Principles

- **Read-only by default**  
  No execution, no wallet access, no contract changes.

- **Simulation before advice**  
  No recommendations without stress testing.

- **Deterministic and auditable**  
  No black-box logic. All outputs are reproducible.

- **Advisory, not autonomous**  
  The system explains risk; it does not act.

---

## What the System Does (v0)

Given a DeFi strategy configuration, the system:

1. Computes core risk metrics (collateral value, LTV)
2. Simulates price shock scenarios
3. Identifies liquidation boundaries
4. Performs parameter sensitivity analysis
5. Identifies the dominant risk driver
6. Produces a structured risk report

---

## What the System Does NOT Do

- ❌ Execute trades
- ❌ Modify smart contracts
- ❌ Connect to wallets
- ❌ Provide profit signals
- ❌ Claim capital optimization

This is a **risk analysis tool**, not a trading agent.

---

## Example Output

Risk Summary:

Current LTV: 60%

Liquidation at ~30% price drop

Dominant risk driver: Price Volatility + Leverage

Sensitivity Analysis:

Reducing borrowed amount significantly increases safety buffer


---

## Project Structure

```text
defi-risk-agent/
├── strategy.yaml        # Toy DeFi strategy configuration
├── simulator.py         # Deterministic risk engine
└── README.md

Current Status

Version: v0 (deterministic core complete)

The current implementation intentionally avoids LLMs or blockchain integration to ensure correctness and auditability.

Planned Extensions (Future)

Expanded stress scenarios (volatility regimes, governance changes)

Formal risk scoring

Natural-language explanations (LLM as an interface, not a core)

Visualization layer

All future additions must preserve the read-only, simulation-first design.

Disclaimer

This project is for research and educational purposes only.
It does not constitute financial advice.