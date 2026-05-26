set.seed(1616)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
n_periods <- 36

agents <- data.frame(
  agent_id = 1:n_agents,
  beta = runif(n_agents, 0.50, 1.00),
  delta = runif(n_agents, 0.94, 0.99),
  temptation_strength = runif(n_agents, 50, 260),
  sophistication = runif(n_agents, 0.20, 1.00),
  liquidity_need = runif(n_agents, 0.05, 0.35),
  future_goal_value = runif(n_agents, 150, 420)
)

simulate_commitment_regime <- function(regime_name, commitment_cost, reminder_strength, flexibility) {
  history <- vector("list", n_periods)
  cumulative_delayed_choices <- rep(0, n_agents)
  cumulative_welfare <- rep(0, n_agents)

  for (t in seq_len(n_periods)) {
    delayed_reward <- agents$future_goal_value * runif(n_agents, 0.80, 1.25)
    immediate_temptation <- agents$temptation_strength * runif(n_agents, 0.80, 1.30)

    discounted_delayed_value <- agents$beta * (agents$delta ^ (n_periods - t)) * delayed_reward
    commitment_support <- commitment_cost + reminder_strength * agents$sophistication * 40
    hardship_adjustment <- agents$liquidity_need * (1 - flexibility) * 25

    immediate_value <- immediate_temptation - commitment_support + hardship_adjustment
    choose_delayed <- as.integer(discounted_delayed_value >= immediate_value)

    period_welfare <- choose_delayed * delayed_reward -
      (1 - choose_delayed) * 0.25 * delayed_reward -
      hardship_adjustment

    cumulative_delayed_choices <- cumulative_delayed_choices + choose_delayed
    cumulative_welfare <- cumulative_welfare + period_welfare

    history[[t]] <- data.frame(
      period = t,
      agent_id = agents$agent_id,
      regime = regime_name,
      beta = agents$beta,
      delta = agents$delta,
      sophistication = agents$sophistication,
      liquidity_need = agents$liquidity_need,
      delayed_reward = delayed_reward,
      immediate_temptation = immediate_temptation,
      discounted_delayed_value = discounted_delayed_value,
      immediate_value = immediate_value,
      choose_delayed = choose_delayed,
      period_welfare = period_welfare,
      cumulative_delayed_choices = cumulative_delayed_choices,
      cumulative_welfare = cumulative_welfare,
      commitment_cost = commitment_cost,
      reminder_strength = reminder_strength,
      flexibility = flexibility
    )
  }

  do.call(rbind, history)
}

panel <- rbind(
  simulate_commitment_regime("weak_commitment", 20, 0.10, 0.95),
  simulate_commitment_regime("medium_commitment", 70, 0.45, 0.75),
  simulate_commitment_regime("strong_commitment", 140, 0.80, 0.55)
)

final <- panel[panel$period == n_periods, ]

summary <- aggregate(
  cbind(choose_delayed, cumulative_delayed_choices, cumulative_welfare) ~ regime,
  data = final,
  FUN = mean
)

final$beta_quartile <- cut(
  final$beta,
  breaks = quantile(final$beta, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

heterogeneity <- aggregate(
  cbind(choose_delayed, cumulative_delayed_choices, cumulative_welfare) ~ regime + beta_quartile,
  data = final,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_present_bias_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_present_bias_regime_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_present_bias_beta_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
