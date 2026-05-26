# Identification Strategy

## Research setting

The synthetic data represent gain-frame, loss-frame, and mixed-gamble decision environments. Agents have heterogeneous prospect-theory parameters, including loss aversion, gain curvature, loss curvature, probability-weighting curvature, CRRA risk aversion, wealth, income security, numeracy, trust, and prior loss exposure.

Regimes include:

1. `gain`
2. `loss`
3. `mixed_gamble`

Additional simulation modules cover expected-utility comparisons, fourfold risk-attitude patterns, insurance and lottery behavior, policy-risk communication, and sustainability-transition losses.

## Core estimands

- Effect of loss framing on risky choice relative to a gain-frame benchmark.
- Effect of mixed-gamble framing on risky choice.
- Effect of loss aversion on mixed-gamble acceptance.
- Effect of probability weighting on low-probability gains and losses.
- Disagreement between prospect-theory and expected-utility predictions.
- Heterogeneous effects by loss-aversion quartile.
- Heterogeneous effects by probability-weighting quartile.
- Heterogeneous effects by income security, numeracy, prior loss exposure, wealth, and trust.
- Sensitivity of policy support to transition losses and avoided future damages.

## Baseline specification

```text
Y_i = alpha
    + beta_1 LossFrame_i
    + beta_2 MixedGamble_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be prospect-theory risky choice, expected-utility risky choice, PT/EU disagreement, risky prospect value, policy support, insurance take-up, lottery interest, or a welfare proxy.

## Prospect-theory valuation

```text
PT_i = sum_s pi_i(p_s) v_i(x_s - r_i)
```

The central parameters are:

- `lambda`: loss-aversion coefficient.
- `alpha`: gain-domain curvature.
- `beta`: loss-domain curvature.
- `gamma`: probability-weighting curvature.
- `r`: reference point.

## Identification cautions for real data

- A perceived loss may be a genuine material loss, not merely a behavioral bias.
- Rejection of a gamble may reflect liquidity constraints, ambiguity, distrust, or structural vulnerability.
- Investor behavior may reflect taxes, transaction costs, beliefs, or private information.
- Policy resistance may reflect real transition burdens.
- Risk perception may reflect lived exposure or distrust of official risk estimates.
- Reference points are empirical objects; they should not be imposed casually.
- Behavior change is not equivalent to welfare improvement.

Because the data here are synthetic, estimates are not empirical claims about actual households, investors, workers, consumers, platforms, firms, agencies, communities, or policy audiences. The value of the workflow is methodological.
