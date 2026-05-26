"""Welfare analysis for behavioral design regimes."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAGNOSTICS = ROOT / "outputs" / "model_diagnostics"

DIAGNOSTICS.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_interface_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_interface_panel.py first."
    )

df = pd.read_csv(data_path)

welfare_summary = df.groupby("regime").agg(
    users=("user_id", "count"),
    join_rate=("joined", "mean"),
    retention_rate=("retained", "mean"),
    consent_rate=("consented", "mean"),
    mean_user_welfare=("user_welfare", "mean"),
    mean_platform_value=("platform_value", "mean"),
    mean_welfare_platform_gap=("welfare_platform_gap", "mean"),
    mean_friction_asymmetry=("friction_asymmetry", "mean"),
).reset_index()

welfare_summary["retention_minus_welfare_signal"] = (
    welfare_summary["retention_rate"] - welfare_summary["mean_user_welfare"]
)

welfare_summary["dark_pattern_risk_flag"] = (
    (welfare_summary["mean_friction_asymmetry"] > 0.25)
    & (welfare_summary["mean_welfare_platform_gap"] > welfare_summary["mean_welfare_platform_gap"].median())
).astype(int)

welfare_summary.to_csv(TABLES / "welfare_regime_summary.csv", index=False)

# Sensitivity to alternative autonomy/privacy weights.
sensitivity_rows = []
for autonomy_weight in [0.3, 0.7, 1.1]:
    for privacy_weight in [0.3, 0.7, 1.1]:
        alt_welfare = (
            df["joined"] * (df["baseline_value"] + 0.35 * df["reward_intensity"])
            - autonomy_weight * df["friction_asymmetry"].clip(lower=0) * df["autonomy_preference"]
            - privacy_weight * df["data_extraction_intensity"] * df["privacy_sensitivity"] * df["consented"]
            - 0.45 * df["cognitive_overload"]
        )

        tmp = df.assign(alt_user_welfare=alt_welfare)
        for regime, sub in tmp.groupby("regime"):
            sensitivity_rows.append({
                "autonomy_weight": autonomy_weight,
                "privacy_weight": privacy_weight,
                "regime": regime,
                "mean_alt_user_welfare": sub["alt_user_welfare"].mean(),
            })

pd.DataFrame(sensitivity_rows).to_csv(
    DIAGNOSTICS / "welfare_weight_sensitivity.csv", index=False
)

print("Wrote welfare summary and sensitivity diagnostics.")
print(welfare_summary)
