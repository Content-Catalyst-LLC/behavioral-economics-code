from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_present_bias_experiment.csv")

outcomes = [
    "choose_delayed",
    "cumulative_delayed_choices",
    "cumulative_welfare",
]
treatments = ["medium_commitment_treat", "strong_commitment_treat"]
controls = [
    "beta",
    "delta",
    "sophistication",
    "liquidity_need",
    "temptation_strength",
    "future_goal_value",
    "commitment_cost",
    "reminder_strength",
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
    base = (df["medium_commitment_treat"] == 0) & (df["strong_commitment_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_present_bias_treatment_effects.csv", index=False)

df["beta_quartile"] = pd.qcut(df["beta"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["liquidity_quartile"] = pd.qcut(df["liquidity_need"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["temptation_quartile"] = pd.qcut(df["temptation_strength"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

beta_heterogeneity = df.groupby(["regime", "beta_quartile"], observed=False).agg(
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
).reset_index()
beta_heterogeneity.to_csv(REG / "python_present_bias_beta_heterogeneity.csv", index=False)

liquidity_heterogeneity = df.groupby(["regime", "liquidity_quartile"], observed=False).agg(
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
).reset_index()
liquidity_heterogeneity.to_csv(REG / "python_present_bias_liquidity_heterogeneity.csv", index=False)

temptation_heterogeneity = df.groupby(["regime", "temptation_quartile"], observed=False).agg(
    mean_choose_delayed=("choose_delayed", "mean"),
    mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
    mean_cumulative_welfare=("cumulative_welfare", "mean"),
).reset_index()
temptation_heterogeneity.to_csv(REG / "python_present_bias_temptation_heterogeneity.csv", index=False)

print("Wrote Python present-bias treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
