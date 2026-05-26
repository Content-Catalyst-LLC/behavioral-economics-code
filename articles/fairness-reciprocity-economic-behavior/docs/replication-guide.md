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
python3 python/generate_synthetic_fairness_reciprocity_panel.py
python3 python/causal_fairness_reciprocity_evaluation.py
python3 python/fairness_reciprocity_welfare_analysis.py
python3 python/bargaining_punishment_simulation.py
```

Run R:

```bash
Rscript r/fairness_reciprocity_evaluation.R
Rscript r/fairness_reciprocity_robustness_checks.R
Rscript r/bargaining_punishment_simulation.R
```

Run Stata manually:

```stata
do stata/fairness_reciprocity_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/fairness_reciprocity.db < sql/schema.sql
```
