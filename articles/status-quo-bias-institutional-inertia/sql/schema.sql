DROP TABLE IF EXISTS default_regimes;
DROP TABLE IF EXISTS status_quo_decisions;
DROP TABLE IF EXISTS default_design_sensitivity;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE default_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  default_shift REAL NOT NULL,
  switching_support REAL NOT NULL,
  disclosure_quality REAL NOT NULL
);

CREATE TABLE status_quo_decisions (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  value_status_quo REAL NOT NULL,
  value_alternative REAL NOT NULL,
  objective_gain REAL NOT NULL,
  switch_cost REAL NOT NULL,
  effective_switch_cost REAL NOT NULL,
  loss_aversion REAL NOT NULL,
  status_quo_premium REAL NOT NULL,
  effective_status_quo_premium REAL NOT NULL,
  perceived_loss REAL NOT NULL,
  effective_perceived_loss REAL NOT NULL,
  uncertainty_sensitivity REAL NOT NULL,
  decision_fatigue REAL NOT NULL,
  sophistication REAL NOT NULL,
  utility_status_quo REAL NOT NULL,
  utility_alternative REAL NOT NULL,
  choose_alternative INTEGER NOT NULL CHECK (choose_alternative IN (0, 1)),
  welfare REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES default_regimes(regime_id)
);

CREATE TABLE default_design_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  default_shift REAL NOT NULL,
  switching_support REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  adoption_rate REAL NOT NULL,
  mean_welfare REAL NOT NULL,
  mean_effective_switch_cost REAL NOT NULL,
  mean_effective_status_quo_premium REAL NOT NULL,
  mean_effective_perceived_loss REAL NOT NULL
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

INSERT INTO default_regimes VALUES
  (1, 'passive_status_quo_default', 0.00, 0.00, 0.10),
  (2, 'active_choice_with_disclosure', 0.35, 0.35, 0.55),
  (3, 'pro_switching_default_with_support', 0.75, 0.70, 0.80);
