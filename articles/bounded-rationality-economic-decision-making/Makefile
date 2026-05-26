.PHONY: data python r sql all

data:
	python3 python/generate_synthetic_bounded_rationality_panel.py

python: data
	python3 python/bounded_rationality_constraint_evaluation.py
	python3 python/administrative_burden_simulation.py
	python3 python/organizational_routine_policy_simplification_models.py
	python3 python/consumer_platform_search_friction_examples.py
	python3 python/sensitivity_bounded_rationality_parameters.py

r: data
	Rscript r/bounded_rationality_evaluation.R
	Rscript r/bounded_rationality_robustness_checks.R
	Rscript r/search_satisficing_simulation.R

sql:
	sqlite3 outputs/tables/bounded_rationality.db < sql/schema.sql

all: data python r sql
