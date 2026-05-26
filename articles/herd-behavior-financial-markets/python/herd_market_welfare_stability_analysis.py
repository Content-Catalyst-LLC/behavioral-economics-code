from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_herd_market_experiment.csv")

summary = df.groupby("regime").agg(
    observations=("period", "count"),
    mean_price=("price", "mean"),
    final_price=("price", "last"),
    mean_buy_rate=("buy_rate", "mean"),
    mean_price_deviation=("price_deviation", "mean"),
    mean_volatility_proxy=("volatility_proxy", "mean"),
    worst_drawdown=("drawdown_from_peak", "min"),
    mean_systemic_herding_risk=("systemic_herding_risk", "mean"),
    max_systemic_herding_risk=("systemic_herding_risk", "max"),
).reset_index()

summary["stability_score"] = (
    1.0
    - summary["mean_volatility_proxy"]
    - abs(summary["mean_price_deviation"])
    + summary["worst_drawdown"]
    - summary["mean_systemic_herding_risk"]
)

summary.to_csv(TABLES / "herd_market_financial_stability_summary.csv", index=False)

rows = []
for liquidity_weight in [0.75, 1.00, 1.25]:
    for leverage_weight in [0.75, 1.00, 1.25]:
        for social_weight in [0.75, 1.00, 1.25]:
            alt_risk = (
                social_weight * df["systemic_herding_risk"]
                + leverage_weight * df["leverage_pressure"] * abs(df["drawdown_from_peak"])
                + (1 / liquidity_weight) * df["volatility_proxy"]
            )
            tmp = df.assign(alt_systemic_risk=alt_risk)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "liquidity_weight": liquidity_weight,
                    "leverage_weight": leverage_weight,
                    "social_signal_weight": social_weight,
                    "regime": regime,
                    "mean_alt_systemic_risk": sub["alt_systemic_risk"].mean(),
                    "max_alt_systemic_risk": sub["alt_systemic_risk"].max(),
                })

pd.DataFrame(rows).to_csv(DIAG / "herd_market_systemic_risk_sensitivity.csv", index=False)

print(summary)
