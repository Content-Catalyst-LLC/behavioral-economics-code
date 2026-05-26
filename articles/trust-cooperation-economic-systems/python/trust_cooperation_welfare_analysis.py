from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_trust_cooperation_experiment.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    trust_rate=("trusted", "mean"),
    reciprocity_rate=("reciprocated", "mean"),
    punishment_rate=("punished", "mean"),
    mean_cooperative_benefit=("cooperative_benefit", "mean"),
    mean_transaction_cost_reduction=("transaction_cost_reduction", "mean"),
    mean_betrayal_loss=("betrayal_loss", "mean"),
    mean_monitoring_cost=("monitoring_cost", "mean"),
    mean_institutional_cost=("institutional_cost", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
summary["trust_welfare_rank_gap"] = summary["trust_rate"].rank(ascending=False) - summary["mean_total_welfare"].rank(ascending=False)
summary.to_csv(TABLES / "trust_cooperation_welfare_summary.csv", index=False)

df["betrayal_sensitivity_quartile"] = pd.qcut(df["betrayal_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
distribution = df.groupby(["regime", "betrayal_sensitivity_quartile"], observed=False).agg(
    agents=("agent_id", "count"),
    trust_rate=("trusted", "mean"),
    reciprocity_rate=("reciprocated", "mean"),
    mean_betrayal_loss=("betrayal_loss", "mean"),
    mean_monitoring_cost=("monitoring_cost", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
distribution.to_csv(TABLES / "trust_cooperation_distributional_summary.csv", index=False)

rows = []
for betrayal_weight in [0.75, 1.00, 1.25]:
    for monitoring_weight in [0.75, 1.00, 1.25]:
        for transaction_weight in [0.75, 1.00, 1.25]:
            alt = (
                df["cooperative_benefit"]
                + transaction_weight * df["transaction_cost_reduction"]
                + df["punishment_value"]
                - betrayal_weight * df["betrayal_loss"]
                - monitoring_weight * df["monitoring_cost"]
                - df["institutional_cost"]
            )
            tmp = df.assign(alt_total_welfare=alt)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "betrayal_loss_weight": betrayal_weight,
                    "monitoring_cost_weight": monitoring_weight,
                    "transaction_cost_reduction_weight": transaction_weight,
                    "regime": regime,
                    "mean_alt_total_welfare": sub["alt_total_welfare"].mean(),
                })
pd.DataFrame(rows).to_csv(DIAG / "trust_cooperation_welfare_sensitivity.csv", index=False)
print(summary)
