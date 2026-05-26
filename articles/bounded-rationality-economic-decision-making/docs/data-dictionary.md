# Data Dictionary

## synthetic_bounded_rationality_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `regime`: low_constraint, medium_constraint, or high_constraint
- `aspiration`: aspiration threshold for satisficing
- `search_cost`: cost of inspecting an additional option
- `time_budget`: time available for search
- `cognitive_capacity`: capacity proxy for information processing
- `numeracy`: numeracy proxy
- `stress`: stress or cognitive-load pressure proxy
- `institutional_trust`: trust proxy
- `digital_access`: digital access proxy
- `income_security`: income-security proxy
- `administrative_capacity`: ability to navigate administrative systems
- `chosen_index`: sequential search depth
- `chosen_value`: value of the selected option
- `optimal_value`: maximum value available in the option set
- `net_value`: chosen value minus search cost
- `optimization_gap`: optimal value minus chosen value
- `cumulative_time`: time used in search
- `cumulative_load`: cognitive load used in search
- `medium_constraint_treat`: treatment indicator
- `high_constraint_treat`: treatment indicator

## bounded_rationality_regime_summary.csv

Regime-level chosen value, optimal value, net value, optimization gap, search depth, time use, and cognitive load.

## administrative_burden_simulation.csv

Synthetic program-access data including burden, completion, take-up, and policy simplification.

## organizational_routine_simulation.csv

Synthetic routine-performance data under stable and changing environments.

## consumer_platform_search_friction_examples.csv

Synthetic consumer switching, plan choice, hidden-fee, and platform-friction examples.
