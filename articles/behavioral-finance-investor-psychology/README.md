# Behavioral Finance: Why Investors Deviate from Rational Models

This article-level folder supports the article **Behavioral Finance: Why Investors Deviate from Rational Models**.

Article URL: https://sustainablecatalyst.com/behavioral-finance-investor-psychology/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/behavioral-finance-investor-psychology

## Purpose

This is a professional behavioral-finance and economist-facing computational scaffold for studying how psychological biases, emotional responses, social influence, institutional incentives, platform design, bounded rationality, and market feedback affect investor behavior and financial-market outcomes.

The scaffold is designed for behavioral finance, financial economics, household finance, investor-protection research, market-stability analysis, platform-governance evaluation, policy design, and reproducible teaching examples.

## Research questions

1. How do overconfidence, loss aversion, anchoring, herding, and sentiment affect investor demand?
2. How do individual behavioral biases scale into market-level mispricing, volatility, and trading intensity?
3. Do stronger behavioral distortions increase absolute mispricing and turnover?
4. Does lower trading friction amplify behavioral market dynamics?
5. Does platform salience intensify herding, momentum, and investor attention?
6. How should analysts distinguish behavioral mispricing from common response to fundamentals?
7. How can investor-protection policy evaluate welfare rather than engagement alone?
8. How can financial systems preserve access while reducing avoidable behavioral harm?
9. How can market governance integrate psychology, institutions, technology, and financial stability?

## Econometric and computational design

The scaffold includes synthetic investor and market-history data that support:

- behavioral market-regime simulation
- investor-bias modeling
- prospect-theory value functions
- overconfidence and turnover diagnostics
- loss-aversion and reference-point workflows
- anchoring and herd-signal models
- platform-salience and trading-friction sensitivity
- mispricing diagnostics
- treatment-effect estimation
- household-finance and investor-protection notes
- financial-stability summary metrics
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, investor-protection analysis, financial education, policy-evaluation scaffolding, and reproducible behavioral-finance workflows. It is not investment advice, trading advice, market prediction, a trading strategy, or a tool for encouraging frequent trading, leverage, speculative activity, financial product promotion, or retail-investor targeting.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/behavioral-finance-investor-psychology

python3 python/generate_synthetic_behavioral_finance_panel.py
python3 python/causal_behavioral_finance_evaluation.py
python3 python/behavioral_finance_mispricing_analysis.py
python3 python/prospect_theory_investor_simulation.py

Rscript r/behavioral_finance_evaluation.R
Rscript r/behavioral_finance_robustness_checks.R
Rscript r/prospect_theory_investor_simulation.R

# In Stata:
# do stata/behavioral_finance_evaluation.do

sqlite3 outputs/tables/behavioral_finance.db < sql/schema.sql
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
