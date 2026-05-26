# Replication Guide

Recommended requirements:

- Python 3.10+
- R 4.2+
- Stata 17+
- SQLite
- Julia 1.9+

Python dependencies:

```bash
pip install -r requirements.txt
```

Run the core workflow:

```bash
python3 python/generate_synthetic_bounded_rationality_panel.py
python3 python/bounded_rationality_constraint_evaluation.py
python3 python/administrative_burden_simulation.py
python3 python/organizational_routine_policy_simplification_models.py
python3 python/consumer_platform_search_friction_examples.py
python3 python/sensitivity_bounded_rationality_parameters.py
```

Run R:

```bash
Rscript r/bounded_rationality_evaluation.R
Rscript r/bounded_rationality_robustness_checks.R
Rscript r/search_satisficing_simulation.R
```

Run Stata manually:

```stata
do stata/bounded_rationality_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/bounded_rationality.db < sql/schema.sql
```
