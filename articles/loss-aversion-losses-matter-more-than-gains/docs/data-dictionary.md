# Data Dictionary

## synthetic_loss_aversion_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `frame`: gain, loss, or mixed_gamble condition
- `sure_value`: prospect-style value of the sure option
- `risky_value`: prospect-style value of the risky option
- `choose_risky`: risky-choice indicator
- `lambda_loss`: loss-aversion coefficient
- `alpha_gain`: gain-domain curvature
- `beta_loss`: loss-domain curvature
- `numeracy`: numeracy proxy
- `income_security`: income-security proxy
- `prior_loss_exposure`: prior loss exposure indicator
- `trust`: institutional trust proxy
- `loss_frame_treat`: treatment indicator
- `mixed_gamble_treat`: treatment indicator

## loss_aversion_frame_summary.csv

Frame-level risky-choice shares and value-function summaries.

## loss_aversion_lambda_heterogeneity.csv

Heterogeneity by loss-aversion quartile.

## disposition_effect_simulation.csv

Synthetic asset-level data for gain/loss realization behavior.

## endowment_effect_simulation.csv

Synthetic WTA/WTP and ownership-gap simulation.

## policy_transition_loss_distribution.csv

Synthetic policy-transition model with gains, losses, distributional weights, and support probabilities.
