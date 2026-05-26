from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_heuristics_biases_panel.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_estimate=("estimated_value", "mean"),
    mean_judgment_error=("judgment_error", "mean"),
    mean_absolute_error=("absolute_error", "mean"),
    mean_decision_quality=("decision_quality", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
    mean_correction_capacity=("correction_capacity", "mean"),
    mean_cognitive_load=("cognitive_load", "mean"),
    mean_disclosure_quality=("disclosure_quality", "mean"),
    mean_debiasing_support=("debiasing_support", "mean"),
).reset_index()

summary["accuracy_index"] = 1 - summary["mean_absolute_error"]
summary.to_csv(TABLES / "correction_capacity_welfare_summary.csv", index=False)

rows = []
for accuracy_weight in [0.75, 1.00, 1.25]:
    for comprehension_weight in [0.75, 1.00, 1.25]:
        for burden_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["welfare_proxy"]
                - accuracy_weight * df["absolute_error"]
                + comprehension_weight * df["correction_capacity"] * 0.08
                - burden_weight * df["cognitive_load"] * 0.08
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "accuracy_weight": accuracy_weight,
                    "comprehension_weight": comprehension_weight,
                    "burden_weight": burden_weight,
                    "regime": regime,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "heuristics_biases_welfare_sensitivity.csv", index=False)

print(summary)
