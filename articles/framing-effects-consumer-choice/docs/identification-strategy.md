# Identification Strategy

## Research setting

The synthetic data represent framing regimes with different frame types, frame strength, disclosure quality, salience, loss aversion, utility curvature, numeracy, trust, and decision fatigue.

Regimes include:

1. `gain_frame`
2. `loss_frame`
3. `balanced_absolute_risk_frame`

## Core estimands

- Effect of loss framing on risky-choice probability.
- Effect of balanced absolute-risk framing on comprehension and welfare proxies.
- Effect of disclosure quality on comprehension.
- Effect of salience and frame strength on adjusted perceived value.
- Heterogeneous effects by loss aversion, numeracy, trust, and decision fatigue.

## Baseline specification

```text
Y_i = alpha
    + beta_1 LossFrame_i
    + beta_2 BalancedFrame_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be risky-choice probability, comprehension, welfare proxy, adjusted risky value, perceived value difference, or decision quality.

## Policy / interface experiment specification

```text
Y_ig = alpha
     + beta_1 Frame_g
     + beta_2 Disclosure_g
     + beta_3 Salience_g
     + X_i'gamma
     + epsilon_ig
```

This is included for workflow demonstration. Real data would require careful attention to randomization, baseline comprehension, selection, trust, numeracy, information content, differential exposure, interface context, product quality, market incentives, and welfare interpretation.

## Identification cautions for real data

- A frame may change information, not only presentation.
- A frame may improve comprehension rather than manipulate preference.
- Behavior change is not automatically welfare improvement.
- Consumer choices may reflect real constraints, not framing alone.
- Health and public-policy framing must distinguish absolute and relative risk.
- Digital-interface frames may interact with defaults, ranking, timing, and friction.
- Sustainability framing can clarify tradeoffs or become greenwashing.
- Vulnerable populations may be more affected by complex or misleading frames.

Because the data here are synthetic, estimates are not empirical claims about any actual consumers, patients, platform users, public-policy audiences, or sustainability campaigns. The value of the workflow is methodological.
