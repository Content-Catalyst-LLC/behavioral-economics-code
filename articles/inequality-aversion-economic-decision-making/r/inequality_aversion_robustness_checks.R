root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_inequality_aversion_experiment.csv"))

weights <- expand.grid(
  social_preference_weight = c(0.75, 1.00, 1.25),
  legitimacy_weight = c(0.50, 1.00, 1.50),
  rejection_cost_weight = c(0.50, 1.00, 1.50)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt <- with(df,
    self_payoff +
      w$social_preference_weight * social_preference_utility +
      w$legitimacy_weight * 0.35 * process_legitimacy +
      0.10 * support_redistribution -
      w$rejection_cost_weight * 0.20 * rejected
  )

  tmp <- cbind(df, alt_total_welfare = alt)
  means <- aggregate(alt_total_welfare ~ regime, data = tmp, FUN = mean)

  means$social_preference_weight <- w$social_preference_weight
  means$legitimacy_weight <- w$legitimacy_weight
  means$rejection_cost_weight <- w$rejection_cost_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_inequality_aversion_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
