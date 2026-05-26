root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_framing_effects_panel.csv"))

outcomes <- c(
  "choose_risky",
  "welfare_proxy",
  "comprehension",
  "adjusted_risky_value"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ loss_frame_treat + balanced_frame_treat + loss_aversion + curvature + numeracy + trust + decision_fatigue + frame_strength + disclosure_quality + salience"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("loss_frame_treat", "balanced_frame_treat")) {
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
write.csv(results, file.path(regression, "r_framing_effects_estimates.csv"), row.names = FALSE)
print(results)
