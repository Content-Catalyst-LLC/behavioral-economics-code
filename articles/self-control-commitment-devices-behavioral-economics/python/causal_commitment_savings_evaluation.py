from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_commitment_savings_experiment.csv")

outcomes = [
    "accumulated_savings",
    "actual_savings",
    "withdrawal",
    "welfare",
]
treatments = ["medium_commitment_treat", "high_commitment_treat"]
controls = [
    "beta",
    "sophistication",
    "liquidity_need",
    "emergency_risk",
    "automation_strength",
    "flexibility",
]

rows = []
try:
    import statsmodels.api as sm
    for outcome in outcomes:
        X = sm.add_constant(df[treatments + controls])
        model = sm.OLS(df[outcome], X).fit(cov_type="HC1")
        for term in treatments:
            rows.append({
                "outcome": outcome,
                "term": term,
                "estimate": model.params[term],
                "std_error_hc1": model.bse[term],
                "p_value": model.pvalues[term],
                "n": int(model.nobs),
                "r_squared": model.rsquared,
            })
except Exception as exc:
    base = (df["medium_commitment_treat"] == 0) & (df["high_commitment_treat"] == 0)
    for outcome in outcomes:
        base_mean = df.loc[base, outcome].mean()
        for term in treatments:
            rows.append({
                "outcome": outcome,
                "term": term,
                "estimate": df.loc[df[term] == 1, outcome].mean() - base_mean,
                "std_error_hc1": np.nan,
                "p_value": np.nan,
                "n": len(df),
                "note": f"Fallback difference-in-means used: {exc}",
            })

pd.DataFrame(rows).to_csv(REG / "python_commitment_savings_treatment_effects.csv", index=False)

df["beta_quartile"] = pd.qcut(df["beta"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["liquidity_need_quartile"] = pd.qcut(df["liquidity_need"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

beta_heterogeneity = df.groupby(["regime", "beta_quartile"], observed=False).agg(
    mean_accumulated_savings=("accumulated_savings", "mean"),
    mean_welfare=("welfare", "mean"),
    mean_withdrawal=("withdrawal", "mean"),
).reset_index()
beta_heterogeneity.to_csv(REG / "python_commitment_beta_heterogeneity.csv", index=False)

liquidity_heterogeneity = df.groupby(["regime", "liquidity_need_quartile"], observed=False).agg(
    mean_accumulated_savings=("accumulated_savings", "mean"),
    mean_welfare=("welfare", "mean"),
    mean_withdrawal=("withdrawal", "mean"),
).reset_index()
liquidity_heterogeneity.to_csv(REG / "python_commitment_liquidity_heterogeneity.csv", index=False)

print("Wrote Python commitment treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
