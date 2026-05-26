# Welfare Analysis Notes

Digital platform analysis should not treat engagement, retention, or click-through as welfare measures by default.

## User welfare proxy

The synthetic workflows define user welfare as a function of:

- baseline item value
- friction cost
- privacy cost
- attention or cognitive overload cost
- exposure quality
- regret or over-engagement penalty where applicable

## Platform value proxy

Platform value is modeled as a function of:

- selected item revenue value
- engagement probability
- retained attention
- data extraction intensity
- social amplification value

## Welfare-platform gap

The key diagnostic is:

```text
welfare_platform_gap = platform_value - user_welfare
```

A high gap signals possible divergence between institutional value and user welfare.

## Policy relevance

This scaffold is useful for:

- platform regulation
- consumer protection
- recommendation-system auditing
- dark-pattern and engagement-risk analysis
- welfare-oriented market design
- platform labor and reputation-system research
