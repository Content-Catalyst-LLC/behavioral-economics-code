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
python3 python/generate_synthetic_overconfidence_panel.py
python3 python/causal_overconfidence_evaluation.py
python3 python/overconfidence_turnover_cost_analysis.py
python3 python/performance_attribution_simulation.py
```

Run R:

```bash
Rscript r/overconfidence_evaluation.R
Rscript r/overconfidence_robustness_checks.R
Rscript r/performance_attribution_simulation.R
```

Run Stata manually:

```stata
do stata/overconfidence_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/overconfidence.db < sql/schema.sql
```
