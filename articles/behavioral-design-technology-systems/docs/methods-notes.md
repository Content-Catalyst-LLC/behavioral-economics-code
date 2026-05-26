# Methods Notes

This scaffold compares stylized behavioral interface regimes using synthetic data.

The models focus on:

- salience
- defaults
- entry friction
- exit friction
- friction asymmetry
- reward intensity
- cognitive overload
- privacy sensitivity
- autonomy preference
- platform value
- user-welfare trade-offs

The examples are intentionally simple so that assumptions remain visible. They are not calibrated to a specific product, platform, population, or user base.

## Conceptual model

A simplified interface utility can be represented as:

```text
U_j = v_j + alpha*S_j + beta*D_j - gamma*F_j + delta*R_j - lambda*C_j
```

where:

- `v_j` is baseline user value
- `S_j` is salience
- `D_j` is default status
- `F_j` is friction
- `R_j` is reward intensity
- `C_j` is cognitive burden

Friction asymmetry can be represented as:

```text
F_out - F_in
```

High positive values may indicate possible lock-in or manipulative design.
