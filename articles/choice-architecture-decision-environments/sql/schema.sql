-- Choice architecture and decision environments: economist-facing schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS architecture_regimes;
DROP TABLE IF EXISTS choice_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  default_sensitivity REAL NOT NULL CHECK (default_sensitivity >= 0 AND default_sensitivity <= 1),
  salience_sensitivity REAL NOT NULL CHECK (salience_sensitivity >= 0 AND salience_sensitivity <= 1),
  framing_sensitivity REAL NOT NULL CHECK (framing_sensitivity >= 0 AND framing_sensitivity <= 1),
  complexity_sensitivity REAL NOT NULL CHECK (complexity_sensitivity >= 0 AND complexity_sensitivity <= 1),
  switching_cost_sensitivity REAL NOT NULL CHECK (switching_cost_sensitivity >= 0 AND switching_cost_sensitivity <= 1),
  digital_literacy REAL NOT NULL CHECK (digital_literacy >= 0 AND digital_literacy <= 1),
  institutional_trust REAL NOT NULL CHECK (institutional_trust >= 0 AND institutional_trust <= 1)
);

CREATE TABLE architecture_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  default_strength REAL NOT NULL,
  salience_strength REAL NOT NULL,
  framing_strength REAL NOT NULL,
  complexity_level REAL NOT NULL,
  switching_cost_level REAL NOT NULL
);

CREATE TABLE choice_outcomes (
  observation_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  post INTEGER NOT NULL CHECK (post IN (0, 1)),
  chosen_option INTEGER NOT NULL,
  chosen_utility REAL NOT NULL,
  realized_welfare REAL NOT NULL,
  selected_default INTEGER NOT NULL CHECK (selected_default IN (0, 1)),
  selected_high_value_option INTEGER NOT NULL CHECK (selected_high_value_option IN (0, 1)),
  cognitive_cost REAL NOT NULL,
  switching_cost REAL NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (regime_id) REFERENCES architecture_regimes(regime_id)
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

INSERT INTO architecture_regimes
  (regime_id, regime_name, default_strength, salience_strength, framing_strength, complexity_level, switching_cost_level)
VALUES
  (1, 'neutral_presentation', 0.00, 0.50, 0.50, 0.20, 0.05),
  (2, 'default_heavy_architecture', 1.00, 0.85, 0.75, 0.12, 0.02),
  (3, 'low_complexity_guided_design', 0.00, 0.65, 0.65, 0.08, 0.04);
