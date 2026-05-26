set.seed(2222)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
true_value <- 0.35

agents <- data.frame(
  agent_id = 1:n_agents,
  alpha_availability = runif(n_agents, 0.00, 0.45),
  beta_representativeness = runif(n_agents, 0.00, 0.45),
  gamma_anchoring = runif(n_agents, 0.00, 0.45),
  delta_framing = runif(n_agents, 0.00, 0.35),
  numeracy = runif(n_agents, 0.20, 1.00),
  domain_knowledge = runif(n_agents, 0.10, 1.00),
  cognitive_load = runif(n_agents, 0.00, 0.60),
  confidence = runif(n_agents, 0.10, 0.90)
)

simulate_environment <- function(regime_name, signal_scale, disclosure_quality, debiasing_support) {

  availability_signal <- runif(n_agents, -0.25, 0.25) * signal_scale
  representativeness_signal <- runif(n_agents, -0.25, 0.25) * signal_scale
  anchor_signal <- runif(n_agents, -0.25, 0.25) * signal_scale
  framing_signal <- runif(n_agents, -0.20, 0.20) * signal_scale

  correction_capacity <- pmin(
    pmax(
      0.35 * agents$numeracy +
        0.30 * agents$domain_knowledge +
        0.20 * disclosure_quality +
        0.15 * debiasing_support -
        0.25 * agents$cognitive_load,
      0
    ),
    1
  )

  raw_error <-
    agents$alpha_availability * availability_signal +
    agents$beta_representativeness * representativeness_signal +
    agents$gamma_anchoring * anchor_signal +
    agents$delta_framing * framing_signal

  corrected_error <- raw_error * (1 - correction_capacity)
  estimated_value <- pmin(pmax(true_value + corrected_error, 0), 1)

  judgment_error <- estimated_value - true_value
  absolute_error <- abs(judgment_error)
  decision_quality <- 1 - absolute_error
  confidence_adjusted_error <- absolute_error * (1 + 0.25 * agents$confidence)

  welfare_proxy <- decision_quality +
    0.06 * disclosure_quality +
    0.05 * debiasing_support -
    0.08 * agents$cognitive_load -
    0.04 * confidence_adjusted_error

  data.frame(
    agent_id = agents$agent_id,
    regime = regime_name,
    true_value = true_value,
    estimated_value = estimated_value,
    judgment_error = judgment_error,
    absolute_error = absolute_error,
    decision_quality = decision_quality,
    welfare_proxy = welfare_proxy,
    correction_capacity = correction_capacity,
    availability_signal = availability_signal,
    representativeness_signal = representativeness_signal,
    anchor_signal = anchor_signal,
    framing_signal = framing_signal,
    numeracy = agents$numeracy,
    domain_knowledge = agents$domain_knowledge,
    cognitive_load = agents$cognitive_load,
    confidence = agents$confidence,
    disclosure_quality = disclosure_quality,
    debiasing_support = debiasing_support
  )
}

panel <- rbind(
  simulate_environment("low_bias_with_context", 0.60, 0.80, 0.75),
  simulate_environment("medium_bias_environment", 1.00, 0.50, 0.40),
  simulate_environment("high_bias_low_context", 1.50, 0.20, 0.10)
)

summary <- aggregate(
  cbind(estimated_value, judgment_error, absolute_error, decision_quality, welfare_proxy, correction_capacity) ~ regime,
  data = panel,
  FUN = mean
)

panel$correction_quartile <- cut(
  panel$correction_capacity,
  breaks = quantile(panel$correction_capacity, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

heterogeneity <- aggregate(
  cbind(absolute_error, decision_quality, welfare_proxy) ~ regime + correction_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_heuristics_biases_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_heuristics_biases_regime_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_heuristics_biases_correction_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
