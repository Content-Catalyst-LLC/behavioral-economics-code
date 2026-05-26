root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_herd_market_experiment.csv"))

weights <- expand.grid(
  liquidity_weight = c(0.75, 1.00, 1.25),
  leverage_weight = c(0.75, 1.00, 1.25),
  social_signal_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_risk <- with(df,
    w$social_signal_weight * systemic_herding_risk +
      w$leverage_weight * leverage_pressure * abs(drawdown_from_peak) +
      (1 / w$liquidity_weight) * volatility_proxy
  )

  tmp <- cbind(df, alt_systemic_risk = alt_risk)
  means <- aggregate(alt_systemic_risk ~ regime, data = tmp, FUN = mean)

  means$liquidity_weight <- w$liquidity_weight
  means$leverage_weight <- w$leverage_weight
  means$social_signal_weight <- w$social_signal_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_herd_market_systemic_risk_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
