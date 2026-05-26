# Choice architecture robustness checks in R
# Synthetic economist-facing workflow.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_choice_architecture_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_choice_architecture_panel.py first.")
}

df <- read.csv(data_path)

weights <- expand.grid(
  cognitive_cost_weight = c(0.50, 1.00, 1.50),
  switching_cost_weight = c(0.50, 1.00, 1.50)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(
    df,
    realized_welfare -
      (w$cognitive_cost_weight - 1.0) * cognitive_cost -
      (w$switching_cost_weight - 1.0) * switching_cost
  )

  tmp <- cbind(df, alt_realized_welfare = alt_welfare)
  means <- aggregate(alt_realized_welfare ~ regime, data = tmp, FUN = mean)

  means$cognitive_cost_weight <- w$cognitive_cost_weight
  means$switching_cost_weight <- w$switching_cost_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_choice_architecture_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
