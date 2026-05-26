# Data Dictionary

## synthetic_herd_market_panel.csv

- `regime`: simulated market regime
- `period`: market period
- `post_shock`: post-shock indicator
- `moderate_herding_treat`: moderate-herding treatment indicator
- `high_herding_treat`: high-herding crowded-trade treatment indicator
- `mean_private_signal`: average private signal among investors
- `herd_signal`: prior aggregate buy rate adjusted for social amplification
- `buy_rate`: share of investors buying in the period
- `price`: simulated market price
- `price_deviation`: deviation from baseline price
- `liquidity_depth`: liquidity-depth parameter
- `leverage_pressure`: leverage and forced-selling pressure parameter
- `social_media_intensity`: platform/social-amplification parameter
- `volatility_proxy`: absolute price-impact proxy
- `shock`: market shock value
- `drawdown_from_peak`: price decline from prior peak
- `systemic_herding_risk`: crowded exposure x leverage pressure / liquidity depth

## synthetic_herd_market_experiment.csv

Period-level market-regime dataset for treatment-effect estimation.

## informational_cascade_history.csv

Investor sequence showing when social signals dominate private signals.
