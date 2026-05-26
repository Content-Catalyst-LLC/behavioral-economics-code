# Nudge policy welfare robustness checks in R
# Synthetic economist-facing workflow.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_nudge_policy_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_nudge_policy_panel.py first.")
}

df <- read.csv(data_path)

weights <- expand.grid(
  user_benefit_weight = c(0.75, 1.00, 1.25),
  social_benefit_weight = c(0.60, 1.00, 1.40),
  burden_cost_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(
    df,
    utility +
      w$user_benefit_weight * user_benefit +
      w$social_benefit_weight * social_benefit -
      w$burden_cost_weight * friction_cost -
      w$burden_cost_weight * admin_cost -
      implementation_cost
  )

  tmp <- cbind(df, alt_total_welfare = alt_welfare)
  means <- aggregate(alt_total_welfare ~ regime, data = tmp, FUN = mean)

  means$user_benefit_weight <- w$user_benefit_weight
  means$social_benefit_weight <- w$social_benefit_weight
  means$burden_cost_weight <- w$burden_cost_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_nudge_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
