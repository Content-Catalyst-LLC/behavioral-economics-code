set.seed(2121)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
true_value <- 65

agents <- data.frame(
  agent_id = 1:n_agents,
  adjustment_rate = runif(n_agents, 0.20, 0.95),
  numeracy = runif(n_agents, 0.20, 1.00),
  confidence = runif(n_agents, 0.10, 0.90),
  cognitive_load = runif(n_agents, 0.00, 0.50),
  domain_knowledge = runif(n_agents, 0.10, 1.00)
)

simulate_anchor_regime <- function(regime_name, anchor_value, disclosure_quality, counter_anchor_support) {

  effective_adjustment <- pmin(
    pmax(
      agents$adjustment_rate +
        0.18 * agents$domain_knowledge +
        0.12 * agents$numeracy +
        0.10 * disclosure_quality +
        0.08 * counter_anchor_support -
        0.20 * agents$cognitive_load,
      0
    ),
    1
  )

  estimate <- anchor_value + effective_adjustment * (true_value - anchor_value)
  bias <- estimate - true_value
  absolute_error <- abs(bias)
  confidence_adjusted_error <- absolute_error * (1 + agents$confidence * 0.25)
  anchor_distance <- max(abs(anchor_value - true_value), 1)

  decision_quality <- 1 -
    absolute_error / anchor_distance +
    0.05 * disclosure_quality +
    0.04 * counter_anchor_support

  welfare_proxy <- decision_quality -
    0.10 * agents$cognitive_load -
    0.05 * confidence_adjusted_error / 100

  data.frame(
    agent_id = agents$agent_id,
    regime = regime_name,
    true_value = true_value,
    anchor_value = anchor_value,
    adjustment_rate = agents$adjustment_rate,
    effective_adjustment = effective_adjustment,
    numeracy = agents$numeracy,
    confidence = agents$confidence,
    cognitive_load = agents$cognitive_load,
    domain_knowledge = agents$domain_knowledge,
    disclosure_quality = disclosure_quality,
    counter_anchor_support = counter_anchor_support,
    estimate = estimate,
    bias = bias,
    absolute_error = absolute_error,
    confidence_adjusted_error = confidence_adjusted_error,
    decision_quality = decision_quality,
    welfare_proxy = welfare_proxy
  )
}

panel <- rbind(
  simulate_anchor_regime("low_anchor_low_support", 25, 0.25, 0.10),
  simulate_anchor_regime("neutral_anchor_with_context", 65, 0.75, 0.65),
  simulate_anchor_regime("high_anchor_low_support", 85, 0.25, 0.10),
  simulate_anchor_regime("high_anchor_with_counter_context", 85, 0.85, 0.85)
)

summary <- aggregate(
  cbind(estimate, bias, absolute_error, effective_adjustment, decision_quality, welfare_proxy) ~ regime,
  data = panel,
  FUN = mean
)

panel$adjustment_quartile <- cut(
  panel$effective_adjustment,
  breaks = quantile(panel$effective_adjustment, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

heterogeneity <- aggregate(
  cbind(estimate, bias, absolute_error, welfare_proxy) ~ regime + adjustment_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_anchoring_bias_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_anchoring_bias_regime_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_anchoring_bias_adjustment_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
