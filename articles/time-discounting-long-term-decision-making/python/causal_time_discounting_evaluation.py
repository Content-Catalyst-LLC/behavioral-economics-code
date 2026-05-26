from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_time_discounting_experiment.csv")

outcomes = [
    "choose_delayed",
    "cumulative_delayed_choices",
    "cumulative_welfare",
]
treatments = ["present_bias_treat", "commitment_support_treat"]
controls = [
    "beta",
    "delta",
    "sophistication",
    "liquidity_need",
    "immediate_reward_base",
    "future_goal_value",
    "commitment_support",
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
    base = (df["present_bias_treat"] == 0) & (df["commitment_support_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_time_discounting_treatment_effects.csv", index=False)

df["beta_quartile"] = pd.qcut(df["beta"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["delta_quartile"] = pd.qcut(df["delta"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["liquidity_quartile"] = pd.qcut(df["liquidity_need"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("beta_quartile", "python_time_discounting_beta_heterogeneity.csv"),
    ("delta_quartile", "python_time_discounting_delta_heterogeneity.csv"),
    ("liquidity_quartile", "python_time_discounting_liquidity_heterogeneity.csv"),
]:
    het = df.groupby(["regime", group_col], observed=False).agg(
        mean_choose_delayed=("choose_delayed", "mean"),
        mean_cumulative_delayed_choices=("cumulative_delayed_choices", "mean"),
        mean_cumulative_welfare=("cumulative_welfare", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

print("Wrote Python time-discounting treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
