# Prospect Theory: How Humans Evaluate Risk and Uncertainty

This article-level folder supports the article **Prospect Theory: How Humans Evaluate Risk and Uncertainty**.

Article URL: https://sustainablecatalyst.com/prospect-theory-psychology-of-risk/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/prospect-theory-psychology-of-risk

## Purpose

This is a professional economist-facing computational scaffold for studying prospect theory, reference-dependent choice, loss aversion, probability weighting, gain/loss framing, mixed gambles, expected-utility comparisons, the fourfold pattern of risk attitudes, behavioral-finance applications, consumer-price frames, insurance and lottery behavior, policy-risk communication, sustainability-transition losses, digital-platform choice architecture, welfare analysis, and institutional design.

The scaffold is designed for behavioral economics, applied microeconomics, decision theory, behavioral finance, consumer protection, public economics, insurance economics, climate economics, sustainability policy, digital-platform governance, institutional economics, and reproducible teaching examples.

## Research questions

1. How do prospect-theory predictions differ from expected-utility predictions under gain, loss, and mixed-gamble frames?
2. How do reference points change the psychological coding of objectively equivalent outcomes?
3. How does loss aversion affect mixed-gamble acceptance?
4. How does probability weighting affect low-probability gain and low-probability loss decisions?
5. How does the fourfold pattern of risk attitudes emerge from value and probability weighting?
6. How do financial investors respond to purchase-price reference points and losses?
7. How do consumer price frames, surcharges, discounts, free trials, and cancellations use gain/loss coding?
8. How do public policies create visible losses and diffuse gains?
9. How can sustainability communication make slow environmental losses visible without manipulating fear?
10. What robustness checks are required before treating a prospect-theory intervention as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic prospect-theory and expected-utility comparison data that support:

- reference-dependent value functions
- probability-weighting functions
- gain-frame, loss-frame, and mixed-gamble simulations
- expected-utility comparison workflows
- prospect-theory / expected-utility disagreement diagnostics
- fourfold-pattern simulations
- insurance and lottery examples
- disposition-effect and behavioral-finance examples
- consumer framing workflows
- policy-risk communication examples
- sustainability-transition loss models
- digital-platform choice-architecture notes
- treatment-effect-style estimation by frame
- heterogeneity by loss aversion, probability weighting, CRRA risk aversion, wealth, income security, prior loss exposure, numeracy, and trust
- welfare and distributional sensitivity analysis
- robustness checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, decision-theory teaching, behavioral-finance research, consumer-protection analysis, public-policy evaluation, sustainability governance, digital-platform accountability, institutional learning, and reproducible behavioral-economics workflows. It is not a toolkit for manipulative loss framing, dark-pattern design, deceptive risk communication, gambling-like interface design, predatory investing prompts, exploitative insurance messaging, or using behavioral insights to bypass informed judgment.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/prospect-theory-psychology-of-risk

python3 python/generate_synthetic_prospect_theory_panel.py
python3 python/prospect_theory_frame_evaluation.py
python3 python/expected_utility_comparison.py
python3 python/fourfold_risk_attitudes_simulation.py
python3 python/insurance_lottery_policy_risk_examples.py
python3 python/sensitivity_prospect_theory_parameters.py

Rscript r/prospect_theory_evaluation.R
Rscript r/prospect_theory_robustness_checks.R
Rscript r/prospect_value_probability_weighting_simulation.R

# In Stata:
# do stata/prospect_theory_evaluation.do

sqlite3 outputs/tables/prospect_theory.db < sql/schema.sql
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
