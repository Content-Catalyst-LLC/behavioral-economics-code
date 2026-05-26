from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_time_discounting_experiment.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
    mean_beta=("beta", "mean"),
    mean_delta=("delta", "mean"),
    mean_liquidity_need=("liquidity_need", "mean"),
    mean_immediate_reward=("immediate_reward_base", "mean"),
    mean_future_goal_value=("future_goal_value", "mean"),
    mean_commitment_support=("commitment_support", "mean"),
    mean_flexibility=("flexibility", "mean"),
).reset_index()

summary["welfare_per_delayed_choice"] = summary["mean_cumulative_welfare"] / summary["mean_cumulative_delayed_choices"].replace(0, float("nan"))
summary.to_csv(TABLES / "time_discounting_welfare_flexibility_summary.csv", index=False)

rows = []
for support_weight in [0.75, 1.00, 1.25]:
    for flexibility_weight in [0.75, 1.00, 1.25]:
        for future_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["cumulative_welfare"]
                + support_weight * df["commitment_support"] * df["sophistication"] * 100
                + future_weight * df["future_goal_value"] * df["choose_delayed"]
                - flexibility_weight * (1 - df["flexibility"]) * df["liquidity_need"] * 600
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "support_weight": support_weight,
                    "flexibility_weight": flexibility_weight,
                    "future_weight": future_weight,
                    "regime": regime,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "time_discounting_welfare_sensitivity.csv", index=False)

print(summary)
