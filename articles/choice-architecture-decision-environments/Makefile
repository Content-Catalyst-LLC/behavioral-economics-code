.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_choice_architecture_panel.py

python: data
	python3 python/causal_choice_architecture_evaluation.py
	python3 python/choice_architecture_welfare_analysis.py

r: data
	Rscript r/choice_architecture_evaluation.R
	Rscript r/choice_architecture_robustness_checks.R

sql:
	sqlite3 outputs/tables/choice_architecture.db < sql/schema.sql

all: data python r sql
