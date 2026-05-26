# Data Dictionary

## synthetic_inequality_aversion_panel.csv

- `agent_id`: synthetic agent identifier
- `period`: time period
- `post`: post-treatment indicator
- `regime`: assigned distributional regime
- `advantageous_treat`: advantageous-inequality treatment indicator
- `disadvantageous_treat`: disadvantageous-inequality treatment indicator
- `alpha`: disadvantageous inequality-aversion parameter
- `beta`: advantageous inequality-aversion parameter
- `income`: synthetic pre-tax income
- `redistribution_norm`: support for redistribution as a fairness norm
- `merit_belief`: belief that outcomes reflect merit
- `institutional_trust`: trust in institutions administering distributional policy
- `self_payoff`: assigned self payoff in a two-person allocation
- `other_payoff`: assigned comparison payoff
- `social_preference_utility`: Fehr-Schmidt utility
- `rejection_propensity`: synthetic likelihood of rejecting the allocation
- `support_redistribution`: synthetic redistribution-support indicator
- `process_legitimacy`: perceived legitimacy of the allocation process
- `total_welfare`: synthetic welfare measure combining material payoff, social preference, and legitimacy

## synthetic_inequality_aversion_experiment.csv

One row per synthetic agent after treatment assignment. Useful for cross-sectional treatment-effect estimation.

## bargaining_redistribution_history.csv

Synthetic ultimatum-style bargaining and tax-rate simulation outputs.
