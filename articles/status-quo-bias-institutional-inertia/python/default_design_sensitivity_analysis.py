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

rng = np.random.default_rng(18181)
n = 2500

base = pd.DataFrame({
    "agent_id": np.arange(1, n + 1),
    "switch_cost": rng.uniform(0.05, 0.45, n),
    "loss_aversion": rng.uniform(1.00, 3.25, n),
    "status_quo_premium": rng.uniform(0.02, 0.30, n),
    "uncertainty_sensitivity": rng.uniform(0.05, 0.35, n),
    "decision_fatigue": rng.uniform(0.00, 0.35, n),
    "sophistication": rng.uniform(0.20, 1.00, n),
})

grid = list(itertools.product(
    [0.00, 0.25, 0.50, 0.75],
    [0.00, 0.25, 0.50, 0.75],
    [0.10, 0.35, 0.60, 0.85],
))

rows = []
for default_shift, switching_support, disclosure_quality in grid:
    value_status_quo = rng.uniform(0.45, 0.60, n)
    value_alternative = value_status_quo + rng.uniform(0.02, 0.25, n)
    perceived_loss = rng.uniform(0.02, 0.20, n)

    effective_switch_cost = np.maximum(
        base["switch_cost"].to_numpy() - switching_support * base["sophistication"].to_numpy() * 0.20,
        0,
    )
    effective_status_quo_premium = np.maximum(
        base["status_quo_premium"].to_numpy()
        + base["decision_fatigue"].to_numpy()
        - default_shift * 0.18
        - disclosure_quality * base["sophistication"].to_numpy() * 0.12,
        0,
    )
    effective_perceived_loss = np.maximum(
        perceived_loss + base["uncertainty_sensitivity"].to_numpy() - disclosure_quality * 0.10,
        0,
    )

    utility_status_quo = value_status_quo + effective_status_quo_premium
    utility_alternative = (
        value_alternative
        - effective_switch_cost
        - base["loss_aversion"].to_numpy() * effective_perceived_loss
    )
    choose_alternative = (utility_alternative >= utility_status_quo).astype(int)
    welfare = np.where(choose_alternative == 1, value_alternative - effective_switch_cost, value_status_quo)

    rows.append({
        "default_shift": default_shift,
        "switching_support": switching_support,
        "disclosure_quality": disclosure_quality,
        "adoption_rate": float(np.mean(choose_alternative)),
        "mean_welfare": float(np.mean(welfare)),
        "mean_effective_switch_cost": float(np.mean(effective_switch_cost)),
        "mean_effective_status_quo_premium": float(np.mean(effective_status_quo_premium)),
        "mean_effective_perceived_loss": float(np.mean(effective_perceived_loss)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "default_design_sensitivity.csv", index=False)
sensitivity.sort_values("mean_welfare", ascending=False).head(15).to_csv(
    DIAG / "default_design_top_welfare_regimes.csv",
    index=False,
)

print(sensitivity.sort_values("mean_welfare", ascending=False).head(10))
