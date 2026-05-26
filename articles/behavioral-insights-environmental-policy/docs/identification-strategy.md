# Identification Strategy

## Research setting

The synthetic data represent an environmental policy experiment in which households are assigned to one of three policy regimes:

1. `price_signal_only`
2. `norm_plus_default`
3. `integrated_policy_design`

The central question is whether behavioral design elements such as defaults, norm feedback, and friction reduction improve environmental uptake and welfare relative to a price-signal-only policy.

## Core estimands

The main estimands are:

- Average treatment effect of norm-plus-default design on adoption.
- Average treatment effect of integrated policy design on adoption.
- Treatment effect on total welfare.
- Treatment effect on environmental benefit net of fiscal and administrative costs.
- Heterogeneous treatment effects by income, energy burden, present bias, and institutional trust.
- Distributional incidence of adoption and welfare gains.

## Baseline experiment specification

```text
Y_i = alpha + beta_1 NormDefault_i + beta_2 Integrated_i + X_i'gamma + epsilon_i
```

where `Y_i` may be adoption, total welfare, environmental benefit, private benefit, fiscal cost, or administrative cost.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = alpha_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. In real environmental policy research, selective rollout, anticipatory behavior, local treatment spillovers, and infrastructure constraints would require careful evaluation.

## Threats to identification in real environmental policy data

- Selection into voluntary environmental programs.
- Differential administrative burden by income, tenure, language, or digital access.
- Infrastructure constraints that affect treatment response.
- Policy spillovers across neighboring households or firms.
- Non-random program rollout.
- Confounding from contemporaneous energy prices or weather shocks.
- Measurement error in adoption, consumption, or environmental benefit.

Because the data here are synthetic, estimates are not empirical claims about a real policy. The value of the workflow is methodological.
