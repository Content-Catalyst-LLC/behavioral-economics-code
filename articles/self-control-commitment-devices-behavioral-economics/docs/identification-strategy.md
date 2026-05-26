# Identification Strategy

## Research setting

The synthetic data represent commitment-device regimes with different commitment costs, automation strength, flexibility, liquidity access, emergency shocks, present-bias parameters, and sophistication.

Regimes include:

1. `low_commitment`
2. `medium_commitment`
3. `high_commitment`

## Core estimands

- Effect of medium commitment on accumulated savings, period savings, withdrawals, and welfare.
- Effect of high commitment on accumulated savings and welfare.
- Effect of automation strength on plan adherence.
- Effect of flexibility on welfare under emergency shocks.
- Heterogeneous effects by present bias, sophistication, liquidity need, income volatility, and emergency risk.

## Baseline specification

```text
Y_i = alpha
    + beta_1 MediumCommitment_i
    + beta_2 HighCommitment_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be accumulated savings, actual savings, emergency withdrawal, welfare, plan-adherence rate, or hardship burden.

## Panel / event-study style specification

```text
Y_it = mu_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real data would require careful attention to selection into commitment devices, liquidity constraints, income volatility, administrative burden, heterogeneous welfare effects, and whether the commitment was voluntary, defaulted, or imposed.

## Identification cautions for real data

- People who select into commitment devices may already differ from those who do not.
- Increased savings is not automatically increased welfare if liquidity needs are unmet.
- Strong penalties can improve adherence while worsening hardship.
- Defaults may reflect institutional convenience rather than user welfare.
- Sophisticated and naive present-biased individuals may respond differently.
- Digital commitment tools may support agency or exploit inertia.
- Commitment demand can be constrained by income, credit access, work schedules, household risk, or structural inequality.

Because the data here are synthetic, estimates are not empirical claims about any actual population, product, employer, platform, or policy. The value of the workflow is methodological.
