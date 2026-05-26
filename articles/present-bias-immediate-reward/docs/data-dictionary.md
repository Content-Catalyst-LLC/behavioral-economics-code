# Data Dictionary

## synthetic_present_bias_panel.csv

- `period`: decision period
- `agent_id`: synthetic agent identifier
- `regime`: commitment regime
- `beta`: present-bias parameter
- `delta`: conventional discount factor
- `sophistication`: awareness of future self-control problems
- `liquidity_need`: proxy for need to preserve flexibility
- `delayed_reward`: delayed reward available in the period
- `immediate_temptation`: immediate-reward / immediate-relief temptation
- `discounted_delayed_value`: present-biased value of delayed reward
- `immediate_value`: temptation value after commitment and hardship adjustment
- `choose_delayed`: delayed-choice indicator
- `period_welfare`: synthetic period welfare
- `cumulative_delayed_choices`: cumulative count of delayed choices
- `cumulative_welfare`: cumulative synthetic welfare
- `commitment_cost`: deviation cost / friction around immediate temptation
- `reminder_strength`: support for reflective goal activation
- `flexibility`: ability to adjust under hardship
- `medium_commitment_treat`: treatment indicator
- `strong_commitment_treat`: treatment indicator

## synthetic_present_bias_experiment.csv

Final-period agent-level data for treatment-effect estimation.

## quasi_hyperbolic_discounting_history.csv

Synthetic choice history under quasi-hyperbolic discounting.
