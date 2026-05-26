"""Welfare and distributional analysis for nudge policy."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAGNOSTICS = ROOT / "outputs" / "model_diagnostics"

DIAGNOSTICS.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_nudge_policy_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_nudge_policy_panel.py first."
    )

df = pd.read_csv(data_path)

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    adoption_rate=("adopted", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_user_benefit=("user_benefit", "mean"),
    mean_social_benefit=("social_benefit", "mean"),
    mean_friction_cost=("friction_cost", "mean"),
    mean_admin_cost=("admin_cost", "mean"),
    mean_implementation_cost=("implementation_cost", "mean"),
).reset_index()

summary["behavior_welfare_rank_gap"] = (
    summary["adoption_rate"].rank(ascending=False)
    - summary["mean_total_welfare"].rank(ascending=False)
)

summary.to_csv(TABLES / "nudge_policy_welfare_summary.csv", index=False)

df["burden_quartile"] = pd.qcut(df["administrative_burden_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

distribution = df.groupby(["regime", "burden_quartile"], observed=False).agg(
    agents=("agent_id", "count"),
    adoption_rate=("adopted", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_admin_cost=("admin_cost", "mean"),
    mean_friction_cost=("friction_cost", "mean"),
).reset_index()

distribution.to_csv(TABLES / "nudge_policy_distributional_summary.csv", index=False)

# Sensitivity to alternative user benefit, social benefit, friction cost, and administrative cost assumptions.
sensitivity_rows = []
for user_weight in [0.75, 1.00, 1.25]:
    for social_weight in [0.60, 1.00, 1.40]:
        for burden_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["utility"]
                + user_weight * df["user_benefit"]
                + social_weight * df["social_benefit"]
                - burden_weight * df["friction_cost"]
                - burden_weight * df["admin_cost"]
                - df["implementation_cost"]
            )

            tmp = df.assign(alt_total_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                sensitivity_rows.append({
                    "user_benefit_weight": user_weight,
                    "social_benefit_weight": social_weight,
                    "burden_cost_weight": burden_weight,
                    "regime": regime,
                    "mean_alt_total_welfare": sub["alt_total_welfare"].mean(),
                })

pd.DataFrame(sensitivity_rows).to_csv(
    DIAGNOSTICS / "nudge_welfare_sensitivity.csv", index=False
)

print("Wrote nudge policy welfare summary, distributional summary, and sensitivity diagnostics.")
print(summary)
