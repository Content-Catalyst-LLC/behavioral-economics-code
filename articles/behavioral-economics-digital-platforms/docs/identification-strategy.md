# Identification Strategy

## Research setting

The synthetic data represent a platform-policy experiment in which users are assigned to one of three platform regimes:

1. `neutral_discovery`
2. `engagement_optimized`
3. `socially_amplified_ranking`

The central question is whether platform ranking and recommendation systems alter user welfare, platform value, exposure concentration, and social-proof-driven selection.

## Core estimands

The main estimands are:

- Average treatment effect of engagement-optimized ranking on user welfare.
- Average treatment effect of socially amplified ranking on user welfare.
- Treatment effect on platform value and platform-user welfare gap.
- Treatment effect on exposure concentration and top-item share.
- Heterogeneous treatment effects by cognitive overload and privacy sensitivity.
- Sensitivity of results to assumptions about privacy, attention, and platform revenue weights.

## Baseline experiment specification

```text
Y_i = alpha + beta_1 EngagementOptimized_i + beta_2 SocialAmplified_i + X_i'gamma + epsilon_i
```

where `Y_i` may be user welfare, platform value, welfare gap, retained, clicked, or consented.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = alpha_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. In real platform research, design validity, selective rollout, interference, and dynamic feedback loops would require careful evaluation.

## Threats to identification in real platform data

- Endogenous recommendation intensity.
- Selective targeting of vulnerable or high-value users.
- Dynamic feedback between clicks and future exposure.
- Interference across users through rankings, ratings, and social proof.
- Non-random item visibility.
- Platform objective changes during the study period.
- Measurement error in welfare outcomes.

Because the data here are synthetic, estimates are not empirical claims about a real platform. The value of the workflow is methodological.
