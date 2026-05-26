from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_status_quo_bias_panel.csv")

outcomes = [
    "choose_alternative",
    "welfare",
    "effective_switch_cost",
    "effective_status_quo_premium",
    "effective_perceived_loss",
]
treatments = ["active_choice_treat", "pro_switching_treat"]
controls = [
    "objective_gain",
    "switch_cost",
    "loss_aversion",
    "status_quo_premium",
    "uncertainty_sensitivity",
    "decision_fatigue",
    "sophistication",
    "default_shift",
    "switching_support",
    "disclosure_quality",
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
    base = (df["active_choice_treat"] == 0) & (df["pro_switching_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_status_quo_bias_treatment_effects.csv", index=False)

df["switch_cost_quartile"] = pd.qcut(df["switch_cost"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["loss_aversion_quartile"] = pd.qcut(df["loss_aversion"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["decision_fatigue_quartile"] = pd.qcut(df["decision_fatigue"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["uncertainty_quartile"] = pd.qcut(df["uncertainty_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("switch_cost_quartile", "python_status_quo_bias_switching_heterogeneity.csv"),
    ("loss_aversion_quartile", "python_status_quo_bias_loss_aversion_heterogeneity.csv"),
    ("decision_fatigue_quartile", "python_status_quo_bias_decision_fatigue_heterogeneity.csv"),
    ("uncertainty_quartile", "python_status_quo_bias_uncertainty_heterogeneity.csv"),
]:
    het = df.groupby(["regime", group_col], observed=False).agg(
        adoption_rate=("choose_alternative", "mean"),
        mean_welfare=("welfare", "mean"),
        mean_effective_switch_cost=("effective_switch_cost", "mean"),
        mean_status_quo_premium=("effective_status_quo_premium", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

print("Wrote Python status quo bias treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
