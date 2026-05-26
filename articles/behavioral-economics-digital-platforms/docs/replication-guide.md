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
python3 python/generate_synthetic_platform_panel.py
```

## Run analysis

```bash
python3 python/causal_platform_policy_evaluation.py
python3 python/platform_welfare_analysis.py
Rscript r/platform_policy_evaluation.R
Rscript r/platform_welfare_robustness_checks.R
```

For Stata:

```stata
do stata/platform_policy_evaluation.do
```

## Expected outputs

- `outputs/tables/synthetic_platform_panel.csv`
- `outputs/tables/synthetic_platform_experiment.csv`
- `outputs/regression_tables/python_platform_treatment_effects.csv`
- `outputs/regression_tables/r_platform_policy_estimates.csv`
- `outputs/regression_tables/stata_platform_policy_estimates.csv`
- `outputs/tables/platform_welfare_regime_summary.csv`
- `outputs/model_diagnostics/platform_welfare_weight_sensitivity.csv`

## Reproducibility note

All data are synthetic and generated from fixed random seeds for repeatability.
