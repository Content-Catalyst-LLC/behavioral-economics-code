# Behavioral Regulation and Institutional Design

This article-level folder supports the article **Behavioral Regulation and Institutional Design**.

Article URL: https://sustainablecatalyst.com/behavioral-regulation-institutional-design/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/behavioral-regulation-institutional-design

## Purpose

This is a professional economist-facing computational scaffold for studying behavioral regulation and institutional design. It focuses on administrative burden, trust, norm signaling, default assistance, deterrence, compliance, enforcement cost, social benefit, welfare accounting, distributional incidence, causal policy evaluation, and robustness testing.

The scaffold is designed for applied behavioral economics, public economics, regulatory economics, public administration research, compliance policy evaluation, institutional design analysis, consumer-protection research, and reproducible teaching examples.

## Research questions

This repository is organized around questions economists and policy researchers can test:

1. Does administrative simplification increase compliance?
2. Does default assistance improve compliance beyond sanction strength?
3. Does institutional trust change the effectiveness of regulatory design?
4. Are norm signals more effective when paired with low administrative burden?
5. Do sanction-heavy regimes increase compliance while reducing total welfare?
6. Are compliance gains distributed evenly across trust, burden sensitivity, and compliance capacity groups?
7. How sensitive are results to assumptions about social benefit, enforcement cost, administrative cost, and sanction intensity?
8. Can integrated behavioral regulation improve compliance without weakening accountability?

## Econometric design

The scaffold includes synthetic panel and experiment-style data that support:

- randomized regulatory policy treatment comparisons
- treatment-effect estimation
- panel / difference-in-differences style workflows
- heterogeneous treatment effects by trust, burden sensitivity, compliance capacity, and private gain from noncompliance
- welfare analysis with social benefit, compliance cost, enforcement cost, and administrative cost
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible regulatory policy analysis. It is not intended for manipulating public consent, obscuring regulatory costs, targeting vulnerable groups, replacing public justification with invisible steering, or substituting behavioral optimization for substantive law, accountability, and democratic governance.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/behavioral-regulation-institutional-design

# Generate synthetic regulatory policy panel and experiment data
python3 python/generate_synthetic_regulatory_policy_panel.py

# Run Python policy evaluation and welfare analysis
python3 python/causal_regulatory_policy_evaluation.py
python3 python/regulatory_welfare_analysis.py

# Run R policy evaluation and robustness checks
Rscript r/regulatory_policy_evaluation.R
Rscript r/regulatory_welfare_robustness_checks.R

# Run Stata workflow manually from Stata
# do stata/regulatory_policy_evaluation.do

# Build SQL database
sqlite3 outputs/tables/regulatory_policy.db < sql/schema.sql
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
