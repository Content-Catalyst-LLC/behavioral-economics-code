-- Behavioral insights in environmental policy: economist-facing schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS households;
DROP TABLE IF EXISTS policy_regimes;
DROP TABLE IF EXISTS policy_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE households (
  household_id INTEGER PRIMARY KEY,
  income REAL NOT NULL,
  energy_burden REAL NOT NULL,
  env_concern REAL NOT NULL CHECK (env_concern >= 0 AND env_concern <= 1),
  present_bias REAL NOT NULL CHECK (present_bias >= 0 AND present_bias <= 1),
  norm_sensitivity REAL NOT NULL CHECK (norm_sensitivity >= 0 AND norm_sensitivity <= 1),
  friction_sensitivity REAL NOT NULL CHECK (friction_sensitivity >= 0 AND friction_sensitivity <= 1),
  loss_aversion REAL NOT NULL,
  trust REAL NOT NULL CHECK (trust >= 0 AND trust <= 1)
);

CREATE TABLE policy_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  subsidy REAL NOT NULL,
  default_green INTEGER NOT NULL CHECK (default_green IN (0, 1)),
  norm_signal REAL NOT NULL,
  friction REAL NOT NULL
);

CREATE TABLE policy_outcomes (
  observation_id INTEGER PRIMARY KEY,
  household_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  post INTEGER NOT NULL CHECK (post IN (0, 1)),
  adopted INTEGER NOT NULL CHECK (adopted IN (0, 1)),
  private_benefit REAL NOT NULL,
  environmental_benefit REAL NOT NULL,
  fiscal_cost REAL NOT NULL,
  admin_cost REAL NOT NULL,
  total_welfare REAL NOT NULL,
  FOREIGN KEY (household_id) REFERENCES households(household_id),
  FOREIGN KEY (regime_id) REFERENCES policy_regimes(regime_id)
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

INSERT INTO policy_regimes
  (regime_id, regime_name, subsidy, default_green, norm_signal, friction)
VALUES
  (1, 'price_signal_only', 0.08, 0, 0.10, 0.20),
  (2, 'norm_plus_default', 0.00, 1, 0.70, 0.08),
  (3, 'integrated_policy_design', 0.06, 1, 0.70, 0.08);
