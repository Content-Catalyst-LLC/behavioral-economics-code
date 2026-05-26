# Data Dictionary

## synthetic_expected_utility_panel.csv

- `agent_id`: synthetic decision-maker identifier
- `regime`: risk-aversion regime
- `wealth`: initial wealth
- `rho`: CRRA risk-aversion parameter
- `numeracy`: numeracy proxy
- `liquidity_constraint`: liquidity pressure proxy
- `trust`: trust in formal/institutional information proxy
- `eu_certain`: expected utility of certain option
- `eu_risky`: expected utility of risky option
- `expected_value_risky`: expected monetary value of risky option
- `certainty_equivalent_payoff`: certain payoff equivalent to risky option
- `risk_premium`: expected value minus certainty equivalent
- `choose_risky_eu`: formal expected-utility risky choice
- `observed_choose_risky`: risky choice after simple implementation-friction overlay
- `medium_risk_aversion_treat`: treatment indicator
- `high_risk_aversion_treat`: treatment indicator

## expected_utility_regime_summary.csv

Regime-level risk aversion, risky-choice shares, certainty equivalents, and risk premia.

## expected_utility_policy_risk_example.csv

Policy-risk example comparing resilience investment and higher-return low-resilience options.

## insurance_demand_simulation.csv

Synthetic insurance-demand model using expected utility and behavioral frictions.

## portfolio_choice_simulation.csv

Synthetic portfolio allocation under risk aversion and return-risk assumptions.
