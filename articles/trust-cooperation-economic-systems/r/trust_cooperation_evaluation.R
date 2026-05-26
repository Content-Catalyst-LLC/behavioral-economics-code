root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_trust_cooperation_experiment.csv"))

outcomes <- c("trusted", "reciprocated", "punished", "transaction_cost_reduction", "monitoring_cost", "total_welfare")
rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(outcome, "~ reciprocal_market_treat + institutional_support_treat + trust_propensity + reciprocity + punishment_willingness + institutional_trust + betrayal_sensitivity + monitoring_cost_sensitivity"))
  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("reciprocal_market_treat", "institutional_support_treat")) {
    rows[[length(rows) + 1]] <- data.frame(
      outcome = outcome,
      term = term,
      estimate = coefs[term, "Estimate"],
      std_error = coefs[term, "Std. Error"],
      p_value = coefs[term, "Pr(>|t|)"],
      n = nobs(model),
      r_squared = summary(model)$r.squared
    )
  }
}

results <- do.call(rbind, rows)
write.csv(results, file.path(regression, "r_trust_cooperation_estimates.csv"), row.names = FALSE)
print(results)
