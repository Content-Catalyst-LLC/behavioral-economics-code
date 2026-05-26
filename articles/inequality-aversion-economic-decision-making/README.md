# Inequality Aversion in Economic Decision-Making

This article-level folder supports the article **Inequality Aversion in Economic Decision-Making**.

Article URL: https://sustainablecatalyst.com/inequality-aversion-economic-decision-making/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/inequality-aversion-economic-decision-making

## Purpose

This is a professional economist-facing computational scaffold for studying inequality aversion, social preferences, bargaining, redistribution, wage fairness, distributive legitimacy, taxation, public policy, organizational compensation, and behavioral political economy.

The scaffold is designed for applied behavioral economics, public economics, labor economics, organizational economics, political economy, welfare analysis, policy evaluation, and reproducible teaching examples.

## Research questions

1. How do disadvantageous and advantageous inequality-aversion parameters alter bargaining outcomes?
2. Do stronger disadvantageous inequality-aversion parameters increase rejection of unequal offers?
3. How do redistribution preferences depend on merit beliefs, institutional trust, and social-preference parameters?
4. Do equal, advantageous-inequality, and disadvantageous-inequality regimes produce different welfare rankings under Fehr-Schmidt preferences?
5. How sensitive are results to alpha, beta, process-legitimacy, tax-rate, and redistribution-weight assumptions?
6. Does reducing measured inequality improve social-preference welfare, institutional legitimacy, or policy support?
7. Are high-inequality-aversion groups affected differently by distributional interventions?
8. Can economists distinguish inequality aversion from altruism, envy, merit beliefs, and process-fairness concerns?

## Econometric and computational design

The scaffold includes synthetic panel and experiment-style data that support:

- Fehr-Schmidt social-preference utility analysis
- ERC-style relative-share diagnostics
- ultimatum-style bargaining simulations
- redistribution and tax-rate simulations
- wage-fairness and compensation-distribution scaffolding
- treatment-effect estimation
- heterogeneous treatment effects by alpha, beta, merit beliefs, redistribution norms, and institutional trust
- welfare analysis with material payoff, inequality penalty, legitimacy effects, and process fairness
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible social-preference analysis. It is not intended for manipulating distributive resentment, suppressing justified fairness concerns, justifying exploitative inequality, or reducing structural injustice to individual preference parameters.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/inequality-aversion-economic-decision-making

python3 python/generate_synthetic_inequality_aversion_panel.py
python3 python/causal_inequality_aversion_evaluation.py
python3 python/inequality_aversion_welfare_analysis.py
python3 python/bargaining_redistribution_simulation.py

Rscript r/inequality_aversion_evaluation.R
Rscript r/inequality_aversion_robustness_checks.R
Rscript r/bargaining_redistribution_simulation.R

# In Stata:
# do stata/inequality_aversion_evaluation.do

sqlite3 outputs/tables/inequality_aversion.db < sql/schema.sql
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
