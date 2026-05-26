# Behavioral Economics and Digital Platforms

This article-level folder supports the article **Behavioral Economics and Digital Platforms**.

Article URL: https://sustainablecatalyst.com/behavioral-economics-digital-platforms/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/behavioral-economics-digital-platforms

## Purpose

This is a professional economist-facing computational scaffold for studying digital platforms as behavioral infrastructures. It focuses on recommendation intensity, ranking salience, social proof, attention allocation, ratings and reputation, platform labor incentives, user welfare, platform value, exposure concentration, and the welfare gap between platform objectives and user outcomes.

The scaffold is designed for applied behavioral economics, platform economics, consumer-protection analysis, digital-governance research, market-design teaching, and reproducible policy-evaluation workflows.

## Research questions

This repository is organized around questions economists and policy researchers can test:

1. Do recommendation and ranking regimes causally alter user welfare and platform value?
2. Do engagement-optimized and socially amplified regimes increase exposure concentration?
3. Does social proof change selection behavior beyond baseline item value?
4. Are cognitively overloaded or privacy-sensitive users more affected by platform ranking?
5. How large is the platform-user welfare gap across platform regimes?
6. Can policy constraints on social amplification or ranking salience reduce welfare loss?
7. How sensitive are results to assumptions about attention costs, privacy costs, and platform revenue weights?

## Econometric design

The scaffold includes synthetic panel and experiment-style data that support:

- randomized platform-regime comparisons
- treatment-effect estimation
- panel / difference-in-differences style workflows
- heterogeneous treatment effects by cognitive overload and privacy sensitivity
- exposure-concentration measurement
- platform-user welfare-gap analysis
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible analysis of digital platforms. It is not intended for manipulative ranking optimization, addictive engagement design, coercive personalization, surveillance, user targeting, or operational user scoring.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/behavioral-economics-digital-platforms

# Generate synthetic platform panel and experiment data
python3 python/generate_synthetic_platform_panel.py

# Run Python policy evaluation and welfare analysis
python3 python/causal_platform_policy_evaluation.py
python3 python/platform_welfare_analysis.py

# Run R policy evaluation and robustness checks
Rscript r/platform_policy_evaluation.R
Rscript r/platform_welfare_robustness_checks.R

# Run Stata workflow manually from Stata
# do stata/platform_policy_evaluation.do

# Build SQL database
sqlite3 outputs/tables/digital_platforms.db < sql/schema.sql
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
