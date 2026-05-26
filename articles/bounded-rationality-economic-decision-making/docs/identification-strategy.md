# Identification Strategy

## Research setting

The synthetic data represent low-, medium-, and high-constraint decision environments. Agents face aspiration thresholds, search costs, time budgets, cognitive-capacity limits, stress, numeracy, institutional trust, income security, digital access, and administrative capacity.

Regimes include:

1. `low_constraint`
2. `medium_constraint`
3. `high_constraint`

Additional modules cover administrative burden, policy simplification, organizational routines, consumer search, digital-platform friction, and sustainability decision systems.

## Core estimands

- Effect of medium- and high-constraint regimes on decision quality.
- Effect of constraint regimes on net value after search costs.
- Effect of constraint regimes on optimization gaps.
- Effect of aspiration thresholds on search depth and choice quality.
- Effect of cognitive capacity, time pressure, stress, numeracy, and trust on bounded decision-making.
- Effect of administrative burden on benefit take-up and completion.
- Effect of policy simplification on access and welfare.
- Effect of organizational routines on decision quality under stable versus changing environments.
- Effect of digital-platform friction on consumer switching and plan quality.

## Baseline specification

```text
Y_i = alpha
    + beta_1 MediumConstraint_i
    + beta_2 HighConstraint_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be chosen value, net value, optimization gap, search depth, completion, take-up, switching, policy support, routine performance, or welfare proxy.

## Bounded-rationality mechanism

A full-search optimizer chooses:

```text
x* = argmax V(x_i)
```

A satisficing agent chooses the first option meeting an aspiration threshold:

```text
choose x_i when V(x_i) >= a
```

Net value subtracts search cost:

```text
U(x_i) = V(x_i) - c s_i
```

## Identification cautions for real data

- A deviation from an optimizing benchmark is not automatically a mistake.
- The benchmark may omit trust, dignity, safety, fairness, liquidity, or identity.
- Low take-up may reflect administrative burden, stigma, distrust, digital exclusion, or real ineligibility.
- Search behavior may reflect scarce time, poverty, caregiving, disability, language barriers, or exclusion.
- Better choices require better systems, not just more information.
- Behavior change is not equivalent to welfare improvement.

Because the data here are synthetic, estimates are not empirical claims about actual households, workers, consumers, agencies, firms, platforms, or communities. The value of the workflow is methodological.
