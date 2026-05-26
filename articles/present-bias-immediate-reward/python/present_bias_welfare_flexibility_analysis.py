from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_present_bias_experiment.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
    mean_beta=("beta", "mean"),
    mean_liquidity_need=("liquidity_need", "mean"),
    mean_temptation_strength=("temptation_strength", "mean"),
    mean_commitment_cost=("commitment_cost", "mean"),
    mean_reminder_strength=("reminder_strength", "mean"),
    mean_flexibility=("flexibility", "mean"),
).reset_index()

summary["delayed_choice_welfare_ratio"] = summary["mean_cumulative_welfare"] / summary["mean_cumulative_delayed_choices"].replace(0, float("nan"))
summary.to_csv(TABLES / "present_bias_welfare_flexibility_summary.csv", index=False)

rows = []
for commitment_weight in [0.75, 1.00, 1.25]:
    for reminder_weight in [0.75, 1.00, 1.25]:
        for flexibility_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["cumulative_welfare"]
                + reminder_weight * df["reminder_strength"] * df["sophistication"] * 50
                - commitment_weight * df["commitment_cost"] * 0.10
                - flexibility_weight * (1 - df["flexibility"]) * df["liquidity_need"] * 500
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "commitment_weight": commitment_weight,
                    "reminder_weight": reminder_weight,
                    "flexibility_weight": flexibility_weight,
                    "regime": regime,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "present_bias_welfare_sensitivity.csv", index=False)

print(summary)
