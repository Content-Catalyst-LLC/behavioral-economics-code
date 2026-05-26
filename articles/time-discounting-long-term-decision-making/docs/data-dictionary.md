# Data Dictionary

## synthetic_time_discounting_panel.csv

- `period`: decision period
- `agent_id`: synthetic agent identifier
- `regime`: discounting regime
- `beta`: present-bias parameter
- `delta`: standard discount factor
- `sophistication`: awareness of future self-control problems
- `liquidity_need`: proxy for need to preserve flexibility
- `delayed_reward`: delayed reward available in the period
- `immediate_reward`: immediate reward available in the period
- `delayed_value`: discounted value of delayed reward
- `immediate_value`: value of immediate reward after support and flexibility adjustment
- `choose_delayed`: delayed-choice indicator
- `period_welfare`: synthetic period welfare
- `cumulative_delayed_choices`: cumulative count of delayed choices
- `cumulative_welfare`: cumulative synthetic welfare
- `commitment_support`: implementation support for long-term choice
- `flexibility`: ability to adjust under hardship
- `present_bias_treat`: treatment indicator for present-biased discounting
- `commitment_support_treat`: treatment indicator for present bias with commitment support

## synthetic_time_discounting_experiment.csv

Final-period agent-level data for treatment-effect estimation.

## discount_rate_sensitivity.csv

Present-value sensitivity for long-horizon public goods under different discount rates.

## quasi_hyperbolic_discounting_history.csv

Synthetic choice history under quasi-hyperbolic discounting.
