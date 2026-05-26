.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_regulatory_policy_panel.py

python: data
	python3 python/causal_regulatory_policy_evaluation.py
	python3 python/regulatory_welfare_analysis.py

r: data
	Rscript r/regulatory_policy_evaluation.R
	Rscript r/regulatory_welfare_robustness_checks.R

sql:
	sqlite3 outputs/tables/regulatory_policy.db < sql/schema.sql

all: data python r sql
