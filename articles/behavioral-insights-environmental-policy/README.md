# Behavioral Insights in Environmental Policy

This article-level folder supports the article **Behavioral Insights in Environmental Policy**.

Article URL: https://sustainablecatalyst.com/behavioral-insights-environmental-policy/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/behavioral-insights-environmental-policy

## Purpose

This is a professional economist-facing computational scaffold for studying behavioral environmental policy. It focuses on green defaults, social-norm feedback, present bias, administrative friction, energy-burden heterogeneity, environmental program uptake, welfare accounting, distributional analysis, causal policy evaluation, and robustness testing.

The scaffold is designed for applied behavioral economics, environmental economics, public economics, policy evaluation, climate-policy implementation research, and reproducible teaching examples.

## Research questions

This repository is organized around questions economists and policy researchers can test:

1. Do green defaults increase environmental program uptake?
2. Do social-norm signals raise adoption beyond private environmental concern?
3. Does administrative friction reduce uptake, especially among high-energy-burden households?
4. Do integrated designs outperform price-signal-only environmental policy?
5. Are welfare gains distributed evenly across income and energy-burden groups?
6. How sensitive are results to assumptions about environmental benefit, fiscal cost, administrative cost, and present bias?
7. Can behavioral design improve environmental policy implementation without substituting for pricing, regulation, infrastructure, or public investment?

## Econometric design

The scaffold includes synthetic panel and experiment-style data that support:

- randomized environmental policy treatment comparisons
- treatment-effect estimation
- panel / difference-in-differences style workflows
- heterogeneous treatment effects by income, energy burden, trust, and present bias
- welfare analysis with household, environmental, fiscal, and administrative components
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible environmental policy analysis. It is not intended for manipulating public consent, greenwashing, targeting vulnerable households, obscuring policy costs, or replacing structural climate and environmental policy with messaging alone.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/behavioral-insights-environmental-policy

# Generate synthetic environmental policy panel and experiment data
python3 python/generate_synthetic_environmental_policy_panel.py

# Run Python policy evaluation and welfare analysis
python3 python/causal_environmental_policy_evaluation.py
python3 python/environmental_welfare_analysis.py

# Run R policy evaluation and robustness checks
Rscript r/environmental_policy_evaluation.R
Rscript r/environmental_welfare_robustness_checks.R

# Run Stata workflow manually from Stata
# do stata/environmental_policy_evaluation.do

# Build SQL database
sqlite3 outputs/tables/environmental_policy.db < sql/schema.sql
```

## Folder structure

```text
data/
  raw/
  processed/
docs/
notebooks/
outputs/
  figures/
  tables/
  regression_tables/
  model_diagnostics/
python/
r/
stata/
julia/
sql/
c/
cpp/
fortran/
rust/
go/
tests/
```
