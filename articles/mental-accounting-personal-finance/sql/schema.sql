DROP TABLE IF EXISTS mental_accounting_regimes;
DROP TABLE IF EXISTS household_regime_outcomes;
DROP TABLE IF EXISTS windfall_events;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE mental_accounting_regimes (
  regime_id INTEGER PRIMARY KEY,
  regime_name TEXT NOT NULL UNIQUE,
  segmentation_level TEXT NOT NULL,
  integrated_prompt INTEGER NOT NULL CHECK (integrated_prompt IN (0, 1)),
  unified_money_view INTEGER NOT NULL CHECK (unified_money_view IN (0, 1))
);

CREATE TABLE household_regime_outcomes (
  observation_id INTEGER PRIMARY KEY,
  household_id INTEGER NOT NULL,
  regime_id INTEGER NOT NULL,
  monthly_income REAL NOT NULL,
  liquid_savings REAL NOT NULL,
  emergency_reserve REAL NOT NULL,
  credit_card_debt REAL NOT NULL,
  windfall REAL NOT NULL,
  savings_label_strength REAL NOT NULL,
  emergency_need_risk REAL NOT NULL,
  present_bias REAL NOT NULL,
  windfall_consumption REAL NOT NULL,
  windfall_debt_payment REAL NOT NULL,
  savings_used_for_debt REAL NOT NULL,
  total_debt_payment REAL NOT NULL,
  remaining_debt REAL NOT NULL,
  remaining_liquid_savings REAL NOT NULL,
  inefficiency_gap REAL NOT NULL,
  annual_interest_cost REAL NOT NULL,
  resilience_index REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES mental_accounting_regimes(regime_id)
);

CREATE TABLE windfall_events (
  event_observation_id INTEGER PRIMARY KEY,
  event_id INTEGER NOT NULL,
  household_id INTEGER NOT NULL,
  prompt_type TEXT NOT NULL,
  windfall_amount REAL NOT NULL,
  spending REAL NOT NULL,
  debt_repayment REAL NOT NULL,
  savings_allocation REAL NOT NULL
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

INSERT INTO mental_accounting_regimes VALUES
  (1, 'segmented_mental_accounts', 'high', 0, 0),
  (2, 'integrated_balance_sheet_prompt', 'moderate', 1, 0),
  (3, 'unified_fungible_money', 'low', 1, 1);
