# Mental Accounting in Personal Finance

This article-level folder supports the article **Mental Accounting in Personal Finance**.

Article URL: https://sustainablecatalyst.com/mental-accounting-personal-finance/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/mental-accounting-personal-finance

## Purpose

This is a professional economist-facing computational scaffold for studying mental accounting, money fungibility, household budgeting, windfall spending, labeled savings, debt repayment, emergency reserves, liquidity constraints, financial resilience, integrated balance-sheet prompts, consumer-protection design, digital finance, and behavioral public policy.

The scaffold is designed for behavioral economics, household finance, consumer finance, public economics, personal-finance research, investor and consumer protection, digital-finance governance, policy evaluation, and reproducible teaching examples.

## Research questions

1. How do mental-account labels affect windfall spending, debt repayment, and savings preservation?
2. Do integrated balance-sheet prompts reduce debt-savings inefficiency?
3. When does mental accounting support household discipline, and when does it block welfare-improving reallocation?
4. How does savings-label strength affect repayment of high-interest debt?
5. How do emergency-risk and liquidity constraints change the interpretation of apparently inefficient behavior?
6. Do unified money views improve financial resilience, or do they reduce useful self-control boundaries?
7. How should budgeting apps and digital-finance interfaces display category-level and whole-balance-sheet information?
8. How can policy work with mental accounting without creating paternalistic or rigid account restrictions?
9. What robustness checks are required before treating mental-accounting interventions as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic household-finance and mental-accounting data that support:

- segmented mental-account simulations
- integrated balance-sheet prompt simulations
- unified fungible-money counterfactual workflows
- windfall-spending models
- labeled-savings and debt-repayment diagnostics
- emergency reserve and liquidity-risk analysis
- debt-savings inefficiency gap measures
- annual interest-cost estimation
- financial resilience indexes
- treatment-effect estimation
- heterogeneous effects by savings-label strength, present bias, income, emergency risk, debt burden, and liquidity constraints
- consumer-protection and digital-finance notes
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, household-finance teaching, consumer-protection analysis, institutional learning, and reproducible behavioral-economics workflows. It is not financial advice, legal advice, credit counseling, product marketing, or a tool for exploiting household financial vulnerability through hidden fees, restrictive account labels, dark patterns, or manipulative spending prompts.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/mental-accounting-personal-finance

python3 python/generate_synthetic_mental_accounting_panel.py
python3 python/causal_mental_accounting_evaluation.py
python3 python/debt_savings_inefficiency_analysis.py
python3 python/windfall_spending_simulation.py

Rscript r/mental_accounting_evaluation.R
Rscript r/mental_accounting_robustness_checks.R
Rscript r/windfall_spending_simulation.R

# In Stata:
# do stata/mental_accounting_evaluation.do

sqlite3 outputs/tables/mental_accounting.db < sql/schema.sql
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
