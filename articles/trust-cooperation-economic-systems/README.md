# Trust and Cooperation in Economic Systems

This article-level folder supports the article **Trust and Cooperation in Economic Systems**.

Article URL: https://sustainablecatalyst.com/trust-cooperation-economic-systems/  
Repository folder: https://github.com/Content-Catalyst-LLC/behavioral-economics-code/tree/main/articles/trust-cooperation-economic-systems

## Purpose

This is a professional economist-facing computational scaffold for studying trust, reciprocity, cooperation, public goods, punishment, transaction costs, institutional support, digital trust systems, and behavioral governance.

The scaffold is designed for applied behavioral economics, institutional economics, public economics, organizational economics, platform-governance research, development economics, public-goods analysis, and reproducible teaching examples.

## Research questions

1. Does institutional support increase trust and reciprocity?
2. Do cooperative norms reduce monitoring costs and stabilize repeated exchange?
3. Does punishment credibility sustain cooperation after betrayal?
4. Do trust-enhancing institutions reduce transaction costs?
5. Are trust and cooperation gains evenly distributed across low-trust and high-trust agents?
6. How sensitive are welfare results to betrayal cost, monitoring cost, transaction-cost reduction, and punishment value?
7. Does higher trust improve welfare only when reciprocity and accountability are credible?
8. Can behavioral governance increase cooperation without merely extracting trust from vulnerable actors?

## Replication workflow

```bash
cd ~/Downloads/behavioral-economics-code/articles/trust-cooperation-economic-systems

python3 python/generate_synthetic_trust_cooperation_panel.py
python3 python/causal_trust_cooperation_evaluation.py
python3 python/trust_cooperation_welfare_analysis.py
python3 python/repeated_exchange_simulation.py

Rscript r/trust_cooperation_evaluation.R
Rscript r/trust_cooperation_robustness_checks.R
Rscript r/repeated_exchange_simulation.R

# In Stata:
# do stata/trust_cooperation_evaluation.do

sqlite3 outputs/tables/trust_cooperation.db < sql/schema.sql
```

## Responsible use

This repository is for synthetic-data research, methods demonstration, institutional learning, and reproducible analysis. It is not intended for manipulating public trust, manufacturing false confidence, suppressing justified distrust, exploiting vulnerable users, or increasing cooperation with untrustworthy institutions.
