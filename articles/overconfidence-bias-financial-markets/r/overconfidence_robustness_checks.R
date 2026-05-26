root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_overconfidence_investor_panel.csv"))

weights <- expand.grid(
  friction_weight = c(0.75, 1.00, 1.25),
  leverage_weight = c(0.75, 1.00, 1.25),
  success_feedback_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_behavioral_cost <- with(df,
    w$friction_weight * trading_cost +
      w$leverage_weight * leverage_access * abs(realized_return) * 0.05 +
      w$success_feedback_weight * prior_success_sensitivity * pmax(rolling_success, 0) * 0.01
  )

  tmp <- cbind(df, alt_behavioral_cost = alt_behavioral_cost)
  means <- aggregate(alt_behavioral_cost ~ regime, data = tmp, FUN = mean)

  means$friction_weight <- w$friction_weight
  means$leverage_weight <- w$leverage_weight
  means$success_feedback_weight <- w$success_feedback_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_overconfidence_behavioral_cost_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
