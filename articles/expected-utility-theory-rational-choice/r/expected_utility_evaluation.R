root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_expected_utility_panel.csv"))

outcomes <- c(
  "choose_risky_eu",
  "observed_choose_risky",
  "certainty_equivalent_payoff",
  "risk_premium"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ medium_risk_aversion_treat + high_risk_aversion_treat + wealth + rho + numeracy + liquidity_constraint + trust"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("medium_risk_aversion_treat", "high_risk_aversion_treat", "rho", "wealth", "numeracy", "liquidity_constraint", "trust")) {
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
write.csv(results, file.path(regression, "r_expected_utility_estimates.csv"), row.names = FALSE)
print(results)
