# Data Dictionary

## synthetic_choice_architecture_panel.csv

| Column | Type | Description |
|---|---:|---|
| user_id | integer | Synthetic user identifier |
| period | integer | Time period |
| post | integer | Post-treatment indicator |
| regime | text | Decision-environment regime |
| default_heavy_treat | integer | Default-heavy architecture treatment indicator |
| guided_design_treat | integer | Low-complexity guided design treatment indicator |
| default_sensitivity | numeric | User sensitivity to default status |
| salience_sensitivity | numeric | User sensitivity to visual/positional prominence |
| framing_sensitivity | numeric | User sensitivity to framing advantage |
| complexity_sensitivity | numeric | User sensitivity to cognitive load |
| switching_cost_sensitivity | numeric | User sensitivity to switching or effort cost |
| digital_literacy | numeric | Synthetic digital/institutional navigation capacity |
| institutional_trust | numeric | Synthetic trust parameter |
| chosen_option | integer | Selected option |
| chosen_utility | numeric | Architecture-adjusted choice utility |
| realized_welfare | numeric | Synthetic realized welfare |
| selected_default | integer | Whether user selected the default option |
| selected_high_value_option | integer | Whether user selected the highest long-run value option |
| cognitive_cost | numeric | Cognitive cost incurred by selected option |
| switching_cost | numeric | Switching/effort cost incurred by selected option |

## synthetic_choice_architecture_experiment.csv

One row per synthetic user after treatment assignment. Useful for cross-sectional treatment-effect estimation.
