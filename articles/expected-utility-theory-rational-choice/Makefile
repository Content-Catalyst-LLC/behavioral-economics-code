.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_expected_utility_panel.py

python: data
	python3 python/expected_utility_risk_aversion_evaluation.py
	python3 python/certainty_equivalent_risk_premium_analysis.py
	python3 python/insurance_portfolio_policy_risk_simulations.py
	python3 python/sensitivity_expected_utility_parameters.py

r: data
	Rscript r/expected_utility_evaluation.R
	Rscript r/expected_utility_robustness_checks.R
	Rscript r/crra_choice_simulation.R

sql:
	sqlite3 outputs/tables/expected_utility.db < sql/schema.sql

all: data python r sql
