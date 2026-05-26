# Data Dictionary

## synthetic_nudge_policy_panel.csv

| Column | Type | Description |
|---|---:|---|
| agent_id | integer | Synthetic agent identifier |
| period | integer | Time period |
| post | integer | Post-treatment indicator |
| regime | text | Nudge-policy regime |
| reminder_norm_treat | integer | Reminder-plus-norm treatment indicator |
| default_reminder_treat | integer | Default-plus-reminder treatment indicator |
| default_sensitivity | numeric | Responsiveness to defaults |
| reminder_sensitivity | numeric | Responsiveness to reminders/prompts |
| norm_sensitivity | numeric | Responsiveness to social-norm messaging |
| friction_sensitivity | numeric | Responsiveness to hassle/friction |
| present_bias | numeric | Tendency to underweight delayed benefits |
| administrative_burden_sensitivity | numeric | Responsiveness to administrative burden |
| trust | numeric | Institutional trust parameter |
| default_on | integer | Whether target action is default |
| reminder_strength | numeric | Reminder/prompt strength |
| norm_signal | numeric | Social-norm signal strength |
| friction | numeric | Hassle or complexity cost |
| administrative_burden | numeric | Administrative burden level |
| adopted | integer | Simulated uptake/adoption outcome |
| user_benefit | numeric | Synthetic user benefit |
| social_benefit | numeric | Synthetic social benefit |
| friction_cost | numeric | Synthetic friction cost |
| admin_cost | numeric | Synthetic administrative cost |
| implementation_cost | numeric | Synthetic implementation cost |
| total_welfare | numeric | Synthetic total welfare |

## synthetic_nudge_policy_experiment.csv

One row per synthetic agent after treatment assignment. Useful for cross-sectional treatment-effect estimation.
