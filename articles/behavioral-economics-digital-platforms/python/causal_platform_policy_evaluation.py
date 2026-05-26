"""Econometric policy evaluation for digital platform regimes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REGRESSION = ROOT / "outputs" / "regression_tables"

REGRESSION.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_platform_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_platform_panel.py first."
    )

df = pd.read_csv(data_path)

outcomes = ["clicked", "retained", "consented", "user_welfare", "platform_value", "welfare_platform_gap"]
controls = [
    "baseline_user_value",
    "cognitive_overload",
    "privacy_sensitivity",
    "digital_literacy",
    "social_susceptibility",
]
treatments = ["engagement_optimized", "socially_amplified"]

rows = []

try:
    import statsmodels.api as sm

    for outcome in outcomes:
        X = df[treatments + controls].copy()
        X = sm.add_constant(X)
        y = df[outcome]
        model = sm.OLS(y, X).fit(cov_type="HC1")

        for var in treatments:
            rows.append({
                "outcome": outcome,
                "term": var,
                "estimate": model.params[var],
                "std_error_hc1": model.bse[var],
                "p_value": model.pvalues[var],
                "n": int(model.nobs),
                "r_squared": model.rsquared,
            })

    results = pd.DataFrame(rows)

except Exception as exc:
    fallback_rows = []
    base_mask = (df["engagement_optimized"] == 0) & (df["socially_amplified"] == 0)

    for outcome in outcomes:
        base = df.loc[base_mask, outcome].mean()
        for var in treatments:
            treated = df.loc[df[var] == 1, outcome].mean()
            fallback_rows.append({
                "outcome": outcome,
                "term": var,
                "estimate": treated - base,
                "std_error_hc1": np.nan,
                "p_value": np.nan,
                "n": len(df),
                "r_squared": np.nan,
                "note": f"Fallback difference-in-means used: {exc}",
            })

    results = pd.DataFrame(fallback_rows)

results.to_csv(REGRESSION / "python_platform_treatment_effects.csv", index=False)

# Heterogeneous treatment effects by cognitive overload quartile.
df["overload_quartile"] = pd.qcut(df["cognitive_overload"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

heterogeneity_rows = []
for q, sub in df.groupby("overload_quartile", observed=False):
    base = sub.loc[(sub["engagement_optimized"] == 0) & (sub["socially_amplified"] == 0), "user_welfare"].mean()
    for var in treatments:
        treated = sub.loc[sub[var] == 1, "user_welfare"].mean()
        heterogeneity_rows.append({
            "group_variable": "cognitive_overload",
            "group": str(q),
            "term": var,
            "outcome": "user_welfare",
            "difference_from_neutral_discovery": treated - base,
            "n": len(sub),
        })

pd.DataFrame(heterogeneity_rows).to_csv(
    REGRESSION / "python_platform_heterogeneous_welfare_effects.csv", index=False
)

summary = df.groupby("regime").agg(
    n=("user_id", "count"),
    mean_clicked=("clicked", "mean"),
    mean_retained=("retained", "mean"),
    mean_consented=("consented", "mean"),
    mean_user_welfare=("user_welfare", "mean"),
    mean_platform_value=("platform_value", "mean"),
    mean_welfare_platform_gap=("welfare_platform_gap", "mean"),
).reset_index()

summary.to_csv(TABLES / "platform_policy_regime_summary.csv", index=False)

print("Wrote Python platform treatment effects and heterogeneity tables.")
print(summary)
