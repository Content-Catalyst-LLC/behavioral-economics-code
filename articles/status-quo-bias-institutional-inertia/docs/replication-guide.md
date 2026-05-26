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
python3 python/generate_synthetic_status_quo_bias_panel.py
python3 python/causal_status_quo_bias_evaluation.py
python3 python/switching_cost_welfare_analysis.py
python3 python/default_design_sensitivity_analysis.py
```

Run R:

```bash
Rscript r/status_quo_bias_evaluation.R
Rscript r/status_quo_bias_robustness_checks.R
Rscript r/default_retention_simulation.R
```

Run Stata manually:

```stata
do stata/status_quo_bias_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/status_quo_bias.db < sql/schema.sql
```
