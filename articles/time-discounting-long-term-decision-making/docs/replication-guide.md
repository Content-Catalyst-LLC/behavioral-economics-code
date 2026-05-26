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
python3 python/generate_synthetic_time_discounting_panel.py
python3 python/causal_time_discounting_evaluation.py
python3 python/time_discounting_welfare_flexibility_analysis.py
python3 python/discount_rate_sensitivity_analysis.py
python3 python/quasi_hyperbolic_discounting_simulation.py
```

Run R:

```bash
Rscript r/time_discounting_evaluation.R
Rscript r/time_discounting_robustness_checks.R
Rscript r/quasi_hyperbolic_discounting_simulation.R
```

Run Stata manually:

```stata
do stata/time_discounting_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/time_discounting.db < sql/schema.sql
```
