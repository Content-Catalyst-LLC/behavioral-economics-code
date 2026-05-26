set.seed(1818)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500

agents <- data.frame(
  agent_id = 1:n_agents,
  switch_cost = runif(n_agents, 0.05, 0.45),
  loss_aversion = runif(n_agents, 1.00, 3.25),
  status_quo_premium = runif(n_agents, 0.02, 0.30),
  uncertainty_sensitivity = runif(n_agents, 0.05, 0.35),
  decision_fatigue = runif(n_agents, 0.00, 0.35),
  sophistication = runif(n_agents, 0.20, 1.00)
)

simulate_default_regime <- function(regime_name, default_shift, switching_support, disclosure_quality) {
  value_status_quo <- runif(n_agents, 0.45, 0.60)
  value_alternative <- value_status_quo + runif(n_agents, 0.02, 0.25)
  perceived_loss <- runif(n_agents, 0.02, 0.20)

  effective_switch_cost <- pmax(
    agents$switch_cost - switching_support * agents$sophistication * 0.20,
    0
  )

  effective_status_quo_premium <- pmax(
    agents$status_quo_premium +
      agents$decision_fatigue -
      default_shift * 0.18 -
      disclosure_quality * agents$sophistication * 0.12,
    0
  )

  effective_perceived_loss <- pmax(
    perceived_loss +
      agents$uncertainty_sensitivity -
      disclosure_quality * 0.10,
    0
  )

  utility_status_quo <- value_status_quo + effective_status_quo_premium

  utility_alternative <- value_alternative -
    effective_switch_cost -
    agents$loss_aversion * effective_perceived_loss

  choose_alternative <- as.integer(utility_alternative >= utility_status_quo)

  welfare <- ifelse(
    choose_alternative == 1,
    value_alternative - effective_switch_cost,
    value_status_quo
  )

  data.frame(
    agent_id = agents$agent_id,
    regime = regime_name,
    value_status_quo = value_status_quo,
    value_alternative = value_alternative,
    objective_gain = value_alternative - value_status_quo,
    switch_cost = agents$switch_cost,
    effective_switch_cost = effective_switch_cost,
    loss_aversion = agents$loss_aversion,
    status_quo_premium = agents$status_quo_premium,
    effective_status_quo_premium = effective_status_quo_premium,
    perceived_loss = perceived_loss,
    effective_perceived_loss = effective_perceived_loss,
    utility_status_quo = utility_status_quo,
    utility_alternative = utility_alternative,
    choose_alternative = choose_alternative,
    welfare = welfare,
    default_shift = default_shift,
    switching_support = switching_support,
    disclosure_quality = disclosure_quality
  )
}

panel <- rbind(
  simulate_default_regime("passive_status_quo_default", 0.00, 0.00, 0.10),
  simulate_default_regime("active_choice_with_disclosure", 0.35, 0.35, 0.55),
  simulate_default_regime("pro_switching_default_with_support", 0.75, 0.70, 0.80)
)

summary <- aggregate(
  cbind(choose_alternative, welfare, objective_gain, effective_switch_cost, effective_status_quo_premium) ~ regime,
  data = panel,
  FUN = mean
)

panel$switch_cost_quartile <- cut(
  panel$switch_cost,
  breaks = quantile(panel$switch_cost, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

heterogeneity <- aggregate(
  cbind(choose_alternative, welfare) ~ regime + switch_cost_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_status_quo_bias_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_status_quo_bias_regime_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_status_quo_bias_switching_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
