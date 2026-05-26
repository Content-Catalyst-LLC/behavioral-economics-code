root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_bounded_rationality_panel.csv"))

outcomes <- c(
  "chosen_value",
  "net_value",
  "optimization_gap",
  "chosen_index"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ medium_constraint_treat + high_constraint_treat + aspiration + search_cost + time_budget + cognitive_capacity + numeracy + stress + institutional_trust + digital_access + income_security + administrative_capacity"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("medium_constraint_treat", "high_constraint_treat", "aspiration", "search_cost", "time_budget", "cognitive_capacity", "numeracy", "stress", "institutional_trust", "digital_access", "income_security", "administrative_capacity")) {
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
write.csv(results, file.path(regression, "r_bounded_rationality_estimates.csv"), row.names = FALSE)
print(results)
