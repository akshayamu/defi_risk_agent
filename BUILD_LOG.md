# BUILD_LOG.md  
## DeFi Risk Agent — Builder’s Log (Step 1 → Step 15)

This document records **how this project was actually built** — not just the final result.

It includes:
- what I tried
- what failed
- how many times it broke
- how I fixed it
- what I learned at each step

This is not a success story.  
It’s an engineering log.

---

## Step 1 — Defining the Problem

**What I tried:**  
I wanted to “build something around DeFi liquidation risk.”

That was the entire idea at the beginning.

**Struggle:**  
I couldn’t clearly explain *what* I was solving. Everything sounded vague:
- simulate price drops
- check LTV
- see liquidation

That’s not a system. That’s just intuition.

**Failure:**  
1 conceptual failure.  
I realized I couldn’t even define the *state* of the problem.

**Correction:**  
I stopped coding and forced myself to define the smallest deterministic unit:
- **Position** (collateral, borrow)
- **Market** (price context)
- **Protocol** (liquidation rules)

Only after separating these did the problem become concrete.

**What I learned:**  
If you can’t define the problem clearly, any code you write is guessing.

---

## Step 2 — Choosing Determinism Over Cleverness

**What I tried:**  
I made an explicit decision:
- no ML
- no randomness
- no LLMs
- no blockchain calls

**Struggle:**  
This felt “boring” compared to adding AI early.

**Failure:**  
0 runtime failures, but a strong temptation to over-engineer.

**Correction:**  
I wrote this rule down and treated it as non-negotiable:
> Simulation first. Intelligence later.

**What I learned:**  
Correctness compounds. Cleverness doesn’t.

---

## Step 3 — First Deterministic Simulator (v0)

**What I tried:**  
A simple price-drop → LTV → liquidation check.

**Struggle:**  
Even simple math can be wrong if you rush.

**Failures:**  
2 failures:
- mixing percentages and decimals
- incorrect liquidation comparison

**Correction:**  
Everything became **pure functions** with explicit inputs and outputs.

**What I learned:**  
If a function isn’t pure, debugging becomes guesswork.

---

## Step 4 — Strategy Configuration (YAML)

**What I tried:**  
Moved assumptions into `strategy.yaml`.

**Struggle:**  
Schema confusion:
- Where does price belong?
- Where does liquidation threshold belong?

**Failures:**  
3 runtime `KeyError`s.

**Correction:**  
Standardized schema:
- `protocol`
- `market`
- `position`

**What I learned:**  
Configuration is part of the system, not an afterthought.

---

## Step 5 — Price Shock Stress Testing

**What I tried:**  
Simulated fixed price drops (10–40%).

**Struggle:**  
Results looked correct, but incomplete.

**Failure:**  
1 conceptual failure — price alone didn’t explain sudden liquidation.

**Correction:**  
Accepted that this was only **one dimension** of risk.

**What I learned:**  
Single-axis analysis hides real danger.

---

## Step 6 — Leverage Sensitivity

**What I tried:**  
Varied borrowed amount while holding everything else constant.

**Struggle:**  
Small leverage changes caused large risk shifts.

**Failure:**  
1 wrong intuition — I blamed price instead of leverage.

**Correction:**  
Separated leverage sensitivity as its own analysis.

**What I learned:**  
Leverage is often the dominant risk driver.

---

## Step 7 — Python Packaging (Major Pain)

**What I tried:**  
Converted scripts into a real package.

**Struggle:**  
This was harder than the math.

**Failures:**  
8+ failures:
- `ModuleNotFoundError`
- broken imports
- wrong execution context

**Correction:**  
Learned:
- absolute imports
- `python -m package.module`
- parent-directory execution

**What I learned:**  
Most “Python bugs” are actually packaging mistakes.

---

## Step 8 — Path Resolution

**What I tried:**  
Loaded files using relative paths.

**Failures:**  
4 failures (`FileNotFoundError`).

**Correction:**  
Used `Path(__file__).resolve()` everywhere.

**What I learned:**  
Never trust the working directory.

---

## Step 9 — Canonical Reporting Layer

**What I tried:**  
Centralized all outputs into `latest.json`.

**Struggle:**  
Temptation to recompute logic in multiple places.

**Failure:**  
1 design mistake (almost let visualization recompute risk).

**Correction:**  
Strict rule:
> Reports compute. Everything else reads.

**What I learned:**  
A single source of truth prevents silent bugs.

---

## Step 10 — Risk Score

**What I tried:**  
Collapsed risk into a single number.

**Struggle:**  
Scores hide nuance.

**Failures:**  
2 redesigns.

**Correction:**  
Score became a **summary**, not a decision-maker.

**What I learned:**  
Numbers should summarize reality, not replace it.

---

## Step 11 — Volatility Regimes

**What I tried:**  
Added calm / normal / turbulent / crisis regimes.

**Struggle:**  
How to model volatility without randomness?

**Failure:**  
1 conceptual dead end (almost added stochastic noise).

**Correction:**  
Used deterministic multipliers.

**What I learned:**  
Volatility is context, not randomness.

---

## Step 12 — Scenario Matrix

**What I tried:**  
Enumerated price × leverage × volatility.

**Struggle:**  
Execution order bugs everywhere.

**Failures:**  
6+ failures:
- undefined variables
- syntax errors
- missing commas

**Correction:**  
Slowed down, enforced strict ordering.

**What I learned:**  
Complexity grows combinatorially. Discipline matters.

---

## Step 13 — Risk Surface Aggregation

**What I tried:**  
Classified scenarios into SAFE / WARNING / LIQUIDATED.

**Struggle:**  
Choosing boundaries felt subjective.

**Failure:**  
1 philosophical struggle — what is “safe”?

**Correction:**  
Used distance to liquidation threshold.

**What I learned:**  
Explainable rules beat “smart” ones.

---

## Step 14 — Visualization

**What I tried:**  
Rendered heatmaps and cliff plots.

**Struggle:**  
Visualization failed when data was incomplete.

**Failures:**  
3 runtime failures.

**Correction:**  
Visualization became strictly read-only.

**What I learned:**  
Visualization should fail loudly if inputs are wrong.

---

## Step 15 — Read-Only Explanation Layer

**What I tried:**  
Added natural-language explanations.

**Struggle:**  
Avoiding hallucination.

**Failures:**  
0 — because design was strict.

**Correction:**  
Explanations only read `latest.json`.

**What I learned:**  
Language should explain systems, not control them.

---

## Final Reflection

This project taught me more about **systems** than DeFi.

Nothing here was individually hard.  
What was hard was **doing each step correctly**, without skipping foundations.

Most bugs weren’t math bugs.  
They were discipline bugs.

If I rebuild this, I’ll be faster — not because I know more tricks, but because I respect structure more.

---

*Educational and research project. Not financial advice.*
