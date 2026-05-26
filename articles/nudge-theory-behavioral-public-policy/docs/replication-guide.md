# Replication Guide

## Requirements

Recommended:

- Python 3.10+
- R 4.2+
- Stata 17+
- SQLite
- Julia 1.9+

Python packages:

```bash
pip install -r requirements.txt
```

R scripts use base R where possible and optional packages only when available.

## Rebuild synthetic data

```bash
python3 python/generate_synthetic_nudge_policy_panel.py
```

## Run analysis

```bash
python3 python/causal_nudge_policy_evaluation.py
python3 python/nudge_welfare_analysis.py
Rscript r/nudge_policy_evaluation.R
Rscript r/nudge_welfare_robustness_checks.R
```

For Stata:

```stata
do stata/nudge_policy_evaluation.do
```

## Expected outputs

- `outputs/tables/synthetic_nudge_policy_panel.csv`
- `outputs/tables/synthetic_nudge_policy_experiment.csv`
- `outputs/regression_tables/python_nudge_policy_treatment_effects.csv`
- `outputs/regression_tables/r_nudge_policy_estimates.csv`
- `outputs/regression_tables/stata_nudge_policy_estimates.csv`
- `outputs/tables/nudge_policy_welfare_summary.csv`
- `outputs/model_diagnostics/nudge_welfare_sensitivity.csv`

## Reproducibility note

All data are synthetic and generated from fixed random seeds for repeatability.
