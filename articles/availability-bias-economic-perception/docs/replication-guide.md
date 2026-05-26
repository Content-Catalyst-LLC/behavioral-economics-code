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
python3 python/generate_synthetic_availability_bias_panel.py
python3 python/causal_availability_bias_evaluation.py
python3 python/availability_calibration_welfare_analysis.py
python3 python/availability_design_sensitivity_analysis.py
```

Run R:

```bash
Rscript r/availability_bias_evaluation.R
Rscript r/availability_bias_robustness_checks.R
Rscript r/availability_salience_simulation.R
```

Run Stata manually:

```stata
do stata/availability_bias_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/availability_bias.db < sql/schema.sql
```
