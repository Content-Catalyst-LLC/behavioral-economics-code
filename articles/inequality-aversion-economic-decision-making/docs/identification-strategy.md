# Identification Strategy

## Research setting

The synthetic data represent a distributional-regime experiment in which agents are assigned to one of three stylized allocation environments:

1. `equal_distribution`
2. `advantageous_inequality`
3. `disadvantageous_inequality`

The core analytical question is how heterogeneous inequality-aversion parameters shape utility, rejection, redistribution support, and policy evaluation.

## Core estimands

- Average treatment effect of advantageous inequality on social-preference utility.
- Average treatment effect of disadvantageous inequality on social-preference utility.
- Treatment effect on rejection propensity, redistribution support, and perceived legitimacy.
- Heterogeneous treatment effects by alpha, beta, merit belief, redistribution norm, and institutional trust.
- Welfare sensitivity to inequality penalty, process legitimacy, and material-payoff assumptions.

## Baseline experiment specification

```text
Y_i = alpha_0 + beta_1 AdvantageousInequality_i + beta_2 DisadvantageousInequality_i + X_i'gamma + epsilon_i
```

where `Y_i` may be social-preference utility, rejection propensity, redistribution support, legitimacy perception, or welfare.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = mu_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real data would require careful attention to income selection, group comparison sets, institutional framing, policy salience, and prior beliefs about merit, luck, discrimination, and mobility.

## Threats to identification in real inequality-aversion data

- Inequality aversion is inferred indirectly from behavior.
- Rejection may reflect strategy, anger, distrust, or identity, not only social preference.
- Redistribution support may reflect self-interest, ideology, altruism, risk aversion, or mobility beliefs.
- People evaluate both distributions and processes.
- Acceptance of unequal offers may reflect constraint rather than consent.
- Comparison groups are endogenous and context-dependent.
- Observed behavior may be shaped by power, labor-market alternatives, legal constraints, or institutional pressure.

Because the data here are synthetic, estimates are not empirical claims about a real institution or population. The value of the workflow is methodological.
