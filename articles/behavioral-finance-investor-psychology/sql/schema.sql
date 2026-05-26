DROP TABLE IF EXISTS behavioral_market_regimes;
DROP TABLE IF EXISTS behavioral_market_periods;
DROP TABLE IF EXISTS prospect_theory_investor_periods;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE behavioral_market_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  behavior_scale REAL NOT NULL,
  trading_friction REAL NOT NULL,
  platform_salience REAL NOT NULL
);

CREATE TABLE behavioral_market_periods (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  price REAL NOT NULL,
  fundamental_value REAL NOT NULL,
  mean_buy_rate REAL NOT NULL,
  mean_trade_intensity REAL NOT NULL,
  trading_cost_drag REAL NOT NULL,
  mispricing REAL NOT NULL,
  absolute_mispricing REAL NOT NULL,
  drawdown_from_peak REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES behavioral_market_regimes(regime_id)
);

CREATE TABLE prospect_theory_investor_periods (
  observation_id INTEGER PRIMARY KEY,
  period INTEGER NOT NULL,
  investor_id INTEGER NOT NULL,
  current_price REAL NOT NULL,
  reference_point REAL NOT NULL,
  paper_gain_loss REAL NOT NULL,
  loss_aversion_lambda REAL NOT NULL,
  curvature_eta REAL NOT NULL,
  subjective_value REAL NOT NULL,
  sell_pressure REAL NOT NULL,
  sold INTEGER NOT NULL CHECK (sold IN (0, 1))
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

INSERT INTO behavioral_market_regimes VALUES
  (1, 'low_behavioral_distortion', 0.60, 0.0030, 0.70),
  (2, 'medium_behavioral_distortion', 1.00, 0.0025, 1.00),
  (3, 'high_behavioral_distortion_low_friction', 1.50, 0.0018, 1.35);
