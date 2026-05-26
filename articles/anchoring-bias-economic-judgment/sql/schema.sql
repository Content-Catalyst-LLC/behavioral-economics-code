DROP TABLE IF EXISTS anchor_regimes;
DROP TABLE IF EXISTS anchor_decisions;
DROP TABLE IF EXISTS anchoring_design_sensitivity;
DROP TABLE IF EXISTS reference_price_simulation;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE anchor_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  anchor_value REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  counter_anchor_support REAL NOT NULL
);

CREATE TABLE anchor_decisions (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  true_value REAL NOT NULL,
  anchor_value REAL NOT NULL,
  adjustment_rate REAL NOT NULL,
  effective_adjustment REAL NOT NULL,
  numeracy REAL NOT NULL,
  confidence REAL NOT NULL,
  cognitive_load REAL NOT NULL,
  domain_knowledge REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  counter_anchor_support REAL NOT NULL,
  estimate REAL NOT NULL,
  bias REAL NOT NULL,
  absolute_error REAL NOT NULL,
  confidence_adjusted_error REAL NOT NULL,
  decision_quality REAL NOT NULL,
  welfare_proxy REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES anchor_regimes(regime_id)
);

CREATE TABLE anchoring_design_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  anchor_value REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  counter_anchor_support REAL NOT NULL,
  mean_estimate REAL NOT NULL,
  mean_bias REAL NOT NULL,
  mean_absolute_error REAL NOT NULL,
  mean_effective_adjustment REAL NOT NULL,
  mean_decision_quality REAL NOT NULL,
  mean_welfare_proxy REAL NOT NULL
);

CREATE TABLE reference_price_simulation (
  observation_id INTEGER PRIMARY KEY,
  consumer_id INTEGER NOT NULL,
  actual_price REAL NOT NULL,
  reference_price REAL NOT NULL,
  market_value REAL NOT NULL,
  perceived_savings REAL NOT NULL,
  purchase_utility REAL NOT NULL,
  purchase INTEGER NOT NULL CHECK (purchase IN (0, 1))
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

INSERT INTO anchor_regimes VALUES
  (1, 'low_anchor_low_support', 25, 0.25, 0.10),
  (2, 'neutral_anchor_with_context', 65, 0.75, 0.65),
  (3, 'high_anchor_low_support', 85, 0.25, 0.10),
  (4, 'high_anchor_with_counter_context', 85, 0.85, 0.85);
