# Identification Strategy

## Research setting

The synthetic data represent gain-frame, loss-frame, and mixed-gamble choice environments with heterogeneous loss-aversion coefficients, gain curvature, loss curvature, numeracy, income security, prior loss exposure, and trust.

Regimes include:

1. `gain`
2. `loss`
3. `mixed_gamble`

Additional modules cover disposition effects, endowment effects, consumer loss framing, policy-transition losses, and sustainability-transition resistance.

## Core estimands

- Effect of loss framing on risky choice relative to a gain-frame benchmark.
- Effect of mixed-gamble framing on risky choice.
- Effect of the loss-aversion coefficient on mixed-gamble acceptance.
- Effect of income security and prior loss exposure on willingness to take risk in loss domains.
- Effect of purchase-price reference points on selling winners versus losers.
- Effect of ownership / entitlement on willingness-to-accept versus willingness-to-pay gaps.
- Effect of concentrated policy losses on support for reform.

## Baseline specification

```text
Y_i = alpha
    + beta_1 LossFrame_i
    + beta_2 MixedGamble_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be risky choice, prospect value, acceptance of a mixed gamble, selling decision, willingness to accept, policy support, or welfare proxy.

## Reference-point model

```text
v(x-r) = (x-r)^alpha              if x >= r
v(x-r) = -lambda(r-x)^beta        if x < r
```

The central parameter is `lambda > 1`, which captures the extra weight placed on losses.

## Identification cautions for real data

- A perceived loss may be a real material loss, not merely a bias.
- Investor selling behavior may reflect taxes, beliefs, transaction costs, or liquidity needs.
- Consumer switching may reflect search costs, distrust, or product complexity.
- Labor-market resistance may reflect genuine insecurity or historical injustice.
- Policy resistance may reflect actual transition burdens, not only psychological loss aversion.
- Reference points are empirical objects; they should not be imposed without evidence.
- Welfare cannot be inferred from behavior change alone.

Because the data here are synthetic, estimates are not empirical claims about actual consumers, workers, investors, platforms, firms, households, public agencies, communities, or policy audiences. The value of the workflow is methodological.
