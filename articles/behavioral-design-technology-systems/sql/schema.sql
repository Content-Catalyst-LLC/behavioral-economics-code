-- Behavioral design in technology systems: economist-facing schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS interface_regimes;
DROP TABLE IF EXISTS experiment_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  baseline_value REAL NOT NULL,
  cognitive_overload REAL NOT NULL CHECK (cognitive_overload >= 0 AND cognitive_overload <= 1),
  privacy_sensitivity REAL NOT NULL CHECK (privacy_sensitivity >= 0 AND privacy_sensitivity <= 1),
  autonomy_preference REAL NOT NULL CHECK (autonomy_preference >= 0 AND autonomy_preference <= 1),
  digital_literacy REAL CHECK (digital_literacy >= 0 AND digital_literacy <= 1)
);

CREATE TABLE interface_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  salience REAL NOT NULL,
  default_on INTEGER NOT NULL CHECK (default_on IN (0, 1)),
  entry_friction REAL NOT NULL,
  exit_friction REAL NOT NULL,
  reward_intensity REAL NOT NULL,
  data_extraction_intensity REAL NOT NULL
);

CREATE TABLE experiment_outcomes (
  observation_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  post INTEGER NOT NULL CHECK (post IN (0, 1)),
  joined INTEGER NOT NULL CHECK (joined IN (0, 1)),
  retained INTEGER NOT NULL CHECK (retained IN (0, 1)),
  consented INTEGER NOT NULL CHECK (consented IN (0, 1)),
  user_welfare REAL NOT NULL,
  platform_value REAL NOT NULL,
  welfare_platform_gap REAL NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (regime_id) REFERENCES interface_regimes(regime_id)
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

INSERT INTO interface_regimes
  (regime_id, regime_name, salience, default_on, entry_friction, exit_friction, reward_intensity, data_extraction_intensity)
VALUES
  (1, 'user_supportive_design', 0.55, 0, 0.08, 0.08, 0.35, 0.10),
  (2, 'engagement_maximizing_design', 0.85, 1, 0.03, 0.22, 0.80, 0.45),
  (3, 'friction_heavy_lock_in', 0.75, 1, 0.02, 0.60, 0.55, 0.60);
