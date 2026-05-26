from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(13130)

n_investors = 1800
n_periods = 120

investors = pd.DataFrame({
    "investor_id": np.arange(1, n_investors + 1),
    "overconfidence": rng.uniform(0.2, 1.2, n_investors),
    "loss_aversion": rng.uniform(1.0, 2.5, n_investors),
    "anchoring_strength": rng.uniform(0.1, 0.9, n_investors),
    "herd_weight": rng.uniform(0.1, 1.0, n_investors),
    "risk_tolerance": rng.uniform(0.50, 1.50, n_investors),
    "diversification_discipline": rng.uniform(0.25, 1.0, n_investors),
})

regimes = {
    "low_behavioral_distortion": {
        "behavior_scale": 0.60,
        "trading_friction": 0.0030,
        "platform_salience": 0.70,
    },
    "medium_behavioral_distortion": {
        "behavior_scale": 1.00,
        "trading_friction": 0.0025,
        "platform_salience": 1.00,
    },
    "high_behavioral_distortion_low_friction": {
        "behavior_scale": 1.50,
        "trading_friction": 0.0018,
        "platform_salience": 1.35,
    },
}

def simulate_market(regime_name: str, behavior_scale: float, trading_friction: float, platform_salience: float) -> pd.DataFrame:
    price = 100.0
    fundamental_value = 100.0
    previous_price = price
    peak_price = price
    rows = []

    for period in range(1, n_periods + 1):
        fundamental_value += rng.normal(0.20, 1.50)

        private_signal = rng.normal(
            loc=fundamental_value - price,
            scale=5.0,
            size=n_investors,
        )

        anchored_view = investors["anchoring_strength"].to_numpy() * behavior_scale * (previous_price - price)
        herd_signal = investors["herd_weight"].to_numpy() * behavior_scale * platform_salience * (price - previous_price)

        expected_return = (
            private_signal * (1 + behavior_scale * investors["overconfidence"].to_numpy())
            + anchored_view
            + herd_signal
        )

        perceived_loss_penalty = np.where(
            expected_return < 0,
            behavior_scale * investors["loss_aversion"].to_numpy() * np.abs(expected_return),
            0,
        )

        demand_signal = expected_return - perceived_loss_penalty

        trade_intensity = (
            np.abs(demand_signal / 10)
            * investors["risk_tolerance"].to_numpy()
            * (1.25 - 0.50 * investors["diversification_discipline"].to_numpy())
        )
        trade_intensity = np.minimum(trade_intensity, 3.0)

        buy_prob = 1 / (1 + np.exp(-demand_signal / 10))
        buys = rng.binomial(1, buy_prob)
        mean_buy_rate = float(buys.mean())

        trading_cost_drag = float(trade_intensity.mean() * trading_friction)

        previous_price = price
        price = price + 3 * (mean_buy_rate - 0.5) - trading_cost_drag + rng.normal(0, 0.8)
        peak_price = max(peak_price, price)
        drawdown_from_peak = (price - peak_price) / peak_price

        rows.append({
            "regime": regime_name,
            "period": period,
            "price": float(price),
            "fundamental_value": float(fundamental_value),
            "mean_buy_rate": mean_buy_rate,
            "mean_trade_intensity": float(trade_intensity.mean()),
            "trading_cost_drag": trading_cost_drag,
            "mispricing": float(price - fundamental_value),
            "absolute_mispricing": float(abs(price - fundamental_value)),
            "drawdown_from_peak": float(drawdown_from_peak),
            "behavior_scale": behavior_scale,
            "trading_friction": trading_friction,
            "platform_salience": platform_salience,
            "medium_behavioral_treat": int(regime_name == "medium_behavioral_distortion"),
            "high_behavioral_treat": int(regime_name == "high_behavioral_distortion_low_friction"),
        })

    return pd.DataFrame(rows)

frames = [simulate_market(name, **params) for name, params in regimes.items()]
market_history = pd.concat(frames, ignore_index=True)

summary = market_history.groupby("regime").agg(
    mean_price=("price", "mean"),
    mean_fundamental_value=("fundamental_value", "mean"),
    mean_buy_rate=("mean_buy_rate", "mean"),
    mean_trade_intensity=("mean_trade_intensity", "mean"),
    mean_trading_cost_drag=("trading_cost_drag", "mean"),
    mean_mispricing=("mispricing", "mean"),
    mean_absolute_mispricing=("absolute_mispricing", "mean"),
    max_absolute_mispricing=("absolute_mispricing", "max"),
    worst_drawdown=("drawdown_from_peak", "min"),
).reset_index()

market_history.to_csv(TABLES / "synthetic_behavioral_finance_market_history.csv", index=False)
market_history.to_csv(TABLES / "synthetic_behavioral_finance_experiment.csv", index=False)
summary.to_csv(TABLES / "behavioral_finance_regime_summary.csv", index=False)

market_history.to_csv(PROCESSED / "synthetic_behavioral_finance_market_history.csv", index=False)
summary.to_csv(PROCESSED / "behavioral_finance_regime_summary.csv", index=False)

print(f"Wrote {len(market_history):,} market-period rows.")
print(summary)
