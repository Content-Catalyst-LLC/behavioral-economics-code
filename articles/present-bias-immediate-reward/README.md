# Present Bias and the Psychology of Immediate Reward

This article-level folder supports the article **Present Bias and the Psychology of Immediate Reward**.

Article URL: https://sustainablecatalyst.com/present-bias-immediate-reward/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/present-bias-immediate-reward

## Purpose

This is a professional economist-facing computational scaffold for studying present bias, immediate reward, intertemporal choice, quasi-hyperbolic discounting, time-inconsistent preferences, delayed gratification, self-control problems, commitment devices, digital-platform immediacy, household finance, health behavior, education, productivity, sustainability governance, and institutional short-termism.

The scaffold is designed for behavioral economics, public economics, household finance, health economics, education policy, labor/productivity research, environmental policy, digital-platform governance, institutional design, and reproducible teaching examples.

## Research questions

1. How does present bias affect delayed choice, cumulative welfare, savings, effort, and long-term goal adherence?
2. Do commitment devices increase delayed-choice rates under time-inconsistent preferences?
3. When does strong commitment improve outcomes, and when does reduced flexibility create welfare loss?
4. How do reminder strength, automation, defaults, and deviation costs interact?
5. Which groups benefit most from commitment: strongly present-biased agents, sophisticated agents, or agents with low liquidity risk?
6. How should analysts distinguish present bias from poverty, scarcity, institutional barriers, health constraints, or information gaps?
7. How do digital platforms amplify present bias through immediacy, low friction, notifications, and variable reward?
8. How can sustainability and infrastructure policy protect future benefits from present-oriented institutional incentives?
9. What robustness checks are required before treating present-bias interventions as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic intertemporal-choice and present-bias data that support:

- quasi-hyperbolic discounting workflows
- delayed-choice simulations
- immediate temptation and future-goal models
- commitment-regime evaluation
- reminder and automation support models
- flexibility and hardship diagnostics
- welfare analysis
- treatment-effect estimation
- heterogeneous treatment effects by present bias, sophistication, liquidity need, patience, and commitment strength
- digital-platform immediacy notes
- sustainability and institutional-design notes
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, teaching, institutional learning, and reproducible behavioral-economics workflows. It is not financial advice, health advice, legal advice, productivity surveillance tooling, platform-engagement optimization, or a tool for punitive design, exploitative commitment, manipulative subscription systems, or shifting structural burdens onto individuals.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/present-bias-immediate-reward

python3 python/generate_synthetic_present_bias_panel.py
python3 python/causal_present_bias_evaluation.py
python3 python/present_bias_welfare_flexibility_analysis.py
python3 python/quasi_hyperbolic_discounting_simulation.py

Rscript r/present_bias_evaluation.R
Rscript r/present_bias_robustness_checks.R
Rscript r/quasi_hyperbolic_discounting_simulation.R

# In Stata:
# do stata/present_bias_evaluation.do

sqlite3 outputs/tables/present_bias.db < sql/schema.sql
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
