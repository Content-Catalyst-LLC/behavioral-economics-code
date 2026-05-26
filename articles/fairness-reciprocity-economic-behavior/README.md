# Fairness and Reciprocity in Economic Behavior

This article-level folder supports the article **Fairness and Reciprocity in Economic Behavior**.

Article URL: https://sustainablecatalyst.com/fairness-reciprocity-economic-behavior/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/fairness-reciprocity-economic-behavior

## Purpose

This is a professional economist-facing computational scaffold for studying fairness, reciprocity, social preferences, bargaining, rejection, punishment, trust, process legitimacy, wage fairness, institutional compliance, public-goods cooperation, market behavior, and behavioral governance.

The scaffold is designed for applied behavioral economics, behavioral game theory, public economics, labor economics, organizational economics, institutional economics, platform-governance research, policy evaluation, and reproducible teaching examples.

## Research questions

1. How do fairness sensitivity and reciprocity sensitivity alter bargaining offers, rejection, punishment, and welfare?
2. Do process-fairness cues reduce rejection of unequal offers?
3. Does reciprocity stabilize cooperation when material allocations are unequal?
4. Do unfair or noncooperative regimes reduce welfare even when material payoffs appear similar?
5. Are high-fairness-sensitivity agents more likely to reject and punish unfair treatment?
6. How sensitive are welfare rankings to assumptions about process fairness, reciprocity, punishment cost, and rejection cost?
7. Can institutions increase cooperation by improving fairness, or only by making unfair systems appear fair?
8. How can economists distinguish fairness, reciprocity, altruism, inequality aversion, trust, and punishment?

## Econometric and computational design

The scaffold includes synthetic panel and experiment-style data that support:

- fairness-adjusted utility analysis
- reciprocity-adjusted utility analysis
- bargaining and rejection simulations
- costly punishment and norm-enforcement workflows
- process-fairness and institutional legitimacy modeling
- public-goods and cooperation extensions
- treatment-effect estimation
- heterogeneous treatment effects by fairness sensitivity, reciprocity sensitivity, trust, punishment willingness, and process-fairness weight
- welfare analysis with material payoff, process fairness, reciprocity, rejection cost, punishment cost, and legitimacy
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible social-preference analysis. It is not intended for manipulating fairness perceptions, suppressing justified complaints, extracting cooperation without accountability, or making unfair systems appear legitimate.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/fairness-reciprocity-economic-behavior

python3 python/generate_synthetic_fairness_reciprocity_panel.py
python3 python/causal_fairness_reciprocity_evaluation.py
python3 python/fairness_reciprocity_welfare_analysis.py
python3 python/bargaining_punishment_simulation.py

Rscript r/fairness_reciprocity_evaluation.R
Rscript r/fairness_reciprocity_robustness_checks.R
Rscript r/bargaining_punishment_simulation.R

# In Stata:
# do stata/fairness_reciprocity_evaluation.do

sqlite3 outputs/tables/fairness_reciprocity.db < sql/schema.sql
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
