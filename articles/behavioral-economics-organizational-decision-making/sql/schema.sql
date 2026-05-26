-- Behavioral economics organizational decision-making schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS organizational_regimes;
DROP TABLE IF EXISTS simulation_results;

CREATE TABLE projects (
  project_id INTEGER PRIMARY KEY,
  expected_payoff REAL NOT NULL,
  risk REAL NOT NULL CHECK (risk >= 0 AND risk <= 1),
  sunk_cost REAL NOT NULL,
  prestige_value REAL NOT NULL CHECK (prestige_value >= 0 AND prestige_value <= 1),
  complexity REAL NOT NULL CHECK (complexity >= 0 AND complexity <= 1),
  overconfidence REAL NOT NULL CHECK (overconfidence >= 0 AND overconfidence <= 1),
  review_strength REAL NOT NULL CHECK (review_strength >= 0 AND review_strength <= 1),
  long_horizon_value REAL NOT NULL CHECK (long_horizon_value >= 0 AND long_horizon_value <= 1)
);

CREATE TABLE organizational_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  short_term_pressure REAL NOT NULL,
  review_strength REAL NOT NULL,
  conformity_pressure REAL NOT NULL,
  long_horizon_weight REAL NOT NULL
);

CREATE TABLE simulation_results (
  result_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  approval_rate REAL NOT NULL,
  mean_approval_probability REAL NOT NULL,
  mean_welfare REAL NOT NULL,
  escalation_prone_approval_rate REAL NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (regime_id) REFERENCES organizational_regimes(regime_id)
);

INSERT INTO organizational_regimes
  (regime_id, regime_name, short_term_pressure, review_strength, conformity_pressure, long_horizon_weight)
VALUES
  (1, 'metric_heavy_short_termism', 1.30, 0.15, 0.65, 0.10),
  (2, 'balanced_governance', 0.90, 0.55, 0.35, 0.35),
  (3, 'high_accountability_adaptive_review', 0.70, 0.85, 0.20, 0.60);
