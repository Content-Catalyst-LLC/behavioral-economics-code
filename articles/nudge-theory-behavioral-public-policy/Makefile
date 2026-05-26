.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_nudge_policy_panel.py

python: data
	python3 python/causal_nudge_policy_evaluation.py
	python3 python/nudge_welfare_analysis.py

r: data
	Rscript r/nudge_policy_evaluation.R
	Rscript r/nudge_welfare_robustness_checks.R

sql:
	sqlite3 outputs/tables/nudge_policy.db < sql/schema.sql

all: data python r sql
