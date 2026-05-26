root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
regression <- file.path(root, "outputs", "regression_tables")
dir.create(regression, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_mental_accounting_household_panel.csv"))

outcomes <- c(
  "windfall_consumption",
  "total_debt_payment",
  "remaining_debt",
  "remaining_liquid_savings",
  "inefficiency_gap",
  "annual_interest_cost",
  "resilience_index"
)

rows <- list()

for (outcome in outcomes) {
  formula <- as.formula(paste(
    outcome,
    "~ integrated_prompt_treat + unified_money_treat + monthly_income + liquid_savings + credit_card_debt + windfall + savings_label_strength + emergency_need_risk + present_bias"
  ))

  model <- lm(formula, data = df)
  coefs <- summary(model)$coefficients

  for (term in c("integrated_prompt_treat", "unified_money_treat")) {
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
write.csv(results, file.path(regression, "r_mental_accounting_estimates.csv"), row.names = FALSE)
print(results)
