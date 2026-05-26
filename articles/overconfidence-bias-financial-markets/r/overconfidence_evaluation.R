root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_overconfidence_experiment.csv"))

outcomes <- c(
  "mean_trade_intensity",
  "mean_trading_cost",
  "mean_gross_position_return",
  "mean_realized_return",
  "volatility_proxy",
  "mean_abs_perceived_signal",
  "portfolio_drag"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ moderate_overconfidence_treat + high_overconfidence_treat + trading_friction + leverage_access"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("moderate_overconfidence_treat", "high_overconfidence_treat")) {
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
write.csv(results, file.path(regression, "r_overconfidence_estimates.csv"), row.names = FALSE)
print(results)
