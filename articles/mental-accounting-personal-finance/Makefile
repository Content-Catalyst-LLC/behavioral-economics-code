.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_mental_accounting_panel.py

python: data
	python3 python/causal_mental_accounting_evaluation.py
	python3 python/debt_savings_inefficiency_analysis.py
	python3 python/windfall_spending_simulation.py

r: data
	Rscript r/mental_accounting_evaluation.R
	Rscript r/mental_accounting_robustness_checks.R
	Rscript r/windfall_spending_simulation.R

sql:
	sqlite3 outputs/tables/mental_accounting.db < sql/schema.sql

all: data python r sql
