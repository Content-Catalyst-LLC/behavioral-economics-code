.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_present_bias_panel.py

python: data
	python3 python/causal_present_bias_evaluation.py
	python3 python/present_bias_welfare_flexibility_analysis.py
	python3 python/quasi_hyperbolic_discounting_simulation.py

r: data
	Rscript r/present_bias_evaluation.R
	Rscript r/present_bias_robustness_checks.R
	Rscript r/quasi_hyperbolic_discounting_simulation.R

sql:
	sqlite3 outputs/tables/present_bias.db < sql/schema.sql

all: data python r sql
