DROP TABLE IF EXISTS time_discounting_regimes;
DROP TABLE IF EXISTS time_discounting_periods;
DROP TABLE IF EXISTS discount_rate_sensitivity;
DROP TABLE IF EXISTS quasi_hyperbolic_choices;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE time_discounting_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  uses_present_bias INTEGER NOT NULL CHECK (uses_present_bias IN (0, 1)),
  commitment_support REAL NOT NULL,
  flexibility REAL NOT NULL
);

CREATE TABLE time_discounting_periods (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  beta REAL NOT NULL,
  delta REAL NOT NULL,
  sophistication REAL NOT NULL,
  liquidity_need REAL NOT NULL,
  immediate_reward_base REAL NOT NULL,
  future_goal_value REAL NOT NULL,
  delayed_reward REAL NOT NULL,
  immediate_reward REAL NOT NULL,
  delayed_value REAL NOT NULL,
  immediate_value REAL NOT NULL,
  choose_delayed INTEGER NOT NULL CHECK (choose_delayed IN (0, 1)),
  period_welfare REAL NOT NULL,
  cumulative_delayed_choices REAL NOT NULL,
  cumulative_welfare REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES time_discounting_regimes(regime_id)
);

CREATE TABLE discount_rate_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  future_value REAL NOT NULL,
  horizon_years INTEGER NOT NULL,
  discount_rate REAL NOT NULL,
  present_value REAL NOT NULL,
  pv_share_of_future_value REAL NOT NULL
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
  commitment_support REAL NOT NULL,
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

INSERT INTO time_discounting_regimes VALUES
  (1, 'exponential_discounting', 0, 0.00, 1.00),
  (2, 'present_biased_discounting', 1, 0.00, 1.00),
  (3, 'present_bias_with_commitment_support', 1, 0.70, 0.75);
