# Expected Utility Theory and Rational Choice

This article-level folder supports the article **Expected Utility Theory and Rational Choice**.

Article URL: https://sustainablecatalyst.com/expected-utility-theory-rational-choice/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/expected-utility-theory-rational-choice

## Purpose

This is a professional economist-facing computational scaffold for studying expected utility theory, rational choice under risk, CRRA and CARA utility, risk aversion, certainty equivalents, risk premia, insurance demand, portfolio choice, policy risk, welfare analysis, ambiguity limitations, behavioral departures, sustainability-risk decision systems, and institutional risk governance.

The scaffold is designed for microeconomics, decision theory, behavioral economics, finance, insurance economics, welfare economics, public economics, climate economics, sustainability policy, health economics, infrastructure resilience, game theory, risk management, and reproducible teaching examples.

## Research questions

1. How do heterogeneous risk-aversion parameters affect risky choice under expected utility?
2. How do certainty equivalents and risk premia vary with wealth and utility curvature?
3. How does expected utility explain insurance demand even when premiums exceed expected losses?
4. How do portfolio-allocation choices change under different CRRA assumptions?
5. How do policy-risk choices change when low-probability high-damage outcomes are included?
6. How do liquidity constraints, numeracy, and trust create observed departures from formal expected-utility predictions?
7. How can expected utility serve as a benchmark for prospect theory, loss aversion, probability weighting, and ambiguity aversion?
8. How should sustainability and climate-policy models handle risk aversion, catastrophic downside risk, and intergenerational utility?
9. What robustness checks are required before treating expected-utility outputs as welfare-relevant policy evidence?

## Econometric and computational design

The scaffold includes synthetic expected-utility data that support:

- CRRA utility workflows
- CARA utility workflows
- certainty-equivalent calculations
- risk-premium estimation
- insurance-demand simulations
- portfolio-allocation scaffolds
- public-policy risk examples
- sustainability and climate-risk decision models
- behavioral-departure overlays
- treatment-effect-style comparisons by risk-aversion regime
- heterogeneous effects by wealth, risk aversion, numeracy, liquidity constraints, and trust
- welfare and distributional sensitivity analysis
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, decision-theory teaching, insurance and finance modeling, policy-evaluation scaffolding, sustainability-risk analysis, institutional learning, and reproducible behavioral-economics workflows. It is not a tool for giving investment advice, pricing real insurance products, making real lending decisions, producing individualized financial recommendations, automating welfare eligibility, or treating formal expected utility as a substitute for ethical, legal, distributional, or democratic judgment.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/expected-utility-theory-rational-choice

python3 python/generate_synthetic_expected_utility_panel.py
python3 python/expected_utility_risk_aversion_evaluation.py
python3 python/certainty_equivalent_risk_premium_analysis.py
python3 python/insurance_portfolio_policy_risk_simulations.py
python3 python/sensitivity_expected_utility_parameters.py

Rscript r/expected_utility_evaluation.R
Rscript r/expected_utility_robustness_checks.R
Rscript r/crra_choice_simulation.R

# In Stata:
# do stata/expected_utility_evaluation.do

sqlite3 outputs/tables/expected_utility.db < sql/schema.sql
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
