from __future__ import annotations

from pathlib import Path
import itertools
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
for folder in [TABLES, DIAG]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(26264)

n_replications = 500
n_options = 30

grid = list(itertools.product(
    [0.55, 0.65, 0.75, 0.85],
    [0.003, 0.010, 0.020, 0.035],
    [8, 15, 25],
    [6, 12, 22],
))

rows = []
for aspiration, search_cost, time_budget, cognitive_capacity in grid:
    chosen_values = []
    net_values = []
    optimization_gaps = []
    search_depths = []

    for _ in range(n_replications):
        option_values = rng.uniform(0, 1, n_options)
        option_times = rng.uniform(0.50, 1.50, n_options)
        option_loads = rng.uniform(0.50, 2.00, n_options)

        optimal_value = float(option_values.max())
        cumulative_time = 0.0
        cumulative_load = 0.0
        chosen_index = None

        for idx, value in enumerate(option_values, start=1):
            cumulative_time += float(option_times[idx - 1])
            cumulative_load += float(option_loads[idx - 1])

            if cumulative_time > time_budget or cumulative_load > cognitive_capacity:
                chosen_index = max(1, idx - 1)
                break

            if value >= aspiration:
                chosen_index = idx
                break

        if chosen_index is None:
            chosen_index = n_options

        chosen_value = float(option_values[chosen_index - 1])
        net_value = chosen_value - search_cost * chosen_index
        optimization_gap = optimal_value - chosen_value

        chosen_values.append(chosen_value)
        net_values.append(net_value)
        optimization_gaps.append(optimization_gap)
        search_depths.append(chosen_index)

    rows.append({
        "aspiration": aspiration,
        "search_cost": search_cost,
        "time_budget": time_budget,
        "cognitive_capacity": cognitive_capacity,
        "mean_chosen_value": float(np.mean(chosen_values)),
        "mean_net_value": float(np.mean(net_values)),
        "mean_optimization_gap": float(np.mean(optimization_gaps)),
        "mean_search_depth": float(np.mean(search_depths)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "bounded_rationality_parameter_sensitivity.csv", index=False)

best_by_net = sensitivity.sort_values("mean_net_value", ascending=False).head(20)
best_by_net.to_csv(DIAG / "bounded_rationality_best_parameter_regions.csv", index=False)

print(sensitivity.head())
print(best_by_net.head())
