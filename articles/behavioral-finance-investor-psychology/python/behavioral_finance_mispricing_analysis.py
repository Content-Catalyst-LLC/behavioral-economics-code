from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_behavioral_finance_market_history.csv")

summary = df.groupby("regime").agg(
    observations=("period", "count"),
    mean_price=("price", "mean"),
    mean_fundamental_value=("fundamental_value", "mean"),
    mean_mispricing=("mispricing", "mean"),
    mean_absolute_mispricing=("absolute_mispricing", "mean"),
    max_absolute_mispricing=("absolute_mispricing", "max"),
    mean_trade_intensity=("mean_trade_intensity", "mean"),
    mean_buy_rate=("mean_buy_rate", "mean"),
    mean_cost_drag=("trading_cost_drag", "mean"),
    worst_drawdown=("drawdown_from_peak", "min"),
).reset_index()

summary["market_stability_score"] = (
    1
    - summary["mean_absolute_mispricing"] / 100
    - summary["mean_trade_intensity"] / 10
    + summary["worst_drawdown"]
)

summary.to_csv(TABLES / "behavioral_finance_mispricing_summary.csv", index=False)

rows = []
for behavior_weight in [0.75, 1.00, 1.25]:
    for friction_weight in [0.75, 1.00, 1.25]:
        for salience_weight in [0.75, 1.00, 1.25]:
            alt_risk = (
                behavior_weight * df["absolute_mispricing"]
                + salience_weight * df["platform_salience"] * df["mean_trade_intensity"]
                + (1 / friction_weight) * df["trading_cost_drag"] * 100
                + df["drawdown_from_peak"].abs() * 10
            )
            tmp = df.assign(alt_behavioral_market_risk=alt_risk)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "behavior_weight": behavior_weight,
                    "friction_weight": friction_weight,
                    "salience_weight": salience_weight,
                    "regime": regime,
                    "mean_alt_behavioral_market_risk": sub["alt_behavioral_market_risk"].mean(),
                    "max_alt_behavioral_market_risk": sub["alt_behavioral_market_risk"].max(),
                })

pd.DataFrame(rows).to_csv(DIAG / "behavioral_finance_market_risk_sensitivity.csv", index=False)

print(summary)
