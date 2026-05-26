from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_loss_aversion_panel.csv")

outcomes = ["choose_risky", "risky_value"]
controls = [
    "loss_frame_treat",
    "mixed_gamble_treat",
    "lambda_loss",
    "alpha_gain",
    "beta_loss",
    "numeracy",
    "income_security",
    "prior_loss_exposure",
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
    base = (df["loss_frame_treat"] == 0) & (df["mixed_gamble_treat"] == 0)
    for outcome in outcomes:
        base_mean = df.loc[base, outcome].mean()
        for term in ["loss_frame_treat", "mixed_gamble_treat"]:
            rows.append({
                "outcome": outcome,
                "term": term,
                "estimate": df.loc[df[term] == 1, outcome].mean() - base_mean,
                "std_error_hc1": np.nan,
                "p_value": np.nan,
                "n": len(df),
                "note": f"Fallback difference-in-means used: {exc}",
            })

pd.DataFrame(rows).to_csv(REG / "python_loss_aversion_frame_estimates.csv", index=False)

df["lambda_quartile"] = pd.qcut(df["lambda_loss"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["security_quartile"] = pd.qcut(df["income_security"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["numeracy_quartile"] = pd.qcut(df["numeracy"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["trust_quartile"] = pd.qcut(df["trust"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("lambda_quartile", "python_loss_aversion_lambda_heterogeneity.csv"),
    ("security_quartile", "python_loss_aversion_security_heterogeneity.csv"),
    ("numeracy_quartile", "python_loss_aversion_numeracy_heterogeneity.csv"),
    ("trust_quartile", "python_loss_aversion_trust_heterogeneity.csv"),
]:
    het = df.groupby(["frame", group_col], observed=False).agg(
        share_choose_risky=("choose_risky", "mean"),
        mean_risky_value=("risky_value", "mean"),
        mean_lambda=("lambda_loss", "mean"),
        mean_income_security=("income_security", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

prior_loss = df.groupby(["frame", "prior_loss_exposure"]).agg(
    share_choose_risky=("choose_risky", "mean"),
    mean_risky_value=("risky_value", "mean"),
    agents=("agent_id", "count"),
).reset_index()
prior_loss.to_csv(REG / "python_loss_aversion_prior_loss_heterogeneity.csv", index=False)

print("Wrote Python loss-aversion frame-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
