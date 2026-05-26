# Identification Strategy

## Research setting

The synthetic data represent intertemporal-choice regimes with different commitment costs, reminder strength, flexibility, present-bias parameters, discount factors, sophistication, liquidity need, temptation intensity, and future-goal value.

Regimes include:

1. `weak_commitment`
2. `medium_commitment`
3. `strong_commitment`

## Core estimands

- Effect of medium commitment on delayed-choice probability, cumulative delayed choices, and cumulative welfare.
- Effect of strong commitment on delayed-choice probability, cumulative delayed choices, and cumulative welfare.
- Effect of reminder strength on delayed-choice behavior.
- Effect of reduced flexibility on welfare for agents with high liquidity need.
- Heterogeneous effects by present-bias quartile, sophistication, liquidity need, patience, and temptation strength.

## Baseline specification

```text
Y_i = alpha
    + beta_1 MediumCommitment_i
    + beta_2 StrongCommitment_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be delayed-choice probability, cumulative delayed choices, cumulative welfare, period welfare, plan adherence, or hardship burden.

## Panel / event-study style specification

```text
Y_it = mu_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real data would require careful attention to selection into commitment devices, scarcity, income volatility, institutional barriers, health constraints, digital-platform design, and whether commitment is voluntary, defaulted, or imposed.

## Identification cautions for real data

- Under-saving, delay, or impulsive spending may reflect scarcity, not only present bias.
- Commitment adoption is often endogenous to sophistication and motivation.
- Increased delayed choice is not automatically welfare-improving.
- Stronger commitment can reduce flexibility and harm people facing shocks.
- Digital platforms can use present-bias design to help users or exploit users.
- Present bias may interact with depression, fatigue, stress, information gaps, and institutional complexity.
- Sustainability policy requires distinguishing behavioral delay from political economy, inequality, and power.

Because the data here are synthetic, estimates are not empirical claims about any actual population, household, app, employer, school, platform, or policy. The value of the workflow is methodological.
