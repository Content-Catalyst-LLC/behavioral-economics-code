root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_anchoring_bias_panel.csv"))

outcomes <- c(
  "estimate",
  "bias",
  "absolute_error",
  "decision_quality",
  "welfare_proxy"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ low_anchor_treat + high_anchor_treat + counter_context_treat + anchor_value + adjustment_rate + effective_adjustment + numeracy + confidence + cognitive_load + domain_knowledge + disclosure_quality + counter_anchor_support"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("low_anchor_treat", "high_anchor_treat", "counter_context_treat")) {
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
write.csv(results, file.path(regression, "r_anchoring_bias_estimates.csv"), row.names = FALSE)
print(results)
