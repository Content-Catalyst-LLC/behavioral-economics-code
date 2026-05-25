# Future of Behavioral Economics in Governance and Policy
# R workflow: compliance under friction, salience, and trust
# Synthetic data only. This is a research-scaffolding example.

set.seed(123)

root <- normalizePath(getwd(), mustWork = FALSE)
output_tables <- file.path(root, "outputs", "tables")
processed <- file.path(root, "data", "processed")
dir.create(output_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(processed, recursive = TRUE, showWarnings = FALSE)

n <- 8000

agents <- data.frame(
  trust = pmin(pmax(rnorm(n, 0.55, 0.20), 0), 1),
  salience = pmin(pmax(rnorm(n, 0.50, 0.18), 0), 1),
  norm_sensitivity = pmin(pmax(rnorm(n, 0.45, 0.20), 0), 1),
  burden_sensitivity = pmin(pmax(rnorm(n, 0.60, 0.16), 0), 1),
  present_bias = pmin(pmax(rbeta(n, 2, 4), 0.05), 0.99)
)

policy_grid <- expand.grid(
  admin_burden = c(0.10, 0.25, 0.40),
  reminder_salience = c(0.20, 0.50, 0.80),
  trust_signal = c(0.30, 0.60, 0.85),
  penalty_strength = c(0.20, 0.50, 0.80)
)

simulate_compliance <- function(
  df,
  admin_burden,
  reminder_salience,
  trust_signal,
  penalty_strength
) {
  perceived_benefit <- 0.8 * reminder_salience * df$salience
  social_component <- 0.7 * df$norm_sensitivity
  trust_component <- 1.0 * trust_signal * df$trust
  burden_component <- 1.2 * admin_burden * df$burden_sensitivity
  present_bias_cost <- 0.7 * df$present_bias * admin_burden
  enforcement_component <- 0.9 * penalty_strength

  utility_compliance <- perceived_benefit +
    social_component +
    trust_component +
    enforcement_component -
    burden_component -
    present_bias_cost

  p_compliance <- plogis(utility_compliance - 0.5)
  compliance_draw <- rbinom(length(p_compliance), 1, p_compliance)

  data.frame(
    compliance_probability = p_compliance,
    complied = compliance_draw
  )
}

results_list <- vector("list", nrow(policy_grid))

for (i in seq_len(nrow(policy_grid))) {
  g <- policy_grid[i, ]

  sim <- simulate_compliance(
    agents,
    admin_burden = g$admin_burden,
    reminder_salience = g$reminder_salience,
    trust_signal = g$trust_signal,
    penalty_strength = g$penalty_strength
  )

  results_list[[i]] <- data.frame(
    admin_burden = g$admin_burden,
    reminder_salience = g$reminder_salience,
    trust_signal = g$trust_signal,
    penalty_strength = g$penalty_strength,
    mean_compliance_prob = mean(sim$compliance_probability),
    realized_compliance_rate = mean(sim$complied)
  )
}

results <- do.call(rbind, results_list)
results <- results[order(-results$realized_compliance_rate), ]

write.csv(results, file.path(output_tables, "r_compliance_policy_grid.csv"), row.names = FALSE)
print(head(results, 15))

if (requireNamespace("dplyr", quietly = TRUE)) {
  library(dplyr)

  comparison <- results %>%
    group_by(admin_burden, penalty_strength) %>%
    summarize(
      avg_compliance = mean(realized_compliance_rate),
      .groups = "drop"
    ) %>%
    arrange(desc(avg_compliance))

  write.csv(comparison, file.path(output_tables, "r_burden_penalty_comparison.csv"), row.names = FALSE)
  print(comparison)
}
