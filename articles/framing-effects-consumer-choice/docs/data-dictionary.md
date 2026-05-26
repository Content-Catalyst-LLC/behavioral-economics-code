# Data Dictionary

## synthetic_framing_effects_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `frame`: gain, loss, or balanced absolute-risk frame
- `loss_aversion`: loss-aversion parameter
- `curvature`: utility curvature parameter
- `numeracy`: ability to understand quantitative risk information
- `trust`: trust in the communicator or institution
- `decision_fatigue`: cognitive burden / limited attention proxy
- `certain_value`: subjective value of certain option
- `risky_value`: subjective value of risky option
- `adjusted_risky_value`: risky value after framing, salience, and comprehension adjustment
- `comprehension`: synthetic comprehension proxy
- `choose_risky`: risky-choice indicator
- `welfare_proxy`: synthetic welfare / decision-quality proxy
- `frame_strength`: strength of framing intervention
- `disclosure_quality`: quality of explanatory disclosure
- `salience`: degree to which the frame is salient
- `loss_frame_treat`: treatment indicator for loss frame
- `balanced_frame_treat`: treatment indicator for balanced absolute-risk frame

## framing_effects_frame_summary.csv

Frame-level choice, comprehension, and welfare summary.

## framing_design_sensitivity.csv

Sensitivity grid over frame strength, disclosure quality, salience, numeracy support, and manipulation-risk penalties.
