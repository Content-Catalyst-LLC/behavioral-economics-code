set.seed(1919)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500

agents <- data.frame(
  agent_id = 1:n_agents,
  loss_aversion = runif(n_agents, 1.0, 3.0),
  curvature = runif(n_agents, 0.70, 1.00),
  numeracy = runif(n_agents, 0.20, 1.00),
  trust = runif(n_agents, 0.20, 1.00),
  decision_fatigue = runif(n_agents, 0.00, 0.40)
)

prospect_value <- function(x, lambda, eta) {
  ifelse(
    x >= 0,
    x ^ eta,
    -lambda * ((-x) ^ eta)
  )
}

simulate_frame <- function(frame_name, frame_strength, disclosure_quality, salience) {
  if (frame_name == "gain_frame") {
    certain_outcome <- 200
    risky_values <- c(600, 0)
    risky_probabilities <- c(1/3, 2/3)
  } else if (frame_name == "loss_frame") {
    certain_outcome <- -400
    risky_values <- c(-600, 0)
    risky_probabilities <- c(2/3, 1/3)
  } else {
    certain_outcome <- 200
    risky_values <- c(600, 0)
    risky_probabilities <- c(1/3, 2/3)
  }

  rows <- vector("list", n_agents)

  for (i in seq_len(n_agents)) {
    lambda <- agents$loss_aversion[i]
    eta <- agents$curvature[i]

    certain_value <- prospect_value(certain_outcome, lambda, eta)
    risky_value <- sum(risky_probabilities * prospect_value(risky_values, lambda, eta))

    comprehension <- pmin(
      pmax(
        disclosure_quality * agents$numeracy[i] +
          0.20 * agents$trust[i] -
          0.25 * agents$decision_fatigue[i],
        0
      ),
      1
    )

    if (frame_name == "gain_frame") {
      framing_shift <- -frame_strength * salience * 20
    } else if (frame_name == "loss_frame") {
      framing_shift <- frame_strength * salience * lambda * 22
    } else {
      framing_shift <- 0.05 * salience * 5
    }

    adjusted_risky_value <- risky_value + framing_shift + comprehension * 5
    choose_risky <- as.integer(adjusted_risky_value >= certain_value)

    welfare_proxy <- ifelse(
      choose_risky == 1,
      risky_value,
      certain_value
    ) + comprehension * 10 - agents$decision_fatigue[i] * 5

    rows[[i]] <- data.frame(
      agent_id = agents$agent_id[i],
      frame = frame_name,
      loss_aversion = lambda,
      curvature = eta,
      numeracy = agents$numeracy[i],
      trust = agents$trust[i],
      decision_fatigue = agents$decision_fatigue[i],
      certain_value = certain_value,
      risky_value = risky_value,
      adjusted_risky_value = adjusted_risky_value,
      comprehension = comprehension,
      choose_risky = choose_risky,
      welfare_proxy = welfare_proxy,
      frame_strength = frame_strength,
      disclosure_quality = disclosure_quality,
      salience = salience
    )
  }

  do.call(rbind, rows)
}

panel <- rbind(
  simulate_frame("gain_frame", 0.70, 0.70, 0.75),
  simulate_frame("loss_frame", 0.70, 0.70, 0.75),
  simulate_frame("balanced_absolute_risk_frame", 0.15, 0.95, 0.35)
)

summary <- aggregate(
  cbind(choose_risky, welfare_proxy, comprehension, adjusted_risky_value) ~ frame,
  data = panel,
  FUN = mean
)

panel$loss_aversion_quartile <- cut(
  panel$loss_aversion,
  breaks = quantile(panel$loss_aversion, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

heterogeneity <- aggregate(
  cbind(choose_risky, welfare_proxy) ~ frame + loss_aversion_quartile,
  data = panel,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_framing_effects_panel.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_framing_effects_frame_summary.csv"), row.names = FALSE)
write.csv(heterogeneity, file.path(tables, "r_framing_effects_loss_aversion_heterogeneity.csv"), row.names = FALSE)

print(summary)
print(heterogeneity)
