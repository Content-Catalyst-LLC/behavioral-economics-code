set.seed(2020)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
true_probability <- 0.12

agents <- data.frame(
  agent_id = 1:n_agents,
  availability_sensitivity = runif(n_agents, 0.10, 0.90),
  numeracy = runif(n_agents, 0.20, 1.00),
  trust_in_statistics = runif(n_agents, 0.20, 1.00),
  risk_tolerance = runif(n_agents, 0.10, 0.90),
  prior_experience = rbinom(n_agents, 1, 0.25)
)

simulate_availability_environment <- function(regime_name, salience_scale, base_rate_disclosure, emotional_intensity) {
  recency_signal <- runif(n_agents, 0, 1) * salience_scale
  vividness_signal <- runif(n_agents, 0, 1) * salience_scale
  media_signal <- runif(n_agents, 0, 1) * salience_scale
  social_repetition_signal <- runif(n_agents, 0, 1) * salience_scale

  availability_score <- 0.25 * recency_signal +
    0.25 * vividness_signal +
    0.25 * media_signal +
    0.25 * social_repetition_signal +
    0.20 * agents$prior_experience * emotional_intensity

  base_rate_correction <- base_rate_disclosure *
    agents$numeracy *
    agents$trust_in_statistics *
    0.18

  subjective_probability <- pmin(
    pmax(
      true_probability +
        agents$availability_sensitivity * availability_score * 0.25 -
        base_rate_correction,
      0
    ),
    1
  )

  calibration_error <- subjective_probability - true_probability

  participate_in_risky_asset <- as.integer(
    subjective_probability < (0.18 + agents$risk_tolerance * 0.12)
  )

  insurance_demand <- as.integer(
    subjective_probability > (0.16 - agents$prior_experience * 0.03)
  )

  policy_support <- as.integer(
    subjective_probability +
      0.10 * emotional_intensity +
      0.05 * agents$trust_in_statistics > 0.25
  )

  welfare_proxy <- 1 -
    abs(calibration_error) -
    0.08 * emotional_intensity * availability_score +
    0.05 * base_rate_disclosure * agents$numeracy

  data.frame(
    agent_id = agents$agent_id,
    regime = regime_name,
    true_probability = true_probability,
    availability_sensitivity = agents$availability_sensitivity,
    numeracy = agents$numeracy,
    trust_in_statistics = agents$trust_in_statistics,
    risk_tolerance = agents$risk_tolerance,
    prior_experience = agents$prior_experience,
    availability_score = availability_score,
    base_rate_disclosure = base_rate_disclosure,
    emotional_intensity = emotional_intensity,
    subjective_probability = subjective_probability,
    calibration_error = calibration_error,
    participate_in_risky_asset = participate_in_risky_asset,
    insurance_demand = insurance_demand,
    policy_support = policy_support,
    welfare_proxy = welfare_proxy
  )
}

panel <- rbind(
  simulate_availability_environment("low_availability_with_base_rates", 0.60, 0.80, 0.25),
  simulate_availability_environment("medium_availability_environment", 1.00, 0.45, 0.55),
  simulate_availability_environment("high_availability_no_base_rates", 1.50, 0.10, 0.85)
)

summary <- aggregate(
  cbind(subjective_probability, calibration_error, participate_in_risky_asset, insurance_demand, policy_support, welfare_proxy) ~ regime,
  data = panel,
  FUN = mean
)

panel$availability_sensitivity_quartile <- cut(
  panel$availability_sensitivity,
  breaks = quantile(panel$availability_sensitivity, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

heterogeneity <- aggregate(
  cbind(subjective_probability, calibration_error, insurance_demand, policy_support) ~ regime + availability_sensitivity_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_availability_bias_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_availability_bias_regime_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_availability_bias_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
