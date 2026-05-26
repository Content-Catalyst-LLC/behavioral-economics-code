# Behavioral Design in Technology Systems

This article-level folder supports the article **Behavioral Design in Technology Systems**.

Article URL: https://sustainablecatalyst.com/behavioral-design-technology-systems/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/behavioral-design-technology-systems

## Purpose

This folder provides a reproducible computational scaffold for studying behavioral design in technology systems: defaults, salience, friction asymmetry, retention dynamics, dark-pattern risk, privacy-consent burden, engagement optimization, platform value, autonomy costs, and user-welfare trade-offs.

The examples use synthetic data only. They are designed for research demonstration, public learning, scenario comparison, and reproducible methods development.

## Scope

The scaffold includes:

- synthetic user-interface behavior data
- R and Python workflows for defaults, friction, retention, welfare, and dark-pattern diagnostics
- SQL schema for interface-regime experiments
- Julia, C, C++, Fortran, Rust, and Go examples for lightweight computational modeling
- notebook scaffolding for reproducible analysis
- documentation for methods, validation, data structure, and responsible use

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible analysis of behavioral design. It is not intended for manipulative targeting, dark-pattern optimization, surveillance, coercive personalization, or operational user scoring.

## Suggested workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/behavioral-design-technology-systems
python3 python/interface_regime_simulation.py
Rscript r/default_friction_retention_simulation.R
sqlite3 outputs/tables/behavioral_design_technology.db < sql/schema.sql
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
