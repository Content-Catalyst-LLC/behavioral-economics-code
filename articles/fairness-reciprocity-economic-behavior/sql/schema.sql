DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS fairness_regimes;
DROP TABLE IF EXISTS fairness_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE agents (
  agent_id INTEGER PRIMARY KEY,
  fairness_sensitivity REAL NOT NULL CHECK (fairness_sensitivity >= 0),
  reciprocity_sensitivity REAL NOT NULL CHECK (reciprocity_sensitivity >= 0),
  trust REAL NOT NULL CHECK (trust >= 0 AND trust <= 1),
  punishment_willingness REAL NOT NULL CHECK (punishment_willingness >= 0 AND punishment_willingness <= 1),
  process_fairness_weight REAL NOT NULL CHECK (process_fairness_weight >= 0 AND process_fairness_weight <= 1)
);

CREATE TABLE fairness_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  self_payoff REAL NOT NULL,
  other_payoff REAL NOT NULL,
  reciprocity_signal REAL NOT NULL,
  process_fairness REAL NOT NULL
);

CREATE TABLE fairness_outcomes (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  fairness_reciprocity_utility REAL NOT NULL,
  rejected INTEGER NOT NULL CHECK (rejected IN (0, 1)),
  punished INTEGER NOT NULL CHECK (punished IN (0, 1)),
  cooperated INTEGER NOT NULL CHECK (cooperated IN (0, 1)),
  total_welfare REAL NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
  FOREIGN KEY (regime_id) REFERENCES fairness_regimes(regime_id)
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

INSERT INTO fairness_regimes VALUES
  (1, 'fair_cooperative_regime', 0.50, 0.50, 0.40, 0.85),
  (2, 'unequal_but_cooperative_regime', 0.35, 0.65, 0.40, 0.70),
  (3, 'unequal_noncooperative_regime', 0.35, 0.65, -0.20, 0.45),
  (4, 'exploitative_low_process_fairness_regime', 0.25, 0.75, -0.35, 0.25);
