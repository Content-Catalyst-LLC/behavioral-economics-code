root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_heuristics_biases_panel.csv"))

outcomes <- c(
  "estimated_value",
  "judgment_error",
  "absolute_error",
  "decision_quality",
  "welfare_proxy"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ medium_bias_treat + high_bias_treat + correction_capacity + numeracy + domain_knowledge + cognitive_load + confidence + disclosure_quality + debiasing_support + availability_signal + representativeness_signal + anchor_signal + framing_signal"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("medium_bias_treat", "high_bias_treat")) {
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
write.csv(results, file.path(regression, "r_heuristics_biases_estimates.csv"), row.names = FALSE)
print(results)
