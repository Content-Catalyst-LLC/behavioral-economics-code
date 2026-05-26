# Nudge policy evaluation in R
# Synthetic economist-facing workflow for behavioral public policy.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_nudge_policy_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_nudge_policy_panel.py first.")
}

df <- read.csv(data_path)

outcomes <- c(
  "adopted",
  "total_welfare",
  "user_benefit",
  "social_benefit",
  "friction_cost",
  "admin_cost",
  "implementation_cost"
)

estimate_rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(
    paste(
      outcome,
      "~ reminder_norm_treat + default_reminder_treat + default_sensitivity + reminder_sensitivity + norm_sensitivity + friction_sensitivity + present_bias + administrative_burden_sensitivity + trust"
    )
  )

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("reminder_norm_treat", "default_reminder_treat")) {
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
write.csv(results, file.path(regression, "r_nudge_policy_estimates.csv"), row.names = FALSE)
print(results)

summary_table <- aggregate(
  cbind(adopted, total_welfare, user_benefit, social_benefit, friction_cost, admin_cost, implementation_cost) ~ regime,
  data = df,
  FUN = mean
)

write.csv(summary_table, file.path(tables, "r_nudge_policy_regime_summary.csv"), row.names = FALSE)
print(summary_table)
