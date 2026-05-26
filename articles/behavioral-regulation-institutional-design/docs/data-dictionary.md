# Data Dictionary

## synthetic_regulatory_policy_panel.csv

| Column | Type | Description |
|---|---:|---|
| agent_id | integer | Synthetic regulated-agent identifier |
| period | integer | Time period |
| post | integer | Post-treatment indicator |
| regime | text | Regulatory regime |
| simplification_treat | integer | Simplification-plus-trust treatment indicator |
| integrated_treat | integer | Integrated behavioral regulation treatment indicator |
| trust | numeric | Institutional trust parameter |
| norm_sensitivity | numeric | Responsiveness to norm signaling |
| burden_sensitivity | numeric | Responsiveness to administrative burden |
| loss_aversion | numeric | Weight placed on perceived losses |
| private_gain_noncompliance | numeric | Perceived gain from noncompliance |
| compliance_capacity | numeric | Ability to understand and carry out compliance |
| admin_burden | numeric | Administrative burden |
| trust_signal | numeric | Institutional legitimacy / trust signal |
| norm_signal | numeric | Social-norm or public-expectation signal |
| default_assistance | integer | Whether compliant pathway is simplified or assisted |
| sanction_strength | numeric | Expected sanction strength |
| complied | integer | Simulated compliance outcome |
| social_benefit | numeric | Synthetic social benefit from compliance |
| compliance_cost | numeric | Synthetic compliance cost |
| enforcement_cost | numeric | Synthetic enforcement cost |
| administrative_cost | numeric | Synthetic administrative cost |
| total_welfare | numeric | Synthetic total welfare |

## synthetic_regulatory_policy_experiment.csv

One row per synthetic agent after treatment assignment. Useful for cross-sectional treatment-effect estimation.
