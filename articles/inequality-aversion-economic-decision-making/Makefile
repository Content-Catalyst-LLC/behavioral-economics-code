.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_inequality_aversion_panel.py

python: data
	python3 python/causal_inequality_aversion_evaluation.py
	python3 python/inequality_aversion_welfare_analysis.py
	python3 python/bargaining_redistribution_simulation.py

r: data
	Rscript r/inequality_aversion_evaluation.R
	Rscript r/inequality_aversion_robustness_checks.R
	Rscript r/bargaining_redistribution_simulation.R

sql:
	sqlite3 outputs/tables/inequality_aversion.db < sql/schema.sql

all: data python r sql
