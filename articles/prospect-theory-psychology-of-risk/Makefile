.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_prospect_theory_panel.py

python: data
	python3 python/prospect_theory_frame_evaluation.py
	python3 python/expected_utility_comparison.py
	python3 python/fourfold_risk_attitudes_simulation.py
	python3 python/insurance_lottery_policy_risk_examples.py
	python3 python/sensitivity_prospect_theory_parameters.py

r: data
	Rscript r/prospect_theory_evaluation.R
	Rscript r/prospect_theory_robustness_checks.R
	Rscript r/prospect_value_probability_weighting_simulation.R

sql:
	sqlite3 outputs/tables/prospect_theory.db < sql/schema.sql

all: data python r sql
