.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_behavioral_finance_panel.py

python: data
	python3 python/causal_behavioral_finance_evaluation.py
	python3 python/behavioral_finance_mispricing_analysis.py
	python3 python/prospect_theory_investor_simulation.py

r: data
	Rscript r/behavioral_finance_evaluation.R
	Rscript r/behavioral_finance_robustness_checks.R
	Rscript r/prospect_theory_investor_simulation.R

sql:
	sqlite3 outputs/tables/behavioral_finance.db < sql/schema.sql

all: data python r sql
