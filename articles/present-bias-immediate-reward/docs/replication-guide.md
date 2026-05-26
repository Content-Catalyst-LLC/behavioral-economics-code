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
python3 python/generate_synthetic_present_bias_panel.py
python3 python/causal_present_bias_evaluation.py
python3 python/present_bias_welfare_flexibility_analysis.py
python3 python/quasi_hyperbolic_discounting_simulation.py
```

Run R:

```bash
Rscript r/present_bias_evaluation.R
Rscript r/present_bias_robustness_checks.R
Rscript r/quasi_hyperbolic_discounting_simulation.R
```

Run Stata manually:

```stata
do stata/present_bias_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/present_bias.db < sql/schema.sql
```
