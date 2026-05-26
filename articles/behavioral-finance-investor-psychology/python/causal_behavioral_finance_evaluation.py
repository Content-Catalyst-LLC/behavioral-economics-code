from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_behavioral_finance_experiment.csv")

outcomes = [
    "absolute_mispricing",
    "mispricing",
    "mean_trade_intensity",
    "mean_buy_rate",
    "trading_cost_drag",
    "drawdown_from_peak",
]
treatments = ["medium_behavioral_treat", "high_behavioral_treat"]
controls = ["trading_friction", "platform_salience"]

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
    base = (df["medium_behavioral_treat"] == 0) & (df["high_behavioral_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_behavioral_finance_treatment_effects.csv", index=False)

regime_period = df.groupby(["regime"]).agg(
    mean_absolute_mispricing=("absolute_mispricing", "mean"),
    max_absolute_mispricing=("absolute_mispricing", "max"),
    mean_trade_intensity=("mean_trade_intensity", "mean"),
    mean_trading_cost_drag=("trading_cost_drag", "mean"),
    worst_drawdown=("drawdown_from_peak", "min"),
).reset_index()
regime_period.to_csv(TABLES / "behavioral_finance_policy_summary.csv", index=False)

print("Wrote Python behavioral-finance treatment-effect and policy summaries.")
print(pd.DataFrame(rows).head())
