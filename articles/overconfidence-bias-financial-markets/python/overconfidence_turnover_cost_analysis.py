from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

panel = pd.read_csv(TABLES / "synthetic_overconfidence_investor_panel.csv")

investor_summary = panel.groupby(["regime", "investor_id"], as_index=False).agg(
    mean_trade_intensity=("trade_intensity", "mean"),
    mean_trading_cost=("trading_cost", "mean"),
    mean_gross_position_return=("gross_position_return", "mean"),
    mean_realized_return=("realized_return", "mean"),
    return_volatility=("realized_return", "std"),
    mean_abs_perceived_signal=("perceived_signal", lambda x: x.abs().mean()),
    risk_tolerance=("risk_tolerance", "mean"),
    information_quality=("information_quality", "mean"),
    diversification_discipline=("diversification_discipline", "mean"),
    prior_success_sensitivity=("prior_success_sensitivity", "mean"),
)

investor_summary["turnover_cost_share"] = investor_summary["mean_trading_cost"] / investor_summary["mean_trade_intensity"].replace(0, float("nan"))
investor_summary["net_gross_gap"] = investor_summary["mean_realized_return"] - investor_summary["mean_gross_position_return"]

regime_summary = investor_summary.groupby("regime").agg(
    investors=("investor_id", "count"),
    mean_trade_intensity=("mean_trade_intensity", "mean"),
    mean_trading_cost=("mean_trading_cost", "mean"),
    mean_gross_position_return=("mean_gross_position_return", "mean"),
    mean_realized_return=("mean_realized_return", "mean"),
    mean_return_volatility=("return_volatility", "mean"),
    mean_net_gross_gap=("net_gross_gap", "mean"),
).reset_index()

investor_summary.to_csv(TABLES / "overconfidence_investor_summary.csv", index=False)
regime_summary.to_csv(TABLES / "overconfidence_turnover_cost_summary.csv", index=False)

rows = []
for friction_weight in [0.75, 1.00, 1.25]:
    for leverage_weight in [0.75, 1.00, 1.25]:
        for success_weight in [0.75, 1.00, 1.25]:
            alt_cost = (
                friction_weight * panel["trading_cost"]
                + leverage_weight * panel["leverage_access"] * panel["realized_return"].abs() * 0.05
                + success_weight * panel["prior_success_sensitivity"] * panel["rolling_success"].clip(lower=0) * 0.01
            )
            tmp = panel.assign(alt_behavioral_cost=alt_cost)
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "friction_weight": friction_weight,
                    "leverage_weight": leverage_weight,
                    "success_feedback_weight": success_weight,
                    "regime": regime,
                    "mean_alt_behavioral_cost": sub["alt_behavioral_cost"].mean(),
                    "max_alt_behavioral_cost": sub["alt_behavioral_cost"].max(),
                })

pd.DataFrame(rows).to_csv(DIAG / "overconfidence_behavioral_cost_sensitivity.csv", index=False)

print(regime_summary)
