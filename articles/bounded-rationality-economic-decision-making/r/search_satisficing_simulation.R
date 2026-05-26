set.seed(2626)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 3000
n_options <- 30

agents <- data.frame(
  agent_id = 1:n_agents,
  aspiration = runif(n_agents, 0.55, 0.85),
  search_cost = runif(n_agents, 0.003, 0.035),
  time_budget = runif(n_agents, 8, 30),
  cognitive_capacity = runif(n_agents, 6, 25),
  numeracy = runif(n_agents, 0.20, 1.00),
  stress = runif(n_agents, 0.00, 0.70)
)

simulate_agent <- function(agent_row, regime) {
  option_values <- runif(n_options, 0, 1)
  option_loads <- runif(n_options, 0.50, 2.00)
  option_times <- runif(n_options, 0.50, 1.50)

  if (regime == "low_constraint") {
    search_multiplier <- 0.75
    load_multiplier <- 0.75
  } else if (regime == "medium_constraint") {
    search_multiplier <- 1.00
    load_multiplier <- 1.00
  } else {
    search_multiplier <- 1.35
    load_multiplier <- 1.35
  }

  adjusted_search_cost <- agent_row$search_cost * search_multiplier * (1 + agent_row$stress)
  adjusted_capacity <- agent_row$cognitive_capacity / load_multiplier
  adjusted_time_budget <- agent_row$time_budget / search_multiplier

  optimal_value <- max(option_values)

  chosen_index <- NA
  chosen_value <- NA
  cumulative_time <- 0
  cumulative_load <- 0

  for (j in 1:n_options) {
    cumulative_time <- cumulative_time + option_times[j]
    cumulative_load <- cumulative_load + option_loads[j]

    if (cumulative_time > adjusted_time_budget || cumulative_load > adjusted_capacity) {
      chosen_index <- max(1, j - 1)
      chosen_value <- option_values[chosen_index]
      break
    }

    if (option_values[j] >= agent_row$aspiration) {
      chosen_index <- j
      chosen_value <- option_values[j]
      break
    }
  }

  if (is.na(chosen_index)) {
    chosen_index <- n_options
    chosen_value <- option_values[n_options]
    cumulative_time <- sum(option_times)
    cumulative_load <- sum(option_loads)
  }

  net_value <- chosen_value - adjusted_search_cost * chosen_index
  optimization_gap <- optimal_value - chosen_value

  data.frame(
    regime = regime,
    agent_id = agent_row$agent_id,
    aspiration = agent_row$aspiration,
    search_cost = agent_row$search_cost,
    time_budget = agent_row$time_budget,
    cognitive_capacity = agent_row$cognitive_capacity,
    numeracy = agent_row$numeracy,
    stress = agent_row$stress,
    chosen_index = chosen_index,
    chosen_value = chosen_value,
    optimal_value = optimal_value,
    net_value = net_value,
    optimization_gap = optimization_gap,
    cumulative_time = cumulative_time,
    cumulative_load = cumulative_load
  )
}

regimes <- c("low_constraint", "medium_constraint", "high_constraint")
rows <- list()
counter <- 1

for (regime in regimes) {
  for (i in 1:n_agents) {
    rows[[counter]] <- simulate_agent(agents[i, ], regime)
    counter <- counter + 1
  }
}

panel <- do.call(rbind, rows)

regime_summary <- aggregate(
  cbind(chosen_value, optimal_value, net_value, optimization_gap, chosen_index) ~ regime,
  data = panel,
  FUN = mean
)

panel$aspiration_quartile <- cut(
  panel$aspiration,
  breaks = quantile(panel$aspiration, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

aspiration_summary <- aggregate(
  cbind(chosen_value, net_value, optimization_gap, chosen_index) ~ regime + aspiration_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_bounded_rationality_panel.csv"), row.names = FALSE)
write.csv(regime_summary, file.path(tables, "r_bounded_rationality_regime_summary.csv"), row.names = FALSE)
write.csv(aspiration_summary, file.path(tables, "r_bounded_rationality_aspiration_heterogeneity.csv"), row.names = FALSE)

print(regime_summary)
print(aspiration_summary)
