.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_environmental_policy_panel.py

python: data
	python3 python/causal_environmental_policy_evaluation.py
	python3 python/environmental_welfare_analysis.py

r: data
	Rscript r/environmental_policy_evaluation.R
	Rscript r/environmental_welfare_robustness_checks.R

sql:
	sqlite3 outputs/tables/environmental_policy.db < sql/schema.sql

all: data python r sql
