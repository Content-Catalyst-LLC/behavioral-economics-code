-- Behavioral Economics and Sustainable Consumption
-- SQL schema for reproducible policy experiments and behavioral microdata.

CREATE TABLE IF NOT EXISTS household (
    household_id INTEGER PRIMARY KEY,
    income NUMERIC NOT NULL,
    income_quintile TEXT,
    urban INTEGER,
    renter INTEGER,
    environmental_concern NUMERIC,
    present_bias NUMERIC,
    loss_aversion NUMERIC,
    norm_sensitivity NUMERIC,
    friction_sensitivity NUMERIC,
    quality_uncertainty NUMERIC,
    infrastructure_access NUMERIC
);

CREATE TABLE IF NOT EXISTS policy_regime (
    policy_regime_id INTEGER PRIMARY KEY,
    regime_name TEXT UNIQUE NOT NULL,
    subsidy NUMERIC NOT NULL,
    default_green INTEGER NOT NULL,
    norm_signal NUMERIC NOT NULL,
    friction NUMERIC NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS adoption_outcome (
    outcome_id INTEGER PRIMARY KEY,
    household_id INTEGER NOT NULL,
    policy_regime_id INTEGER NOT NULL,
    adoption_probability NUMERIC,
    adopted INTEGER,
    private_welfare NUMERIC,
    external_benefit NUMERIC,
    fiscal_cost NUMERIC,
    total_welfare NUMERIC,
    FOREIGN KEY (household_id) REFERENCES household(household_id),
    FOREIGN KEY (policy_regime_id) REFERENCES policy_regime(policy_regime_id)
);

CREATE TABLE IF NOT EXISTS provenance_log (
    provenance_id INTEGER PRIMARY KEY,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    generated_by TEXT,
    generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
