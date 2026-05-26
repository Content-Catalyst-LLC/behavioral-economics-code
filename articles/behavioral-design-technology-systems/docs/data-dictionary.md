# Data Dictionary

The data in this folder are synthetic and are used only to demonstrate behavioral-design models.

## synthetic_users.csv

| Column | Type | Description |
|---|---:|---|
| user_id | integer | Synthetic user identifier |
| baseline_value | numeric | Intrinsic value from the service or interface |
| salience_sensitivity | numeric | Response to visual prominence |
| default_sensitivity | numeric | Response to defaults and preselection |
| friction_sensitivity | numeric | Response to effort and friction |
| reward_sensitivity | numeric | Response to feedback and reward intensity |
| cognitive_overload | numeric | Burden from complexity or interface overload |
| privacy_sensitivity | numeric | Sensitivity to data extraction and privacy risk |
| autonomy_preference | numeric | Preference for control and reversibility |

## interface_regime_comparison.csv

| Column | Type | Description |
|---|---:|---|
| regime | text | Interface design regime |
| join_rate | numeric | Simulated conversion or joining rate |
| retention_rate | numeric | Simulated retention rate |
| mean_user_welfare | numeric | Synthetic user-welfare proxy |
| mean_platform_value | numeric | Synthetic platform-value proxy |
| friction_asymmetry | numeric | Difference between exit friction and entry friction |
| welfare_platform_gap | numeric | Difference between platform value and user welfare |
