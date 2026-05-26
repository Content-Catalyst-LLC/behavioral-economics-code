# Status Quo Bias and Institutional Inertia

This article-level folder supports the article **Status Quo Bias and Institutional Inertia**.

Article URL: https://sustainablecatalyst.com/status-quo-bias-institutional-inertia/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/status-quo-bias-institutional-inertia

## Purpose

This is a professional economist-facing computational scaffold for studying status quo bias, institutional inertia, default retention, switching costs, loss aversion, regret avoidance, active choice, pro-switching support, administrative burden, consumer switching, retirement defaults, digital subscriptions, platform lock-in, policy reform, and sustainability transitions.

The scaffold is designed for behavioral economics, applied microeconomics, household finance, public economics, consumer protection, digital-platform governance, regulatory policy, institutional economics, sustainability policy, organizational economics, and reproducible teaching examples.

## Research questions

1. How do defaults, switching costs, loss aversion, and status quo premiums affect adoption of objectively better alternatives?
2. When does persistence reflect genuine preference, and when does it reflect inertia?
3. Do active-choice designs reduce harmful default retention?
4. Do pro-switching defaults and switching support improve welfare?
5. Which groups are most affected by switching costs, decision fatigue, uncertainty, and administrative burden?
6. How do digital subscriptions, auto-renewal systems, and platform ecosystems monetize status quo bias?
7. How does institutional inertia slow policy reform, technology migration, and sustainability transitions?
8. How can default design support autonomy without exploiting inattention?
9. What robustness checks are required before treating default interventions as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic decision-regime data that support:

- status quo bias simulations
- default-retention models
- switching-cost diagnostics
- loss-aversion and regret-avoidance workflows
- active-choice policy simulations
- pro-switching default simulations
- institutional-inertia and path-dependence notes
- subscription and digital-platform switching-friction notes
- sustainability-transition inertia notes
- treatment-effect estimation
- heterogeneous treatment effects by switching cost, loss aversion, decision fatigue, uncertainty, and sophistication
- welfare analysis
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, consumer-protection analysis, institutional learning, public-interest design review, and reproducible behavioral-economics workflows. It is not a tool for exploitative subscription design, dark-pattern defaults, manipulative lock-in, anti-competitive switching friction, administrative exclusion, or using behavioral insights to preserve unjust or inefficient status quos.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/status-quo-bias-institutional-inertia

python3 python/generate_synthetic_status_quo_bias_panel.py
python3 python/causal_status_quo_bias_evaluation.py
python3 python/switching_cost_welfare_analysis.py
python3 python/default_design_sensitivity_analysis.py

Rscript r/status_quo_bias_evaluation.R
Rscript r/status_quo_bias_robustness_checks.R
Rscript r/default_retention_simulation.R

# In Stata:
# do stata/status_quo_bias_evaluation.do

sqlite3 outputs/tables/status_quo_bias.db < sql/schema.sql
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
