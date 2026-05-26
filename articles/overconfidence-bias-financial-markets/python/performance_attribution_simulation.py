from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(12121)

n_managers = 500
n_periods = 120

managers = pd.DataFrame({
    "manager_id": np.arange(1, n_managers + 1),
    "beta_market": rng.normal(1.0, 0.20, n_managers),
    "factor_loading": rng.normal(0.35, 0.15, n_managers),
    "true_skill_alpha": rng.normal(0.001, 0.006, n_managers),
    "overconfidence_score": np.clip(rng.normal(1.3, 0.35, n_managers), 0.5, 2.5),
})

rows = []
for period in range(1, n_periods + 1):
    market_return = rng.normal(0.006, 0.045)
    factor_return = rng.normal(0.002, 0.030)

    residual_noise = rng.normal(0, 0.025, n_managers)
    reported_conviction = managers["overconfidence_score"].to_numpy() * np.abs(
        managers["true_skill_alpha"].to_numpy() + residual_noise
    )

    returns = (
        managers["beta_market"].to_numpy() * market_return
        + managers["factor_loading"].to_numpy() * factor_return
        + managers["true_skill_alpha"].to_numpy()
        + residual_noise
    )

    rows.append(pd.DataFrame({
        "period": period,
        "manager_id": managers["manager_id"],
        "market_return": market_return,
        "factor_return": factor_return,
        "observed_return": returns,
        "reported_conviction": reported_conviction,
        "beta_market": managers["beta_market"],
        "factor_loading": managers["factor_loading"],
        "true_skill_alpha": managers["true_skill_alpha"],
        "overconfidence_score": managers["overconfidence_score"],
    }))

panel = pd.concat(rows, ignore_index=True)

summary = panel.groupby("manager_id", as_index=False).agg(
    mean_observed_return=("observed_return", "mean"),
    return_volatility=("observed_return", "std"),
    mean_reported_conviction=("reported_conviction", "mean"),
    beta_market=("beta_market", "mean"),
    factor_loading=("factor_loading", "mean"),
    true_skill_alpha=("true_skill_alpha", "mean"),
    overconfidence_score=("overconfidence_score", "mean"),
)

summary["skill_misattribution_risk"] = summary["mean_reported_conviction"] / (summary["true_skill_alpha"].abs() + 0.001)

panel.to_csv(TABLES / "performance_attribution_panel.csv", index=False)
summary.to_csv(TABLES / "performance_attribution_manager_summary.csv", index=False)

print(summary.head())
