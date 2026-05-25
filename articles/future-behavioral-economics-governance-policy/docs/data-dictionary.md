# Data Dictionary

The data in this folder are synthetic and are used only to demonstrate behavioral-governance modeling concepts.

## synthetic_citizens.csv

| Column | Type | Description |
|---|---:|---|
| citizen_id | integer | Synthetic identifier |
| trust | numeric | Simulated institutional trust score from 0 to 1 |
| salience | numeric | Simulated attention/salience score from 0 to 1 |
| norm_sensitivity | numeric | Responsiveness to social or civic norms |
| burden_sensitivity | numeric | Responsiveness to administrative friction |
| present_bias | numeric | Present-bias parameter from 0 to 1 |
| income | numeric | Synthetic household income |
| digital_access | numeric | Simulated access to reliable digital tools |
| baseline_compliance | numeric | Synthetic baseline compliance propensity |

## regime_summary.csv

| Column | Type | Description |
|---|---:|---|
| regime | text | Governance scenario name |
| compliance_rate | numeric | Simulated share complying |
| mean_compliance_probability | numeric | Mean predicted compliance probability |
| mean_welfare | numeric | Synthetic welfare proxy |
