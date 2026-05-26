-- Behavioral economics and digital platforms: economist-facing schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS platform_regimes;
DROP TABLE IF EXISTS platform_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  baseline_user_value REAL NOT NULL,
  cognitive_overload REAL NOT NULL CHECK (cognitive_overload >= 0 AND cognitive_overload <= 1),
  privacy_sensitivity REAL NOT NULL CHECK (privacy_sensitivity >= 0 AND privacy_sensitivity <= 1),
  digital_literacy REAL CHECK (digital_literacy >= 0 AND digital_literacy <= 1),
  social_susceptibility REAL CHECK (social_susceptibility >= 0 AND social_susceptibility <= 1)
);

CREATE TABLE platform_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  recommendation_intensity REAL NOT NULL,
  salience REAL NOT NULL,
  social_proof REAL NOT NULL,
  friction REAL NOT NULL,
  data_extraction_intensity REAL NOT NULL
);

CREATE TABLE platform_outcomes (
  observation_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  post INTEGER NOT NULL CHECK (post IN (0, 1)),
  clicked INTEGER NOT NULL CHECK (clicked IN (0, 1)),
  retained INTEGER NOT NULL CHECK (retained IN (0, 1)),
  consented INTEGER NOT NULL CHECK (consented IN (0, 1)),
  exposure_quality REAL NOT NULL,
  user_welfare REAL NOT NULL,
  platform_value REAL NOT NULL,
  welfare_platform_gap REAL NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (regime_id) REFERENCES platform_regimes(regime_id)
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

INSERT INTO platform_regimes
  (regime_id, regime_name, recommendation_intensity, salience, social_proof, friction, data_extraction_intensity)
VALUES
  (1, 'neutral_discovery', 0.45, 0.45, 0.20, 0.18, 0.10),
  (2, 'engagement_optimized', 0.85, 0.80, 0.55, 0.10, 0.45),
  (3, 'socially_amplified_ranking', 0.70, 0.65, 0.90, 0.12, 0.35);
