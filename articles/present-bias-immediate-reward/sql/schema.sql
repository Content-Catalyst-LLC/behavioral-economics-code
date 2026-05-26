DROP TABLE IF EXISTS present_bias_regimes;
DROP TABLE IF EXISTS present_bias_periods;
DROP TABLE IF EXISTS quasi_hyperbolic_choices;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE present_bias_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  commitment_cost REAL NOT NULL,
  reminder_strength REAL NOT NULL,
  flexibility REAL NOT NULL
);

CREATE TABLE present_bias_periods (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  beta REAL NOT NULL,
  delta REAL NOT NULL,
  sophistication REAL NOT NULL,
  liquidity_need REAL NOT NULL,
  temptation_strength REAL NOT NULL,
  future_goal_value REAL NOT NULL,
  delayed_reward REAL NOT NULL,
  immediate_temptation REAL NOT NULL,
  discounted_delayed_value REAL NOT NULL,
  immediate_value REAL NOT NULL,
  choose_delayed INTEGER NOT NULL CHECK (choose_delayed IN (0, 1)),
  period_welfare REAL NOT NULL,
  cumulative_delayed_choices REAL NOT NULL,
  cumulative_welfare REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES present_bias_regimes(regime_id)
);

CREATE TABLE quasi_hyperbolic_choices (
  observation_id INTEGER PRIMARY KEY,
  choice_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  beta REAL NOT NULL,
  delta REAL NOT NULL,
  immediate_reward REAL NOT NULL,
  delayed_reward REAL NOT NULL,
  delay_periods INTEGER NOT NULL,
  commitment_cost REAL NOT NULL,
  discounted_delayed_value REAL NOT NULL,
  immediate_value REAL NOT NULL,
  patient_choice INTEGER NOT NULL CHECK (patient_choice IN (0, 1))
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

INSERT INTO present_bias_regimes VALUES
  (1, 'weak_commitment', 20, 0.10, 0.95),
  (2, 'medium_commitment', 70, 0.45, 0.75),
  (3, 'strong_commitment', 140, 0.80, 0.55);
