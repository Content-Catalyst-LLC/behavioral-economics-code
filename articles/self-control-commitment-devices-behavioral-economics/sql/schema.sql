DROP TABLE IF EXISTS commitment_regimes;
DROP TABLE IF EXISTS commitment_savings_periods;
DROP TABLE IF EXISTS quasi_hyperbolic_choices;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE commitment_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  commitment_cost REAL NOT NULL,
  automation_strength REAL NOT NULL,
  flexibility REAL NOT NULL
);

CREATE TABLE commitment_savings_periods (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  beta REAL NOT NULL,
  delta REAL NOT NULL,
  income REAL NOT NULL,
  sophistication REAL NOT NULL,
  liquidity_need REAL NOT NULL,
  emergency_risk REAL NOT NULL,
  emergency_shock INTEGER NOT NULL CHECK (emergency_shock IN (0, 1)),
  planned_savings REAL NOT NULL,
  actual_savings REAL NOT NULL,
  withdrawal REAL NOT NULL,
  accumulated_savings REAL NOT NULL,
  welfare REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES commitment_regimes(regime_id)
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

INSERT INTO commitment_regimes VALUES
  (1, 'low_commitment', 100, 0.15, 0.90),
  (2, 'medium_commitment', 400, 0.55, 0.65),
  (3, 'high_commitment', 800, 0.85, 0.35);
