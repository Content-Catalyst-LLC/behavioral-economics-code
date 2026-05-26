# Data Dictionary

## synthetic_availability_bias_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `regime`: availability environment
- `true_probability`: objective/evidence-based probability
- `availability_sensitivity`: susceptibility to salience and recall
- `numeracy`: ability to use quantitative probability information
- `trust_in_statistics`: trust in statistical or institutional information
- `risk_tolerance`: tolerance for financial or behavioral risk
- `prior_experience`: indicator for previous direct experience of the event type
- `recency_signal`: recent exposure to the risk event
- `vividness_signal`: vividness or memorability of the risk example
- `media_signal`: media exposure to the event or category
- `social_repetition_signal`: repeated exposure through social communication
- `availability_score`: composite cognitive accessibility index
- `base_rate_disclosure`: quality/strength of base-rate communication
- `emotional_intensity`: intensity of affective risk cue
- `subjective_probability`: perceived probability after availability and correction
- `calibration_error`: subjective probability minus true probability
- `participate_in_risky_asset`: risky-asset participation indicator
- `insurance_demand`: insurance demand indicator
- `policy_support`: support for protective/regulatory policy
- `welfare_proxy`: synthetic calibration and welfare proxy
- `medium_availability_treat`: treatment indicator
- `high_availability_treat`: treatment indicator

## availability_bias_regime_summary.csv

Regime-level perceived probability, calibration error, behavior, and welfare summary.

## availability_design_sensitivity.csv

Sensitivity grid over salience scale, base-rate disclosure, emotional intensity, and welfare weights.
