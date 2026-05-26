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
python3 python/generate_synthetic_herd_market_panel.py
python3 python/causal_herd_market_evaluation.py
python3 python/herd_market_welfare_stability_analysis.py
python3 python/informational_cascade_simulation.py
```

Run R:

```bash
Rscript r/herd_market_evaluation.R
Rscript r/herd_market_robustness_checks.R
Rscript r/informational_cascade_simulation.R
```

Run Stata manually:

```stata
do stata/herd_market_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/herd_market.db < sql/schema.sql
```
