"""Econometric policy evaluation for choice architecture regimes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REGRESSION = ROOT / "outputs" / "regression_tables"

REGRESSION.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_choice_architecture_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_choice_architecture_panel.py first."
    )

df = pd.read_csv(data_path)

outcomes = [
    "realized_welfare",
    "chosen_utility",
    "selected_default",
    "selected_high_value_option",
    "cognitive_cost",
    "switching_cost",
]
controls = [
    "default_sensitivity",
    "salience_sensitivity",
    "framing_sensitivity",
    "complexity_sensitivity",
    "switching_cost_sensitivity",
    "digital_literacy",
    "institutional_trust",
]
treatments = ["default_heavy_treat", "guided_design_treat"]

rows = []

try:
    import statsmodels.api as sm

    for outcome in outcomes:
        X = df[treatments + controls].copy()
        X = sm.add_constant(X)
        y = df[outcome]
        model = sm.OLS(y, X).fit(cov_type="HC1")

        for var in treatments:
            rows.append({
                "outcome": outcome,
                "term": var,
                "estimate": model.params[var],
                "std_error_hc1": model.bse[var],
                "p_value": model.pvalues[var],
                "n": int(model.nobs),
                "r_squared": model.rsquared,
            })

    results = pd.DataFrame(rows)

except Exception as exc:
    fallback_rows = []
    base_mask = (df["default_heavy_treat"] == 0) & (df["guided_design_treat"] == 0)

    for outcome in outcomes:
        base = df.loc[base_mask, outcome].mean()
        for var in treatments:
            treated = df.loc[df[var] == 1, outcome].mean()
            fallback_rows.append({
                "outcome": outcome,
                "term": var,
                "estimate": treated - base,
                "std_error_hc1": np.nan,
                "p_value": np.nan,
                "n": len(df),
                "r_squared": np.nan,
                "note": f"Fallback difference-in-means used: {exc}",
            })

    results = pd.DataFrame(fallback_rows)

results.to_csv(REGRESSION / "python_choice_architecture_treatment_effects.csv", index=False)

# Heterogeneous welfare effects by complexity sensitivity.
df["complexity_quartile"] = pd.qcut(df["complexity_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

heterogeneity_rows = []
for q, sub in df.groupby("complexity_quartile", observed=False):
    base = sub.loc[(sub["default_heavy_treat"] == 0) & (sub["guided_design_treat"] == 0), "realized_welfare"].mean()
    for var in treatments:
        treated = sub.loc[sub[var] == 1, "realized_welfare"].mean()
        heterogeneity_rows.append({
            "group_variable": "complexity_sensitivity",
            "group": str(q),
            "term": var,
            "outcome": "realized_welfare",
            "difference_from_neutral_presentation": treated - base,
            "n": len(sub),
        })

pd.DataFrame(heterogeneity_rows).to_csv(
    REGRESSION / "python_choice_architecture_heterogeneous_welfare_effects.csv", index=False
)

summary = df.groupby("regime").agg(
    n=("user_id", "count"),
    mean_realized_welfare=("realized_welfare", "mean"),
    mean_chosen_utility=("chosen_utility", "mean"),
    default_selection_rate=("selected_default", "mean"),
    high_value_selection_rate=("selected_high_value_option", "mean"),
    mean_cognitive_cost=("cognitive_cost", "mean"),
    mean_switching_cost=("switching_cost", "mean"),
).reset_index()

summary.to_csv(TABLES / "choice_architecture_regime_summary.csv", index=False)

print("Wrote Python choice architecture treatment effects and heterogeneity tables.")
print(summary)
