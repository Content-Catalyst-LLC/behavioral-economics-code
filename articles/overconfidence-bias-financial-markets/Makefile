.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_overconfidence_panel.py

python: data
	python3 python/causal_overconfidence_evaluation.py
	python3 python/overconfidence_turnover_cost_analysis.py
	python3 python/performance_attribution_simulation.py

r: data
	Rscript r/overconfidence_evaluation.R
	Rscript r/overconfidence_robustness_checks.R
	Rscript r/performance_attribution_simulation.R

sql:
	sqlite3 outputs/tables/overconfidence.db < sql/schema.sql

all: data python r sql
