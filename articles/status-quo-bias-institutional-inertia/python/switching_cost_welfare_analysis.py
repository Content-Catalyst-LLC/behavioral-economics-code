from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_status_quo_bias_panel.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    adoption_rate=("choose_alternative", "mean"),
    mean_welfare=("welfare", "mean"),
    mean_objective_gain=("objective_gain", "mean"),
    mean_effective_switch_cost=("effective_switch_cost", "mean"),
    mean_loss_aversion=("loss_aversion", "mean"),
    mean_effective_status_quo_premium=("effective_status_quo_premium", "mean"),
    mean_effective_perceived_loss=("effective_perceived_loss", "mean"),
    mean_decision_fatigue=("decision_fatigue", "mean"),
).reset_index()

summary["welfare_per_adoption_point"] = summary["mean_welfare"] / summary["adoption_rate"].replace(0, float("nan"))
summary.to_csv(TABLES / "status_quo_bias_welfare_switching_summary.csv", index=False)

rows = []
for switching_weight in [0.75, 1.00, 1.25]:
    for autonomy_weight in [0.75, 1.00, 1.25]:
        for burden_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["welfare"]
                + autonomy_weight * df["disclosure_quality"] * df["sophistication"] * 0.10
                - switching_weight * df["effective_switch_cost"] * 0.50
                - burden_weight * df["decision_fatigue"] * 0.20
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "switching_weight": switching_weight,
                    "autonomy_weight": autonomy_weight,
                    "burden_weight": burden_weight,
                    "regime": regime,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "status_quo_bias_welfare_sensitivity.csv", index=False)

print(summary)
