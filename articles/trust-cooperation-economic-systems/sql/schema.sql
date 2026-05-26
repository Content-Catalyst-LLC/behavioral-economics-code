DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS trust_regimes;
DROP TABLE IF EXISTS trust_outcomes;

CREATE TABLE agents (
  agent_id INTEGER PRIMARY KEY,
  trust_propensity REAL NOT NULL,
  reciprocity REAL NOT NULL,
  punishment_willingness REAL NOT NULL,
  institutional_trust REAL NOT NULL,
  betrayal_sensitivity REAL NOT NULL,
  monitoring_cost_sensitivity REAL NOT NULL
);

CREATE TABLE trust_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  institutional_support REAL NOT NULL,
  norm_strength REAL NOT NULL,
  betrayal_cost REAL NOT NULL,
  monitoring_intensity REAL NOT NULL
);

CREATE TABLE trust_outcomes (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  trusted INTEGER NOT NULL,
  reciprocated INTEGER NOT NULL,
  punished INTEGER NOT NULL,
  monitoring_cost REAL NOT NULL,
  transaction_cost_reduction REAL NOT NULL,
  total_welfare REAL NOT NULL
);

INSERT INTO trust_regimes VALUES
  (1, 'low_trust_exchange', 0.10, 0.15, 0.70, 0.35),
  (2, 'reciprocal_market_exchange', 0.45, 0.55, 0.50, 0.20),
  (3, 'institutionally_supported_cooperation', 0.80, 0.75, 0.35, 0.10);
