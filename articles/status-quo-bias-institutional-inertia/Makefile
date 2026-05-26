.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_status_quo_bias_panel.py

python: data
	python3 python/causal_status_quo_bias_evaluation.py
	python3 python/switching_cost_welfare_analysis.py
	python3 python/default_design_sensitivity_analysis.py

r: data
	Rscript r/status_quo_bias_evaluation.R
	Rscript r/status_quo_bias_robustness_checks.R
	Rscript r/default_retention_simulation.R

sql:
	sqlite3 outputs/tables/status_quo_bias.db < sql/schema.sql

all: data python r sql
