# Data Dictionary

## synthetic_behavioral_finance_market_history.csv

- `regime`: behavioral market regime
- `period`: market period
- `price`: simulated asset price
- `fundamental_value`: simulated fundamental-value benchmark
- `mean_buy_rate`: share of synthetic investors buying
- `mean_trade_intensity`: turnover / trade-intensity proxy
- `trading_cost_drag`: average cost drag from trading activity
- `mispricing`: price minus fundamental value
- `absolute_mispricing`: absolute price-fundamental gap
- `behavior_scale`: intensity of behavioral distortion
- `trading_friction`: transaction-cost/friction parameter
- `platform_salience`: salience/amplification parameter for price movement and herd cues

## synthetic_behavioral_finance_experiment.csv

Period-level market-regime dataset for treatment-effect estimation.

## prospect_theory_investor_panel.csv

Synthetic investor-period dataset for studying reference points, loss aversion, trading response, and utility under prospect-theoretic assumptions.
