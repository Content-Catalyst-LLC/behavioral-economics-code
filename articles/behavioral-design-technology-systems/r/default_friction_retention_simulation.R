# Behavioral Design in Technology Systems
# R workflow: default effects, friction, and retention dynamics
# Synthetic data only. This is a research-scaffolding example.

set.seed(202)

root <- normalizePath(getwd(), mustWork = FALSE)
output_tables <- file.path(root, "outputs", "tables")
processed <- file.path(root, "data", "processed")
dir.create(output_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(processed, recursive = TRUE, showWarnings = FALSE)

n_users <- 7000

users <- data.frame(
  user_id = seq_len(n_users),
  baseline_value = rnorm(n_users, mean = 0.45, sd = 0.18),
  salience_sensitivity = pmin(pmax(rnorm(n_users, 0.55, 0.18), 0), 1),
  default_sensitivity = pmin(pmax(rnorm(n_users, 0.50, 0.20), 0), 1),
  friction_sensitivity = pmin(pmax(rnorm(n_users, 0.60, 0.16), 0), 1),
  reward_sensitivity = pmin(pmax(rnorm(n_users, 0.58, 0.17), 0), 1),
  cognitive_overload = pmin(pmax(rnorm(n_users, 0.42, 0.15), 0), 1),
  autonomy_preference = pmin(pmax(rnorm(n_users, 0.55, 0.18), 0), 1)
)

interface_grid <- expand.grid(
  salience = c(0.25, 0.55, 0.85),
  default_on = c(0, 1),
  entry_friction = c(0.05, 0.15),
  exit_friction = c(0.10, 0.35, 0.60),
  reward_intensity = c(0.20, 0.50, 0.80)
)

simulate_retention <- function(
  df,
  salience,
  default_on,
  entry_friction,
  exit_friction,
  reward_intensity
) {
  join_score <- with(
    df,
    baseline_value +
      salience_sensitivity * salience +
      default_sensitivity * default_on -
      friction_sensitivity * entry_friction +
      reward_sensitivity * reward_intensity -
      cognitive_overload * 0.4
  )

  joined_prob <- plogis(join_score)
  joined <- rbinom(nrow(df), 1, joined_prob)

  stay_score <- with(
    df,
    baseline_value * 0.5 +
      reward_sensitivity * reward_intensity +
      default_sensitivity * default_on +
      friction_sensitivity * exit_friction -
      cognitive_overload * 0.35
  )

  retained_prob <- plogis(stay_score)
  retained <- ifelse(joined == 1, rbinom(nrow(df), 1, retained_prob), 0)

  friction_asymmetry <- exit_friction - entry_friction

  welfare <- with(
    df,
    joined * (baseline_value + 0.4 * reward_intensity) -
      0.8 * friction_asymmetry -
      0.5 * cognitive_overload -
      0.4 * autonomy_preference * max(friction_asymmetry, 0)
  )

  data.frame(
    joined_prob = joined_prob,
    retained_prob = retained_prob,
    joined = joined,
    retained = retained,
    welfare = welfare
  )
}

results_list <- vector("list", nrow(interface_grid))

for (i in seq_len(nrow(interface_grid))) {
  g <- interface_grid[i, ]

  sim <- simulate_retention(
    users,
    salience = g$salience,
    default_on = g$default_on,
    entry_friction = g$entry_friction,
    exit_friction = g$exit_friction,
    reward_intensity = g$reward_intensity
  )

  results_list[[i]] <- data.frame(
    salience = g$salience,
    default_on = g$default_on,
    entry_friction = g$entry_friction,
    exit_friction = g$exit_friction,
    reward_intensity = g$reward_intensity,
    join_rate = mean(sim$joined),
    retention_rate = mean(sim$retained),
    mean_welfare = mean(sim$welfare)
  )
}

results <- do.call(rbind, results_list)

results$friction_asymmetry <- results$exit_friction - results$entry_friction
results$possible_dark_pattern <- ifelse(
  results$friction_asymmetry > 0.25 & results$default_on == 1,
  1,
  0
)

results_by_retention <- results[order(-results$retention_rate), ]
print(head(results_by_retention, 15))

dark_pattern_summary <- aggregate(
  cbind(join_rate, retention_rate, mean_welfare) ~ possible_dark_pattern,
  data = results,
  FUN = mean
)

print(dark_pattern_summary)

welfare_ranked <- results[order(-results$mean_welfare), ]
print(head(welfare_ranked, 15))

write.csv(results, file.path(output_tables, "interface_design_simulation_results.csv"), row.names = FALSE)
write.csv(dark_pattern_summary, file.path(output_tables, "dark_pattern_summary.csv"), row.names = FALSE)
