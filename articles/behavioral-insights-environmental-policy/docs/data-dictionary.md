# Data Dictionary

## synthetic_environmental_policy_panel.csv

| Column | Type | Description |
|---|---:|---|
| household_id | integer | Synthetic household identifier |
| period | integer | Time period |
| post | integer | Post-treatment indicator |
| regime | text | Environmental policy regime |
| norm_default_treat | integer | Norm-plus-default treatment indicator |
| integrated_treat | integer | Integrated policy treatment indicator |
| income | numeric | Synthetic household income |
| energy_burden | numeric | Energy burden as share of income |
| env_concern | numeric | Environmental concern parameter |
| present_bias | numeric | Present-bias parameter |
| norm_sensitivity | numeric | Responsiveness to social norms |
| friction_sensitivity | numeric | Responsiveness to hassle and administrative burden |
| loss_aversion | numeric | Weight placed on perceived short-run loss |
| trust | numeric | Institutional trust parameter |
| subsidy | numeric | Policy subsidy amount |
| default_green | integer | Whether green option is default |
| norm_signal | numeric | Strength of social-norm feedback |
| friction | numeric | Administrative/logistical friction |
| adopted | integer | Simulated adoption outcome |
| private_benefit | numeric | Synthetic private/household benefit |
| environmental_benefit | numeric | Synthetic environmental benefit |
| fiscal_cost | numeric | Synthetic fiscal cost |
| admin_cost | numeric | Synthetic administrative cost |
| total_welfare | numeric | Synthetic total welfare |

## synthetic_environmental_policy_experiment.csv

One row per synthetic household after treatment assignment. Useful for cross-sectional treatment-effect estimation.
