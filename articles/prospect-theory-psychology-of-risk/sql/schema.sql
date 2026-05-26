DROP TABLE IF EXISTS frame_regimes;
DROP TABLE IF EXISTS prospect_theory_choices;
DROP TABLE IF EXISTS fourfold_risk_attitudes;
DROP TABLE IF EXISTS insurance_lottery_policy_examples;
DROP TABLE IF EXISTS parameter_sensitivity;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE frame_regimes (
  regime_id INTEGER PRIMARY KEY,
  frame_name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL
);

CREATE TABLE prospect_theory_choices (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  pt_sure_value REAL NOT NULL,
  pt_risky_value REAL NOT NULL,
  eu_sure_value REAL NOT NULL,
  eu_risky_value REAL NOT NULL,
  choose_risky_pt INTEGER NOT NULL CHECK (choose_risky_pt IN (0, 1)),
  choose_risky_eu INTEGER NOT NULL CHECK (choose_risky_eu IN (0, 1)),
  pt_eu_disagreement INTEGER NOT NULL CHECK (pt_eu_disagreement IN (0, 1)),
  lambda_loss REAL NOT NULL,
  alpha_gain REAL NOT NULL,
  beta_loss REAL NOT NULL,
  gamma_weight REAL NOT NULL,
  rho_crra REAL NOT NULL,
  wealth REAL NOT NULL,
  numeracy REAL NOT NULL,
  income_security REAL NOT NULL,
  trust REAL NOT NULL,
  prior_loss_exposure INTEGER NOT NULL CHECK (prior_loss_exposure IN (0, 1)),
  FOREIGN KEY (regime_id) REFERENCES frame_regimes(regime_id)
);

CREATE TABLE fourfold_risk_attitudes (
  observation_id INTEGER PRIMARY KEY,
  scenario TEXT NOT NULL,
  domain TEXT NOT NULL,
  p_event REAL NOT NULL,
  risky_event REAL NOT NULL,
  sure_outcome REAL NOT NULL,
  risky_value REAL NOT NULL,
  sure_value REAL NOT NULL,
  choose_risky INTEGER NOT NULL CHECK (choose_risky IN (0, 1)),
  lambda_loss REAL NOT NULL,
  gamma_weight REAL NOT NULL
);

CREATE TABLE insurance_lottery_policy_examples (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  lambda_loss REAL NOT NULL,
  gamma_weight REAL NOT NULL,
  income_security REAL NOT NULL,
  trust REAL NOT NULL,
  insurance_value REAL NOT NULL,
  no_insurance_value REAL NOT NULL,
  choose_insurance INTEGER NOT NULL CHECK (choose_insurance IN (0, 1)),
  lottery_value REAL NOT NULL,
  buy_lottery INTEGER NOT NULL CHECK (buy_lottery IN (0, 1)),
  climate_action_value REAL NOT NULL,
  no_action_value REAL NOT NULL,
  support_climate_action INTEGER NOT NULL CHECK (support_climate_action IN (0, 1))
);

CREATE TABLE parameter_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  lambda_loss REAL NOT NULL,
  alpha_gain REAL NOT NULL,
  beta_loss REAL NOT NULL,
  gamma_weight REAL NOT NULL,
  gain REAL NOT NULL,
  loss REAL NOT NULL,
  mixed_gamble_value REAL NOT NULL,
  accept_mixed_gamble INTEGER NOT NULL CHECK (accept_mixed_gamble IN (0, 1)),
  gain_loss_ratio REAL NOT NULL
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

INSERT INTO frame_regimes VALUES
  (1, 'gain', 'Sure gain versus risky gain'),
  (2, 'loss', 'Sure loss versus risky loss'),
  (3, 'mixed_gamble', 'Mixed gain/loss gamble relative to reference point');
