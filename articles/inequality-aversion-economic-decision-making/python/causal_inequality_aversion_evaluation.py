from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_inequality_aversion_experiment.csv")

outcomes = [
    "social_preference_utility",
    "rejected",
    "support_redistribution",
    "process_legitimacy",
    "total_welfare",
]
treatments = ["advantageous_treat", "disadvantageous_treat"]
controls = ["alpha", "beta", "redistribution_norm", "merit_belief", "institutional_trust", "process_fairness_sensitivity"]

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
    base = (df["advantageous_treat"] == 0) & (df["disadvantageous_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_inequality_aversion_treatment_effects.csv", index=False)

df["alpha_quartile"] = pd.qcut(df["alpha"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
het = []
for q, sub in df.groupby("alpha_quartile", observed=False):
    base = sub.loc[(sub["advantageous_treat"] == 0) & (sub["disadvantageous_treat"] == 0), "total_welfare"].mean()
    for term in treatments:
        het.append({
            "group_variable": "alpha",
            "group": str(q),
            "term": term,
            "outcome": "total_welfare",
            "difference_from_equal_distribution": sub.loc[sub[term] == 1, "total_welfare"].mean() - base,
            "n": len(sub),
        })
pd.DataFrame(het).to_csv(REG / "python_inequality_aversion_heterogeneous_welfare_effects.csv", index=False)

summary = df.groupby("regime").agg(
    n=("agent_id", "count"),
    mean_self_payoff=("self_payoff", "mean"),
    mean_social_preference_utility=("social_preference_utility", "mean"),
    rejection_rate=("rejected", "mean"),
    redistribution_support_rate=("support_redistribution", "mean"),
    mean_process_legitimacy=("process_legitimacy", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
summary.to_csv(TABLES / "inequality_aversion_regime_summary.csv", index=False)
print(summary)
