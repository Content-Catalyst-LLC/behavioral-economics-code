from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_commitment_savings_experiment.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_accumulated_savings=("accumulated_savings", "mean"),
    mean_actual_savings=("actual_savings", "mean"),
    mean_withdrawal=("withdrawal", "mean"),
    mean_welfare=("welfare", "mean"),
    mean_beta=("beta", "mean"),
    mean_liquidity_need=("liquidity_need", "mean"),
    mean_emergency_risk=("emergency_risk", "mean"),
    mean_automation_strength=("automation_strength", "mean"),
    mean_flexibility=("flexibility", "mean"),
).reset_index()

summary["savings_welfare_gap"] = summary["mean_accumulated_savings"] / 1000 - summary["mean_welfare"]
summary.to_csv(TABLES / "commitment_welfare_flexibility_summary.csv", index=False)

rows = []
for commitment_weight in [0.75, 1.00, 1.25]:
    for automation_weight in [0.75, 1.00, 1.25]:
        for flexibility_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["accumulated_savings"] * 0.01
                + automation_weight * df["actual_savings"] * 0.05
                + flexibility_weight * df["flexibility"] * df["emergency_cost"] * 0.002
                - commitment_weight * df["commitment_cost"] * 0.0005
                - (1 - df["flexibility"]) * df["liquidity_need"] * 50
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "commitment_weight": commitment_weight,
                    "automation_weight": automation_weight,
                    "flexibility_weight": flexibility_weight,
                    "regime": regime,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "commitment_welfare_sensitivity.csv", index=False)

print(summary)
