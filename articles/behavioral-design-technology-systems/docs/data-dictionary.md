# Data Dictionary

## synthetic_interface_panel.csv

| Column | Type | Description |
|---|---:|---|
| user_id | integer | Synthetic user identifier |
| period | integer | Time period |
| post | integer | Post-treatment period indicator |
| regime | text | Assigned interface regime |
| engagement_design | integer | Engagement-maximizing regime indicator |
| lockin_design | integer | Friction-heavy lock-in regime indicator |
| baseline_value | numeric | Intrinsic user value |
| cognitive_overload | numeric | Cognitive burden |
| privacy_sensitivity | numeric | Sensitivity to privacy/data extraction cost |
| autonomy_preference | numeric | Preference for control and reversibility |
| salience | numeric | Interface salience |
| default_on | integer | Whether the design uses active defaults |
| entry_friction | numeric | Friction to join or accept |
| exit_friction | numeric | Friction to cancel, reverse, or opt out |
| friction_asymmetry | numeric | Exit friction minus entry friction |
| reward_intensity | numeric | Strength of feedback/reward design |
| data_extraction_intensity | numeric | Intensity of data extraction |
| joined | integer | Simulated joining/conversion outcome |
| retained | integer | Simulated retention outcome |
| consented | integer | Simulated data-sharing consent outcome |
| user_welfare | numeric | Synthetic user-welfare proxy |
| platform_value | numeric | Synthetic platform-value proxy |

## synthetic_interface_experiment.csv

One row per synthetic user after treatment assignment. Useful for cross-sectional treatment-effect estimation.
