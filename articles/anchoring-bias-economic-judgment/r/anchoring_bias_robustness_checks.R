root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_anchoring_bias_panel.csv"))

weights <- expand.grid(
  accuracy_weight = c(0.75, 1.00, 1.25),
  autonomy_weight = c(0.75, 1.00, 1.25),
  burden_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    welfare_proxy -
      w$accuracy_weight * absolute_error / 100 +
      w$autonomy_weight * disclosure_quality * counter_anchor_support * 0.08 -
      w$burden_weight * cognitive_load * 0.08
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ regime, data = tmp, FUN = mean)

  means$accuracy_weight <- w$accuracy_weight
  means$autonomy_weight <- w$autonomy_weight
  means$burden_weight <- w$burden_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_anchoring_bias_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
