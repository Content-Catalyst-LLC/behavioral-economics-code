# Identification Strategy

## Research setting

The synthetic data represent a digital interface experiment in which users are assigned to one of three interface regimes:

1. `user_supportive_design`
2. `engagement_maximizing_design`
3. `friction_heavy_lock_in`

The main policy-relevant concern is whether conversion and retention gains reflect genuine user welfare or behaviorally induced lock-in.

## Core estimands

The main estimands are:

- Average treatment effect of engagement-maximizing design on retention.
- Average treatment effect of friction-heavy lock-in design on retention.
- Average treatment effect of interface regime on user welfare.
- Heterogeneous treatment effects by cognitive overload, privacy sensitivity, and autonomy preference.
- Welfare-platform gap across interface regimes.

## Baseline regression

A simple cross-sectional experiment specification is:

```text
Y_i = alpha + beta_1 Engagement_i + beta_2 LockIn_i + X_i'gamma + epsilon_i
```

where `Y_i` may be joining, retention, consent, user welfare, or platform value.

## Panel / difference-in-differences style specification

The synthetic panel includes pre/post observations and allows:

```text
Y_it = alpha_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for teaching and workflow demonstration. In real research, parallel trends and design validity would need careful evaluation.

## Interpretation

Because the data are synthetic, estimates are not empirical claims about a real platform. The value of the workflow is methodological: it clarifies how economists could structure behavioral-design evaluation, welfare analysis, and policy-relevant robustness checks.
