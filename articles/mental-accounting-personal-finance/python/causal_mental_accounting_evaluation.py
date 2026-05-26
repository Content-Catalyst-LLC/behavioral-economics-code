from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_mental_accounting_household_panel.csv")

outcomes = [
    "windfall_consumption",
    "total_debt_payment",
    "remaining_debt",
    "remaining_liquid_savings",
    "inefficiency_gap",
    "annual_interest_cost",
    "resilience_index",
]
treatments = ["integrated_prompt_treat", "unified_money_treat"]
controls = [
    "monthly_income",
    "liquid_savings",
    "credit_card_debt",
    "windfall",
    "savings_label_strength",
    "emergency_need_risk",
    "present_bias",
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
    base = (df["integrated_prompt_treat"] == 0) & (df["unified_money_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_mental_accounting_treatment_effects.csv", index=False)

df["label_quartile"] = pd.qcut(df["savings_label_strength"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["emergency_risk_quartile"] = pd.qcut(df["emergency_need_risk"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

label_heterogeneity = df.groupby(["regime", "label_quartile"], observed=False).agg(
    mean_total_debt_payment=("total_debt_payment", "mean"),
    mean_remaining_debt=("remaining_debt", "mean"),
    mean_inefficiency_gap=("inefficiency_gap", "mean"),
    mean_resilience_index=("resilience_index", "mean"),
).reset_index()
label_heterogeneity.to_csv(REG / "python_mental_accounting_label_heterogeneity.csv", index=False)

emergency_heterogeneity = df.groupby(["regime", "emergency_risk_quartile"], observed=False).agg(
    mean_remaining_liquid_savings=("remaining_liquid_savings", "mean"),
    mean_remaining_debt=("remaining_debt", "mean"),
    mean_inefficiency_gap=("inefficiency_gap", "mean"),
    mean_resilience_index=("resilience_index", "mean"),
).reset_index()
emergency_heterogeneity.to_csv(REG / "python_mental_accounting_emergency_risk_heterogeneity.csv", index=False)

print("Wrote Python mental-accounting treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
