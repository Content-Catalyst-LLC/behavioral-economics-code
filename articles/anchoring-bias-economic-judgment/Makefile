.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_anchoring_bias_panel.py

python: data
	python3 python/causal_anchoring_bias_evaluation.py
	python3 python/anchoring_adjustment_welfare_analysis.py
	python3 python/anchoring_design_sensitivity_analysis.py
	python3 python/reference_price_simulation.py

r: data
	Rscript r/anchoring_bias_evaluation.R
	Rscript r/anchoring_bias_robustness_checks.R
	Rscript r/anchor_adjustment_simulation.R

sql:
	sqlite3 outputs/tables/anchoring_bias.db < sql/schema.sql

all: data python r sql
