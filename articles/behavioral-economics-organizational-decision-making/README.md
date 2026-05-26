# Behavioral Economics in Organizational Decision-Making

This article-level folder supports the article **Behavioral Economics in Organizational Decision-Making**.

Article URL: https://sustainablecatalyst.com/behavioral-economics-organizational-decision-making/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/behavioral-economics-organizational-decision-making

## Purpose

This folder provides a reproducible computational scaffold for studying behavioral economics inside organizations: bounded rationality, incentive distortion, metric pressure, escalation of commitment, group conformity, review structures, organizational governance, long-horizon decision-making, risk perception, and sustainability-related investment choices.

The examples use synthetic data only. They are designed for research demonstration, public learning, scenario comparison, and reproducible methods development.

## Scope

The scaffold includes:

- synthetic project-portfolio data
- R and Python workflows for escalation, incentives, review structures, and organizational regime comparison
- SQL schema for organizational decision experiments
- Julia, C, C++, Fortran, Rust, and Go examples for lightweight computational modeling
- notebook scaffolding for reproducible analysis
- documentation for methods, validation, data structure, and responsible use

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible organizational-behavior analysis. It is not intended for employee screening, hiring, promotion, compensation, discipline, termination, workplace surveillance, individual performance management, psychological assessment, or automated decision-making about workers.

## Suggested workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/behavioral-economics-organizational-decision-making
python3 python/organizational_regime_simulation.py
Rscript r/escalation_incentives_review_structures.R
sqlite3 outputs/tables/organizational_decision_making.db < sql/schema.sql
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
python/
r/
julia/
sql/
c/
cpp/
fortran/
rust/
go/
tests/
```
