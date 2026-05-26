# Identification Strategy

## Research setting

The synthetic data represent a decision-environment experiment in which users are assigned to one of three choice-architecture regimes:

1. `neutral_presentation`
2. `default_heavy_architecture`
3. `low_complexity_guided_design`

The central question is whether defaults, salience, framing, cognitive load, and switching costs change observed behavior and whether those changes improve user welfare.

## Core estimands

The main estimands are:

- Average treatment effect of default-heavy architecture on selected option.
- Average treatment effect of low-complexity guided design on realized welfare.
- Treatment effect on concentration of choice shares.
- Treatment effect on cognitive and switching-cost burden.
- Heterogeneous treatment effects by complexity sensitivity and default sensitivity.
- Difference between architecture-adjusted choice utility and long-run user welfare.

## Baseline experiment specification

```text
Y_i = alpha + beta_1 DefaultHeavy_i + beta_2 GuidedDesign_i + X_i'gamma + epsilon_i
```

where `Y_i` may be realized welfare, chosen utility, selected high-value option, cognitive cost, switching cost, or option concentration.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = alpha_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. In real choice-architecture research, selective rollout, prior user learning, platform personalization, and interference across users would require careful evaluation.

## Threats to identification in real choice-architecture data

- Non-random exposure to interface regimes.
- Personalization based on prior behavior.
- Sorting into defaults by user type.
- Dynamic learning after repeated exposure.
- Concurrent changes in prices, content, or product quality.
- Measurement error in welfare and comprehension.
- Spillovers through social proof or platform ranking.

Because the data here are synthetic, estimates are not empirical claims about a real environment. The value of the workflow is methodological.
