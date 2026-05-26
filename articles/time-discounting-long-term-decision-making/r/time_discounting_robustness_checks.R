root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_time_discounting_experiment.csv"))

weights <- expand.grid(
  support_weight = c(0.75, 1.00, 1.25),
  flexibility_weight = c(0.75, 1.00, 1.25),
  future_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    cumulative_welfare +
      w$support_weight * commitment_support * sophistication * 100 +
      w$future_weight * future_goal_value * choose_delayed -
      w$flexibility_weight * (1 - flexibility) * liquidity_need * 600
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ regime, data = tmp, FUN = mean)

  means$support_weight <- w$support_weight
  means$flexibility_weight <- w$flexibility_weight
  means$future_weight <- w$future_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_time_discounting_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
