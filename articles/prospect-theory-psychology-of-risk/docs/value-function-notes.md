# Prospect-Theory Value Function Notes

## Reference dependence

Prospect theory evaluates outcomes relative to a reference point rather than final wealth alone.

```text
z = x - r
```

where `x` is the outcome and `r` is the reference point.

## Value function

```text
v(z) = z^alpha                 if z >= 0
v(z) = -lambda(-z)^beta        if z < 0
```

## Parameters

- `lambda > 1`: loss aversion.
- `alpha`: diminishing sensitivity for gains.
- `beta`: diminishing sensitivity for losses.
- `r`: reference point.
- `z`: gain or loss relative to the reference point.

## Interpretation

Losses reduce value more than equivalent gains increase value. Sensitivity to gains and losses often diminishes as outcomes move farther from the reference point.

## Caution

Reference points may be material, social, contractual, political, institutional, or moral. They require empirical interpretation.
