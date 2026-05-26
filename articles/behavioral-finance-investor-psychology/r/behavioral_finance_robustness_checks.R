root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_behavioral_finance_market_history.csv"))

weights <- expand.grid(
  behavior_weight = c(0.75, 1.00, 1.25),
  friction_weight = c(0.75, 1.00, 1.25),
  salience_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_risk <- with(df,
    w$behavior_weight * absolute_mispricing +
      w$salience_weight * platform_salience * mean_trade_intensity +
      (1 / w$friction_weight) * trading_cost_drag * 100 +
      abs(drawdown_from_peak) * 10
  )

  tmp <- cbind(df, alt_behavioral_market_risk = alt_risk)
  means <- aggregate(alt_behavioral_market_risk ~ regime, data = tmp, FUN = mean)

  means$behavior_weight <- w$behavior_weight
  means$friction_weight <- w$friction_weight
  means$salience_weight <- w$salience_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_behavioral_finance_market_risk_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
