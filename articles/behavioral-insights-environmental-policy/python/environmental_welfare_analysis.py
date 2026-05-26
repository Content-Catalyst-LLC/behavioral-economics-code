"""Welfare and distributional analysis for behavioral environmental policy."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAGNOSTICS = ROOT / "outputs" / "model_diagnostics"

DIAGNOSTICS.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_environmental_policy_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_environmental_policy_panel.py first."
    )

df = pd.read_csv(data_path)

summary = df.groupby("regime").agg(
    households=("household_id", "count"),
    adoption_rate=("adopted", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_private_benefit=("private_benefit", "mean"),
    mean_environmental_benefit=("environmental_benefit", "mean"),
    mean_fiscal_cost=("fiscal_cost", "mean"),
    mean_admin_cost=("admin_cost", "mean"),
    mean_energy_burden=("energy_burden", "mean"),
    mean_trust=("trust", "mean"),
).reset_index()

summary["benefit_cost_ratio"] = (
    (summary["mean_private_benefit"] + summary["mean_environmental_benefit"])
    / (summary["mean_fiscal_cost"] + summary["mean_admin_cost"])
)

summary.to_csv(TABLES / "environmental_policy_welfare_summary.csv", index=False)

df["income_quintile"] = pd.qcut(df["income"], 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
distribution = df.groupby(["regime", "income_quintile"], observed=False).agg(
    households=("household_id", "count"),
    adoption_rate=("adopted", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_energy_burden=("energy_burden", "mean"),
    mean_fiscal_cost=("fiscal_cost", "mean"),
).reset_index()

distribution.to_csv(TABLES / "environmental_policy_distributional_summary.csv", index=False)

# Sensitivity to alternative environmental benefit, administrative cost, and fiscal cost assumptions.
sensitivity_rows = []
for env_weight in [0.60, 0.90, 1.20]:
    for admin_weight in [0.50, 1.00, 1.50]:
        for fiscal_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["uptake_prob"]
                + df["private_benefit"]
                + env_weight * df["environmental_benefit"]
                - fiscal_weight * df["fiscal_cost"]
                - admin_weight * df["admin_cost"]
                - 0.20 * df["friction_cost"]
            )

            tmp = df.assign(alt_total_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                sensitivity_rows.append({
                    "environmental_benefit_weight": env_weight,
                    "admin_cost_weight": admin_weight,
                    "fiscal_cost_weight": fiscal_weight,
                    "regime": regime,
                    "mean_alt_total_welfare": sub["alt_total_welfare"].mean(),
                })

pd.DataFrame(sensitivity_rows).to_csv(
    DIAGNOSTICS / "environmental_welfare_sensitivity.csv", index=False
)

print("Wrote environmental welfare summary, distributional summary, and sensitivity diagnostics.")
print(summary)
