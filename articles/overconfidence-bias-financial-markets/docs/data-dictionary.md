# Data Dictionary

## synthetic_overconfidence_investor_panel.csv

- `regime`: confidence / platform-friction regime
- `period`: trading period
- `investor_id`: synthetic investor identifier
- `true_market_return`: synthetic market return in the period
- `signal`: noisy private signal
- `perceived_signal`: private signal inflated by overconfidence and success feedback
- `trade_intensity`: turnover / trading-intensity proxy
- `trading_cost`: trading-cost drag
- `realized_return`: simulated net realized return after trading cost
- `gross_position_return`: simulated return before trading cost
- `rolling_success`: success-feedback state variable
- `overconfidence_multiplier`: signal-confidence inflation parameter
- `trading_friction`: transaction-cost parameter
- `leverage_access`: exposure-amplification parameter

## synthetic_overconfidence_experiment.csv

Regime-period dataset for treatment-effect estimation.

## performance_attribution_panel.csv

Synthetic performance-attribution panel decomposing returns into market beta, factor exposure, alpha-like component, and residual noise.
