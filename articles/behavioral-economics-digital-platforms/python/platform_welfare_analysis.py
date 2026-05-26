"""Welfare and concentration analysis for digital platform regimes."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAGNOSTICS = ROOT / "outputs" / "model_diagnostics"

DIAGNOSTICS.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_platform_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_platform_panel.py first."
    )

df = pd.read_csv(data_path)

summary = df.groupby("regime").agg(
    users=("user_id", "count"),
    click_rate=("clicked", "mean"),
    retention_rate=("retained", "mean"),
    consent_rate=("consented", "mean"),
    mean_exposure_quality=("exposure_quality", "mean"),
    mean_user_welfare=("user_welfare", "mean"),
    mean_platform_value=("platform_value", "mean"),
    mean_welfare_platform_gap=("welfare_platform_gap", "mean"),
    mean_recommendation_intensity=("recommendation_intensity", "mean"),
    mean_social_proof=("social_proof", "mean"),
).reset_index()

summary["platform_welfare_divergence_flag"] = (
    (summary["mean_welfare_platform_gap"] > summary["mean_welfare_platform_gap"].median())
    & (summary["mean_user_welfare"] < summary["mean_user_welfare"].median())
).astype(int)

summary.to_csv(TABLES / "platform_welfare_regime_summary.csv", index=False)

# Sensitivity to alternative welfare weights.
sensitivity_rows = []
for privacy_weight in [0.25, 0.45, 0.75]:
    for overload_weight in [0.15, 0.30, 0.50]:
        for friction_weight in [0.05, 0.15, 0.30]:
            alt_welfare = (
                df["clicked"] * df["exposure_quality"]
                - overload_weight * df["cognitive_overload"]
                - privacy_weight * df["privacy_sensitivity"] * df["data_extraction_intensity"] * df["consented"]
                - friction_weight * df["friction"]
            )

            tmp = df.assign(alt_user_welfare=alt_welfare)
            for regime, sub in tmp.groupby("regime"):
                sensitivity_rows.append({
                    "privacy_weight": privacy_weight,
                    "overload_weight": overload_weight,
                    "friction_weight": friction_weight,
                    "regime": regime,
                    "mean_alt_user_welfare": sub["alt_user_welfare"].mean(),
                })

pd.DataFrame(sensitivity_rows).to_csv(
    DIAGNOSTICS / "platform_welfare_weight_sensitivity.csv", index=False
)

print("Wrote platform welfare summary and sensitivity diagnostics.")
print(summary)
