root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_mental_accounting_household_panel.csv"))

weights <- expand.grid(
  debt_interest_rate = c(0.15, 0.22, 0.29),
  liquidity_weight = c(0.75, 1.00, 1.25),
  label_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_interest_cost <- df$remaining_debt * w$debt_interest_rate

  alt_resilience <- with(df,
    w$liquidity_weight * remaining_liquid_savings +
      emergency_reserve -
      remaining_debt -
      alt_interest_cost -
      w$label_weight * savings_label_strength * 50
  )

  tmp <- cbind(df, alt_interest_cost = alt_interest_cost, alt_resilience = alt_resilience)
  means <- aggregate(cbind(alt_interest_cost, alt_resilience) ~ regime, data = tmp, FUN = mean)

  means$debt_interest_rate <- w$debt_interest_rate
  means$liquidity_weight <- w$liquidity_weight
  means$label_weight <- w$label_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_mental_accounting_resilience_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
