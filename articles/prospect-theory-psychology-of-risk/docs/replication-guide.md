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
python3 python/generate_synthetic_prospect_theory_panel.py
python3 python/prospect_theory_frame_evaluation.py
python3 python/expected_utility_comparison.py
python3 python/fourfold_risk_attitudes_simulation.py
python3 python/insurance_lottery_policy_risk_examples.py
python3 python/sensitivity_prospect_theory_parameters.py
```

Run R:

```bash
Rscript r/prospect_theory_evaluation.R
Rscript r/prospect_theory_robustness_checks.R
Rscript r/prospect_value_probability_weighting_simulation.R
```

Run Stata manually:

```stata
do stata/prospect_theory_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/prospect_theory.db < sql/schema.sql
```
