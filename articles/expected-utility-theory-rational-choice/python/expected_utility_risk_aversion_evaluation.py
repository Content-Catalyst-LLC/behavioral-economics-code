from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_expected_utility_panel.csv")

outcomes = [
    "choose_risky_eu",
    "observed_choose_risky",
    "certainty_equivalent_payoff",
    "risk_premium",
]
controls = [
    "medium_risk_aversion_treat",
    "high_risk_aversion_treat",
    "wealth",
    "rho",
    "numeracy",
    "liquidity_constraint",
    "trust",
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
    base = (df["medium_risk_aversion_treat"] == 0) & (df["high_risk_aversion_treat"] == 0)
    for outcome in outcomes:
        base_mean = df.loc[base, outcome].mean()
        for term in ["medium_risk_aversion_treat", "high_risk_aversion_treat"]:
            rows.append({
                "outcome": outcome,
                "term": term,
                "estimate": df.loc[df[term] == 1, outcome].mean() - base_mean,
                "std_error_hc1": np.nan,
                "p_value": np.nan,
                "n": len(df),
                "note": f"Fallback difference-in-means used: {exc}",
            })

pd.DataFrame(rows).to_csv(REG / "python_expected_utility_estimates.csv", index=False)

df["rho_quartile"] = pd.qcut(df["rho"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["wealth_quartile"] = pd.qcut(df["wealth"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["numeracy_quartile"] = pd.qcut(df["numeracy"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["liquidity_quartile"] = pd.qcut(df["liquidity_constraint"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["trust_quartile"] = pd.qcut(df["trust"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("rho_quartile", "python_expected_utility_risk_aversion_heterogeneity.csv"),
    ("wealth_quartile", "python_expected_utility_wealth_heterogeneity.csv"),
    ("numeracy_quartile", "python_expected_utility_numeracy_heterogeneity.csv"),
    ("liquidity_quartile", "python_expected_utility_liquidity_heterogeneity.csv"),
    ("trust_quartile", "python_expected_utility_trust_heterogeneity.csv"),
]:
    het = df.groupby(["regime", group_col], observed=False).agg(
        share_choose_risky_eu=("choose_risky_eu", "mean"),
        share_choose_risky_observed=("observed_choose_risky", "mean"),
        mean_certainty_equivalent=("certainty_equivalent_payoff", "mean"),
        mean_risk_premium=("risk_premium", "mean"),
        mean_rho=("rho", "mean"),
        mean_wealth=("wealth", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

print("Wrote Python expected-utility regression and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
