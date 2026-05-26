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
python3 python/generate_synthetic_anchoring_bias_panel.py
python3 python/causal_anchoring_bias_evaluation.py
python3 python/anchoring_adjustment_welfare_analysis.py
python3 python/anchoring_design_sensitivity_analysis.py
python3 python/reference_price_simulation.py
```

Run R:

```bash
Rscript r/anchoring_bias_evaluation.R
Rscript r/anchoring_bias_robustness_checks.R
Rscript r/anchor_adjustment_simulation.R
```

Run Stata manually:

```stata
do stata/anchoring_bias_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/anchoring_bias.db < sql/schema.sql
```
