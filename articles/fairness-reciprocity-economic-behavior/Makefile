.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_fairness_reciprocity_panel.py

python: data
	python3 python/causal_fairness_reciprocity_evaluation.py
	python3 python/fairness_reciprocity_welfare_analysis.py
	python3 python/bargaining_punishment_simulation.py

r: data
	Rscript r/fairness_reciprocity_evaluation.R
	Rscript r/fairness_reciprocity_robustness_checks.R
	Rscript r/bargaining_punishment_simulation.R

sql:
	sqlite3 outputs/tables/fairness_reciprocity.db < sql/schema.sql

all: data python r sql
