root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_trust_cooperation_experiment.csv"))

weights <- expand.grid(
  betrayal_loss_weight = c(0.75, 1.00, 1.25),
  monitoring_cost_weight = c(0.75, 1.00, 1.25),
  transaction_cost_reduction_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]
  alt <- with(df,
    cooperative_benefit +
      w$transaction_cost_reduction_weight * transaction_cost_reduction +
      punishment_value -
      w$betrayal_loss_weight * betrayal_loss -
      w$monitoring_cost_weight * monitoring_cost -
      institutional_cost
  )
  tmp <- cbind(df, alt_total_welfare = alt)
  means <- aggregate(alt_total_welfare ~ regime, data = tmp, FUN = mean)
  means$betrayal_loss_weight <- w$betrayal_loss_weight
  means$monitoring_cost_weight <- w$monitoring_cost_weight
  means$transaction_cost_reduction_weight <- w$transaction_cost_reduction_weight
  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_trust_cooperation_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
