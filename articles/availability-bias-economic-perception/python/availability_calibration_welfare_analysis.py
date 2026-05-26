from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_availability_bias_panel.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_availability_score=("availability_score", "mean"),
    mean_subjective_probability=("subjective_probability", "mean"),
    mean_calibration_error=("calibration_error", "mean"),
    mean_absolute_calibration_error=("calibration_error", lambda s: s.abs().mean()),
    share_participating_risky_asset=("participate_in_risky_asset", "mean"),
    insurance_demand_rate=("insurance_demand", "mean"),
    policy_support_rate=("policy_support", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
    mean_base_rate_disclosure=("base_rate_disclosure", "mean"),
    mean_emotional_intensity=("emotional_intensity", "mean"),
).reset_index()

summary["calibration_quality"] = 1 - summary["mean_absolute_calibration_error"]
summary.to_csv(TABLES / "availability_calibration_welfare_summary.csv", index=False)

rows = []
for calibration_weight in [0.75, 1.00, 1.25]:
    for comprehension_weight in [0.75, 1.00, 1.25]:
        for emotional_burden_weight in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["welfare_proxy"]
                - calibration_weight * df["calibration_error"].abs()
                + comprehension_weight * df["base_rate_disclosure"] * df["numeracy"] * 0.08
                - emotional_burden_weight * df["emotional_intensity"] * df["availability_score"] * 0.06
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "calibration_weight": calibration_weight,
                    "comprehension_weight": comprehension_weight,
                    "emotional_burden_weight": emotional_burden_weight,
                    "regime": regime,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "availability_welfare_sensitivity.csv", index=False)

print(summary)
