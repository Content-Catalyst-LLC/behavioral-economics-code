"""Welfare and distributional analysis for behavioral regulation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAGNOSTICS = ROOT / "outputs" / "model_diagnostics"

DIAGNOSTICS.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_regulatory_policy_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_regulatory_policy_panel.py first."
    )

df = pd.read_csv(data_path)

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    compliance_rate=("complied", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_social_benefit=("social_benefit", "mean"),
    mean_compliance_cost=("compliance_cost", "mean"),
    mean_enforcement_cost=("enforcement_cost", "mean"),
    mean_administrative_cost=("administrative_cost", "mean"),
    mean_admin_burden=("admin_burden", "mean"),
    mean_trust_signal=("trust_signal", "mean"),
).reset_index()

summary["benefit_cost_ratio"] = (
    summary["mean_social_benefit"]
    / (
        summary["mean_compliance_cost"]
        + summary["mean_enforcement_cost"]
        + summary["mean_administrative_cost"]
    )
)

summary.to_csv(TABLES / "regulatory_policy_welfare_summary.csv", index=False)

df["burden_sensitivity_quartile"] = pd.qcut(df["burden_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
distribution = df.groupby(["regime", "burden_sensitivity_quartile"], observed=False).agg(
    agents=("agent_id", "count"),
    compliance_rate=("complied", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_compliance_cost=("compliance_cost", "mean"),
    mean_admin_burden=("admin_burden", "mean"),
).reset_index()

distribution.to_csv(TABLES / "regulatory_policy_distributional_summary.csv", index=False)

# Sensitivity to alternative social benefit, administrative cost, and enforcement cost assumptions.
sensitivity_rows = []
for social_weight in [0.60, 0.90, 1.20]:
    for admin_weight in [0.50, 1.00, 1.50]:
        for enforcement_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["utility_compliance"]
                + social_weight * df["social_benefit"]
                - df["compliance_cost"]
                - admin_weight * df["administrative_cost"]
                - enforcement_weight * df["enforcement_cost"]
            )

            tmp = df.assign(alt_total_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                sensitivity_rows.append({
                    "social_benefit_weight": social_weight,
                    "admin_cost_weight": admin_weight,
                    "enforcement_cost_weight": enforcement_weight,
                    "regime": regime,
                    "mean_alt_total_welfare": sub["alt_total_welfare"].mean(),
                })

pd.DataFrame(sensitivity_rows).to_csv(
    DIAGNOSTICS / "regulatory_welfare_sensitivity.csv", index=False
)

print("Wrote regulatory welfare summary, distributional summary, and sensitivity diagnostics.")
print(summary)
