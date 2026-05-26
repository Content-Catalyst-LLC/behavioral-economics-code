from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_bounded_rationality_panel.csv")

outcomes = [
    "chosen_value",
    "net_value",
    "optimization_gap",
    "chosen_index",
]
controls = [
    "medium_constraint_treat",
    "high_constraint_treat",
    "aspiration",
    "search_cost",
    "time_budget",
    "cognitive_capacity",
    "numeracy",
    "stress",
    "institutional_trust",
    "digital_access",
    "income_security",
    "administrative_capacity",
]

rows = []
try:
    import statsmodels.api as sm
    for outcome in outcomes:
        X = sm.add_constant(df[controls])
        model = sm.OLS(df[outcome], X).fit(cov_type="HC1")
        for term in controls:
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
    base = (df["medium_constraint_treat"] == 0) & (df["high_constraint_treat"] == 0)
    for outcome in outcomes:
        base_mean = df.loc[base, outcome].mean()
        for term in ["medium_constraint_treat", "high_constraint_treat"]:
            rows.append({
                "outcome": outcome,
                "term": term,
                "estimate": df.loc[df[term] == 1, outcome].mean() - base_mean,
                "std_error_hc1": np.nan,
                "p_value": np.nan,
                "n": len(df),
                "note": f"Fallback difference-in-means used: {exc}",
            })

pd.DataFrame(rows).to_csv(REG / "python_bounded_rationality_estimates.csv", index=False)

quartile_columns = [
    ("aspiration", "python_bounded_rationality_aspiration_heterogeneity.csv"),
    ("search_cost", "python_bounded_rationality_search_cost_heterogeneity.csv"),
    ("cognitive_capacity", "python_bounded_rationality_capacity_heterogeneity.csv"),
    ("time_budget", "python_bounded_rationality_time_budget_heterogeneity.csv"),
    ("stress", "python_bounded_rationality_stress_heterogeneity.csv"),
    ("numeracy", "python_bounded_rationality_numeracy_heterogeneity.csv"),
    ("institutional_trust", "python_bounded_rationality_trust_heterogeneity.csv"),
    ("digital_access", "python_bounded_rationality_digital_access_heterogeneity.csv"),
    ("administrative_capacity", "python_bounded_rationality_administrative_capacity_heterogeneity.csv"),
]

for col, out_name in quartile_columns:
    qcol = f"{col}_quartile"
    df[qcol] = pd.qcut(df[col], 4, labels=["Q1", "Q2", "Q3", "Q4"])
    het = df.groupby(["regime", qcol], observed=False).agg(
        mean_chosen_value=("chosen_value", "mean"),
        mean_net_value=("net_value", "mean"),
        mean_optimization_gap=("optimization_gap", "mean"),
        mean_search_depth=("chosen_index", "mean"),
        mean_time_used=("cumulative_time", "mean"),
        mean_cognitive_load=("cumulative_load", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

print("Wrote Python bounded-rationality estimates and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
