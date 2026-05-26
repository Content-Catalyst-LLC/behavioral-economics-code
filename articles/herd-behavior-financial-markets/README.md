# Herd Behavior in Financial Markets

This article-level folder supports the article **Herd Behavior in Financial Markets**.

Article URL: https://sustainablecatalyst.com/herd-behavior-financial-markets/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/herd-behavior-financial-markets

## Purpose

This is a professional economist-facing computational scaffold for studying herd behavior, informational cascades, investor imitation, price momentum, crowded trades, market bubbles, crash dynamics, retail herding, institutional herding, liquidity stress, leverage feedback, platform-mediated attention, and behavioral finance.

The scaffold is designed for behavioral finance, financial economics, market microstructure, financial-stability research, policy analysis, risk management, computational social science, and reproducible teaching examples.

## Research questions

1. How does herding intensity affect price deviations, volatility, buy rates, and boom-bust range?
2. When do public herd signals dominate private information?
3. How do liquidity depth and leverage pressure amplify herd-driven reversals?
4. Can social-media intensity or platform salience increase synchronized buying?
5. Are high-herding regimes more vulnerable to shocks than low-herding regimes under identical fundamentals?
6. How should analysts distinguish herding from common response to common information?
7. How do crowded trades interact with liquidity and leverage to create systemic risk?
8. Can institutional benchmarking, career risk, and reputation pressure generate rational institutional herding?
9. How can market supervisors monitor herding without treating all correlated trading as irrational?

## Econometric and computational design

The scaffold includes synthetic panel and market-history data that support:

- agent-based herding simulation
- informational-cascade workflow
- market-regime comparison
- retail and institutional herding parameters
- liquidity-depth and leverage-feedback stress tests
- social-media amplification diagnostics
- treatment-effect estimation
- heterogeneous treatment effects by private-signal weight, herd weight, loss aversion, reputation pressure, and information quality
- financial-stability summary metrics
- robustness and sensitivity checks
- Stata, R, Python, Julia, SQL, and systems-language examples

## Responsible use

This repository is for synthetic-data research, methods demonstration, financial-stability learning, institutional risk analysis, and reproducible behavioral-finance workflows. It is not investment advice, trading advice, or a tool for manipulating retail investors, amplifying speculative narratives, coordinating trades, or promoting financial products.

## Suggested replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/herd-behavior-financial-markets

python3 python/generate_synthetic_herd_market_panel.py
python3 python/causal_herd_market_evaluation.py
python3 python/herd_market_welfare_stability_analysis.py
python3 python/informational_cascade_simulation.py

Rscript r/herd_market_evaluation.R
Rscript r/herd_market_robustness_checks.R
Rscript r/informational_cascade_simulation.R

# In Stata:
# do stata/herd_market_evaluation.do

sqlite3 outputs/tables/herd_market.db < sql/schema.sql
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
