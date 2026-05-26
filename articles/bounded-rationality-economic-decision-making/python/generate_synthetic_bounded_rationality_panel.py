from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(26260)
n_agents = 3000
n_options = 30

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "aspiration": rng.uniform(0.55, 0.85, n_agents),
    "search_cost": rng.uniform(0.003, 0.035, n_agents),
    "time_budget": rng.uniform(8, 30, n_agents),
    "cognitive_capacity": rng.uniform(6, 25, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "stress": rng.uniform(0.00, 0.70, n_agents),
    "institutional_trust": rng.uniform(0.20, 1.00, n_agents),
    "digital_access": rng.uniform(0.10, 1.00, n_agents),
    "income_security": rng.uniform(0.10, 1.00, n_agents),
    "administrative_capacity": rng.uniform(0.10, 1.00, n_agents),
})

def simulate_agent(agent: pd.Series, regime: str) -> dict:
    option_values = rng.uniform(0, 1, n_options)
    option_loads = rng.uniform(0.50, 2.00, n_options)
    option_times = rng.uniform(0.50, 1.50, n_options)

    if regime == "low_constraint":
        search_multiplier = 0.75
        load_multiplier = 0.75
    elif regime == "medium_constraint":
        search_multiplier = 1.00
        load_multiplier = 1.00
    elif regime == "high_constraint":
        search_multiplier = 1.35
        load_multiplier = 1.35
    else:
        raise ValueError(f"Unknown regime: {regime}")

    adjusted_search_cost = agent["search_cost"] * search_multiplier * (1 + agent["stress"])
    adjusted_capacity = agent["cognitive_capacity"] / load_multiplier
    adjusted_time_budget = agent["time_budget"] / search_multiplier

    optimal_value = float(option_values.max())

    chosen_index = None
    chosen_value = None
    cumulative_time = 0.0
    cumulative_load = 0.0

    for idx, value in enumerate(option_values, start=1):
        cumulative_time += float(option_times[idx - 1])
        cumulative_load += float(option_loads[idx - 1])

        if cumulative_time > adjusted_time_budget or cumulative_load > adjusted_capacity:
            chosen_index = max(1, idx - 1)
            chosen_value = float(option_values[chosen_index - 1])
            break

        if value >= agent["aspiration"]:
            chosen_index = idx
            chosen_value = float(value)
            break

    if chosen_index is None:
        chosen_index = n_options
        chosen_value = float(option_values[-1])
        cumulative_time = float(option_times.sum())
        cumulative_load = float(option_loads.sum())

    net_value = chosen_value - adjusted_search_cost * chosen_index
    optimization_gap = optimal_value - chosen_value

    return {
        "regime": regime,
        "agent_id": int(agent["agent_id"]),
        "aspiration": agent["aspiration"],
        "search_cost": agent["search_cost"],
        "time_budget": agent["time_budget"],
        "cognitive_capacity": agent["cognitive_capacity"],
        "numeracy": agent["numeracy"],
        "stress": agent["stress"],
        "institutional_trust": agent["institutional_trust"],
        "digital_access": agent["digital_access"],
        "income_security": agent["income_security"],
        "administrative_capacity": agent["administrative_capacity"],
        "chosen_index": chosen_index,
        "chosen_value": chosen_value,
        "optimal_value": optimal_value,
        "net_value": net_value,
        "optimization_gap": optimization_gap,
        "cumulative_time": cumulative_time,
        "cumulative_load": cumulative_load,
    }

rows = []
for regime in ["low_constraint", "medium_constraint", "high_constraint"]:
    for _, agent in agents.iterrows():
        rows.append(simulate_agent(agent, regime))

panel = pd.DataFrame(rows)
panel["medium_constraint_treat"] = (panel["regime"] == "medium_constraint").astype(int)
panel["high_constraint_treat"] = (panel["regime"] == "high_constraint").astype(int)

summary = panel.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_chosen_value=("chosen_value", "mean"),
    mean_optimal_value=("optimal_value", "mean"),
    mean_net_value=("net_value", "mean"),
    mean_optimization_gap=("optimization_gap", "mean"),
    mean_search_depth=("chosen_index", "mean"),
    mean_time_used=("cumulative_time", "mean"),
    mean_cognitive_load=("cumulative_load", "mean"),
    mean_stress=("stress", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_bounded_rationality_panel.csv", index=False)
summary.to_csv(TABLES / "bounded_rationality_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_bounded_rationality_panel.csv", index=False)
summary.to_csv(PROCESSED / "bounded_rationality_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} bounded-rationality rows.")
print(summary)
