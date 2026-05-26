# Identification Strategy

## Research setting

The synthetic data represent cognitive environments with different levels of heuristic-signal intensity, disclosure quality, debiasing support, correction capacity, numeracy, domain knowledge, cognitive load, and confidence.

Regimes include:

1. `low_bias_with_context`
2. `medium_bias_environment`
3. `high_bias_low_context`

## Core estimands

- Effect of a medium-bias environment on estimated value, judgment error, absolute error, decision quality, and welfare proxy.
- Effect of a high-bias low-context environment on estimated value, judgment error, absolute error, decision quality, and welfare proxy.
- Effect of correction capacity on reducing judgment error.
- Effect of cognitive load on increasing error and reducing welfare.
- Heterogeneous effects by correction capacity, numeracy, domain knowledge, cognitive load, and confidence.

## Baseline specification

```text
Y_i = alpha
    + beta_1 MediumBias_i
    + beta_2 HighBias_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be estimated value, judgment error, absolute error, decision quality, welfare proxy, or correction capacity.

## Design / policy specification

```text
Y_ig = alpha
     + beta_1 SignalScale_g
     + beta_2 DisclosureQuality_g
     + beta_3 DebiasingSupport_g
     + X_i'gamma
     + epsilon_ig
```

This is included for workflow demonstration. Real data would require careful attention to randomization, information content, selection into environments, institutional credibility, prior experience, and whether the observed behavior reflects bias, rational adaptation, or structural constraint.

## Identification cautions for real data

- A vivid signal may convey real risk, not merely availability bias.
- A pattern may be predictive in valid environments, not merely representativeness bias.
- An anchor may carry useful information, not merely distortion.
- A decision that appears biased may reflect liquidity constraints, precarity, or lived exposure.
- Formal models may undercount marginalized experience or environmental harms.
- Platform-generated choice environments may intentionally amplify bias.
- Welfare cannot be inferred from behavior change alone.

Because the data here are synthetic, estimates are not empirical claims about actual households, consumers, investors, platforms, public agencies, sustainability campaigns, or institutions. The value of the workflow is methodological.
