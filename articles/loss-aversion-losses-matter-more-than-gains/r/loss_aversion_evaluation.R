root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_loss_aversion_panel.csv"))

outcomes <- c("choose_risky", "risky_value")

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ loss_frame_treat + mixed_gamble_treat + lambda_loss + alpha_gain + beta_loss + numeracy + income_security + prior_loss_exposure + trust"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("loss_frame_treat", "mixed_gamble_treat", "lambda_loss", "alpha_gain", "beta_loss", "numeracy", "income_security", "prior_loss_exposure", "trust")) {
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
write.csv(results, file.path(regression, "r_loss_aversion_estimates.csv"), row.names = FALSE)
print(results)
