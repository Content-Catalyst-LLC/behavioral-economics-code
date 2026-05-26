# Identification Strategy

## Research setting

The synthetic data represent a regulatory policy experiment in which regulated agents are assigned to one of three regimes:

1. `sanction_heavy_deterrence`
2. `simplification_plus_trust`
3. `integrated_behavioral_regulation`

The central question is whether administrative simplification, default assistance, norm signaling, and trust-oriented design improve compliance and welfare relative to sanction-heavy deterrence.

## Core estimands

The main estimands are:

- Average treatment effect of simplification-plus-trust on compliance.
- Average treatment effect of integrated behavioral regulation on compliance.
- Treatment effect on total welfare.
- Treatment effect on social benefit net of compliance, administrative, and enforcement costs.
- Heterogeneous treatment effects by trust, burden sensitivity, compliance capacity, and private gain from noncompliance.
- Distributional incidence of compliance and welfare gains.

## Baseline experiment specification

```text
Y_i = alpha + beta_1 Simplification_i + beta_2 Integrated_i + X_i'gamma + epsilon_i
```

where `Y_i` may be compliance, total welfare, social benefit, compliance cost, administrative cost, or enforcement cost.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = alpha_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. In real regulatory research, selective rollout, anticipatory behavior, regulatory spillovers, organizational learning, and enforcement-risk changes would require careful evaluation.

## Threats to identification in real regulatory data

- Selection into compliance support programs.
- Selective targeting of firms, households, or users with known risk profiles.
- Non-random enforcement intensity.
- Dynamic learning after prior enforcement actions.
- Spillovers across regulated actors through professional networks or norms.
- Measurement error in compliance, burden, and welfare outcomes.
- Institutional changes occurring alongside behavioral redesign.

Because the data here are synthetic, estimates are not empirical claims about a real regulatory regime. The value of the workflow is methodological.
