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

R packages are optional. The R scripts use base R where possible and use additional packages only when available.

## Rebuild synthetic data

```bash
python3 python/generate_synthetic_interface_panel.py
```

## Run analysis

```bash
python3 python/causal_interface_policy_evaluation.py
python3 python/welfare_analysis.py
Rscript r/interface_policy_evaluation.R
Rscript r/welfare_robustness_checks.R
```

For Stata:

```stata
do stata/interface_policy_evaluation.do
```

## Expected outputs

- `outputs/tables/synthetic_interface_panel.csv`
- `outputs/tables/synthetic_interface_experiment.csv`
- `outputs/regression_tables/python_treatment_effects.csv`
- `outputs/regression_tables/r_interface_policy_estimates.csv`
- `outputs/regression_tables/stata_interface_policy_estimates.csv`
- `outputs/tables/welfare_regime_summary.csv`
- `outputs/model_diagnostics/robustness_summary.csv`

## Reproducibility note

All data are synthetic and generated from fixed random seeds for repeatability.
