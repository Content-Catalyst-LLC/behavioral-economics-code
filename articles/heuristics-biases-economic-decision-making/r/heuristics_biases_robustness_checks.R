root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_heuristics_biases_panel.csv"))

weights <- expand.grid(
  accuracy_weight = c(0.75, 1.00, 1.25),
  comprehension_weight = c(0.75, 1.00, 1.25),
  burden_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    welfare_proxy -
      w$accuracy_weight * absolute_error +
      w$comprehension_weight * correction_capacity * 0.08 -
      w$burden_weight * cognitive_load * 0.08
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ regime, data = tmp, FUN = mean)

  means$accuracy_weight <- w$accuracy_weight
  means$comprehension_weight <- w$comprehension_weight
  means$burden_weight <- w$burden_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_heuristics_biases_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
