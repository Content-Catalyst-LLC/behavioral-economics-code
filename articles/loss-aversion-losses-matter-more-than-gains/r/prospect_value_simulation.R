set.seed(2424)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500

agents <- data.frame(
  agent_id = 1:n_agents,
  lambda = runif(n_agents, 1.0, 3.0),
  alpha = runif(n_agents, 0.75, 1.0),
  beta = runif(n_agents, 0.75, 1.0),
  numeracy = runif(n_agents, 0.20, 1.00),
  income_security = runif(n_agents, 0.10, 1.00),
  prior_loss_exposure = rbinom(n_agents, 1, 0.35),
  trust = runif(n_agents, 0.20, 1.00)
)

prospect_value <- function(x, lambda, alpha, beta) {
  ifelse(
    x >= 0,
    x ^ alpha,
    -lambda * ((-x) ^ beta)
  )
}

simulate_frame <- function(frame) {
  rows <- list()

  for (i in 1:n_agents) {
    lambda_i <- agents$lambda[i]
    alpha_i <- agents$alpha[i]
    beta_i <- agents$beta[i]

    if (frame == "gain") {
      sure_value <- prospect_value(200, lambda_i, alpha_i, beta_i)
      risky_value <- (1 / 3) * prospect_value(600, lambda_i, alpha_i, beta_i) +
        (2 / 3) * prospect_value(0, lambda_i, alpha_i, beta_i)
    } else if (frame == "loss") {
      sure_value <- prospect_value(-400, lambda_i, alpha_i, beta_i)
      risky_value <- (2 / 3) * prospect_value(-600, lambda_i, alpha_i, beta_i) +
        (1 / 3) * prospect_value(0, lambda_i, alpha_i, beta_i)
    } else {
      sure_value <- 0
      risky_value <- 0.5 * prospect_value(240, lambda_i, alpha_i, beta_i) +
        0.5 * prospect_value(-100, lambda_i, alpha_i, beta_i)
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

results <- rbind(
  simulate_frame("gain"),
  simulate_frame("loss"),
  simulate_frame("mixed_gamble")
)

panel <- merge(results, agents, by = "agent_id")

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

lambda_summary <- aggregate(
  choose_risky ~ frame + lambda_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_loss_aversion_panel.csv"), row.names = FALSE)
write.csv(frame_summary, file.path(tables, "r_loss_aversion_frame_summary.csv"), row.names = FALSE)
write.csv(lambda_summary, file.path(tables, "r_loss_aversion_lambda_heterogeneity.csv"), row.names = FALSE)

print(frame_summary)
print(lambda_summary)
