# Identification Strategy

## Research setting

The synthetic data represent expected-utility choice environments with different risk-aversion regimes, wealth levels, numeracy, liquidity constraints, trust, utility curvature, insurance pricing, portfolio risk, and policy-risk exposure.

Regimes include:

1. `low_risk_aversion`
2. `medium_risk_aversion`
3. `high_risk_aversion`

Additional simulation modules cover insurance demand, portfolio allocation, policy risk, CRRA/CARA sensitivity, and behavioral departures.

## Core estimands

- Effect of medium and high risk-aversion regimes on formal risky choice under expected utility.
- Effect of risk aversion on certainty equivalents and risk premia.
- Effect of risk aversion, wealth, liquidity constraints, and numeracy on observed risky choice with implementation frictions.
- Effect of catastrophic downside risk on expected utility in policy choice.
- Heterogeneous effects by wealth quartile, risk-aversion quartile, numeracy, liquidity constraints, and trust.

## Baseline specification

```text
Y_i = alpha
    + beta_1 MediumRiskAversion_i
    + beta_2 HighRiskAversion_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be formal risky choice, observed risky choice, certainty equivalent, risk premium, insurance take-up, portfolio risky share, or policy choice.

## Expected-utility benchmark

```text
EU_j = sum_s p_s u(x_s | a_j)
```

A decision-maker chooses the action with the highest expected utility.

## Identification cautions for real data

- Observed insurance non-purchase may reflect liquidity constraints, distrust, limited information, or affordability rather than low risk aversion.
- Portfolio choices may reflect access barriers, financial literacy, past experience, discrimination, or advice quality.
- Estimated utility curvature is model-dependent.
- Real decisions may involve reference dependence, loss aversion, probability weighting, ambiguity aversion, regret, social preferences, or moral commitments.
- Climate and sustainability decisions often involve deep uncertainty rather than known probabilities.
- Welfare cannot be inferred from expected utility unless distribution, rights, vulnerability, and assumptions are made explicit.

Because the data here are synthetic, estimates are not empirical claims about actual households, investors, insurers, governments, firms, communities, or policy audiences. The value of the workflow is methodological.
