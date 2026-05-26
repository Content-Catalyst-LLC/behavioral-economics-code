# Identification Strategy

## Research setting

The synthetic data represent investor regimes with different overconfidence levels, trading frictions, leverage access, signal quality, diversification discipline, prior-success sensitivity, and risk tolerance.

Regimes include:

1. `calibrated_confidence`
2. `moderate_overconfidence`
3. `high_overconfidence_low_friction`

## Core estimands

- Effect of moderate overconfidence on trading intensity, trading cost, realized net return, and volatility.
- Effect of high overconfidence under low-friction/high-leverage access on turnover and net performance.
- Effect of trading friction on the behavioral translation of confidence into action.
- Effect of leverage access on realized-return volatility.
- Heterogeneous effects by true signal quality, risk tolerance, diversification discipline, and prior-success sensitivity.

## Baseline regime specification

```text
Y_it = alpha
     + beta_1 ModerateOverconfidence_i
     + beta_2 HighOverconfidenceLowFriction_i
     + X_it'gamma
     + epsilon_it
```

where `Y_it` may be trade intensity, trading cost, realized return, perceived-signal magnitude, volatility proxy, or drawdown.

## Panel / event-study style specification

```text
Y_it = mu_i + tau_t + beta(Regime_i x PostSuccess_it) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real investor data would require careful separation of overconfidence from genuine information advantage, liquidity needs, tax-loss harvesting, rebalancing, hedging, institutional mandate, and product constraints.

## Identification cautions for real data

- High turnover is not automatically overconfidence.
- Portfolio concentration can reflect information advantage or constrained choice.
- Net performance must be measured after costs, taxes, spreads, and risk adjustment.
- Investor success may reflect beta, factor exposure, or market regime rather than skill.
- Platform friction may be endogenous to product access and investor sophistication.
- Survey confidence measures may not map cleanly onto realized behavior.
- Professional overconfidence may appear through models, forecasts, and committees rather than frequent trading.

Because the data here are synthetic, estimates are not empirical claims about any actual investor, brokerage, platform, product, or market. The value of the workflow is methodological.
