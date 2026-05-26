# Identification Strategy

## Research setting

The synthetic data represent default and switching regimes with different status quo premiums, switching costs, loss aversion, perceived loss, uncertainty sensitivity, decision fatigue, sophistication, disclosure quality, and switching support.

Regimes include:

1. `passive_status_quo_default`
2. `active_choice_with_disclosure`
3. `pro_switching_default_with_support`

## Core estimands

- Effect of active choice with disclosure on alternative adoption and welfare.
- Effect of a pro-switching default with support on alternative adoption and welfare.
- Effect of switching support on adoption among high-switching-cost agents.
- Effect of disclosure quality on perceived loss and status quo premium.
- Heterogeneous effects by switching cost, loss aversion, decision fatigue, uncertainty sensitivity, and sophistication.

## Baseline specification

```text
Y_i = alpha
    + beta_1 ActiveChoice_i
    + beta_2 ProSwitchingDefault_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be alternative adoption, welfare, effective switching cost, effective status quo premium, or expected value improvement.

## Panel / grouped specification

```text
Y_ig = alpha
     + beta_1 ActiveChoice_g
     + beta_2 ProSwitchingDefault_g
     + X_i'gamma
     + epsilon_ig
```

This is included for workflow demonstration. Real data would require careful attention to selection, switching costs, user satisfaction, search costs, inertia, administrative burden, information asymmetry, market power, and distributional effects.

## Identification cautions for real data

- Observed persistence does not prove bias; people may genuinely prefer the status quo.
- Switching costs may be real rather than psychological.
- Defaults may signal institutional endorsement.
- Active choice can improve agency but can also increase burden.
- Pro-switching defaults can be beneficial or paternalistic depending on design.
- Digital platforms may hide switching costs through data lock-in, subscription friction, or network effects.
- Institutional inertia may reflect power, sunk costs, legal constraints, or coordination failure, not cognition alone.
- Sustainability transition resistance may reflect real distributional burdens as well as status quo bias.

Because the data here are synthetic, estimates are not empirical claims about any actual population, platform, subscription service, retirement plan, public agency, energy system, or institution. The value of the workflow is methodological.
