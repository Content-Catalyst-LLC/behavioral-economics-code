# Robustness and Sensitivity Plan

A professional behavioral-economics workflow should include robustness checks rather than one preferred estimate.

## Recommended checks

1. Estimate models with and without covariates.
2. Compare linear probability, logit/probit, and OLS welfare models.
3. Re-estimate treatment effects by cognitive-overload quartile.
4. Re-estimate by privacy-sensitivity quartile.
5. Re-estimate by autonomy-preference quartile.
6. Test sensitivity to alternative welfare weights.
7. Compare retention effects with welfare effects.
8. Flag regimes with high retention but negative mean user welfare.
9. Evaluate whether friction asymmetry explains retention after controls.
10. Report standard errors and confidence intervals where packages are available.

## Placebo checks

Possible placebo outcomes in a real study:

- pre-treatment engagement
- baseline preference
- prior subscription history
- pre-treatment consent behavior

## External validity

Real platform environments differ in trust, product category, user population, regulatory context, and switching costs. Synthetic results should not be interpreted as real-world estimates.
