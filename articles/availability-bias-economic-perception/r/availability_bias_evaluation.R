root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_availability_bias_panel.csv"))

outcomes <- c(
  "subjective_probability",
  "calibration_error",
  "participate_in_risky_asset",
  "insurance_demand",
  "policy_support",
  "welfare_proxy"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ medium_availability_treat + high_availability_treat + availability_sensitivity + numeracy + trust_in_statistics + risk_tolerance + prior_experience + availability_score + base_rate_disclosure + emotional_intensity"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("medium_availability_treat", "high_availability_treat")) {
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
write.csv(results, file.path(regression, "r_availability_bias_estimates.csv"), row.names = FALSE)
print(results)
