DROP TABLE IF EXISTS availability_regimes;
DROP TABLE IF EXISTS availability_decisions;
DROP TABLE IF EXISTS availability_design_sensitivity;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE availability_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  salience_scale REAL NOT NULL,
  base_rate_disclosure REAL NOT NULL,
  emotional_intensity REAL NOT NULL
);

CREATE TABLE availability_decisions (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  true_probability REAL NOT NULL,
  availability_sensitivity REAL NOT NULL,
  numeracy REAL NOT NULL,
  trust_in_statistics REAL NOT NULL,
  risk_tolerance REAL NOT NULL,
  prior_experience INTEGER NOT NULL CHECK (prior_experience IN (0, 1)),
  recency_signal REAL NOT NULL,
  vividness_signal REAL NOT NULL,
  media_signal REAL NOT NULL,
  social_repetition_signal REAL NOT NULL,
  availability_score REAL NOT NULL,
  subjective_probability REAL NOT NULL,
  calibration_error REAL NOT NULL,
  participate_in_risky_asset INTEGER NOT NULL CHECK (participate_in_risky_asset IN (0, 1)),
  insurance_demand INTEGER NOT NULL CHECK (insurance_demand IN (0, 1)),
  policy_support INTEGER NOT NULL CHECK (policy_support IN (0, 1)),
  welfare_proxy REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES availability_regimes(regime_id)
);

CREATE TABLE availability_design_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  salience_scale REAL NOT NULL,
  base_rate_disclosure REAL NOT NULL,
  emotional_intensity REAL NOT NULL,
  mean_availability_score REAL NOT NULL,
  mean_subjective_probability REAL NOT NULL,
  mean_calibration_error REAL NOT NULL,
  mean_absolute_calibration_error REAL NOT NULL,
  insurance_demand_rate REAL NOT NULL,
  policy_support_rate REAL NOT NULL,
  mean_welfare_proxy REAL NOT NULL
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

INSERT INTO availability_regimes VALUES
  (1, 'low_availability_with_base_rates', 0.60, 0.80, 0.25),
  (2, 'medium_availability_environment', 1.00, 0.45, 0.55),
  (3, 'high_availability_no_base_rates', 1.50, 0.10, 0.85);
