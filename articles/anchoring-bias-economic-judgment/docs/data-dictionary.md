# Data Dictionary

## synthetic_anchoring_bias_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `regime`: anchor regime
- `true_value`: evidence-based target value
- `anchor_value`: starting reference value
- `adjustment_rate`: baseline adjustment capacity
- `effective_adjustment`: adjustment after knowledge, numeracy, disclosure, support, and load
- `numeracy`: ability to use quantitative information
- `confidence`: subjective confidence
- `cognitive_load`: limited attention / burden proxy
- `domain_knowledge`: domain expertise proxy
- `disclosure_quality`: explanatory context around the anchor
- `counter_anchor_support`: contextual support that helps revise away from anchor
- `estimate`: final estimate
- `bias`: estimate minus true value
- `absolute_error`: absolute value of bias
- `confidence_adjusted_error`: error penalized by overconfidence
- `decision_quality`: synthetic decision-quality index
- `welfare_proxy`: synthetic welfare proxy
- `low_anchor_treat`: low-anchor treatment indicator
- `high_anchor_treat`: high-anchor treatment indicator
- `counter_context_treat`: high-anchor with counter-context indicator

## anchoring_bias_regime_summary.csv

Regime-level estimate, bias, error, adjustment, decision-quality, and welfare summary.

## anchoring_design_sensitivity.csv

Sensitivity grid over anchor values, disclosure quality, counter-anchor support, and cognitive-load assumptions.

## reference_price_simulation.csv

Consumer reference-price and discount-anchor simulation.
