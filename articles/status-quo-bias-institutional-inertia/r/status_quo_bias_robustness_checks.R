root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_status_quo_bias_panel.csv"))

weights <- expand.grid(
  switching_weight = c(0.75, 1.00, 1.25),
  autonomy_weight = c(0.75, 1.00, 1.25),
  burden_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    welfare +
      w$autonomy_weight * disclosure_quality * sophistication * 0.10 -
      w$switching_weight * effective_switch_cost * 0.50 -
      w$burden_weight * decision_fatigue * 0.20
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ regime, data = tmp, FUN = mean)

  means$switching_weight <- w$switching_weight
  means$autonomy_weight <- w$autonomy_weight
  means$burden_weight <- w$burden_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_status_quo_bias_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
