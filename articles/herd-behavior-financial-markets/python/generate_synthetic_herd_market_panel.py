from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(11110)

n_investors = 1500
n_periods = 120

investors = pd.DataFrame({
    "investor_id": np.arange(1, n_investors + 1),
    "private_signal_weight": np.clip(rng.normal(1.0, 0.25, n_investors), 0.2, 2.0),
    "risk_weight": np.clip(rng.normal(0.8, 0.25, n_investors), 0.1, 2.5),
    "loss_aversion": np.clip(rng.normal(1.8, 0.35, n_investors), 1.0, 3.0),
    "reputation_pressure": np.clip(rng.normal(0.50, 0.20, n_investors), 0, 1),
    "information_quality": np.clip(rng.normal(0.55, 0.20, n_investors), 0, 1),
})

regimes = {
    "low_herding_deep_liquidity": {
        "herd_weight": 0.25,
        "liquidity_depth": 1.40,
        "leverage_pressure": 0.10,
        "social_media_intensity": 0.10,
    },
    "moderate_herding": {
        "herd_weight": 0.85,
        "liquidity_depth": 1.00,
        "leverage_pressure": 0.25,
        "social_media_intensity": 0.35,
    },
    "high_herding_crowded_trade": {
        "herd_weight": 1.45,
        "liquidity_depth": 0.65,
        "leverage_pressure": 0.55,
        "social_media_intensity": 0.75,
    },
}

def simulate_market(
    regime_name: str,
    herd_weight: float,
    liquidity_depth: float,
    leverage_pressure: float,
    social_media_intensity: float,
    fundamental_value: float = 0.15,
    shock_period: int = 80,
    shock_size: float = -0.35,
) -> pd.DataFrame:
    price = 1.0
    prior_buy_rate = 0.5
    reference_price = price
    peak_price = price
    rows = []

    for period in range(1, n_periods + 1):
        private_signals = rng.normal(
            loc=fundamental_value,
            scale=0.25 * (1.0 - 0.30 * investors["information_quality"].to_numpy()),
            size=n_investors,
        )

        shock = shock_size if period == shock_period else 0.0
        post_shock = int(period >= shock_period)

        loss_domain = float(price < reference_price)
        herd_signal = prior_buy_rate + 0.15 * social_media_intensity * max(prior_buy_rate - 0.5, 0)

        buy_utility = (
            investors["private_signal_weight"].to_numpy() * private_signals
            + herd_weight * herd_signal
            + investors["reputation_pressure"].to_numpy() * prior_buy_rate
            - investors["risk_weight"].to_numpy() * abs(price - 1.0)
            - investors["loss_aversion"].to_numpy() * loss_domain * abs(price - reference_price)
            + shock
        )

        buy_prob = 1 / (1 + np.exp(-buy_utility))
        buys = rng.binomial(1, buy_prob)
        buy_rate = float(buys.mean())

        liquidity_adjusted_impact = (0.16 / liquidity_depth) * (buy_rate - 0.5)
        leverage_feedback = -leverage_pressure * max(0, 0.5 - buy_rate) * abs(price - reference_price)
        noise = rng.normal(0, 0.012)

        price = max(0.10, price + liquidity_adjusted_impact + leverage_feedback + noise + shock * 0.08)
        peak_price = max(peak_price, price)
        drawdown_from_peak = (price - peak_price) / peak_price

        systemic_herding_risk = max(buy_rate - 0.5, 0) * leverage_pressure / liquidity_depth

        rows.append({
            "regime": regime_name,
            "period": period,
            "post_shock": post_shock,
            "moderate_herding_treat": int(regime_name == "moderate_herding"),
            "high_herding_treat": int(regime_name == "high_herding_crowded_trade"),
            "mean_private_signal": float(private_signals.mean()),
            "herd_signal": float(herd_signal),
            "buy_rate": buy_rate,
            "price": float(price),
            "price_deviation": float(price - 1.0),
            "liquidity_depth": liquidity_depth,
            "leverage_pressure": leverage_pressure,
            "social_media_intensity": social_media_intensity,
            "volatility_proxy": float(abs(liquidity_adjusted_impact + leverage_feedback + noise)),
            "shock": shock,
            "drawdown_from_peak": float(drawdown_from_peak),
            "systemic_herding_risk": float(systemic_herding_risk),
        })

        prior_buy_rate = buy_rate

    return pd.DataFrame(rows)

frames = [simulate_market(name, **params) for name, params in regimes.items()]
panel = pd.concat(frames, ignore_index=True)

summary = panel.groupby("regime").agg(
    mean_buy_rate=("buy_rate", "mean"),
    mean_price=("price", "mean"),
    max_price=("price", "max"),
    min_price=("price", "min"),
    final_price=("price", "last"),
    mean_price_deviation=("price_deviation", "mean"),
    mean_volatility_proxy=("volatility_proxy", "mean"),
    max_drawdown=("drawdown_from_peak", "min"),
    mean_systemic_herding_risk=("systemic_herding_risk", "mean"),
).reset_index()
summary["boom_bust_range"] = summary["max_price"] - summary["min_price"]

panel.to_csv(TABLES / "synthetic_herd_market_panel.csv", index=False)
panel.to_csv(TABLES / "synthetic_herd_market_experiment.csv", index=False)
summary.to_csv(TABLES / "herd_market_regime_summary.csv", index=False)

panel.to_csv(PROCESSED / "synthetic_herd_market_panel.csv", index=False)
summary.to_csv(PROCESSED / "herd_market_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} market-period rows.")
print(summary)
