-- Behavioral economics governance-policy schema.
-- Synthetic-data research scaffold only.

DROP TABLE IF EXISTS citizens;
DROP TABLE IF EXISTS governance_regimes;
DROP TABLE IF EXISTS simulation_results;

CREATE TABLE citizens (
  citizen_id INTEGER PRIMARY KEY,
  trust REAL NOT NULL CHECK (trust >= 0 AND trust <= 1),
  salience REAL NOT NULL CHECK (salience >= 0 AND salience <= 1),
  norm_sensitivity REAL NOT NULL CHECK (norm_sensitivity >= 0 AND norm_sensitivity <= 1),
  burden_sensitivity REAL NOT NULL CHECK (burden_sensitivity >= 0 AND burden_sensitivity <= 1),
  present_bias REAL NOT NULL CHECK (present_bias >= 0 AND present_bias <= 1),
  income REAL NOT NULL,
  digital_access REAL CHECK (digital_access >= 0 AND digital_access <= 1),
  baseline_compliance REAL CHECK (baseline_compliance >= 0 AND baseline_compliance <= 1)
);

CREATE TABLE governance_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  admin_burden REAL NOT NULL,
  reminder_salience REAL NOT NULL,
  trust_signal REAL NOT NULL,
  penalty_strength REAL NOT NULL
);

CREATE TABLE simulation_results (
  result_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  compliance_rate REAL NOT NULL,
  mean_compliance_probability REAL NOT NULL,
  mean_welfare REAL NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (regime_id) REFERENCES governance_regimes(regime_id)
);

INSERT INTO governance_regimes
  (regime_id, regime_name, admin_burden, reminder_salience, trust_signal, penalty_strength)
VALUES
  (1, 'enforcement_heavy', 0.35, 0.30, 0.35, 0.85),
  (2, 'simplification_first', 0.10, 0.55, 0.50, 0.35),
  (3, 'trust_plus_salience', 0.12, 0.80, 0.80, 0.30);
