"""Econometric policy evaluation for behavioral regulatory regimes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REGRESSION = ROOT / "outputs" / "regression_tables"

REGRESSION.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_regulatory_policy_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_regulatory_policy_panel.py first."
    )

df = pd.read_csv(data_path)

outcomes = [
    "complied",
    "total_welfare",
    "social_benefit",
    "compliance_cost",
    "enforcement_cost",
    "administrative_cost",
]
controls = [
    "trust",
    "norm_sensitivity",
    "burden_sensitivity",
    "loss_aversion",
    "private_gain_noncompliance",
    "compliance_capacity",
]
treatments = ["simplification_treat", "integrated_treat"]

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
    base_mask = (df["simplification_treat"] == 0) & (df["integrated_treat"] == 0)

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

results.to_csv(REGRESSION / "python_regulatory_policy_treatment_effects.csv", index=False)

# Heterogeneous treatment effects by trust quartile.
df["trust_quartile"] = pd.qcut(df["trust"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

heterogeneity_rows = []
for q, sub in df.groupby("trust_quartile", observed=False):
    base = sub.loc[(sub["simplification_treat"] == 0) & (sub["integrated_treat"] == 0), "total_welfare"].mean()
    for var in treatments:
        treated = sub.loc[sub[var] == 1, "total_welfare"].mean()
        heterogeneity_rows.append({
            "group_variable": "trust",
            "group": str(q),
            "term": var,
            "outcome": "total_welfare",
            "difference_from_sanction_heavy_deterrence": treated - base,
            "n": len(sub),
        })

pd.DataFrame(heterogeneity_rows).to_csv(
    REGRESSION / "python_regulatory_policy_heterogeneous_welfare_effects.csv", index=False
)

summary = df.groupby("regime").agg(
    n=("agent_id", "count"),
    compliance_rate=("complied", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    mean_social_benefit=("social_benefit", "mean"),
    mean_compliance_cost=("compliance_cost", "mean"),
    mean_enforcement_cost=("enforcement_cost", "mean"),
    mean_administrative_cost=("administrative_cost", "mean"),
).reset_index()

summary.to_csv(TABLES / "regulatory_policy_regime_summary.csv", index=False)

print("Wrote Python regulatory policy treatment effects and heterogeneity tables.")
print(summary)
