# Platform policy evaluation in R
# Synthetic economist-facing workflow for behavioral economics and digital platforms.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_platform_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_platform_panel.py first.")
}

df <- read.csv(data_path)

outcomes <- c("clicked", "retained", "consented", "user_welfare", "platform_value", "welfare_platform_gap")

estimate_rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(
    paste(
      outcome,
      "~ engagement_optimized + socially_amplified + baseline_user_value + cognitive_overload + privacy_sensitivity + digital_literacy + social_susceptibility"
    )
  )

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("engagement_optimized", "socially_amplified")) {
    estimate_rows[[length(estimate_rows) + 1]] <- data.frame(
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

results <- do.call(rbind, estimate_rows)
write.csv(results, file.path(regression, "r_platform_policy_estimates.csv"), row.names = FALSE)
print(results)

summary_table <- aggregate(
  cbind(clicked, retained, consented, user_welfare, platform_value, welfare_platform_gap) ~ regime,
  data = df,
  FUN = mean
)

write.csv(summary_table, file.path(tables, "r_platform_regime_welfare_summary.csv"), row.names = FALSE)
print(summary_table)
