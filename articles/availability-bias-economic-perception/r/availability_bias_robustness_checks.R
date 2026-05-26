root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_availability_bias_panel.csv"))

weights <- expand.grid(
  calibration_weight = c(0.75, 1.00, 1.25),
  comprehension_weight = c(0.75, 1.00, 1.25),
  emotional_burden_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    welfare_proxy -
      w$calibration_weight * abs(calibration_error) +
      w$comprehension_weight * base_rate_disclosure * numeracy * 0.08 -
      w$emotional_burden_weight * emotional_intensity * availability_score * 0.06
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ regime, data = tmp, FUN = mean)

  means$calibration_weight <- w$calibration_weight
  means$comprehension_weight <- w$comprehension_weight
  means$emotional_burden_weight <- w$emotional_burden_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_availability_bias_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
