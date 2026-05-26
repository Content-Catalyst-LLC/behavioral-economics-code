# Identification Strategy

## Research setting

The synthetic data represent behavioral market regimes with different levels of investor-bias intensity, trading friction, platform salience, and market feedback.

Regimes include:

1. `low_behavioral_distortion`
2. `medium_behavioral_distortion`
3. `high_behavioral_distortion_low_friction`

## Core estimands

- Effect of medium behavioral distortion on absolute mispricing, trade intensity, buy rate, and trading-cost drag.
- Effect of high behavioral distortion under low-friction/high-salience design on market mispricing.
- Effect of platform salience on herd-signal amplification.
- Effect of trading friction on the translation of behavioral bias into action.
- Heterogeneous effects by overconfidence, loss aversion, anchoring strength, herd weight, risk tolerance, and diversification discipline.

## Baseline market-regime specification

```text
Y_t = alpha
    + beta_1 MediumBehavioralDistortion_t
    + beta_2 HighBehavioralDistortionLowFriction_t
    + X_t'gamma
    + epsilon_t
```

where `Y_t` may be absolute mispricing, mean trade intensity, mean buy rate, trading-cost drag, or price deviation.

## Panel / event-study style specification

```text
Y_it = mu_i + tau_t + beta(Regime_i x PostShock_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real data would require careful separation of behavioral mechanisms from public information, fundamentals, liquidity needs, tax motives, rebalancing, passive flows, product mandates, and institutional constraints.

## Identification cautions for real behavioral-finance data

- Mispricing is difficult to measure without a credible fundamental benchmark.
- Correlated trading does not automatically prove herding.
- High turnover can reflect information, liquidity needs, tax strategy, hedging, or mandate constraints.
- Platform engagement does not automatically imply investor welfare.
- Behavioral responses may be heterogeneous by experience, income, risk capacity, and financial literacy.
- Professional investors can exhibit bias through models and institutional incentives rather than visible retail-style trading.

Because the data here are synthetic, estimates are not empirical claims about any actual market, asset, investor, brokerage, or platform. The value of the workflow is methodological.
