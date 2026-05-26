# Choice Architecture and Decision Environments

This article-level folder supports the article **Choice Architecture and Decision Environments**.

Article URL: https://sustainablecatalyst.com/choice-architecture-decision-environments/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/choice-architecture-decision-environments

## Purpose

This is a professional economist-facing computational scaffold for studying choice architecture and decision environments. It focuses on defaults, salience, framing, cognitive load, switching costs, friction asymmetry, disclosure design, welfare analysis, heterogeneous treatment effects, and policy-evaluation workflows.

The scaffold is designed for applied behavioral economics, public economics, consumer protection, digital platform governance, administrative burden research, market design, and reproducible teaching examples.

## Research questions

This repository is organized around questions economists and policy researchers can test:

1. Do default-heavy architectures alter choice shares relative to neutral presentation?
2. Do low-complexity guided designs improve welfare rather than simply changing behavior?
3. How do salience and framing affect observed choice when option values are unchanged?
4. Are high-complexity-sensitivity users more affected by defaults and cognitive load?
5. How large is the gap between architecture-adjusted choice utility and long-run user welfare?
6. Can decision-environment redesign reduce unequal burden across user groups?
7. How sensitive are results to assumptions about cognitive cost, switching cost, default strength, and welfare weights?

## Econometric design

The scaffold includes synthetic panel and experiment-style data that support:

- randomized choice-architecture treatment comparisons
- treatment-effect estimation
- panel / difference-in-differences style workflows
- heterogeneous treatment effects by complexity sensitivity, default sensitivity, digital literacy, and institutional trust
- welfare analysis with user benefit, cognitive cost, friction cost, and administrative cost
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible analysis of decision environments. It is not intended for manipulative dark-pattern design, coercive defaults, deceptive disclosure, exploitative friction, consent extraction, or operational user targeting.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/choice-architecture-decision-environments

# Generate synthetic choice architecture panel and experiment data
python3 python/generate_synthetic_choice_architecture_panel.py

# Run Python policy evaluation and welfare analysis
python3 python/causal_choice_architecture_evaluation.py
python3 python/choice_architecture_welfare_analysis.py

# Run R policy evaluation and robustness checks
Rscript r/choice_architecture_evaluation.R
Rscript r/choice_architecture_robustness_checks.R

# Run Stata workflow manually from Stata
# do stata/choice_architecture_evaluation.do

# Build SQL database
sqlite3 outputs/tables/choice_architecture.db < sql/schema.sql
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
