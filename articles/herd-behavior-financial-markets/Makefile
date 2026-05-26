.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_herd_market_panel.py

python: data
	python3 python/causal_herd_market_evaluation.py
	python3 python/herd_market_welfare_stability_analysis.py
	python3 python/informational_cascade_simulation.py

r: data
	Rscript r/herd_market_evaluation.R
	Rscript r/herd_market_robustness_checks.R
	Rscript r/informational_cascade_simulation.R

sql:
	sqlite3 outputs/tables/herd_market.db < sql/schema.sql

all: data python r sql
