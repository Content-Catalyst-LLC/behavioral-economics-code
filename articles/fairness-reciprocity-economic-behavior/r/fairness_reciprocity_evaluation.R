root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_fairness_reciprocity_experiment.csv"))

outcomes <- c(
  "fairness_reciprocity_utility",
  "rejected",
  "punished",
  "cooperated",
  "process_fairness",
  "total_welfare"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ unequal_cooperative_treat + unequal_noncooperative_treat + exploitative_low_process_treat + fairness_sensitivity + reciprocity_sensitivity + trust + punishment_willingness + process_fairness_weight"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("unequal_cooperative_treat", "unequal_noncooperative_treat", "exploitative_low_process_treat")) {
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
write.csv(results, file.path(regression, "r_fairness_reciprocity_estimates.csv"), row.names = FALSE)
print(results)
