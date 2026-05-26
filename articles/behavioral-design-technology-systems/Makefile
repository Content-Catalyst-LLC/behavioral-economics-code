.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_interface_panel.py

python: data
	python3 python/causal_interface_policy_evaluation.py
	python3 python/welfare_analysis.py

r: data
	Rscript r/interface_policy_evaluation.R
	Rscript r/welfare_robustness_checks.R

sql:
	sqlite3 outputs/tables/behavioral_design_technology.db < sql/schema.sql

all: data python r sql
