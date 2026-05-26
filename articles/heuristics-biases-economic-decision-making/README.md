# Heuristics and Biases in Economic Decision-Making

This article-level folder supports the article **Heuristics and Biases in Economic Decision-Making**.

Article URL: https://sustainablecatalyst.com/heuristics-biases-economic-decision-making/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/heuristics-biases-economic-decision-making

## Purpose

This is a professional economist-facing computational scaffold for studying heuristic judgment, systematic bias, availability, representativeness, anchoring, framing effects, overconfidence, cognitive load, correction capacity, base-rate neglect, judgment error, decision quality, welfare proxies, behavioral public policy, consumer protection, digital-platform choice environments, sustainability governance, and institutional decision design.

The scaffold is designed for behavioral economics, applied microeconomics, behavioral finance, household finance, consumer protection, public economics, platform governance, risk communication, climate economics, sustainability policy, institutional economics, and reproducible teaching examples.

## Research questions

1. How do availability, representativeness, anchoring, and framing signals compound into judgment error?
2. How do numeracy, domain knowledge, disclosure quality, and debiasing support reduce heuristic distortion?
3. How does cognitive load amplify judgment error?
4. How does confidence interact with error and welfare?
5. Which cognitive environments produce the greatest absolute judgment error?
6. Which decision-environment designs improve correction capacity?
7. How should policy distinguish behavior change from welfare improvement?
8. How can digital platforms correct rather than exploit predictable cognitive shortcuts?
9. How should sustainability communication make slow systemic risks visible without manipulating fear?
10. What robustness checks are required before treating a debiasing intervention as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic judgment-regime data that support:

- low-bias, medium-bias, and high-bias cognitive environments
- availability-bias simulations
- representativeness and base-rate neglect examples
- anchoring and adjustment examples
- framing-effect models
- overconfidence and confidence-adjusted error diagnostics
- correction-capacity workflows
- cognitive-load sensitivity analysis
- decision-quality and welfare proxy analysis
- consumer-protection and platform-design notes
- sustainability and climate-risk communication notes
- treatment-effect estimation
- heterogeneous treatment effects by correction capacity, numeracy, domain knowledge, cognitive load, and confidence
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, consumer-protection analysis, digital-platform governance, sustainability-risk communication, institutional learning, and reproducible behavioral-economics workflows. It is not a toolkit for manipulative nudging, dark-pattern design, exploitative pricing, fear-based persuasion, deceptive risk communication, engagement-maximizing bias amplification, or using behavioral insights to bypass informed judgment.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/heuristics-biases-economic-decision-making

python3 python/generate_synthetic_heuristics_biases_panel.py
python3 python/causal_heuristics_biases_evaluation.py
python3 python/correction_capacity_welfare_analysis.py
python3 python/heuristic_design_sensitivity_analysis.py
python3 python/base_rate_neglect_simulation.py

Rscript r/heuristics_biases_evaluation.R
Rscript r/heuristics_biases_robustness_checks.R
Rscript r/heuristic_judgment_simulation.R

# In Stata:
# do stata/heuristics_biases_evaluation.do

sqlite3 outputs/tables/heuristics_biases.db < sql/schema.sql
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
