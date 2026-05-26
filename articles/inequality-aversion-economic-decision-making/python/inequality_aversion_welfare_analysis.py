from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_inequality_aversion_experiment.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_material_payoff=("self_payoff", "mean"),
    mean_other_payoff=("other_payoff", "mean"),
    mean_inequality_gap=("inequality_gap", "mean"),
    mean_social_preference_utility=("social_preference_utility", "mean"),
    rejection_rate=("rejected", "mean"),
    redistribution_support_rate=("support_redistribution", "mean"),
    mean_process_legitimacy=("process_legitimacy", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()

summary["material_vs_social_rank_gap"] = (
    summary["mean_material_payoff"].rank(ascending=False)
    - summary["mean_social_preference_utility"].rank(ascending=False)
)

summary.to_csv(TABLES / "inequality_aversion_welfare_summary.csv", index=False)

df["beta_quartile"] = pd.qcut(df["beta"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
distribution = df.groupby(["regime", "beta_quartile"], observed=False).agg(
    agents=("agent_id", "count"),
    mean_social_preference_utility=("social_preference_utility", "mean"),
    rejection_rate=("rejected", "mean"),
    redistribution_support_rate=("support_redistribution", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
distribution.to_csv(TABLES / "inequality_aversion_distributional_summary.csv", index=False)

rows = []
for social_weight in [0.75, 1.00, 1.25]:
    for legitimacy_weight in [0.50, 1.00, 1.50]:
        for rejection_cost_weight in [0.50, 1.00, 1.50]:
            alt = (
                df["self_payoff"]
                + social_weight * df["social_preference_utility"]
                + legitimacy_weight * 0.35 * df["process_legitimacy"]
                + 0.10 * df["support_redistribution"]
                - rejection_cost_weight * 0.20 * df["rejected"]
            )
            tmp = df.assign(alt_total_welfare=alt)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "social_preference_weight": social_weight,
                    "legitimacy_weight": legitimacy_weight,
                    "rejection_cost_weight": rejection_cost_weight,
                    "regime": regime,
                    "mean_alt_total_welfare": sub["alt_total_welfare"].mean(),
                })
pd.DataFrame(rows).to_csv(DIAG / "inequality_aversion_welfare_sensitivity.csv", index=False)

print(summary)
