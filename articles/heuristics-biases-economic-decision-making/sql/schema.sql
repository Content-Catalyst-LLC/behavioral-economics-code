DROP TABLE IF EXISTS heuristic_regimes;
DROP TABLE IF EXISTS heuristic_judgments;
DROP TABLE IF EXISTS heuristic_design_sensitivity;
DROP TABLE IF EXISTS base_rate_neglect_simulation;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE heuristic_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  signal_scale REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  debiasing_support REAL NOT NULL
);

CREATE TABLE heuristic_judgments (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  true_value REAL NOT NULL,
  estimated_value REAL NOT NULL,
  judgment_error REAL NOT NULL,
  absolute_error REAL NOT NULL,
  decision_quality REAL NOT NULL,
  welfare_proxy REAL NOT NULL,
  correction_capacity REAL NOT NULL,
  availability_signal REAL NOT NULL,
  representativeness_signal REAL NOT NULL,
  anchor_signal REAL NOT NULL,
  framing_signal REAL NOT NULL,
  numeracy REAL NOT NULL,
  domain_knowledge REAL NOT NULL,
  cognitive_load REAL NOT NULL,
  confidence REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES heuristic_regimes(regime_id)
);

CREATE TABLE heuristic_design_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  signal_scale REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  debiasing_support REAL NOT NULL,
  mean_estimate REAL NOT NULL,
  mean_judgment_error REAL NOT NULL,
  mean_absolute_error REAL NOT NULL,
  mean_correction_capacity REAL NOT NULL,
  mean_decision_quality REAL NOT NULL,
  mean_welfare_proxy REAL NOT NULL
);

CREATE TABLE base_rate_neglect_simulation (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  true_base_rate REAL NOT NULL,
  representativeness_sensitivity REAL NOT NULL,
  base_rate_attention REAL NOT NULL,
  numeracy REAL NOT NULL,
  story_vividness REAL NOT NULL,
  story_consistency REAL NOT NULL,
  subjective_probability REAL NOT NULL,
  calibration_error REAL NOT NULL,
  overestimation INTEGER NOT NULL CHECK (overestimation IN (0, 1))
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

INSERT INTO heuristic_regimes VALUES
  (1, 'low_bias_with_context', 0.60, 0.80, 0.75),
  (2, 'medium_bias_environment', 1.00, 0.50, 0.40),
  (3, 'high_bias_low_context', 1.50, 0.20, 0.10);
