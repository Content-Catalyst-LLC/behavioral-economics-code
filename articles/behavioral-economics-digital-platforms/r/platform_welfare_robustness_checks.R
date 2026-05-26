# Platform welfare robustness checks in R
# Synthetic economist-facing workflow.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_platform_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_platform_panel.py first.")
}

df <- read.csv(data_path)

weights <- expand.grid(
  privacy_weight = c(0.25, 0.45, 0.75),
  overload_weight = c(0.15, 0.30, 0.50),
  friction_weight = c(0.05, 0.15, 0.30)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(
    df,
    clicked * exposure_quality -
      w$overload_weight * cognitive_overload -
      w$privacy_weight * privacy_sensitivity * data_extraction_intensity * consented -
      w$friction_weight * friction
  )

  tmp <- cbind(df, alt_user_welfare = alt_welfare)
  means <- aggregate(alt_user_welfare ~ regime, data = tmp, FUN = mean)

  means$privacy_weight <- w$privacy_weight
  means$overload_weight <- w$overload_weight
  means$friction_weight <- w$friction_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_platform_welfare_weight_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
