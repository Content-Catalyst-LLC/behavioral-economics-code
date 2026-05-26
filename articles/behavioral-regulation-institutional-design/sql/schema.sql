-- Behavioral regulation and institutional design: economist-facing schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS regulatory_regimes;
DROP TABLE IF EXISTS regulatory_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE agents (
  agent_id INTEGER PRIMARY KEY,
  trust REAL NOT NULL CHECK (trust >= 0 AND trust <= 1),
  norm_sensitivity REAL NOT NULL CHECK (norm_sensitivity >= 0 AND norm_sensitivity <= 1),
  burden_sensitivity REAL NOT NULL CHECK (burden_sensitivity >= 0 AND burden_sensitivity <= 1),
  loss_aversion REAL NOT NULL,
  private_gain_noncompliance REAL NOT NULL CHECK (private_gain_noncompliance >= 0 AND private_gain_noncompliance <= 1),
  compliance_capacity REAL NOT NULL CHECK (compliance_capacity >= 0 AND compliance_capacity <= 1)
);

CREATE TABLE regulatory_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  admin_burden REAL NOT NULL,
  trust_signal REAL NOT NULL,
  norm_signal REAL NOT NULL,
  default_assistance INTEGER NOT NULL CHECK (default_assistance IN (0, 1)),
  sanction_strength REAL NOT NULL
);

CREATE TABLE regulatory_outcomes (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  post INTEGER NOT NULL CHECK (post IN (0, 1)),
  complied INTEGER NOT NULL CHECK (complied IN (0, 1)),
  social_benefit REAL NOT NULL,
  compliance_cost REAL NOT NULL,
  enforcement_cost REAL NOT NULL,
  administrative_cost REAL NOT NULL,
  total_welfare REAL NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
  FOREIGN KEY (regime_id) REFERENCES regulatory_regimes(regime_id)
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

INSERT INTO regulatory_regimes
  (regime_id, regime_name, admin_burden, trust_signal, norm_signal, default_assistance, sanction_strength)
VALUES
  (1, 'sanction_heavy_deterrence', 0.28, 0.20, 0.20, 0, 0.85),
  (2, 'simplification_plus_trust', 0.08, 0.80, 0.45, 1, 0.35),
  (3, 'integrated_behavioral_regulation', 0.10, 0.75, 0.65, 1, 0.55);
