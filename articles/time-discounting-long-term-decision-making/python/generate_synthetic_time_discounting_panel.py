from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(17170)

n_agents = 3000
n_periods = 36

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "beta": rng.uniform(0.55, 1.00, n_agents),
    "delta": rng.uniform(0.93, 0.99, n_agents),
    "immediate_reward_base": rng.uniform(80, 190, n_agents),
    "future_goal_value": rng.uniform(140, 320, n_agents),
    "sophistication": rng.uniform(0.20, 1.00, n_agents),
    "liquidity_need": rng.uniform(0.05, 0.35, n_agents),
})

regimes = [
    {
        "regime_name": "exponential_discounting",
        "use_present_bias": False,
        "commitment_support": 0.00,
        "flexibility": 1.00,
    },
    {
        "regime_name": "present_biased_discounting",
        "use_present_bias": True,
        "commitment_support": 0.00,
        "flexibility": 1.00,
    },
    {
        "regime_name": "present_bias_with_commitment_support",
        "use_present_bias": True,
        "commitment_support": 0.70,
        "flexibility": 0.75,
    },
]

def simulate_discount_regime(
    regime_name: str,
    use_present_bias: bool,
    commitment_support: float,
    flexibility: float,
) -> pd.DataFrame:
    cumulative_delayed_choices = np.zeros(n_agents)
    cumulative_welfare = np.zeros(n_agents)
    rows = []

    for period in range(1, n_periods + 1):
        delayed_reward = agents["future_goal_value"].to_numpy() * rng.uniform(0.80, 1.30, n_agents)
        immediate_reward = agents["immediate_reward_base"].to_numpy() * rng.uniform(0.85, 1.25, n_agents)

        if use_present_bias:
            delayed_value = (
                agents["beta"].to_numpy()
                * (agents["delta"].to_numpy() ** (n_periods - period))
                * delayed_reward
            )
        else:
            delayed_value = (agents["delta"].to_numpy() ** (n_periods - period)) * delayed_reward

        support_value = commitment_support * agents["sophistication"].to_numpy() * 50
        flexibility_penalty = agents["liquidity_need"].to_numpy() * (1 - flexibility) * 30

        immediate_value = immediate_reward - support_value + flexibility_penalty
        choose_delayed = (delayed_value >= immediate_value).astype(int)

        period_welfare = (
            choose_delayed * delayed_reward
            - (1 - choose_delayed) * 0.20 * delayed_reward
            - flexibility_penalty
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
            "immediate_reward_base": agents["immediate_reward_base"],
            "future_goal_value": agents["future_goal_value"],
            "delayed_reward": delayed_reward,
            "immediate_reward": immediate_reward,
            "delayed_value": delayed_value,
            "immediate_value": immediate_value,
            "choose_delayed": choose_delayed,
            "period_welfare": period_welfare,
            "cumulative_delayed_choices": cumulative_delayed_choices,
            "cumulative_welfare": cumulative_welfare,
            "commitment_support": commitment_support,
            "flexibility": flexibility,
            "present_bias_treat": int(regime_name == "present_biased_discounting"),
            "commitment_support_treat": int(regime_name == "present_bias_with_commitment_support"),
        }))

    return pd.concat(rows, ignore_index=True)

panel = pd.concat([simulate_discount_regime(**regime) for regime in regimes], ignore_index=True)
final = panel.loc[panel["period"] == n_periods].copy()

summary = final.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
    mean_commitment_support=("commitment_support", "mean"),
    mean_flexibility=("flexibility", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_time_discounting_panel.csv", index=False)
final.to_csv(TABLES / "synthetic_time_discounting_experiment.csv", index=False)
summary.to_csv(TABLES / "time_discounting_regime_summary.csv", index=False)

panel.to_csv(PROCESSED / "synthetic_time_discounting_panel.csv", index=False)
final.to_csv(PROCESSED / "synthetic_time_discounting_experiment.csv", index=False)
summary.to_csv(PROCESSED / "time_discounting_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} agent-period rows.")
print(summary)
