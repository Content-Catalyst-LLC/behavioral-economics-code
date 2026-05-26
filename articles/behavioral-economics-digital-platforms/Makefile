.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_platform_panel.py

python: data
	python3 python/causal_platform_policy_evaluation.py
	python3 python/platform_welfare_analysis.py

r: data
	Rscript r/platform_policy_evaluation.R
	Rscript r/platform_welfare_robustness_checks.R

sql:
	sqlite3 outputs/tables/digital_platforms.db < sql/schema.sql

all: data python r sql
