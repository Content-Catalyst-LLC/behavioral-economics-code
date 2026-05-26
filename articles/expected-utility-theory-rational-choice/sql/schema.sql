DROP TABLE IF EXISTS risk_aversion_regimes;
DROP TABLE IF EXISTS expected_utility_choices;
DROP TABLE IF EXISTS insurance_demand;
DROP TABLE IF EXISTS portfolio_choice;
DROP TABLE IF EXISTS policy_risk_examples;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE risk_aversion_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  rho_low REAL NOT NULL,
  rho_high REAL NOT NULL
);

CREATE TABLE expected_utility_choices (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  wealth REAL NOT NULL,
  rho REAL NOT NULL,
  numeracy REAL NOT NULL,
  liquidity_constraint REAL NOT NULL,
  trust REAL NOT NULL,
  eu_certain REAL NOT NULL,
  eu_risky REAL NOT NULL,
  expected_value_risky REAL NOT NULL,
  certainty_equivalent_payoff REAL NOT NULL,
  risk_premium REAL NOT NULL,
  choose_risky_eu INTEGER NOT NULL CHECK (choose_risky_eu IN (0, 1)),
  observed_choose_risky INTEGER NOT NULL CHECK (observed_choose_risky IN (0, 1)),
  FOREIGN KEY (regime_id) REFERENCES risk_aversion_regimes(regime_id)
);

CREATE TABLE insurance_demand (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  wealth REAL NOT NULL,
  rho REAL NOT NULL,
  trust REAL NOT NULL,
  liquidity_constraint REAL NOT NULL,
  loss_probability REAL NOT NULL,
  loss_amount REAL NOT NULL,
  expected_loss REAL NOT NULL,
  premium REAL NOT NULL,
  formal_insurance_takeup INTEGER NOT NULL CHECK (formal_insurance_takeup IN (0, 1)),
  observed_insurance_takeup INTEGER NOT NULL CHECK (observed_insurance_takeup IN (0, 1))
);

CREATE TABLE portfolio_choice (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  wealth REAL NOT NULL,
  rho REAL NOT NULL,
  optimal_risky_share REAL NOT NULL,
  expected_utility REAL NOT NULL
);

CREATE TABLE policy_risk_examples (
  observation_id INTEGER PRIMARY KEY,
  rho REAL NOT NULL,
  policy TEXT NOT NULL,
  expected_monetary_value REAL NOT NULL,
  expected_utility REAL NOT NULL
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

INSERT INTO risk_aversion_regimes VALUES
  (1, 'low_risk_aversion', 0.10, 0.80),
  (2, 'medium_risk_aversion', 0.80, 1.50),
  (3, 'high_risk_aversion', 1.50, 3.00);
