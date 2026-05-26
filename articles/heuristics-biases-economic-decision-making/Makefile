.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_heuristics_biases_panel.py

python: data
	python3 python/causal_heuristics_biases_evaluation.py
	python3 python/correction_capacity_welfare_analysis.py
	python3 python/heuristic_design_sensitivity_analysis.py
	python3 python/base_rate_neglect_simulation.py

r: data
	Rscript r/heuristics_biases_evaluation.R
	Rscript r/heuristics_biases_robustness_checks.R
	Rscript r/heuristic_judgment_simulation.R

sql:
	sqlite3 outputs/tables/heuristics_biases.db < sql/schema.sql

all: data python r sql
