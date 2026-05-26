from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_trust_cooperation_experiment.csv")

outcomes = ["trusted", "reciprocated", "punished", "transaction_cost_reduction", "monitoring_cost", "total_welfare"]
treatments = ["reciprocal_market_treat", "institutional_support_treat"]
controls = ["trust_propensity", "reciprocity", "punishment_willingness", "institutional_trust", "betrayal_sensitivity", "monitoring_cost_sensitivity"]

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
    base = (df["reciprocal_market_treat"] == 0) & (df["institutional_support_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_trust_cooperation_treatment_effects.csv", index=False)

df["trust_propensity_quartile"] = pd.qcut(df["trust_propensity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
het = []
for q, sub in df.groupby("trust_propensity_quartile", observed=False):
    base = sub.loc[(sub["reciprocal_market_treat"] == 0) & (sub["institutional_support_treat"] == 0), "total_welfare"].mean()
    for term in treatments:
        het.append({
            "group_variable": "trust_propensity",
            "group": str(q),
            "term": term,
            "outcome": "total_welfare",
            "difference_from_low_trust_exchange": sub.loc[sub[term] == 1, "total_welfare"].mean() - base,
            "n": len(sub),
        })
pd.DataFrame(het).to_csv(REG / "python_trust_cooperation_heterogeneous_welfare_effects.csv", index=False)

summary = df.groupby("regime").agg(
    n=("agent_id", "count"),
    trust_rate=("trusted", "mean"),
    reciprocity_rate=("reciprocated", "mean"),
    punishment_rate=("punished", "mean"),
    mean_transaction_cost_reduction=("transaction_cost_reduction", "mean"),
    mean_monitoring_cost=("monitoring_cost", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
summary.to_csv(TABLES / "trust_cooperation_regime_summary.csv", index=False)
print(summary)
