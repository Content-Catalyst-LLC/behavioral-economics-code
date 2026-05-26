"""Econometric policy evaluation for behavioral environmental policy regimes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REGRESSION = ROOT / "outputs" / "regression_tables"

REGRESSION.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_environmental_policy_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_environmental_policy_panel.py first."
    )

df = pd.read_csv(data_path)

outcomes = [
    "adopted",
    "total_welfare",
    "private_benefit",
    "environmental_benefit",
    "fiscal_cost",
    "admin_cost",
]
controls = [
    "income",
    "energy_burden",
    "env_concern",
    "present_bias",
    "norm_sensitivity",
    "friction_sensitivity",
    "loss_aversion",
    "trust",
]
treatments = ["norm_default_treat", "integrated_treat"]

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
    base_mask = (df["norm_default_treat"] == 0) & (df["integrated_treat"] == 0)

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

results.to_csv(REGRESSION / "python_environmental_policy_treatment_effects.csv", index=False)

# Heterogeneous treatment effects by energy burden quartile.
df["energy_burden_quartile"] = pd.qcut(df["energy_burden"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

heterogeneity_rows = []
for q, sub in df.groupby("energy_burden_quartile", observed=False):
    base = sub.loc[(sub["norm_default_treat"] == 0) & (sub["integrated_treat"] == 0), "total_welfare"].mean()
    for var in treatments:
        treated = sub.loc[sub[var] == 1, "total_welfare"].mean()
        heterogeneity_rows.append({
            "group_variable": "energy_burden",
            "group": str(q),
            "term": var,
            "outcome": "total_welfare",
            "difference_from_price_signal_only": treated - base,
            "n": len(sub),
        })

pd.DataFrame(heterogeneity_rows).to_csv(
    REGRESSION / "python_environmental_policy_heterogeneous_welfare_effects.csv", index=False
)

summary = df.groupby("regime").agg(
    n=("household_id", "count"),
    adoption_rate=("adopted", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_private_benefit=("private_benefit", "mean"),
    mean_environmental_benefit=("environmental_benefit", "mean"),
    mean_fiscal_cost=("fiscal_cost", "mean"),
    mean_admin_cost=("admin_cost", "mean"),
).reset_index()

summary.to_csv(TABLES / "environmental_policy_regime_summary.csv", index=False)

print("Wrote Python environmental policy treatment effects and heterogeneity tables.")
print(summary)
