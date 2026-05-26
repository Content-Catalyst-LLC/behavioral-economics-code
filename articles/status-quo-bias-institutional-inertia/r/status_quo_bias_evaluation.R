root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_status_quo_bias_panel.csv"))

outcomes <- c(
  "choose_alternative",
  "welfare",
  "effective_switch_cost",
  "effective_status_quo_premium",
  "effective_perceived_loss"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ active_choice_treat + pro_switching_treat + objective_gain + switch_cost + loss_aversion + status_quo_premium + uncertainty_sensitivity + decision_fatigue + sophistication + default_shift + switching_support + disclosure_quality"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("active_choice_treat", "pro_switching_treat")) {
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
write.csv(results, file.path(regression, "r_status_quo_bias_estimates.csv"), row.names = FALSE)
print(results)
