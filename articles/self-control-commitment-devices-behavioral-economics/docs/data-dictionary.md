# Data Dictionary

## synthetic_commitment_savings_panel.csv

- `period`: planning period
- `agent_id`: synthetic household/person identifier
- `regime`: commitment regime
- `income`: simulated period income
- `beta`: present-bias parameter
- `delta`: conventional discount factor
- `sophistication`: awareness of future self-control problems
- `liquidity_need`: baseline need for accessible funds
- `emergency_shock`: emergency indicator
- `emergency_cost`: emergency cost if shock occurs
- `planned_savings`: intended savings
- `actual_savings`: realized savings
- `withdrawal`: emergency withdrawal
- `accumulated_savings`: running savings stock
- `welfare`: synthetic welfare index
- `commitment_cost`: cost of deviating from plan
- `automation_strength`: share of savings automated
- `flexibility`: ability to access funds during hardship

## synthetic_commitment_savings_experiment.csv

Final-period agent-level data for treatment-effect estimation.

## quasi_hyperbolic_discounting_history.csv

Synthetic decision history under quasi-hyperbolic discounting.
