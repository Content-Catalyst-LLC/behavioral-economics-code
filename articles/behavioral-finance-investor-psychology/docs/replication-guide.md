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
python3 python/generate_synthetic_behavioral_finance_panel.py
python3 python/causal_behavioral_finance_evaluation.py
python3 python/behavioral_finance_mispricing_analysis.py
python3 python/prospect_theory_investor_simulation.py
```

Run R:

```bash
Rscript r/behavioral_finance_evaluation.R
Rscript r/behavioral_finance_robustness_checks.R
Rscript r/prospect_theory_investor_simulation.R
```

Run Stata manually:

```stata
do stata/behavioral_finance_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/behavioral_finance.db < sql/schema.sql
```
