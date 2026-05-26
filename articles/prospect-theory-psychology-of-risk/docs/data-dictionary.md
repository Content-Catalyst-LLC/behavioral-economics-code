# Data Dictionary

## synthetic_prospect_theory_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `frame`: gain, loss, or mixed_gamble condition
- `pt_sure_value`: prospect-theory value of certain option
- `pt_risky_value`: prospect-theory value of risky option
- `eu_sure_value`: expected-utility value of certain option
- `eu_risky_value`: expected-utility value of risky option
- `choose_risky_pt`: risky-choice indicator under prospect theory
- `choose_risky_eu`: risky-choice indicator under expected utility
- `pt_eu_disagreement`: indicator for PT/EU model disagreement
- `lambda_loss`: loss-aversion coefficient
- `alpha_gain`: gain-domain curvature
- `beta_loss`: loss-domain curvature
- `gamma_weight`: probability-weighting curvature
- `rho_crra`: CRRA risk-aversion parameter
- `wealth`: synthetic wealth
- `numeracy`: numeracy proxy
- `income_security`: income-security proxy
- `trust`: institutional trust proxy
- `prior_loss_exposure`: prior loss exposure indicator
- `loss_frame_treat`: treatment indicator
- `mixed_gamble_treat`: treatment indicator

## prospect_theory_frame_summary.csv

Frame-level risky-choice rates, PT/EU disagreement, and parameter means.

## prospect_theory_lambda_heterogeneity.csv

Heterogeneity by loss-aversion quartile.

## prospect_theory_probability_weighting_heterogeneity.csv

Heterogeneity by probability-weighting quartile.

## fourfold_risk_attitudes_simulation.csv

Low/high probability by gain/loss domain simulation.

## insurance_lottery_policy_risk_examples.csv

Insurance, lottery, and policy-risk examples using probability weighting and reference-dependent value.
