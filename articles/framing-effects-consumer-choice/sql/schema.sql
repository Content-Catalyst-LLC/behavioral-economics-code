DROP TABLE IF EXISTS framing_regimes;
DROP TABLE IF EXISTS framing_decisions;
DROP TABLE IF EXISTS framing_design_sensitivity;
DROP TABLE IF EXISTS regression_results;

CREATE TABLE framing_regimes (
  regime_id INTEGER PRIMARY KEY,
  frame_name TEXT NOT NULL UNIQUE,
  frame_strength REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  salience REAL NOT NULL
);

CREATE TABLE framing_decisions (
  observation_id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  loss_aversion REAL NOT NULL,
  curvature REAL NOT NULL,
  numeracy REAL NOT NULL,
  trust REAL NOT NULL,
  decision_fatigue REAL NOT NULL,
  certain_value REAL NOT NULL,
  risky_value REAL NOT NULL,
  adjusted_risky_value REAL NOT NULL,
  comprehension REAL NOT NULL,
  choose_risky INTEGER NOT NULL CHECK (choose_risky IN (0, 1)),
  welfare_proxy REAL NOT NULL,
  FOREIGN KEY (regime_id) REFERENCES framing_regimes(regime_id)
);

CREATE TABLE framing_design_sensitivity (
  observation_id INTEGER PRIMARY KEY,
  frame_name TEXT NOT NULL,
  frame_strength REAL NOT NULL,
  disclosure_quality REAL NOT NULL,
  salience REAL NOT NULL,
  risky_choice_rate REAL NOT NULL,
  mean_comprehension REAL NOT NULL,
  mean_welfare_proxy REAL NOT NULL,
  mean_manipulation_risk REAL NOT NULL,
  mean_decision_quality_index REAL NOT NULL
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

INSERT INTO framing_regimes VALUES
  (1, 'gain_frame', 0.70, 0.70, 0.75),
  (2, 'loss_frame', 0.70, 0.70, 0.75),
  (3, 'balanced_absolute_risk_frame', 0.15, 0.95, 0.35);
