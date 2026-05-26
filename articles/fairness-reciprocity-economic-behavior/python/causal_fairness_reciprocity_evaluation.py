from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_fairness_reciprocity_experiment.csv")

outcomes = [
    "fairness_reciprocity_utility",
    "rejected",
    "punished",
    "cooperated",
    "process_fairness",
    "total_welfare",
]
treatments = [
    "unequal_cooperative_treat",
    "unequal_noncooperative_treat",
    "exploitative_low_process_treat",
]
controls = [
    "fairness_sensitivity",
    "reciprocity_sensitivity",
    "trust",
    "punishment_willingness",
    "process_fairness_weight",
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
    base = (
        (df["unequal_cooperative_treat"] == 0)
        & (df["unequal_noncooperative_treat"] == 0)
        & (df["exploitative_low_process_treat"] == 0)
    )
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

pd.DataFrame(rows).to_csv(REG / "python_fairness_reciprocity_treatment_effects.csv", index=False)

df["fairness_quartile"] = pd.qcut(df["fairness_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
het = []
for q, sub in df.groupby("fairness_quartile", observed=False):
    base = sub.loc[
        (sub["unequal_cooperative_treat"] == 0)
        & (sub["unequal_noncooperative_treat"] == 0)
        & (sub["exploitative_low_process_treat"] == 0),
        "total_welfare"
    ].mean()
    for term in treatments:
        het.append({
            "group_variable": "fairness_sensitivity",
            "group": str(q),
            "term": term,
            "outcome": "total_welfare",
            "difference_from_fair_cooperative_regime": sub.loc[sub[term] == 1, "total_welfare"].mean() - base,
            "n": len(sub),
        })
pd.DataFrame(het).to_csv(REG / "python_fairness_reciprocity_heterogeneous_welfare_effects.csv", index=False)

summary = df.groupby("regime").agg(
    n=("agent_id", "count"),
    mean_self_payoff=("self_payoff", "mean"),
    mean_fairness_reciprocity_utility=("fairness_reciprocity_utility", "mean"),
    rejection_rate=("rejected", "mean"),
    punishment_rate=("punished", "mean"),
    cooperation_rate=("cooperated", "mean"),
    mean_process_fairness=("process_fairness", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
summary.to_csv(TABLES / "fairness_reciprocity_regime_summary.csv", index=False)
print(summary)
