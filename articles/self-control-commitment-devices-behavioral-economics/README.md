# Self-Control and Commitment Devices in Behavioral Economics

This article-level folder supports the article **Self-Control and Commitment Devices in Behavioral Economics**.

Article URL: https://sustainablecatalyst.com/self-control-commitment-devices-behavioral-economics/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/self-control-commitment-devices-behavioral-economics

## Purpose

This is a professional economist-facing computational scaffold for studying self-control problems, time-inconsistent preferences, present bias, quasi-hyperbolic discounting, planner-doer conflict, commitment devices, automatic enrollment, withdrawal penalties, default escalation, digital commitment tools, liquidity constraints, welfare tradeoffs, and long-horizon institutional design.

The scaffold is designed for behavioral economics, household finance, public economics, development economics, health economics, education policy, labor/productivity research, digital-platform governance, sustainability governance, and reproducible teaching examples.

## Research questions

1. How do present bias and time inconsistency affect long-term savings, welfare, and plan adherence?
2. Do stronger commitment devices increase accumulated savings?
3. When does stronger commitment reduce welfare by limiting flexibility during emergencies?
4. How do automation, default enrollment, withdrawal penalties, and commitment costs interact?
5. Which groups benefit most from commitment: sophisticated agents, strongly present-biased agents, or agents with stable income?
6. How should policy distinguish behavior change from welfare improvement?
7. How do liquidity risk and emergency shocks change the optimal commitment design?
8. Can digital commitment tools support agency without becoming manipulative?
9. What robustness checks are required before treating commitment-device effects as policy evidence?

## Econometric and computational design

The scaffold includes synthetic household-finance and commitment-regime data that support:

- present-bias simulation
- quasi-hyperbolic discounting workflows
- planner-doer and temptation models
- automatic enrollment and savings-default simulations
- commitment-cost and withdrawal-penalty analysis
- liquidity and emergency-shock diagnostics
- welfare analysis
- treatment-effect estimation
- heterogeneous treatment effects by present bias, sophistication, liquidity need, income volatility, and emergency risk
- digital commitment and institutional-design notes
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, household-finance teaching, institutional learning, and reproducible behavioral-economics workflows. It is not financial advice, health advice, legal advice, or a tool for punitive design, exploitative penalties, manipulative subscriptions, coercive productivity systems, or shifting structural burdens onto individuals.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/self-control-commitment-devices-behavioral-economics

python3 python/generate_synthetic_commitment_savings_panel.py
python3 python/causal_commitment_savings_evaluation.py
python3 python/commitment_welfare_flexibility_analysis.py
python3 python/quasi_hyperbolic_discounting_simulation.py

Rscript r/commitment_savings_evaluation.R
Rscript r/commitment_robustness_checks.R
Rscript r/quasi_hyperbolic_discounting_simulation.R

# In Stata:
# do stata/commitment_savings_evaluation.do

sqlite3 outputs/tables/commitment_devices.db < sql/schema.sql
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
