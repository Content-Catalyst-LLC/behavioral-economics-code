from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(16161)

n_agents = 2500
n_choices = 72

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "beta": rng.uniform(0.50, 1.00, n_agents),
    "delta": rng.uniform(0.92, 0.99, n_agents),
    "sophistication": rng.uniform(0.20, 1.00, n_agents),
})

rows = []
for choice_id in range(1, n_choices + 1):
    immediate_reward = rng.uniform(40, 260, n_agents)
    delayed_reward = immediate_reward * rng.uniform(1.15, 2.35, n_agents)
    delay_periods = rng.integers(2, 24, n_agents)
    commitment_cost = rng.choice([0, 25, 70, 140], n_agents)

    discounted_delayed_value = agents["beta"].to_numpy() * (agents["delta"].to_numpy() ** delay_periods) * delayed_reward
    immediate_value = immediate_reward - commitment_cost
    patient_choice = (discounted_delayed_value >= immediate_value).astype(int)

    rows.append(pd.DataFrame({
        "choice_id": choice_id,
        "agent_id": agents["agent_id"],
        "beta": agents["beta"],
        "delta": agents["delta"],
        "sophistication": agents["sophistication"],
        "immediate_reward": immediate_reward,
        "delayed_reward": delayed_reward,
        "delay_periods": delay_periods,
        "commitment_cost": commitment_cost,
        "discounted_delayed_value": discounted_delayed_value,
        "immediate_value": immediate_value,
        "patient_choice": patient_choice,
    }))

history = pd.concat(rows, ignore_index=True)
summary = history.groupby("commitment_cost").agg(
    choices=("choice_id", "count"),
    patient_choice_rate=("patient_choice", "mean"),
    mean_beta=("beta", "mean"),
    mean_delay=("delay_periods", "mean"),
    mean_immediate_reward=("immediate_reward", "mean"),
    mean_delayed_reward=("delayed_reward", "mean"),
).reset_index()

history.to_csv(TABLES / "quasi_hyperbolic_discounting_history.csv", index=False)
summary.to_csv(TABLES / "quasi_hyperbolic_discounting_summary.csv", index=False)

print(summary)
