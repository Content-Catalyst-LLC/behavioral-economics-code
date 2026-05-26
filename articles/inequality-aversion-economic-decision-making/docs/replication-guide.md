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
python3 python/generate_synthetic_inequality_aversion_panel.py
python3 python/causal_inequality_aversion_evaluation.py
python3 python/inequality_aversion_welfare_analysis.py
python3 python/bargaining_redistribution_simulation.py
```

Run R:

```bash
Rscript r/inequality_aversion_evaluation.R
Rscript r/inequality_aversion_robustness_checks.R
Rscript r/bargaining_redistribution_simulation.R
```

Run Stata manually:

```stata
do stata/inequality_aversion_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/inequality_aversion.db < sql/schema.sql
```
