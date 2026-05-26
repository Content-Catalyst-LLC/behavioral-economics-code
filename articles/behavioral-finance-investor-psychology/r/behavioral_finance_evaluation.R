root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_behavioral_finance_experiment.csv"))

outcomes <- c(
  "absolute_mispricing",
  "mispricing",
  "mean_trade_intensity",
  "mean_buy_rate",
  "trading_cost_drag",
  "drawdown_from_peak"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ medium_behavioral_treat + high_behavioral_treat + trading_friction + platform_salience"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("medium_behavioral_treat", "high_behavioral_treat")) {
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
write.csv(results, file.path(regression, "r_behavioral_finance_estimates.csv"), row.names = FALSE)
print(results)
