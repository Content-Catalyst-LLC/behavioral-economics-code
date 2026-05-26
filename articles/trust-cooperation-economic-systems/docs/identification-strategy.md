# Identification Strategy

The synthetic data represent a trust-and-cooperation experiment in which agents are assigned to one of three institutional regimes:

1. `low_trust_exchange`
2. `reciprocal_market_exchange`
3. `institutionally_supported_cooperation`

## Core estimands

- Average treatment effect of reciprocal-market exchange on trust.
- Average treatment effect of institutionally supported cooperation on trust.
- Treatment effect on reciprocity, transaction-cost reduction, monitoring cost, and total welfare.
- Heterogeneous treatment effects by trust propensity, institutional trust, betrayal sensitivity, reciprocity, and monitoring-cost sensitivity.

## Baseline specification

```text
Y_i = alpha + beta_1 ReciprocalMarket_i + beta_2 InstitutionalSupport_i + X_i'gamma + epsilon_i
```

## Real-world identification cautions

Trust is both cause and consequence. Real data require attention to selection, institutional history, network spillovers, unobserved prior betrayal, and the difference between justified trust and trust extraction.
