from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_availability_bias_panel.csv")

outcomes = [
    "subjective_probability",
    "calibration_error",
    "participate_in_risky_asset",
    "insurance_demand",
    "policy_support",
    "welfare_proxy",
]
treatments = ["medium_availability_treat", "high_availability_treat"]
controls = [
    "availability_sensitivity",
    "numeracy",
    "trust_in_statistics",
    "risk_tolerance",
    "prior_experience",
    "availability_score",
    "base_rate_disclosure",
    "emotional_intensity",
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
    base = (df["medium_availability_treat"] == 0) & (df["high_availability_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_availability_bias_treatment_effects.csv", index=False)

df["availability_sensitivity_quartile"] = pd.qcut(df["availability_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["numeracy_quartile"] = pd.qcut(df["numeracy"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["trust_quartile"] = pd.qcut(df["trust_in_statistics"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["risk_tolerance_quartile"] = pd.qcut(df["risk_tolerance"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("availability_sensitivity_quartile", "python_availability_bias_sensitivity_heterogeneity.csv"),
    ("numeracy_quartile", "python_availability_bias_numeracy_heterogeneity.csv"),
    ("trust_quartile", "python_availability_bias_trust_heterogeneity.csv"),
    ("risk_tolerance_quartile", "python_availability_bias_risk_tolerance_heterogeneity.csv"),
]:
    het = df.groupby(["regime", group_col], observed=False).agg(
        mean_subjective_probability=("subjective_probability", "mean"),
        mean_calibration_error=("calibration_error", "mean"),
        insurance_demand_rate=("insurance_demand", "mean"),
        policy_support_rate=("policy_support", "mean"),
        mean_welfare_proxy=("welfare_proxy", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

experience_heterogeneity = df.groupby(["regime", "prior_experience"], observed=False).agg(
    mean_subjective_probability=("subjective_probability", "mean"),
    mean_calibration_error=("calibration_error", "mean"),
    insurance_demand_rate=("insurance_demand", "mean"),
    policy_support_rate=("policy_support", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
).reset_index()
experience_heterogeneity.to_csv(REG / "python_availability_bias_prior_experience_heterogeneity.csv", index=False)

print("Wrote Python availability-bias treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
