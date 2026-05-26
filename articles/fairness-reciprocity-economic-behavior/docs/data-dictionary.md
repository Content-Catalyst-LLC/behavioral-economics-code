# Data Dictionary

## synthetic_fairness_reciprocity_panel.csv

- `agent_id`: synthetic agent identifier
- `period`: time period
- `post`: post-treatment indicator
- `regime`: assigned interaction regime
- `unequal_cooperative_treat`: unequal but cooperative treatment indicator
- `unequal_noncooperative_treat`: unequal noncooperative treatment indicator
- `exploitative_low_process_treat`: exploitative low-process-fairness treatment indicator
- `fairness_sensitivity`: sensitivity to unfair or unequal allocations
- `reciprocity_sensitivity`: sensitivity to cooperative or hostile behavior
- `trust`: baseline trust parameter
- `punishment_willingness`: willingness to punish unfairness
- `process_fairness_weight`: sensitivity to procedural fairness
- `self_payoff`: assigned self payoff
- `other_payoff`: assigned comparison payoff
- `reciprocity_signal`: positive or negative reciprocal interpretation
- `process_fairness`: process fairness value
- `fairness_reciprocity_utility`: utility adjusted for fairness, reciprocity, and process
- `rejected`: simulated rejection indicator
- `punished`: simulated punishment indicator
- `cooperated`: simulated cooperation indicator
- `total_welfare`: synthetic welfare measure

## synthetic_fairness_reciprocity_experiment.csv

One row per synthetic agent after treatment assignment. Useful for cross-sectional treatment-effect estimation.

## bargaining_punishment_history.csv

Synthetic ultimatum-style bargaining, rejection, and punishment simulation outputs.
