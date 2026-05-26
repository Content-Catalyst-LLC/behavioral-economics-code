# Identification Strategy

## Research setting

The synthetic data represent a behavioral public-policy experiment in which agents are assigned to one of three nudge regimes:

1. `information_only`
2. `reminder_plus_norm`
3. `default_plus_reminder`

The central question is whether defaults, reminders, social-norm signals, and lower administrative burden improve public-policy uptake and welfare relative to an information-only environment.

## Core estimands

The main estimands are:

- Average treatment effect of reminder-plus-norm design on adoption.
- Average treatment effect of default-plus-reminder design on adoption.
- Treatment effect on total welfare.
- Treatment effect on user benefit and social benefit net of friction, administrative burden, and implementation cost.
- Heterogeneous treatment effects by present bias, trust, administrative-burden sensitivity, and default sensitivity.
- Distributional incidence of uptake and welfare gains.

## Baseline experiment specification

```text
Y_i = alpha + beta_1 ReminderNorm_i + beta_2 DefaultReminder_i + X_i'gamma + epsilon_i
```

where `Y_i` may be adoption, total welfare, user benefit, social benefit, friction cost, administrative cost, or implementation cost.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = alpha_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. In real policy research, selective rollout, anticipatory behavior, program awareness, institutional trust, and changing administrative rules would require careful evaluation.

## Threats to identification in real nudge-policy data

- Selection into program exposure.
- Selective targeting of likely compliers.
- Concurrent changes in benefits, eligibility, deadlines, or enforcement.
- Measurement error in take-up and welfare.
- Spillovers through social networks or public campaigns.
- Decay of treatment effects over time.
- Unequal digital or administrative access.

Because the data here are synthetic, estimates are not empirical claims about a real intervention. The value of the workflow is methodological.
