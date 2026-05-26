set.seed(1717)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
n_periods <- 36

agents <- data.frame(
  agent_id = 1:n_agents,
  beta = runif(n_agents, 0.55, 1.00),
  delta = runif(n_agents, 0.93, 0.99),
  immediate_reward_base = runif(n_agents, 80, 190),
  future_goal_value = runif(n_agents, 140, 320),
  sophistication = runif(n_agents, 0.20, 1.00),
  liquidity_need = runif(n_agents, 0.05, 0.35)
)

simulate_discount_regime <- function(regime_name, use_present_bias, commitment_support, flexibility) {
  history <- vector("list", n_periods)
  cumulative_delayed_choices <- rep(0, n_agents)
  cumulative_welfare <- rep(0, n_agents)

  for (t in seq_len(n_periods)) {
    delayed_reward <- agents$future_goal_value * runif(n_agents, 0.80, 1.30)
    immediate_reward <- agents$immediate_reward_base * runif(n_agents, 0.85, 1.25)

    if (use_present_bias) {
      delayed_value <- agents$beta * (agents$delta ^ (n_periods - t)) * delayed_reward
    } else {
      delayed_value <- (agents$delta ^ (n_periods - t)) * delayed_reward
    }

    support_value <- commitment_support * agents$sophistication * 50
    flexibility_penalty <- agents$liquidity_need * (1 - flexibility) * 30

    immediate_value <- immediate_reward - support_value + flexibility_penalty
    choose_delayed <- as.integer(delayed_value >= immediate_value)

    period_welfare <- choose_delayed * delayed_reward -
      (1 - choose_delayed) * 0.20 * delayed_reward -
      flexibility_penalty

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
      immediate_reward = immediate_reward,
      delayed_value = delayed_value,
      immediate_value = immediate_value,
      choose_delayed = choose_delayed,
      period_welfare = period_welfare,
      cumulative_delayed_choices = cumulative_delayed_choices,
      cumulative_welfare = cumulative_welfare,
      commitment_support = commitment_support,
      flexibility = flexibility
    )
  }

  do.call(rbind, history)
}

panel <- rbind(
  simulate_discount_regime("exponential_discounting", FALSE, 0.00, 1.00),
  simulate_discount_regime("present_biased_discounting", TRUE, 0.00, 1.00),
  simulate_discount_regime("present_bias_with_commitment_support", TRUE, 0.70, 0.75)
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

write.csv(panel, file.path(tables, "r_time_discounting_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_time_discounting_regime_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_time_discounting_beta_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
