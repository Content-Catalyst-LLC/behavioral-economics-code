.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_commitment_savings_panel.py

python: data
	python3 python/causal_commitment_savings_evaluation.py
	python3 python/commitment_welfare_flexibility_analysis.py
	python3 python/quasi_hyperbolic_discounting_simulation.py

r: data
	Rscript r/commitment_savings_evaluation.R
	Rscript r/commitment_robustness_checks.R
	Rscript r/quasi_hyperbolic_discounting_simulation.R

sql:
	sqlite3 outputs/tables/commitment_devices.db < sql/schema.sql

all: data python r sql
