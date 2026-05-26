DROP TABLE IF EXISTS market_regimes;
DROP TABLE IF EXISTS herd_market_periods;
DROP TABLE IF EXISTS cascade_sequences;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE market_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  herd_weight REAL NOT NULL,
  liquidity_depth REAL NOT NULL,
  leverage_pressure REAL NOT NULL,
  social_media_intensity REAL NOT NULL
);

CREATE TABLE herd_market_periods (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  post_shock INTEGER NOT NULL CHECK (post_shock IN (0, 1)),
  mean_private_signal REAL NOT NULL,
  herd_signal REAL NOT NULL,
  buy_rate REAL NOT NULL,
  price REAL NOT NULL,
  price_deviation REAL NOT NULL,
  volatility_proxy REAL NOT NULL,
  drawdown_from_peak REAL NOT NULL,
  systemic_herding_risk REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES market_regimes(regime_id)
);

CREATE TABLE cascade_sequences (
  observation_id INTEGER PRIMARY KEY,
  sequence_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  true_state INTEGER NOT NULL,
  private_signal INTEGER NOT NULL,
  social_signal REAL NOT NULL,
  cascade_indicator INTEGER NOT NULL,
  buy INTEGER NOT NULL,
  decision_matches_private_signal INTEGER NOT NULL,
  decision_matches_true_state INTEGER NOT NULL
);

CREATE TABLE regression_results (
  result_id INTEGER PRIMARY KEY,
  model_name TEXT NOT NULL,
  outcome TEXT NOT NULL,
  term TEXT NOT NULL,
  estimate REAL NOT NULL,
  std_error REAL,
  p_value REAL,
  n INTEGER,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO market_regimes VALUES
  (1, 'low_herding_deep_liquidity', 0.25, 1.40, 0.10, 0.10),
  (2, 'moderate_herding', 0.85, 1.00, 0.25, 0.35),
  (3, 'high_herding_crowded_trade', 1.45, 0.65, 0.55, 0.75);
