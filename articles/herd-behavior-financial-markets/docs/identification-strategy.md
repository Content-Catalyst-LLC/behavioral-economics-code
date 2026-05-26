# Identification Strategy

## Research setting

The synthetic data represent market regimes with different levels of herding, liquidity depth, leverage pressure, social-media intensity, private-information quality, reputation pressure, and shock exposure.

Regimes include:

1. `low_herding_deep_liquidity`
2. `moderate_herding`
3. `high_herding_crowded_trade`

## Core estimands

- Effect of moderate herding on price deviation, buy rate, volatility proxy, and final price.
- Effect of high herding and crowded-trade conditions on boom-bust range.
- Effect of liquidity depth on shock absorption.
- Effect of leverage pressure on synchronized reversals.
- Effect of social-media intensity on herd-signal amplification.
- Heterogeneous effects by information quality, loss aversion, reputation pressure, and private-signal weight.

## Baseline market-regime specification

```text
Y_it = alpha
     + beta_1 ModerateHerding_i
     + beta_2 HighHerdingCrowdedTrade_i
     + X_it'gamma
     + epsilon_it
```

where `Y_it` may be price, price deviation, buy rate, volatility proxy, liquidity stress, or crash drawdown.

## Panel / event-study style specification

```text
Y_it = mu_i + tau_t + beta(Regime_i x PostShock_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real market data would require careful separation of herding from common information, mechanical rebalancing, benchmark effects, fundamental news, and liquidity constraints.

## Identification cautions for real financial data

- Correlated trading does not prove imitation.
- Investors may move together because fundamentals changed.
- Herding may be confounded with common risk models, passive flows, or benchmark rebalancing.
- Social-media attention may reflect price movement rather than cause it.
- Order-flow data may be incomplete or institutionally filtered.
- Institutional herding may reflect career risk rather than investor psychology alone.
- Retail herding may combine narrative, platform design, distrust of institutions, and real coordination.

Because the data here are synthetic, estimates are not empirical claims about any actual market, asset, or security. The value of the workflow is methodological.
