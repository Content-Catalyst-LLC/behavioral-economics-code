# Framing Effects in Consumer Choice

This article-level folder supports the article **Framing Effects in Consumer Choice**.

Article URL: https://sustainablecatalyst.com/framing-effects-consumer-choice/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/framing-effects-consumer-choice

## Purpose

This is a professional economist-facing computational scaffold for studying framing effects, consumer choice, prospect theory, gain frames, loss frames, attribute framing, price framing, risk communication, absolute versus relative risk, digital-interface framing, consumer protection, health-risk communication, sustainability communication, public-policy messaging, comprehension, welfare, and ethical decision architecture.

The scaffold is designed for behavioral economics, applied microeconomics, consumer finance, consumer protection, health economics, public economics, digital-platform governance, sustainability policy, marketing-science research, institutional design, and reproducible teaching examples.

## Research questions

1. How do gain frames, loss frames, and balanced absolute-risk frames affect risky choice under formally equivalent outcomes?
2. How do loss aversion, curvature, numeracy, trust, and decision fatigue moderate framing effects?
3. When does a frame improve comprehension, and when does it merely shift behavior?
4. How do price frames, subscription frames, and total-cost frames influence consumer welfare?
5. How do absolute-risk and relative-risk frames alter health and public-policy decisions?
6. How can digital interfaces frame options through buttons, ranking, salience, defaults, and comparison sets?
7. How should sustainability policies be framed without greenwashing or hiding distributional costs?
8. What distinguishes clarifying communication from manipulative framing?
9. What robustness checks are required before treating a framing intervention as welfare-improving?

## Econometric and computational design

The scaffold includes synthetic framing-regime data that support:

- gain-frame and loss-frame simulations
- balanced absolute-risk frame simulations
- prospect-theory risk-choice workflows
- attribute-framing examples
- price-framing diagnostics
- total-cost versus monthly-cost examples
- health-risk communication scaffolds
- sustainability-message framing notes
- digital-interface framing notes
- consumer-protection analysis
- treatment-effect estimation
- heterogeneous treatment effects by loss aversion, numeracy, trust, fatigue, frame strength, salience, and disclosure quality
- comprehension diagnostics
- welfare proxy analysis
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, policy-evaluation scaffolding, consumer-protection analysis, health-risk communication review, sustainability-message analysis, digital-interface governance, institutional learning, and reproducible behavioral-economics workflows. It is not a tool for manipulative advertising, deceptive price framing, greenwashing, hidden fees, dark-pattern interface design, fear-based coercion, or using behavioral insights to bypass informed judgment.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/framing-effects-consumer-choice

python3 python/generate_synthetic_framing_effects_panel.py
python3 python/causal_framing_effects_evaluation.py
python3 python/framing_comprehension_welfare_analysis.py
python3 python/framing_design_sensitivity_analysis.py

Rscript r/framing_effects_evaluation.R
Rscript r/framing_effects_robustness_checks.R
Rscript r/gain_loss_frame_simulation.R

# In Stata:
# do stata/framing_effects_evaluation.do

sqlite3 outputs/tables/framing_effects.db < sql/schema.sql
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
