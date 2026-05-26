# Data Dictionary

## synthetic_heuristics_biases_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `regime`: cognitive environment
- `true_value`: evidence-based target value
- `estimated_value`: heuristic estimate
- `judgment_error`: estimated value minus true value
- `absolute_error`: absolute judgment error
- `decision_quality`: synthetic decision-quality index
- `welfare_proxy`: synthetic welfare proxy
- `correction_capacity`: ability to correct heuristic distortion
- `availability_signal`: availability-related judgment cue
- `representativeness_signal`: representativeness-related judgment cue
- `anchor_signal`: anchoring-related judgment cue
- `framing_signal`: framing-related judgment cue
- `numeracy`: numerical reasoning proxy
- `domain_knowledge`: domain expertise proxy
- `cognitive_load`: burden / limited attention proxy
- `confidence`: subjective confidence proxy
- `disclosure_quality`: quality of explanatory context
- `debiasing_support`: support for correcting bias
- `medium_bias_treat`: treatment indicator
- `high_bias_treat`: treatment indicator

## heuristics_biases_regime_summary.csv

Regime-level estimate, error, correction-capacity, decision-quality, and welfare summary.

## heuristic_design_sensitivity.csv

Sensitivity grid over signal scale, disclosure quality, debiasing support, and cognitive-load assumptions.

## base_rate_neglect_simulation.csv

Representativeness and base-rate neglect simulation.
