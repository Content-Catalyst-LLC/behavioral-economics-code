# Identification Strategy

## Research setting

The synthetic data represent availability environments with different salience levels, base-rate disclosure, emotional intensity, recency, vividness, media exposure, social repetition, prior experience, numeracy, trust in statistics, risk tolerance, and availability sensitivity.

Regimes include:

1. `low_availability_with_base_rates`
2. `medium_availability_environment`
3. `high_availability_no_base_rates`

## Core estimands

- Effect of medium availability on perceived probability, calibration error, risky-asset participation, insurance demand, policy support, and welfare proxy.
- Effect of high availability with weak base-rate disclosure on perceived probability, calibration error, risky-asset participation, insurance demand, policy support, and welfare proxy.
- Effect of base-rate disclosure on calibration error.
- Heterogeneous effects by availability sensitivity, numeracy, trust in statistics, risk tolerance, and prior experience.

## Baseline specification

```text
Y_i = alpha
    + beta_1 MediumAvailability_i
    + beta_2 HighAvailability_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be subjective probability, calibration error, risky-asset participation, insurance demand, policy support, or welfare proxy.

## Communication / risk-perception specification

```text
Y_ig = alpha
     + beta_1 Salience_g
     + beta_2 BaseRateDisclosure_g
     + beta_3 EmotionalIntensity_g
     + X_i'gamma
     + epsilon_ig
```

This is included for workflow demonstration. Real data would require careful attention to randomization, selection into media exposure, confounding events, prior beliefs, trust, personal experience, group vulnerability, and whether a salient event conveys real new information.

## Identification cautions for real data

- A salient event may reveal real risk rather than merely distort perception.
- Availability can be informative when personal experience or local evidence is relevant.
- Base rates may undercount risks affecting marginalized communities.
- Risk perception may differ rationally by exposure and vulnerability.
- Media exposure is often endogenous to interests, fear, ideology, and platform behavior.
- Digital platforms may amplify salience through algorithmic engagement incentives.
- Climate and disaster communication must distinguish evidence-based warning from fear amplification.
- Behavior change is not automatically welfare improvement; calibration matters.

Because the data here are synthetic, estimates are not empirical claims about any actual investors, households, platforms, media systems, public agencies, climate campaigns, or policy audiences. The value of the workflow is methodological.
