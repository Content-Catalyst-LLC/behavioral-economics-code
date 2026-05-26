root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_herd_market_experiment.csv"))

outcomes <- c(
  "price",
  "price_deviation",
  "buy_rate",
  "volatility_proxy",
  "drawdown_from_peak",
  "systemic_herding_risk"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ moderate_herding_treat + high_herding_treat + liquidity_depth + leverage_pressure + social_media_intensity + post_shock"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("moderate_herding_treat", "high_herding_treat")) {
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
write.csv(results, file.path(regression, "r_herd_market_estimates.csv"), row.names = FALSE)
print(results)
