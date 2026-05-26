DROP TABLE IF EXISTS investor_regimes;
DROP TABLE IF EXISTS investor_periods;
DROP TABLE IF EXISTS performance_attribution;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE investor_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  overconfidence_multiplier REAL NOT NULL,
  trading_friction REAL NOT NULL,
  leverage_access REAL NOT NULL
);

CREATE TABLE investor_periods (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  investor_id INTEGER NOT NULL,
  true_market_return REAL NOT NULL,
  signal REAL NOT NULL,
  perceived_signal REAL NOT NULL,
  trade_intensity REAL NOT NULL,
  trading_cost REAL NOT NULL,
  gross_position_return REAL NOT NULL,
  realized_return REAL NOT NULL,
  rolling_success REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES investor_regimes(regime_id)
);

CREATE TABLE performance_attribution (
  observation_id INTEGER PRIMARY KEY,
  period INTEGER NOT NULL,
  manager_id INTEGER NOT NULL,
  market_return REAL NOT NULL,
  factor_return REAL NOT NULL,
  observed_return REAL NOT NULL,
  reported_conviction REAL NOT NULL,
  beta_market REAL NOT NULL,
  factor_loading REAL NOT NULL,
  true_skill_alpha REAL NOT NULL,
  overconfidence_score REAL NOT NULL
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

INSERT INTO investor_regimes VALUES
  (1, 'calibrated_confidence', 1.00, 0.0025, 1.00),
  (2, 'moderate_overconfidence', 1.45, 0.0025, 1.15),
  (3, 'high_overconfidence_low_friction', 2.05, 0.0018, 1.35);
