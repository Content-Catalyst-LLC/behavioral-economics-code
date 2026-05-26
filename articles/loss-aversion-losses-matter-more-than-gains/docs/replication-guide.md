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
python3 python/generate_synthetic_loss_aversion_panel.py
python3 python/loss_aversion_frame_evaluation.py
python3 python/disposition_effect_simulation.py
python3 python/endowment_consumer_policy_transition_models.py
python3 python/sensitivity_loss_aversion_parameters.py
```

Run R:

```bash
Rscript r/loss_aversion_evaluation.R
Rscript r/loss_aversion_robustness_checks.R
Rscript r/prospect_value_simulation.R
```

Run Stata manually:

```stata
do stata/loss_aversion_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/loss_aversion.db < sql/schema.sql
```
