.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_trust_cooperation_panel.py

python: data
	python3 python/causal_trust_cooperation_evaluation.py
	python3 python/trust_cooperation_welfare_analysis.py
	python3 python/repeated_exchange_simulation.py

r: data
	Rscript r/trust_cooperation_evaluation.R
	Rscript r/trust_cooperation_robustness_checks.R
	Rscript r/repeated_exchange_simulation.R

sql:
	sqlite3 outputs/tables/trust_cooperation.db < sql/schema.sql

all: data python r sql
