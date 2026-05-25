-- Synthetic behavioral economics schema.
-- Designed for reproducible article examples, not production behavioral tracking.

CREATE TABLE decision_regime_observations (
    observation_id INTEGER PRIMARY KEY,
    article_slug TEXT NOT NULL,
    regime TEXT NOT NULL,
    framing_signal REAL,
    loss_signal REAL,
    time_signal REAL,
    social_signal REAL,
    trust_signal REAL,
    default_status INTEGER,
    effort_cost REAL,
    uptake_probability REAL,
    choose_option INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE model_runs (
    model_run_id INTEGER PRIMARY KEY,
    article_slug TEXT NOT NULL,
    model_name TEXT NOT NULL,
    synthetic_data_only INTEGER NOT NULL DEFAULT 1,
    assumptions TEXT,
    limitations TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
