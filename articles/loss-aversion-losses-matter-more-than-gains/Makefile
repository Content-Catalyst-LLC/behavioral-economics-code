.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_loss_aversion_panel.py

python: data
	python3 python/loss_aversion_frame_evaluation.py
	python3 python/disposition_effect_simulation.py
	python3 python/endowment_consumer_policy_transition_models.py
	python3 python/sensitivity_loss_aversion_parameters.py

r: data
	Rscript r/loss_aversion_evaluation.R
	Rscript r/loss_aversion_robustness_checks.R
	Rscript r/prospect_value_simulation.R

sql:
	sqlite3 outputs/tables/loss_aversion.db < sql/schema.sql

all: data python r sql
