from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(16160)

n_agents = 3000
n_periods = 36

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "beta": rng.uniform(0.50, 1.00, n_agents),
    "delta": rng.uniform(0.94, 0.99, n_agents),
    "temptation_strength": rng.uniform(50, 260, n_agents),
    "sophistication": rng.uniform(0.20, 1.00, n_agents),
    "liquidity_need": rng.uniform(0.05, 0.35, n_agents),
    "future_goal_value": rng.uniform(150, 420, n_agents),
})

regimes = {
    "weak_commitment": {
        "commitment_cost": 20,
        "reminder_strength": 0.10,
        "flexibility": 0.95,
    },
    "medium_commitment": {
        "commitment_cost": 70,
        "reminder_strength": 0.45,
        "flexibility": 0.75,
    },
    "strong_commitment": {
        "commitment_cost": 140,
        "reminder_strength": 0.80,
        "flexibility": 0.55,
    },
}

def simulate_commitment_regime(regime_name: str, commitment_cost: float, reminder_strength: float, flexibility: float) -> pd.DataFrame:
    cumulative_delayed_choices = np.zeros(n_agents)
    cumulative_welfare = np.zeros(n_agents)
    rows = []

    for period in range(1, n_periods + 1):
        delayed_reward = agents["future_goal_value"].to_numpy() * rng.uniform(0.80, 1.25, n_agents)
        immediate_temptation = agents["temptation_strength"].to_numpy() * rng.uniform(0.80, 1.30, n_agents)

        discounted_delayed_value = (
            agents["beta"].to_numpy()
            * (agents["delta"].to_numpy() ** (n_periods - period))
            * delayed_reward
        )

        commitment_support = commitment_cost + reminder_strength * agents["sophistication"].to_numpy() * 40
        hardship_adjustment = agents["liquidity_need"].to_numpy() * (1 - flexibility) * 25

        immediate_value = immediate_temptation - commitment_support + hardship_adjustment
        choose_delayed = (discounted_delayed_value >= immediate_value).astype(int)

        period_welfare = (
            choose_delayed * delayed_reward
            - (1 - choose_delayed) * 0.25 * delayed_reward
            - hardship_adjustment
        )

        cumulative_delayed_choices += choose_delayed
        cumulative_welfare += period_welfare

        rows.append(pd.DataFrame({
            "period": period,
            "agent_id": agents["agent_id"],
            "regime": regime_name,
            "beta": agents["beta"],
            "delta": agents["delta"],
            "sophistication": agents["sophistication"],
            "liquidity_need": agents["liquidity_need"],
            "temptation_strength": agents["temptation_strength"],
            "future_goal_value": agents["future_goal_value"],
            "delayed_reward": delayed_reward,
            "immediate_temptation": immediate_temptation,
            "discounted_delayed_value": discounted_delayed_value,
            "immediate_value": immediate_value,
            "choose_delayed": choose_delayed,
            "period_welfare": period_welfare,
            "cumulative_delayed_choices": cumulative_delayed_choices,
            "cumulative_welfare": cumulative_welfare,
            "commitment_cost": commitment_cost,
            "reminder_strength": reminder_strength,
            "flexibility": flexibility,
            "medium_commitment_treat": int(regime_name == "medium_commitment"),
            "strong_commitment_treat": int(regime_name == "strong_commitment"),
        }))

    return pd.concat(rows, ignore_index=True)

panel = pd.concat(
    [simulate_commitment_regime(name, **params) for name, params in regimes.items()],
    ignore_index=True,
)

final = panel.loc[panel["period"] == n_periods].copy()

summary = final.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
    mean_commitment_cost=("commitment_cost", "mean"),
    mean_reminder_strength=("reminder_strength", "mean"),
    mean_flexibility=("flexibility", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_present_bias_panel.csv", index=False)
final.to_csv(TABLES / "synthetic_present_bias_experiment.csv", index=False)
summary.to_csv(TABLES / "present_bias_regime_summary.csv", index=False)

panel.to_csv(PROCESSED / "synthetic_present_bias_panel.csv", index=False)
final.to_csv(PROCESSED / "synthetic_present_bias_experiment.csv", index=False)
summary.to_csv(PROCESSED / "present_bias_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} agent-period rows.")
print(summary)
