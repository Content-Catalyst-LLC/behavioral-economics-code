# Methods Notes

This scaffold compares stylized behavioral-governance regimes using synthetic data.

The models focus on:

- administrative burden
- salience and reminder design
- institutional trust
- norm sensitivity
- penalty strength
- present bias
- distributional differences

The examples are intentionally simple so that assumptions remain visible. They are not calibrated to a jurisdiction, agency, or real population.

## Conceptual model

A simplified compliance utility can be represented as:

```text
U_C = B - P_f * penalty + S + T - A
```

where:

- `B` is perceived benefit
- `P_f` is perceived enforcement probability
- `penalty` is perceived penalty severity
- `S` is social or normative value
- `T` is institutional trust or legitimacy
- `A` is administrative burden

The workflows treat compliance as probabilistic rather than deterministic.
