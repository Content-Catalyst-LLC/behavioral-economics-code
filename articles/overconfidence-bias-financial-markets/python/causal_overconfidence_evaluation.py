from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_overconfidence_experiment.csv")

outcomes = [
    "mean_trade_intensity",
    "mean_trading_cost",
    "mean_gross_position_return",
    "mean_realized_return",
    "volatility_proxy",
    "mean_abs_perceived_signal",
    "portfolio_drag",
]
treatments = ["moderate_overconfidence_treat", "high_overconfidence_treat"]
controls = ["trading_friction", "leverage_access"]

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
    base = (df["moderate_overconfidence_treat"] == 0) & (df["high_overconfidence_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_overconfidence_treatment_effects.csv", index=False)

panel = pd.read_csv(TABLES / "synthetic_overconfidence_investor_panel.csv")
panel["risk_tolerance_quartile"] = pd.qcut(panel["risk_tolerance"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

heterogeneity = panel.groupby(["regime", "risk_tolerance_quartile"], observed=False).agg(
    mean_trade_intensity=("trade_intensity", "mean"),
    mean_trading_cost=("trading_cost", "mean"),
    mean_realized_return=("realized_return", "mean"),
    mean_abs_perceived_signal=("perceived_signal", lambda x: np.mean(np.abs(x))),
).reset_index()
heterogeneity.to_csv(REG / "python_overconfidence_risk_tolerance_heterogeneity.csv", index=False)

print("Wrote Python overconfidence treatment-effect and heterogeneity summaries.")
print(pd.DataFrame(rows).head())
