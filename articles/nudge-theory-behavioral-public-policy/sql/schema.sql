-- Nudge theory and behavioral public policy: economist-facing schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS nudge_regimes;
DROP TABLE IF EXISTS nudge_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE agents (
  agent_id INTEGER PRIMARY KEY,
  default_sensitivity REAL NOT NULL CHECK (default_sensitivity >= 0 AND default_sensitivity <= 1),
  reminder_sensitivity REAL NOT NULL CHECK (reminder_sensitivity >= 0 AND reminder_sensitivity <= 1),
  norm_sensitivity REAL NOT NULL CHECK (norm_sensitivity >= 0 AND norm_sensitivity <= 1),
  friction_sensitivity REAL NOT NULL CHECK (friction_sensitivity >= 0 AND friction_sensitivity <= 1),
  present_bias REAL NOT NULL CHECK (present_bias >= 0 AND present_bias <= 1),
  administrative_burden_sensitivity REAL NOT NULL CHECK (administrative_burden_sensitivity >= 0 AND administrative_burden_sensitivity <= 1),
  trust REAL NOT NULL CHECK (trust >= 0 AND trust <= 1)
);

CREATE TABLE nudge_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  default_on INTEGER NOT NULL CHECK (default_on IN (0, 1)),
  reminder_strength REAL NOT NULL,
  norm_signal REAL NOT NULL,
  friction REAL NOT NULL,
  administrative_burden REAL NOT NULL
);

CREATE TABLE nudge_outcomes (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  post INTEGER NOT NULL CHECK (post IN (0, 1)),
  adopted INTEGER NOT NULL CHECK (adopted IN (0, 1)),
  user_benefit REAL NOT NULL,
  social_benefit REAL NOT NULL,
  friction_cost REAL NOT NULL,
  admin_cost REAL NOT NULL,
  implementation_cost REAL NOT NULL,
  total_welfare REAL NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
  FOREIGN KEY (regime_id) REFERENCES nudge_regimes(regime_id)
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

INSERT INTO nudge_regimes
  (regime_id, regime_name, default_on, reminder_strength, norm_signal, friction, administrative_burden)
VALUES
  (1, 'information_only', 0, 0.10, 0.10, 0.22, 0.25),
  (2, 'reminder_plus_norm', 0, 0.70, 0.70, 0.12, 0.15),
  (3, 'default_plus_reminder', 1, 0.70, 0.60, 0.10, 0.10);
