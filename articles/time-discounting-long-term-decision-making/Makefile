.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_time_discounting_panel.py

python: data
	python3 python/causal_time_discounting_evaluation.py
	python3 python/time_discounting_welfare_flexibility_analysis.py
	python3 python/discount_rate_sensitivity_analysis.py
	python3 python/quasi_hyperbolic_discounting_simulation.py

r: data
	Rscript r/time_discounting_evaluation.R
	Rscript r/time_discounting_robustness_checks.R
	Rscript r/quasi_hyperbolic_discounting_simulation.R

sql:
	sqlite3 outputs/tables/time_discounting.db < sql/schema.sql

all: data python r sql
