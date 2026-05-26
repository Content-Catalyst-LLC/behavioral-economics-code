set.seed(2323)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500

agents <- data.frame(
  agent_id = 1:n_agents,
  wealth = runif(n_agents, 5000, 100000),
  rho = runif(n_agents, 0.10, 3.00),
  numeracy = runif(n_agents, 0.20, 1.00),
  liquidity_constraint = runif(n_agents, 0.00, 0.50),
  trust = runif(n_agents, 0.20, 1.00)
)

crra_utility <- function(x, rho) {
  ifelse(
    abs(rho - 1) < 1e-8,
    log(x),
    (x^(1 - rho)) / (1 - rho)
  )
}

inverse_crra_utility <- function(u, rho) {
  ifelse(
    abs(rho - 1) < 1e-8,
    exp(u),
    (u * (1 - rho))^(1 / (1 - rho))
  )
}

evaluate_agent <- function(wealth, rho, numeracy, liquidity_constraint, trust) {
  payoff_a <- 100
  payoff_b_low <- 40
  payoff_b_high <- 220

  eu_a <- crra_utility(wealth + payoff_a, rho)
  eu_b <- 0.5 * crra_utility(wealth + payoff_b_low, rho) +
    0.5 * crra_utility(wealth + payoff_b_high, rho)

  expected_value_b <- 0.5 * payoff_b_low + 0.5 * payoff_b_high

  certainty_equivalent_total_wealth <- inverse_crra_utility(eu_b, rho)
  certainty_equivalent_payoff <- certainty_equivalent_total_wealth - wealth
  risk_premium <- expected_value_b - certainty_equivalent_payoff

  choose_risky <- as.integer(eu_b > eu_a)

  observed_choose_risky <- as.integer(
    choose_risky == 1 &&
      liquidity_constraint < 0.45 &&
      numeracy > 0.25 &&
      trust > 0.30
  )

  data.frame(
    eu_certain = eu_a,
    eu_risky = eu_b,
    expected_value_risky = expected_value_b,
    certainty_equivalent_payoff = certainty_equivalent_payoff,
    risk_premium = risk_premium,
    choose_risky = choose_risky,
    observed_choose_risky = observed_choose_risky
  )
}

rows <- list()

for (i in 1:n_agents) {
  result <- evaluate_agent(
    wealth = agents$wealth[i],
    rho = agents$rho[i],
    numeracy = agents$numeracy[i],
    liquidity_constraint = agents$liquidity_constraint[i],
    trust = agents$trust[i]
  )

  rows[[i]] <- cbind(agents[i, ], result)
}

panel <- do.call(rbind, rows)

summary_stats <- data.frame(
  agents = nrow(panel),
  mean_rho = mean(panel$rho),
  mean_wealth = mean(panel$wealth),
  share_choose_risky_eu = mean(panel$choose_risky),
  share_choose_risky_observed = mean(panel$observed_choose_risky),
  mean_certainty_equivalent = mean(panel$certainty_equivalent_payoff),
  mean_risk_premium = mean(panel$risk_premium)
)

panel$rho_quartile <- cut(
  panel$rho,
  breaks = quantile(panel$rho, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

risk_aversion_summary <- aggregate(
  cbind(choose_risky, observed_choose_risky, certainty_equivalent_payoff, risk_premium) ~ rho_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_expected_utility_panel.csv"), row.names = FALSE)
write.csv(summary_stats, file.path(tables, "r_expected_utility_summary.csv"), row.names = FALSE)
write.csv(risk_aversion_summary, file.path(tables, "r_expected_utility_risk_aversion_summary.csv"), row.names = FALSE)

print(summary_stats)
print(risk_aversion_summary)
