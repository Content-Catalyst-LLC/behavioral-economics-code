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
python3 python/generate_synthetic_heuristics_biases_panel.py
python3 python/causal_heuristics_biases_evaluation.py
python3 python/correction_capacity_welfare_analysis.py
python3 python/heuristic_design_sensitivity_analysis.py
python3 python/base_rate_neglect_simulation.py
```

Run R:

```bash
Rscript r/heuristics_biases_evaluation.R
Rscript r/heuristics_biases_robustness_checks.R
Rscript r/heuristic_judgment_simulation.R
```

Run Stata manually:

```stata
do stata/heuristics_biases_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/heuristics_biases.db < sql/schema.sql
```
