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
python3 python/generate_synthetic_mental_accounting_panel.py
python3 python/causal_mental_accounting_evaluation.py
python3 python/debt_savings_inefficiency_analysis.py
python3 python/windfall_spending_simulation.py
```

Run R:

```bash
Rscript r/mental_accounting_evaluation.R
Rscript r/mental_accounting_robustness_checks.R
Rscript r/windfall_spending_simulation.R
```

Run Stata manually:

```stata
do stata/mental_accounting_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/mental_accounting.db < sql/schema.sql
```
