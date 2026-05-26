# Bounded Rationality: Cognitive Limits and Economic Decision-Making

This article-level folder supports the article **Bounded Rationality: Cognitive Limits and Economic Decision-Making**.

Article URL: https://sustainablecatalyst.com/bounded-rationality-economic-decision-making/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/bounded-rationality-economic-decision-making

## Purpose

This is a professional economist-facing computational scaffold for studying bounded rationality, search costs, satisficing, aspiration thresholds, cognitive-load constraints, time pressure, decision quality, optimization gaps, administrative burden, organizational routines, consumer search frictions, financial decision complexity, digital-platform choice architecture, sustainability decision systems, institutional design, public-policy simplification, and welfare analysis.

The scaffold is designed for behavioral economics, applied microeconomics, public economics, organizational economics, institutional economics, consumer protection, behavioral finance, public administration, platform governance, sustainability policy, and reproducible teaching examples.

## Research questions

1. How do search costs and cognitive-load constraints change decision quality?
2. When does satisficing outperform exhaustive search once search costs are included?
3. How do aspiration thresholds affect search depth and optimization gaps?
4. How do time pressure and stress change sequential search behavior?
5. How does administrative burden reduce access to public benefits or rights?
6. How do organizational routines reduce decision burden while creating path dependence?
7. How do consumer search frictions affect plan choice, switching, fees, and welfare?
8. How do digital platforms use defaults, rankings, and friction asymmetry to shape bounded decision-making?
9. How can policy simplification improve take-up, comprehension, and welfare?
10. What robustness checks are required before calling a bounded-rationality intervention welfare-improving?

## Econometric and computational design

The scaffold includes synthetic bounded-rationality data that support:

- sequential-search simulations
- satisficing versus optimization comparisons
- search-cost and time-pressure models
- cognitive-load constraints
- aspiration-threshold workflows
- optimization-gap analysis
- administrative-burden simulations
- policy-simplification workflows
- organizational-routine models
- consumer-search and switching-cost examples
- financial-decision complexity examples
- digital-platform default and friction scaffolds
- sustainability-decision system simulations
- treatment-effect-style estimation by constraint regime
- heterogeneity by aspiration level, search cost, cognitive capacity, stress, numeracy, institutional trust, digital access, income security, and administrative capacity
- welfare and distributional sensitivity analysis
- robustness checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, decision-theory teaching, administrative-burden analysis, policy-simplification design, consumer-protection analysis, organizational learning, sustainability governance, platform accountability, institutional design, and reproducible behavioral-economics workflows. It is not a toolkit for designing confusing disclosures, hidden fees, burdensome public programs, manipulative defaults, dark-pattern interfaces, exclusionary administrative systems, or complexity that exploits cognitive limits.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/bounded-rationality-economic-decision-making

python3 python/generate_synthetic_bounded_rationality_panel.py
python3 python/bounded_rationality_constraint_evaluation.py
python3 python/administrative_burden_simulation.py
python3 python/organizational_routine_policy_simplification_models.py
python3 python/consumer_platform_search_friction_examples.py
python3 python/sensitivity_bounded_rationality_parameters.py

Rscript r/bounded_rationality_evaluation.R
Rscript r/bounded_rationality_robustness_checks.R
Rscript r/search_satisficing_simulation.R

# In Stata:
# do stata/bounded_rationality_evaluation.do

sqlite3 outputs/tables/bounded_rationality.db < sql/schema.sql
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
