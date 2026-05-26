# Welfare robustness checks in R
# Synthetic economist-facing workflow.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_interface_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_interface_panel.py first.")
}

df <- read.csv(data_path)

weights <- expand.grid(
  autonomy_weight = c(0.3, 0.7, 1.1),
  privacy_weight = c(0.3, 0.7, 1.1),
  overload_weight = c(0.25, 0.45, 0.65)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(
    df,
    joined * (baseline_value + 0.35 * reward_intensity) -
      w$autonomy_weight * pmax(friction_asymmetry, 0) * autonomy_preference -
      w$privacy_weight * data_extraction_intensity * privacy_sensitivity * consented -
      w$overload_weight * cognitive_overload
  )

  tmp <- cbind(df, alt_user_welfare = alt_welfare)
  means <- aggregate(alt_user_welfare ~ regime, data = tmp, FUN = mean)

  means$autonomy_weight <- w$autonomy_weight
  means$privacy_weight <- w$privacy_weight
  means$overload_weight <- w$overload_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_welfare_weight_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
