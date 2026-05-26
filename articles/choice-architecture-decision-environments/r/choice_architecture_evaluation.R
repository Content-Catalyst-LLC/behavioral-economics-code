# Choice architecture policy evaluation in R
# Synthetic economist-facing workflow for decision environments.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_choice_architecture_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_choice_architecture_panel.py first.")
}

df <- read.csv(data_path)

outcomes <- c(
  "realized_welfare",
  "chosen_utility",
  "selected_default",
  "selected_high_value_option",
  "cognitive_cost",
  "switching_cost"
)

estimate_rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(
    paste(
      outcome,
      "~ default_heavy_treat + guided_design_treat + default_sensitivity + salience_sensitivity + framing_sensitivity + complexity_sensitivity + switching_cost_sensitivity + digital_literacy + institutional_trust"
    )
  )

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("default_heavy_treat", "guided_design_treat")) {
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
write.csv(results, file.path(regression, "r_choice_architecture_estimates.csv"), row.names = FALSE)
print(results)

summary_table <- aggregate(
  cbind(realized_welfare, chosen_utility, selected_default, selected_high_value_option, cognitive_cost, switching_cost) ~ regime,
  data = df,
  FUN = mean
)

write.csv(summary_table, file.path(tables, "r_choice_architecture_regime_summary.csv"), row.names = FALSE)
print(summary_table)
