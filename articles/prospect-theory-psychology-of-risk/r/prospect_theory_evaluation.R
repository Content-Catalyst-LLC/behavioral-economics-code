root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_prospect_theory_panel.csv"))

outcomes <- c(
  "choose_risky_pt",
  "choose_risky_eu",
  "pt_eu_disagreement",
  "pt_risky_value"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ loss_frame_treat + mixed_gamble_treat + lambda_loss + alpha_gain + beta_loss + gamma_weight + rho_crra + wealth + numeracy + income_security + trust + prior_loss_exposure"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("loss_frame_treat", "mixed_gamble_treat", "lambda_loss", "alpha_gain", "beta_loss", "gamma_weight", "rho_crra", "wealth", "numeracy", "income_security", "trust", "prior_loss_exposure")) {
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
write.csv(results, file.path(regression, "r_prospect_theory_estimates.csv"), row.names = FALSE)
print(results)
