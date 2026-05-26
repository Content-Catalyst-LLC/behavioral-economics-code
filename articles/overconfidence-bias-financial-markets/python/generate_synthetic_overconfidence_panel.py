from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(12120)

n_investors = 3000
n_periods = 140

investors = pd.DataFrame({
    "investor_id": np.arange(1, n_investors + 1),
    "true_signal_sd": rng.uniform(0.15, 0.35, n_investors),
    "risk_tolerance": rng.uniform(0.5, 1.5, n_investors),
    "diversification_discipline": rng.uniform(0.25, 1.0, n_investors),
    "prior_success_sensitivity": rng.uniform(0.0, 0.8, n_investors),
    "information_quality": rng.uniform(0.25, 0.95, n_investors),
})

regimes = {
    "calibrated_confidence": {
        "overconfidence_multiplier": 1.00,
        "trading_friction": 0.0025,
        "leverage_access": 1.00,
    },
    "moderate_overconfidence": {
        "overconfidence_multiplier": 1.45,
        "trading_friction": 0.0025,
        "leverage_access": 1.15,
    },
    "high_overconfidence_low_friction": {
        "overconfidence_multiplier": 2.05,
        "trading_friction": 0.0018,
        "leverage_access": 1.35,
    },
}

def simulate_regime(regime_name: str, overconfidence_multiplier: float, trading_friction: float, leverage_access: float) -> pd.DataFrame:
    rows = []
    rolling_success = np.zeros(n_investors)

    for period in range(1, n_periods + 1):
        true_market_return = rng.normal(0.008, 0.075)

        signals = rng.normal(
            loc=true_market_return,
            scale=investors["true_signal_sd"].to_numpy() * (1.15 - 0.30 * investors["information_quality"].to_numpy()),
        )

        confidence_boost = 1 + investors["prior_success_sensitivity"].to_numpy() * np.maximum(rolling_success, 0)
        perceived_signal = signals * overconfidence_multiplier * confidence_boost

        trade_intensity = (
            np.abs(perceived_signal)
            * investors["risk_tolerance"].to_numpy()
            * (1.25 - 0.50 * investors["diversification_discipline"].to_numpy())
            * leverage_access
        )

        trade_intensity = np.minimum(trade_intensity, 3.5)
        trading_cost = trading_friction * trade_intensity
        gross_position_return = true_market_return * np.sign(perceived_signal) * trade_intensity
        realized_return = gross_position_return - trading_cost

        rolling_success = 0.80 * rolling_success + 0.20 * realized_return

        rows.append(pd.DataFrame({
            "regime": regime_name,
            "period": period,
            "investor_id": investors["investor_id"],
            "true_market_return": true_market_return,
            "signal": signals,
            "perceived_signal": perceived_signal,
            "trade_intensity": trade_intensity,
            "trading_cost": trading_cost,
            "gross_position_return": gross_position_return,
            "realized_return": realized_return,
            "rolling_success": rolling_success,
            "overconfidence_multiplier": overconfidence_multiplier,
            "trading_friction": trading_friction,
            "leverage_access": leverage_access,
            "true_signal_sd": investors["true_signal_sd"],
            "risk_tolerance": investors["risk_tolerance"],
            "diversification_discipline": investors["diversification_discipline"],
            "prior_success_sensitivity": investors["prior_success_sensitivity"],
            "information_quality": investors["information_quality"],
        }))

    return pd.concat(rows, ignore_index=True)

frames = [simulate_regime(name, **params) for name, params in regimes.items()]
panel = pd.concat(frames, ignore_index=True)

experiment = panel.groupby(["regime", "period"], as_index=False).agg(
    mean_trade_intensity=("trade_intensity", "mean"),
    mean_trading_cost=("trading_cost", "mean"),
    mean_gross_position_return=("gross_position_return", "mean"),
    mean_realized_return=("realized_return", "mean"),
    volatility_proxy=("realized_return", "std"),
    mean_abs_perceived_signal=("perceived_signal", lambda x: np.mean(np.abs(x))),
    overconfidence_multiplier=("overconfidence_multiplier", "mean"),
    trading_friction=("trading_friction", "mean"),
    leverage_access=("leverage_access", "mean"),
)

experiment["moderate_overconfidence_treat"] = (experiment["regime"] == "moderate_overconfidence").astype(int)
experiment["high_overconfidence_treat"] = (experiment["regime"] == "high_overconfidence_low_friction").astype(int)
experiment["portfolio_drag"] = experiment["mean_trading_cost"]
experiment["net_minus_gross"] = experiment["mean_realized_return"] - experiment["mean_gross_position_return"]

summary = experiment.groupby("regime").agg(
    mean_trade_intensity=("mean_trade_intensity", "mean"),
    mean_trading_cost=("mean_trading_cost", "mean"),
    mean_gross_position_return=("mean_gross_position_return", "mean"),
    mean_realized_return=("mean_realized_return", "mean"),
    volatility_realized_return=("volatility_proxy", "mean"),
    mean_abs_perceived_signal=("mean_abs_perceived_signal", "mean"),
    mean_portfolio_drag=("portfolio_drag", "mean"),
).reset_index()

summary["return_to_turnover_ratio"] = summary["mean_realized_return"] / summary["mean_trade_intensity"]

panel.to_csv(TABLES / "synthetic_overconfidence_investor_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_overconfidence_experiment.csv", index=False)
summary.to_csv(TABLES / "overconfidence_regime_summary.csv", index=False)

panel.to_csv(PROCESSED / "synthetic_overconfidence_investor_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_overconfidence_experiment.csv", index=False)
summary.to_csv(PROCESSED / "overconfidence_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} investor-period rows.")
print(summary)
