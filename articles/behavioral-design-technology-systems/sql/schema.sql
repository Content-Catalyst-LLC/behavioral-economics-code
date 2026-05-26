-- Behavioral design in technology systems schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS interface_regimes;
DROP TABLE IF EXISTS simulation_results;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  baseline_value REAL NOT NULL,
  salience_sensitivity REAL NOT NULL CHECK (salience_sensitivity >= 0 AND salience_sensitivity <= 1),
  default_sensitivity REAL NOT NULL CHECK (default_sensitivity >= 0 AND default_sensitivity <= 1),
  friction_sensitivity REAL NOT NULL CHECK (friction_sensitivity >= 0 AND friction_sensitivity <= 1),
  reward_sensitivity REAL NOT NULL CHECK (reward_sensitivity >= 0 AND reward_sensitivity <= 1),
  cognitive_overload REAL NOT NULL CHECK (cognitive_overload >= 0 AND cognitive_overload <= 1),
  privacy_sensitivity REAL NOT NULL CHECK (privacy_sensitivity >= 0 AND privacy_sensitivity <= 1),
  autonomy_preference REAL NOT NULL CHECK (autonomy_preference >= 0 AND autonomy_preference <= 1)
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

CREATE TABLE simulation_results (
  result_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  join_rate REAL NOT NULL,
  retention_rate REAL NOT NULL,
  mean_user_welfare REAL NOT NULL,
  mean_platform_value REAL NOT NULL,
  friction_asymmetry REAL NOT NULL,
  welfare_platform_gap REAL NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (regime_id) REFERENCES interface_regimes(regime_id)
);

INSERT INTO interface_regimes
  (regime_id, regime_name, salience, default_on, entry_friction, exit_friction, reward_intensity, data_extraction_intensity)
VALUES
  (1, 'user_supportive_design', 0.55, 0, 0.08, 0.08, 0.35, 0.10),
  (2, 'engagement_maximizing_design', 0.85, 1, 0.03, 0.22, 0.80, 0.45),
  (3, 'friction_heavy_lock_in', 0.75, 1, 0.02, 0.60, 0.55, 0.60);
