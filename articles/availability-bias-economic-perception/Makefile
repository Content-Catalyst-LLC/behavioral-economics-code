.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_availability_bias_panel.py

python: data
	python3 python/causal_availability_bias_evaluation.py
	python3 python/availability_calibration_welfare_analysis.py
	python3 python/availability_design_sensitivity_analysis.py

r: data
	Rscript r/availability_bias_evaluation.R
	Rscript r/availability_bias_robustness_checks.R
	Rscript r/availability_salience_simulation.R

sql:
	sqlite3 outputs/tables/availability_bias.db < sql/schema.sql

all: data python r sql
