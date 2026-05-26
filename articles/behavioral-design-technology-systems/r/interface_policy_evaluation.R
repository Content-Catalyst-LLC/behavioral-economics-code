# Interface policy evaluation in R
# Synthetic economist-facing workflow for behavioral design in technology systems.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_interface_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_interface_panel.py first.")
}

df <- read.csv(data_path)

outcomes <- c("joined", "retained", "consented", "user_welfare", "platform_value", "welfare_platform_gap")

estimate_rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(
    paste(
      outcome,
      "~ engagement_design + lockin_design + baseline_value + cognitive_overload + privacy_sensitivity + autonomy_preference + digital_literacy"
    )
  )

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("engagement_design", "lockin_design")) {
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
write.csv(results, file.path(regression, "r_interface_policy_estimates.csv"), row.names = FALSE)
print(results)

# Regime-level welfare summary.
summary_table <- aggregate(
  cbind(joined, retained, consented, user_welfare, platform_value, welfare_platform_gap) ~ regime,
  data = df,
  FUN = mean
)

write.csv(summary_table, file.path(tables, "r_regime_welfare_summary.csv"), row.names = FALSE)
print(summary_table)
