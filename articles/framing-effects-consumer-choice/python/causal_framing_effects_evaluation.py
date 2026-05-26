from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_framing_effects_panel.csv")

outcomes = [
    "choose_risky",
    "welfare_proxy",
    "comprehension",
    "adjusted_risky_value",
]
treatments = ["loss_frame_treat", "balanced_frame_treat"]
controls = [
    "loss_aversion",
    "curvature",
    "numeracy",
    "trust",
    "decision_fatigue",
    "frame_strength",
    "disclosure_quality",
    "salience",
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
    base = (df["loss_frame_treat"] == 0) & (df["balanced_frame_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_framing_effects_treatment_effects.csv", index=False)

df["loss_aversion_quartile"] = pd.qcut(df["loss_aversion"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["numeracy_quartile"] = pd.qcut(df["numeracy"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["trust_quartile"] = pd.qcut(df["trust"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
df["fatigue_quartile"] = pd.qcut(df["decision_fatigue"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

for group_col, out_name in [
    ("loss_aversion_quartile", "python_framing_effects_loss_aversion_heterogeneity.csv"),
    ("numeracy_quartile", "python_framing_effects_numeracy_heterogeneity.csv"),
    ("trust_quartile", "python_framing_effects_trust_heterogeneity.csv"),
    ("fatigue_quartile", "python_framing_effects_fatigue_heterogeneity.csv"),
]:
    het = df.groupby(["frame", group_col], observed=False).agg(
        risky_choice_rate=("choose_risky", "mean"),
        mean_welfare_proxy=("welfare_proxy", "mean"),
        mean_comprehension=("comprehension", "mean"),
    ).reset_index()
    het.to_csv(REG / out_name, index=False)

print("Wrote Python framing-effects treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
