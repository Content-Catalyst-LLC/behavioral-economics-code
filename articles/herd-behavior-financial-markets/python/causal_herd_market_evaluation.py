from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
REG = ROOT / "outputs" / "regression_tables"
REG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_herd_market_experiment.csv")

outcomes = [
    "price",
    "price_deviation",
    "buy_rate",
    "volatility_proxy",
    "drawdown_from_peak",
    "systemic_herding_risk",
]
treatments = ["moderate_herding_treat", "high_herding_treat"]
controls = ["liquidity_depth", "leverage_pressure", "social_media_intensity", "post_shock"]

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
    base = (df["moderate_herding_treat"] == 0) & (df["high_herding_treat"] == 0)
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

pd.DataFrame(rows).to_csv(REG / "python_herd_market_treatment_effects.csv", index=False)

shock_summary = df.groupby(["regime", "post_shock"]).agg(
    mean_price=("price", "mean"),
    mean_buy_rate=("buy_rate", "mean"),
    mean_volatility_proxy=("volatility_proxy", "mean"),
    mean_drawdown=("drawdown_from_peak", "mean"),
    mean_systemic_herding_risk=("systemic_herding_risk", "mean"),
).reset_index()
shock_summary.to_csv(TABLES / "herd_market_shock_window_summary.csv", index=False)

print("Wrote Python herding treatment-effect and shock-window summaries.")
print(shock_summary)
