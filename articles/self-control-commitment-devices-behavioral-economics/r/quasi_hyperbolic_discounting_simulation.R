set.seed(1414)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
n_periods <- 36

agents <- data.frame(
  agent_id = 1:n_agents,
  beta = runif(n_agents, 0.55, 1.00),
  delta = runif(n_agents, 0.94, 0.99),
  income = runif(n_agents, 1800, 5200),
  sophistication = runif(n_agents, 0.20, 1.00),
  liquidity_need = runif(n_agents, 0.05, 0.35),
  emergency_risk = runif(n_agents, 0.02, 0.18)
)

simulate_commitment_regime <- function(regime_name, commitment_cost, automation_strength, flexibility) {
  history <- vector("list", n_periods)
  accumulated_savings <- rep(0, n_agents)

  for (t in seq_len(n_periods)) {
    income_t <- agents$income * runif(n_agents, 0.90, 1.10)
    temptation <- runif(n_agents, 200, 1400)
    emergency_shock <- rbinom(n_agents, 1, agents$emergency_risk)
    emergency_cost <- emergency_shock * runif(n_agents, 400, 1800)

    planned_savings <- 0.12 * income_t
    automated_savings <- automation_strength * planned_savings
    discretionary_savings <- (1 - automation_strength) * planned_savings

    future_value_weight <- agents$beta * (agents$delta ^ (n_periods - t))
    utility_stick <- future_value_weight * planned_savings + automation_strength * agents$sophistication * 150
    utility_deviate <- temptation - commitment_cost
    hardship_access <- emergency_shock * flexibility * emergency_cost

    actual_savings <- ifelse(
      utility_stick + hardship_access >= utility_deviate,
      automated_savings + discretionary_savings,
      automated_savings * flexibility
    )

    withdrawal <- pmin(accumulated_savings, emergency_cost * flexibility)
    accumulated_savings <- accumulated_savings + actual_savings - withdrawal

    welfare <- accumulated_savings * 0.01 +
      actual_savings * 0.05 +
      flexibility * hardship_access * 0.002 -
      emergency_shock * (1 - flexibility) * 3.0 -
      commitment_cost * 0.0005

    history[[t]] <- data.frame(
      period = t,
      agent_id = agents$agent_id,
      regime = regime_name,
      beta = agents$beta,
      sophistication = agents$sophistication,
      liquidity_need = agents$liquidity_need,
      emergency_shock = emergency_shock,
      emergency_cost = emergency_cost,
      planned_savings = planned_savings,
      actual_savings = actual_savings,
      withdrawal = withdrawal,
      accumulated_savings = accumulated_savings,
      welfare = welfare,
      commitment_cost = commitment_cost,
      automation_strength = automation_strength,
      flexibility = flexibility
    )
  }

  do.call(rbind, history)
}

panel <- rbind(
  simulate_commitment_regime("low_commitment", 100, 0.15, 0.90),
  simulate_commitment_regime("medium_commitment", 400, 0.55, 0.65),
  simulate_commitment_regime("high_commitment", 800, 0.85, 0.35)
)

final <- panel[panel$period == n_periods, ]

summary <- aggregate(
  cbind(accumulated_savings, actual_savings, withdrawal, welfare) ~ regime,
  data = final,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_commitment_savings_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_commitment_savings_regime_summary.csv"), row.names = FALSE)

print(summary)
