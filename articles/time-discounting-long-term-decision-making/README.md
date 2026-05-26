# Time Discounting and Long-Term Decision-Making

This article-level folder supports the article **Time Discounting and Long-Term Decision-Making**.

Article URL: https://sustainablecatalyst.com/time-discounting-long-term-decision-making/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/time-discounting-long-term-decision-making

## Purpose

This is a professional economist-facing computational scaffold for studying time discounting, intertemporal choice, exponential discounting, hyperbolic discounting, quasi-hyperbolic discounting, present bias, delayed reward, commitment support, savings behavior, debt, health investment, education, sustainability governance, digital-platform immediacy, institutional short-termism, and long-horizon policy design.

The scaffold is designed for behavioral economics, public economics, household finance, health economics, education policy, labor/productivity research, climate economics, sustainability policy, digital-platform governance, institutional design, and reproducible teaching examples.

## Research questions

1. How do exponential, present-biased, and commitment-supported discounting regimes affect delayed-choice rates?
2. How does present bias change cumulative delayed choices and synthetic welfare?
3. Does commitment support restore long-term choice under present-biased discounting?
4. When does commitment support create welfare gains, and when does reduced flexibility create burden?
5. How do discount factors, present-bias parameters, sophistication, and liquidity need shape intertemporal decisions?
6. How should analysts distinguish steep discounting from poverty, uncertainty, distrust, inflation risk, debt pressure, or liquidity constraint?
7. How do digital platforms compress time by making immediate action easier and future cost less salient?
8. How do discount rates affect climate policy, infrastructure maintenance, and intergenerational responsibility?
9. What robustness checks are required before treating discounting-related interventions as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic intertemporal-choice and time-discounting data that support:

- exponential discounting simulations
- present-biased discounting simulations
- quasi-hyperbolic discounting workflows
- commitment-support evaluation
- delayed-choice models
- present-value examples
- welfare and flexibility analysis
- treatment-effect estimation
- heterogeneous treatment effects by present bias, discount factor, sophistication, liquidity need, and future-goal value
- sustainability and long-horizon governance notes
- digital-platform timing and immediacy notes
- discount-rate sensitivity analysis
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, teaching, institutional learning, and reproducible behavioral-economics workflows. It is not financial advice, health advice, legal advice, productivity surveillance tooling, platform-engagement optimization, investment advice, or a tool for punitive design, exploitative commitment, manipulative credit products, or shifting structural burdens onto individuals.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/time-discounting-long-term-decision-making

python3 python/generate_synthetic_time_discounting_panel.py
python3 python/causal_time_discounting_evaluation.py
python3 python/time_discounting_welfare_flexibility_analysis.py
python3 python/discount_rate_sensitivity_analysis.py
python3 python/quasi_hyperbolic_discounting_simulation.py

Rscript r/time_discounting_evaluation.R
Rscript r/time_discounting_robustness_checks.R
Rscript r/quasi_hyperbolic_discounting_simulation.R

# In Stata:
# do stata/time_discounting_evaluation.do

sqlite3 outputs/tables/time_discounting.db < sql/schema.sql
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
