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
python3 python/generate_synthetic_framing_effects_panel.py
python3 python/causal_framing_effects_evaluation.py
python3 python/framing_comprehension_welfare_analysis.py
python3 python/framing_design_sensitivity_analysis.py
```

Run R:

```bash
Rscript r/framing_effects_evaluation.R
Rscript r/framing_effects_robustness_checks.R
Rscript r/gain_loss_frame_simulation.R
```

Run Stata manually:

```stata
do stata/framing_effects_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/framing_effects.db < sql/schema.sql
```
