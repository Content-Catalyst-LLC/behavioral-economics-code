from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_fairness_reciprocity_experiment.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_material_payoff=("self_payoff", "mean"),
    mean_other_payoff=("other_payoff", "mean"),
    mean_inequality_gap=("inequality_gap", "mean"),
    mean_reciprocity_signal=("reciprocity_signal", "mean"),
    mean_process_fairness=("process_fairness", "mean"),
    mean_fairness_reciprocity_utility=("fairness_reciprocity_utility", "mean"),
    rejection_rate=("rejected", "mean"),
    punishment_rate=("punished", "mean"),
    cooperation_rate=("cooperated", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()

summary["material_vs_social_rank_gap"] = (
    summary["mean_material_payoff"].rank(ascending=False)
    - summary["mean_fairness_reciprocity_utility"].rank(ascending=False)
)

summary.to_csv(TABLES / "fairness_reciprocity_welfare_summary.csv", index=False)

df["reciprocity_quartile"] = pd.qcut(df["reciprocity_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
distribution = df.groupby(["regime", "reciprocity_quartile"], observed=False).agg(
    agents=("agent_id", "count"),
    mean_fairness_reciprocity_utility=("fairness_reciprocity_utility", "mean"),
    rejection_rate=("rejected", "mean"),
    punishment_rate=("punished", "mean"),
    cooperation_rate=("cooperated", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
distribution.to_csv(TABLES / "fairness_reciprocity_distributional_summary.csv", index=False)

rows = []
for process_weight in [0.75, 1.00, 1.25]:
    for rejection_cost_weight in [0.50, 1.00, 1.50]:
        for punishment_cost_weight in [0.50, 1.00, 1.50]:
            alt = (
                df["fairness_reciprocity_utility"]
                + process_weight * 0.25 * df["process_fairness"]
                + 0.15 * df["cooperated"]
                - rejection_cost_weight * 0.20 * df["rejected"]
                - punishment_cost_weight * 0.10 * df["punished"]
            )
            tmp = df.assign(alt_total_welfare=alt)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "process_weight": process_weight,
                    "rejection_cost_weight": rejection_cost_weight,
                    "punishment_cost_weight": punishment_cost_weight,
                    "regime": regime,
                    "mean_alt_total_welfare": sub["alt_total_welfare"].mean(),
                })
pd.DataFrame(rows).to_csv(DIAG / "fairness_reciprocity_welfare_sensitivity.csv", index=False)

print(summary)
