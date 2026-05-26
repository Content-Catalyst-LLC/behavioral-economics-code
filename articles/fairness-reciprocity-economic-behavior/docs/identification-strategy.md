# Identification Strategy

## Research setting

The synthetic data represent a fairness-and-reciprocity experiment in which agents are assigned to one of four stylized interaction regimes:

1. `fair_cooperative_regime`
2. `unequal_but_cooperative_regime`
3. `unequal_noncooperative_regime`
4. `exploitative_low_process_fairness_regime`

The core analytical question is how fairness sensitivity, reciprocity sensitivity, trust, punishment willingness, and process fairness shape utility, rejection, punishment, cooperation, and welfare.

## Core estimands

- Average treatment effect of unequal-but-cooperative interaction on fairness-reciprocity utility.
- Average treatment effect of unequal-noncooperative interaction on fairness-reciprocity utility.
- Average treatment effect of exploitative low-process-fairness interaction on rejection and punishment.
- Treatment effect on welfare, process legitimacy, cooperation, and compliance.
- Heterogeneous treatment effects by fairness sensitivity, reciprocity sensitivity, trust, punishment willingness, and process-fairness weight.

## Baseline experiment specification

```text
Y_i = alpha_0
    + beta_1 UnequalCooperative_i
    + beta_2 UnequalNoncooperative_i
    + beta_3 ExploitativeLowProcess_i
    + X_i'gamma
    + epsilon_i
```

where `Y_i` may be fairness-reciprocity utility, rejection, punishment, process legitimacy, cooperation, or total welfare.

## Panel / difference-in-differences style specification

The synthetic panel supports:

```text
Y_it = mu_i + tau_t + beta(Regime_i x Post_t) + X_it'gamma + epsilon_it
```

This is included for workflow demonstration. Real data would require careful attention to assignment, prior fairness expectations, power asymmetry, institutional history, labor-market alternatives, and process legitimacy.

## Threats to identification in real fairness data

- Rejection can reflect fairness, anger, strategy, identity, distrust, or bargaining tactics.
- Cooperation may reflect voluntary reciprocity or constrained compliance.
- Process fairness may be correlated with unobserved institutional quality.
- Punishment can enforce fairness or unjust norms.
- Survey fairness measures can be sensitive to framing and reference points.
- Observed acceptance of unfair terms may reflect weak alternatives rather than legitimacy.
- Platform and workplace data can embed unobserved power asymmetries.

Because the data here are synthetic, estimates are not empirical claims about a real institution or population. The value of the workflow is methodological.
