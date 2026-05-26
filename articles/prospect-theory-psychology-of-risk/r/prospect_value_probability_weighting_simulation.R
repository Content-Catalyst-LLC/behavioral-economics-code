set.seed(2525)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500

agents <- data.frame(
  agent_id = 1:n_agents,
  lambda = runif(n_agents, 1.0, 3.0),
  alpha = runif(n_agents, 0.75, 1.0),
  beta = runif(n_agents, 0.75, 1.0),
  gamma = runif(n_agents, 0.55, 1.0),
  numeracy = runif(n_agents, 0.20, 1.00),
  income_security = runif(n_agents, 0.10, 1.00),
  trust = runif(n_agents, 0.20, 1.00),
  prior_loss_exposure = rbinom(n_agents, 1, 0.35)
)

prospect_value <- function(x, lambda, alpha, beta) {
  ifelse(x >= 0, x ^ alpha, -lambda * ((-x) ^ beta))
}

probability_weight <- function(p, gamma) {
  numerator <- p ^ gamma
  denominator <- (p ^ gamma + (1 - p) ^ gamma) ^ (1 / gamma)
  numerator / denominator
}

simulate_frame <- function(frame) {
  rows <- list()

  for (i in 1:n_agents) {
    lambda_i <- agents$lambda[i]
    alpha_i <- agents$alpha[i]
    beta_i <- agents$beta[i]
    gamma_i <- agents$gamma[i]

    if (frame == "gain") {
      sure_value <- prospect_value(200, lambda_i, alpha_i, beta_i)
      risky_value <- probability_weight(1 / 3, gamma_i) *
        prospect_value(600, lambda_i, alpha_i, beta_i) +
        probability_weight(2 / 3, gamma_i) *
        prospect_value(0, lambda_i, alpha_i, beta_i)
    } else if (frame == "loss") {
      sure_value <- prospect_value(-400, lambda_i, alpha_i, beta_i)
      risky_value <- probability_weight(2 / 3, gamma_i) *
        prospect_value(-600, lambda_i, alpha_i, beta_i) +
        probability_weight(1 / 3, gamma_i) *
        prospect_value(0, lambda_i, alpha_i, beta_i)
    } else {
      sure_value <- 0
      risky_value <- probability_weight(0.5, gamma_i) *
        prospect_value(240, lambda_i, alpha_i, beta_i) +
        probability_weight(0.5, gamma_i) *
        prospect_value(-100, lambda_i, alpha_i, beta_i)
    }

    rows[[i]] <- data.frame(
      agent_id = agents$agent_id[i],
      frame = frame,
      sure_value = sure_value,
      risky_value = risky_value,
      choose_risky = as.integer(risky_value > sure_value)
    )
  }

  do.call(rbind, rows)
}

panel <- rbind(
  simulate_frame("gain"),
  simulate_frame("loss"),
  simulate_frame("mixed_gamble")
)

panel <- merge(panel, agents, by = "agent_id")

frame_summary <- aggregate(
  cbind(choose_risky, sure_value, risky_value) ~ frame,
  data = panel,
  FUN = mean
)

panel$lambda_quartile <- cut(
  panel$lambda,
  breaks = quantile(panel$lambda, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

panel$gamma_quartile <- cut(
  panel$gamma,
  breaks = quantile(panel$gamma, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

loss_aversion_heterogeneity <- aggregate(
  choose_risky ~ frame + lambda_quartile,
  data = panel,
  FUN = mean
)

probability_weighting_heterogeneity <- aggregate(
  choose_risky ~ frame + gamma_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_prospect_theory_panel.csv"), row.names = FALSE)
write.csv(frame_summary, file.path(tables, "r_prospect_theory_frame_summary.csv"), row.names = FALSE)
write.csv(loss_aversion_heterogeneity, file.path(tables, "r_prospect_theory_lambda_heterogeneity.csv"), row.names = FALSE)
write.csv(probability_weighting_heterogeneity, file.path(tables, "r_prospect_theory_probability_weighting_heterogeneity.csv"), row.names = FALSE)

print(frame_summary)
print(loss_aversion_heterogeneity)
print(probability_weighting_heterogeneity)
