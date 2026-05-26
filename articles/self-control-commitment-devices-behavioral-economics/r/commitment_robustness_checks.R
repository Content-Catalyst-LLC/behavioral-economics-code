root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_commitment_savings_experiment.csv"))

weights <- expand.grid(
  commitment_weight = c(0.75, 1.00, 1.25),
  automation_weight = c(0.75, 1.00, 1.25),
  flexibility_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    accumulated_savings * 0.01 +
      w$automation_weight * actual_savings * 0.05 +
      w$flexibility_weight * flexibility * emergency_cost * 0.002 -
      w$commitment_weight * commitment_cost * 0.0005 -
      (1 - flexibility) * liquidity_need * 50
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ regime, data = tmp, FUN = mean)

  means$commitment_weight <- w$commitment_weight
  means$automation_weight <- w$automation_weight
  means$flexibility_weight <- w$flexibility_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_commitment_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
