from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(14140)

n_agents = 3000
n_periods = 36

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "beta": rng.uniform(0.55, 1.00, n_agents),
    "delta": rng.uniform(0.94, 0.99, n_agents),
    "income": rng.uniform(1800, 5200, n_agents),
    "sophistication": rng.uniform(0.20, 1.00, n_agents),
    "liquidity_need": rng.uniform(0.05, 0.35, n_agents),
    "emergency_risk": rng.uniform(0.02, 0.18, n_agents),
})

regimes = {
    "low_commitment": {
        "commitment_cost": 100,
        "automation_strength": 0.15,
        "flexibility": 0.90,
    },
    "medium_commitment": {
        "commitment_cost": 400,
        "automation_strength": 0.55,
        "flexibility": 0.65,
    },
    "high_commitment": {
        "commitment_cost": 800,
        "automation_strength": 0.85,
        "flexibility": 0.35,
    },
}

def simulate_commitment_regime(regime_name: str, commitment_cost: float, automation_strength: float, flexibility: float) -> pd.DataFrame:
    accumulated_savings = np.zeros(n_agents)
    rows = []

    for period in range(1, n_periods + 1):
        income_t = agents["income"].to_numpy() * rng.uniform(0.90, 1.10, n_agents)
        temptation = rng.uniform(200, 1400, n_agents)

        emergency_shock = rng.binomial(1, agents["emergency_risk"].to_numpy())
        emergency_cost = emergency_shock * rng.uniform(400, 1800, n_agents)

        planned_savings = 0.12 * income_t
        automated_savings = automation_strength * planned_savings
        discretionary_savings = (1 - automation_strength) * planned_savings

        future_value_weight = agents["beta"].to_numpy() * (agents["delta"].to_numpy() ** (n_periods - period))
        utility_stick = future_value_weight * planned_savings + automation_strength * agents["sophistication"].to_numpy() * 150
        utility_deviate = temptation - commitment_cost
        hardship_access = emergency_shock * flexibility * emergency_cost

        actual_savings = np.where(
            utility_stick + hardship_access >= utility_deviate,
            automated_savings + discretionary_savings,
            automated_savings * flexibility,
        )

        withdrawal = np.minimum(accumulated_savings, emergency_cost * flexibility)
        accumulated_savings = accumulated_savings + actual_savings - withdrawal

        hardship_cost = emergency_shock * (1 - flexibility) * agents["liquidity_need"].to_numpy() * 100
        behavioral_burden = commitment_cost * 0.0005 + (1 - flexibility) * 0.5

        welfare = (
            accumulated_savings * 0.01
            + actual_savings * 0.05
            + flexibility * hardship_access * 0.002
            - hardship_cost
            - behavioral_burden
        )

        rows.append(pd.DataFrame({
            "period": period,
            "agent_id": agents["agent_id"],
            "regime": regime_name,
            "income": income_t,
            "beta": agents["beta"],
            "delta": agents["delta"],
            "sophistication": agents["sophistication"],
            "liquidity_need": agents["liquidity_need"],
            "emergency_risk": agents["emergency_risk"],
            "emergency_shock": emergency_shock,
            "emergency_cost": emergency_cost,
            "planned_savings": planned_savings,
            "actual_savings": actual_savings,
            "withdrawal": withdrawal,
            "accumulated_savings": accumulated_savings,
            "welfare": welfare,
            "commitment_cost": commitment_cost,
            "automation_strength": automation_strength,
            "flexibility": flexibility,
            "medium_commitment_treat": int(regime_name == "medium_commitment"),
            "high_commitment_treat": int(regime_name == "high_commitment"),
        }))

    return pd.concat(rows, ignore_index=True)

panel = pd.concat([simulate_commitment_regime(name, **params) for name, params in regimes.items()], ignore_index=True)
final = panel.loc[panel["period"] == n_periods].copy()

summary = final.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_accumulated_savings=("accumulated_savings", "mean"),
    mean_actual_savings=("actual_savings", "mean"),
    mean_withdrawal=("withdrawal", "mean"),
    mean_welfare=("welfare", "mean"),
    mean_commitment_cost=("commitment_cost", "mean"),
    mean_automation_strength=("automation_strength", "mean"),
    mean_flexibility=("flexibility", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_commitment_savings_panel.csv", index=False)
final.to_csv(TABLES / "synthetic_commitment_savings_experiment.csv", index=False)
summary.to_csv(TABLES / "commitment_savings_regime_summary.csv", index=False)

panel.to_csv(PROCESSED / "synthetic_commitment_savings_panel.csv", index=False)
final.to_csv(PROCESSED / "synthetic_commitment_savings_experiment.csv", index=False)
summary.to_csv(PROCESSED / "commitment_savings_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} agent-period rows.")
print(summary)
