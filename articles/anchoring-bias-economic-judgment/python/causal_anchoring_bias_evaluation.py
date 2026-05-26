from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_anchoring_bias_panel.csv")

outcomes = [
    "estimate",
    "bias",
    "absolute_error",
    "decision_quality",
    "welfare_proxy",
]
treatments = ["low_anchor_treat", "high_anchor_treat", "counter_context_treat"]
controls = [
    "anchor_value",
    "adjustment_rate",
    "effective_adjustment",
    "numeracy",
    "confidence",
    "cognitive_load",
    "domain_knowledge",
    "disclosure_quality",
    "counter_anchor_support",
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
    base = (df["low_anchor_treat"] == 0) & (df["high_anchor_treat"] == 0) & (df["counter_context_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_anchoring_bias_treatment_effects.csv", index=False)

df["adjustment_quartile"] = pd.qcut(df["effective_adjustment"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["numeracy_quartile"] = pd.qcut(df["numeracy"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["knowledge_quartile"] = pd.qcut(df["domain_knowledge"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["load_quartile"] = pd.qcut(df["cognitive_load"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["confidence_quartile"] = pd.qcut(df["confidence"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("adjustment_quartile", "python_anchoring_bias_adjustment_heterogeneity.csv"),
    ("numeracy_quartile", "python_anchoring_bias_numeracy_heterogeneity.csv"),
    ("knowledge_quartile", "python_anchoring_bias_knowledge_heterogeneity.csv"),
    ("load_quartile", "python_anchoring_bias_load_heterogeneity.csv"),
    ("confidence_quartile", "python_anchoring_bias_confidence_heterogeneity.csv"),
]:
    het = df.groupby(["regime", group_col], observed=False).agg(
        mean_estimate=("estimate", "mean"),
        mean_bias=("bias", "mean"),
        mean_absolute_error=("absolute_error", "mean"),
        mean_decision_quality=("decision_quality", "mean"),
        mean_welfare_proxy=("welfare_proxy", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

print("Wrote Python anchoring-bias treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
