set.seed(808)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 1000
rounds <- 50

agents <- data.frame(
  agent_id = seq_len(n_agents),
  trust_propensity = pmin(pmax(rnorm(n_agents, 0.55, 0.18), 0), 1),
  reciprocity = pmin(pmax(rnorm(n_agents, 0.50, 0.20), 0), 1),
  punishment_willingness = pmin(pmax(rnorm(n_agents, 0.40, 0.18), 0), 1),
  institutional_trust = pmin(pmax(rnorm(n_agents, 0.55, 0.20), 0), 1),
  betrayal_sensitivity = pmin(pmax(rnorm(n_agents, 0.60, 0.16), 0), 1)
)

history <- list()

for (t in seq_len(rounds)) {
  institutional_support <- ifelse(t <= 20, 0.35, 0.70)
  norm_strength <- ifelse(t <= 20, 0.40, 0.70)
  punishment_credibility <- ifelse(t <= 20, 0.35, 0.65)
  shuffled <- sample(agents$agent_id, n_agents)
  pairs <- matrix(shuffled, ncol = 2, byrow = TRUE)
  rows <- list()

  for (i in seq_len(nrow(pairs))) {
    sender <- agents[agents$agent_id == pairs[i, 1], ]
    receiver <- agents[agents$agent_id == pairs[i, 2], ]
    sent <- rbinom(1, 1, plogis(1.6 * sender$trust_propensity + 0.8 * sender$institutional_trust * institutional_support + 0.6 * norm_strength - 0.7 * sender$betrayal_sensitivity))
    returned <- ifelse(sent == 1, rbinom(1, 1, plogis(1.8 * receiver$reciprocity + 0.7 * norm_strength + 0.5 * institutional_support - 0.4)), 0)
    punished <- ifelse(sent == 1 && returned == 0, rbinom(1, 1, plogis(1.7 * sender$punishment_willingness + 0.8 * punishment_credibility - 0.8)), 0)
    sender_welfare <- sent * (0.80 * returned - 0.70 * (1 - returned)) - 0.15 * punished + 0.20 * institutional_support
    receiver_welfare <- sent * (0.50 + 0.30 * returned - 0.20 * punished)

    rows[[length(rows) + 1]] <- data.frame(
      round = t,
      sent = sent,
      returned = returned,
      punished = punished,
      sender_welfare = sender_welfare,
      receiver_welfare = receiver_welfare,
      total_welfare = sender_welfare + receiver_welfare
    )
  }

  history[[t]] <- do.call(rbind, rows)
}

history <- do.call(rbind, history)
summary <- aggregate(cbind(sent, returned, punished, total_welfare) ~ round, data = history, FUN = mean)

write.csv(history, file.path(tables, "r_repeated_exchange_history.csv"), row.names = FALSE)
write.csv(summary, file.path(tables, "r_repeated_exchange_round_summary.csv"), row.names = FALSE)
print(tail(summary))
