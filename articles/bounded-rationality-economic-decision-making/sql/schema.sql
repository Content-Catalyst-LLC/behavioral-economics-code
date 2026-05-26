DROP TABLE IF EXISTS constraint_regimes;
DROP TABLE IF EXISTS bounded_rationality_choices;
DROP TABLE IF EXISTS administrative_burden;
DROP TABLE IF EXISTS organizational_routines;
DROP TABLE IF EXISTS policy_simplification;
DROP TABLE IF EXISTS consumer_platform_search;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE constraint_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL
);

CREATE TABLE bounded_rationality_choices (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  aspiration REAL NOT NULL,
  search_cost REAL NOT NULL,
  time_budget REAL NOT NULL,
  cognitive_capacity REAL NOT NULL,
  numeracy REAL NOT NULL,
  stress REAL NOT NULL,
  institutional_trust REAL NOT NULL,
  digital_access REAL NOT NULL,
  income_security REAL NOT NULL,
  administrative_capacity REAL NOT NULL,
  chosen_index INTEGER NOT NULL,
  chosen_value REAL NOT NULL,
  optimal_value REAL NOT NULL,
  net_value REAL NOT NULL,
  optimization_gap REAL NOT NULL,
  cumulative_time REAL NOT NULL,
  cumulative_load REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES constraint_regimes(regime_id)
);

CREATE TABLE administrative_burden (
  observation_id INTEGER PRIMARY KEY,
  regime TEXT NOT NULL,
  person_id INTEGER NOT NULL,
  eligible INTEGER NOT NULL CHECK (eligible IN (0, 1)),
  digital_access REAL NOT NULL,
  administrative_capacity REAL NOT NULL,
  institutional_trust REAL NOT NULL,
  time_scarcity REAL NOT NULL,
  stress REAL NOT NULL,
  language_access REAL NOT NULL,
  income_security REAL NOT NULL,
  total_burden REAL NOT NULL,
  completed_application INTEGER NOT NULL CHECK (completed_application IN (0, 1)),
  takeup INTEGER NOT NULL CHECK (takeup IN (0, 1))
);

CREATE TABLE organizational_routines (
  observation_id INTEGER PRIMARY KEY,
  org_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  routine_strength REAL NOT NULL,
  learning_capacity REAL NOT NULL,
  frontline_feedback REAL NOT NULL,
  metric_quality REAL NOT NULL,
  environment_change INTEGER NOT NULL CHECK (environment_change IN (0, 1)),
  performance REAL NOT NULL
);

CREATE TABLE policy_simplification (
  observation_id INTEGER PRIMARY KEY,
  arm TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  baseline_need REAL NOT NULL,
  administrative_capacity REAL NOT NULL,
  digital_access REAL NOT NULL,
  trust REAL NOT NULL,
  time_scarcity REAL NOT NULL,
  procedural_burden REAL NOT NULL,
  comprehension REAL NOT NULL,
  takeup INTEGER NOT NULL CHECK (takeup IN (0, 1))
);

CREATE TABLE consumer_platform_search (
  observation_id INTEGER PRIMARY KEY,
  design TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  search_skill REAL NOT NULL,
  time_available REAL NOT NULL,
  price_sensitivity REAL NOT NULL,
  digital_access REAL NOT NULL,
  trust_platform REAL NOT NULL,
  status_quo_attachment REAL NOT NULL,
  search_burden REAL NOT NULL,
  hidden_total_cost REAL NOT NULL,
  plan_quality REAL NOT NULL,
  switched INTEGER NOT NULL CHECK (switched IN (0, 1))
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

INSERT INTO constraint_regimes VALUES
  (1, 'low_constraint', 'Lower search cost and cognitive load environment'),
  (2, 'medium_constraint', 'Moderate constraint environment'),
  (3, 'high_constraint', 'Higher search cost and cognitive load environment');
