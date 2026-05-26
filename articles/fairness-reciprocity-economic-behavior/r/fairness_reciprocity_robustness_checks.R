root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_fairness_reciprocity_experiment.csv"))

weights <- expand.grid(
  process_weight = c(0.75, 1.00, 1.25),
  rejection_cost_weight = c(0.50, 1.00, 1.50),
  punishment_cost_weight = c(0.50, 1.00, 1.50)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt <- with(df,
    fairness_reciprocity_utility +
      w$process_weight * 0.25 * process_fairness +
      0.15 * cooperated -
      w$rejection_cost_weight * 0.20 * rejected -
      w$punishment_cost_weight * 0.10 * punished
  )

  tmp <- cbind(df, alt_total_welfare = alt)
  means <- aggregate(alt_total_welfare ~ regime, data = tmp, FUN = mean)

  means$process_weight <- w$process_weight
  means$rejection_cost_weight <- w$rejection_cost_weight
  means$punishment_cost_weight <- w$punishment_cost_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_fairness_reciprocity_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
