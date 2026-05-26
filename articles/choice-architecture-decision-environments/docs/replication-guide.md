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
python3 python/generate_synthetic_choice_architecture_panel.py
```

## Run analysis

```bash
python3 python/causal_choice_architecture_evaluation.py
python3 python/choice_architecture_welfare_analysis.py
Rscript r/choice_architecture_evaluation.R
Rscript r/choice_architecture_robustness_checks.R
```

For Stata:

```stata
do stata/choice_architecture_evaluation.do
```

## Expected outputs

- `outputs/tables/synthetic_choice_architecture_panel.csv`
- `outputs/tables/synthetic_choice_architecture_experiment.csv`
- `outputs/regression_tables/python_choice_architecture_treatment_effects.csv`
- `outputs/regression_tables/r_choice_architecture_estimates.csv`
- `outputs/regression_tables/stata_choice_architecture_estimates.csv`
- `outputs/tables/choice_architecture_welfare_summary.csv`
- `outputs/model_diagnostics/choice_architecture_welfare_sensitivity.csv`

## Reproducibility note

All data are synthetic and generated from fixed random seeds for repeatability.
