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
python3 python/generate_synthetic_expected_utility_panel.py
python3 python/expected_utility_risk_aversion_evaluation.py
python3 python/certainty_equivalent_risk_premium_analysis.py
python3 python/insurance_portfolio_policy_risk_simulations.py
python3 python/sensitivity_expected_utility_parameters.py
```

Run R:

```bash
Rscript r/expected_utility_evaluation.R
Rscript r/expected_utility_robustness_checks.R
Rscript r/crra_choice_simulation.R
```

Run Stata manually:

```stata
do stata/expected_utility_evaluation.do
```

Build SQLite schema:

```bash
sqlite3 outputs/tables/expected_utility.db < sql/schema.sql
```
