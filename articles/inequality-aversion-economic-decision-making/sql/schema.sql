DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS distributional_regimes;
DROP TABLE IF EXISTS inequality_aversion_outcomes;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE agents (
  agent_id INTEGER PRIMARY KEY,
  alpha REAL NOT NULL CHECK (alpha >= 0),
  beta REAL NOT NULL CHECK (beta >= 0),
  income REAL NOT NULL,
  redistribution_norm REAL NOT NULL CHECK (redistribution_norm >= 0 AND redistribution_norm <= 1),
  merit_belief REAL NOT NULL CHECK (merit_belief >= 0 AND merit_belief <= 1),
  institutional_trust REAL NOT NULL CHECK (institutional_trust >= 0 AND institutional_trust <= 1)
);

CREATE TABLE distributional_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  self_payoff REAL NOT NULL,
  other_payoff REAL NOT NULL,
  baseline_legitimacy REAL NOT NULL
);

CREATE TABLE inequality_aversion_outcomes (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  period INTEGER NOT NULL,
  social_preference_utility REAL NOT NULL,
  rejected INTEGER NOT NULL CHECK (rejected IN (0, 1)),
  support_redistribution INTEGER NOT NULL CHECK (support_redistribution IN (0, 1)),
  process_legitimacy REAL NOT NULL,
  total_welfare REAL NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
  FOREIGN KEY (regime_id) REFERENCES distributional_regimes(regime_id)
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

INSERT INTO distributional_regimes VALUES
  (1, 'equal_distribution', 0.50, 0.50, 0.75),
  (2, 'advantageous_inequality', 0.70, 0.30, 0.48),
  (3, 'disadvantageous_inequality', 0.30, 0.70, 0.42);
