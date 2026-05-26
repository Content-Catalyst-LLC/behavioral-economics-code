# Regulatory welfare robustness checks in R
# Synthetic economist-facing workflow.

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

data_path <- file.path(tables, "synthetic_regulatory_policy_experiment.csv")

if (!file.exists(data_path)) {
  stop("Synthetic experiment data not found. Run python/generate_synthetic_regulatory_policy_panel.py first.")
}

df <- read.csv(data_path)

weights <- expand.grid(
  social_benefit_weight = c(0.60, 0.90, 1.20),
  admin_cost_weight = c(0.50, 1.00, 1.50),
  enforcement_cost_weight = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(
    df,
    utility_compliance +
      w$social_benefit_weight * social_benefit -
      compliance_cost -
      w$admin_cost_weight * administrative_cost -
      w$enforcement_cost_weight * enforcement_cost
  )

  tmp <- cbind(df, alt_total_welfare = alt_welfare)
  means <- aggregate(alt_total_welfare ~ regime, data = tmp, FUN = mean)

  means$social_benefit_weight <- w$social_benefit_weight
  means$admin_cost_weight <- w$admin_cost_weight
  means$enforcement_cost_weight <- w$enforcement_cost_weight

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_regulatory_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
