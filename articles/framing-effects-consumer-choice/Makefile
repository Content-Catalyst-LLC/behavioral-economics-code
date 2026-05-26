.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_framing_effects_panel.py

python: data
	python3 python/causal_framing_effects_evaluation.py
	python3 python/framing_comprehension_welfare_analysis.py
	python3 python/framing_design_sensitivity_analysis.py

r: data
	Rscript r/framing_effects_evaluation.R
	Rscript r/framing_effects_robustness_checks.R
	Rscript r/gain_loss_frame_simulation.R

sql:
	sqlite3 outputs/tables/framing_effects.db < sql/schema.sql

all: data python r sql
