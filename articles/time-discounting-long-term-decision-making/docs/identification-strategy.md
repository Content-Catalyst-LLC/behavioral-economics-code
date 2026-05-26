# Identification Strategy

## Research setting

The synthetic data represent intertemporal-choice regimes with different discount structures, commitment-support levels, flexibility assumptions, present-bias parameters, discount factors, sophistication, liquidity need, immediate reward, and future-goal value.

Regimes include:

1. `exponential_discounting`
2. `present_biased_discounting`
3. `present_bias_with_commitment_support`

## Core estimands

- Effect of present-biased discounting on delayed-choice probability, cumulative delayed choices, and cumulative welfare.
- Effect of commitment support under present bias on delayed-choice probability, cumulative delayed choices, and cumulative welfare.
- Effect of flexibility loss on welfare for agents with high liquidity need.
- Heterogeneous effects by present-bias quartile, discount-factor quartile, sophistication, liquidity need, and future-goal value.

## Baseline specification

```text
Y_i = alpha
    + beta_1 PresentBias_i
    + beta_2 CommitmentSupport_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be delayed-choice probability, cumulative delayed choices, cumulative welfare, period welfare, plan adherence, present-value error, or hardship burden.

## Panel / event-study style specification

```text
Y_it = mu_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real data would require careful attention to selection, liquidity constraints, uncertainty, income volatility, institutional trust, digital-platform design, and whether commitment support is voluntary, defaulted, or imposed.

## Identification cautions for real data

- High discounting may reflect rational response to scarcity, uncertainty, inflation, distrust, or constrained access to future resources.
- Under-saving, delay, or immediate consumption may not be present bias alone.
- Commitment adoption is often endogenous to sophistication and motivation.
- Increased delayed choice is not automatically welfare-improving.
- Stronger commitment can reduce flexibility and harm people facing shocks.
- Discount-rate assumptions in climate and infrastructure policy are ethically loaded, not merely technical.
- Digital platforms can use timing architecture to support users or exploit them.

Because the data here are synthetic, estimates are not empirical claims about any actual population, household, app, employer, school, platform, environmental policy, or public institution. The value of the workflow is methodological.
