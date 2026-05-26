DROP TABLE IF EXISTS frame_regimes;
DROP TABLE IF EXISTS loss_aversion_choices;
DROP TABLE IF EXISTS disposition_effect_assets;
DROP TABLE IF EXISTS endowment_effect;
DROP TABLE IF EXISTS consumer_loss_framing;
DROP TABLE IF EXISTS policy_transition_losses;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE frame_regimes (
  regime_id INTEGER PRIMARY KEY,
  frame_name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL
);

CREATE TABLE loss_aversion_choices (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  sure_value REAL NOT NULL,
  risky_value REAL NOT NULL,
  choose_risky INTEGER NOT NULL CHECK (choose_risky IN (0, 1)),
  lambda_loss REAL NOT NULL,
  alpha_gain REAL NOT NULL,
  beta_loss REAL NOT NULL,
  numeracy REAL NOT NULL,
  income_security REAL NOT NULL,
  prior_loss_exposure INTEGER NOT NULL CHECK (prior_loss_exposure IN (0, 1)),
  trust REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES frame_regimes(regime_id)
);

CREATE TABLE disposition_effect_assets (
  observation_id INTEGER PRIMARY KEY,
  investor_id INTEGER NOT NULL,
  asset_id INTEGER NOT NULL,
  lambda_loss REAL NOT NULL,
  purchase_price REAL NOT NULL,
  current_price REAL NOT NULL,
  paper_gain_loss REAL NOT NULL,
  winner INTEGER NOT NULL CHECK (winner IN (0, 1)),
  sale_probability REAL NOT NULL,
  sold INTEGER NOT NULL CHECK (sold IN (0, 1))
);

CREATE TABLE endowment_effect (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  market_value REAL NOT NULL,
  owned INTEGER NOT NULL CHECK (owned IN (0, 1)),
  willingness_to_pay REAL NOT NULL,
  willingness_to_accept REAL NOT NULL,
  endowment_gap REAL NOT NULL,
  lambda_loss REAL NOT NULL
);

CREATE TABLE consumer_loss_framing (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  monthly_savings_from_cancel REAL NOT NULL,
  perceived_lost_benefits REAL NOT NULL,
  cancellation_friction REAL NOT NULL,
  cancel_probability REAL NOT NULL,
  cancel INTEGER NOT NULL CHECK (cancel IN (0, 1)),
  lambda_loss REAL NOT NULL
);

CREATE TABLE policy_transition_losses (
  observation_id INTEGER PRIMARY KEY,
  agent_id INTEGER NOT NULL,
  policy_gain REAL NOT NULL,
  policy_loss REAL NOT NULL,
  transition_support REAL NOT NULL,
  distributional_weight REAL NOT NULL,
  net_reference_value REAL NOT NULL,
  support_probability REAL NOT NULL,
  support_policy INTEGER NOT NULL CHECK (support_policy IN (0, 1)),
  lambda_loss REAL NOT NULL
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
