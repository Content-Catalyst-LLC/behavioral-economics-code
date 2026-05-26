set.seed(1001)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 3000
n_rounds <- 7000

agents <- data.frame(
  id = 1:n_agents,
  fairness_sensitivity = pmin(pmax(rnorm(n_agents, mean = 1.2, sd = 0.4), 0), 3),
  reciprocity_sensitivity = pmin(pmax(rnorm(n_agents, mean = 1.0, sd = 0.35), 0), 3),
  trust = pmin(pmax(rnorm(n_agents, mean = 0.55, sd = 0.20), 0), 1),
  punishment_willingness = pmin(pmax(rnorm(n_agents, mean = 0.45, sd = 0.18), 0), 1),
  process_fairness_weight = pmin(pmax(rnorm(n_agents, mean = 0.55, sd = 0.18), 0), 1)
)

utility_from_offer <- function(offer_to_responder, fairness_sensitivity, process_fairness) {
  responder_share <- offer_to_responder
  proposer_share <- 1 - offer_to_responder
  inequality_penalty <- fairness_sensitivity * max(proposer_share - responder_share, 0)
  responder_share - inequality_penalty + 0.25 * process_fairness
}

history <- vector("list", n_rounds)

for (t in seq_len(n_rounds)) {
  pair_ids <- sample(agents$id, 2, replace = FALSE)

  proposer <- agents[agents$id == pair_ids[1], ]
  responder <- agents[agents$id == pair_ids[2], ]

  process_fairness <- runif(1, min = 0.30, max = 0.90)
  candidate_offers <- seq(0.05, 0.95, by = 0.05)

  proposer_scores <- sapply(candidate_offers, function(offer) {
    proposer_share <- 1 - offer
    expected_acceptance <- plogis(
      5 * (offer - 0.30) -
        responder$fairness_sensitivity +
        responder$trust +
        process_fairness
    )
    reciprocity_bonus <- proposer$reciprocity_sensitivity * offer * process_fairness
    proposer_share * expected_acceptance + 0.10 * reciprocity_bonus
  })

  chosen_offer <- candidate_offers[which.max(proposer_scores)]

  responder_utility <- utility_from_offer(
    offer_to_responder = chosen_offer,
    fairness_sensitivity = responder$fairness_sensitivity,
    process_fairness = process_fairness
  )

  accepted <- as.integer(responder_utility >= 0)

  punishment_probability <- plogis(
    responder$punishment_willingness * 2.0 -
      chosen_offer * 4.0 -
      process_fairness
  )

  punished <- ifelse(
    accepted == 0,
    rbinom(1, 1, punishment_probability),
    0
  )

  total_welfare <- accepted * 1.0 -
    punished * 0.15 +
    process_fairness * 0.20 -
    abs(0.50 - chosen_offer) * 0.30

  history[[t]] <- data.frame(
    round = t,
    proposer_id = proposer$id,
    responder_id = responder$id,
    offer_to_responder = chosen_offer,
    proposer_share = 1 - chosen_offer,
    accepted = accepted,
    punished = punished,
    process_fairness = process_fairness,
    responder_utility = responder_utility,
    total_welfare = total_welfare,
    responder_fairness_sensitivity = responder$fairness_sensitivity,
    responder_reciprocity_sensitivity = responder$reciprocity_sensitivity,
    responder_trust = responder$trust,
    responder_punishment_willingness = responder$punishment_willingness
  )
}

bargaining <- do.call(rbind, history)
write.csv(bargaining, file.path(tables, "r_bargaining_punishment_history.csv"), row.names = FALSE)

summary <- data.frame(
  mean_offer = mean(bargaining$offer_to_responder),
  median_offer = median(bargaining$offer_to_responder),
  acceptance_rate = mean(bargaining$accepted),
  rejection_rate = 1 - mean(bargaining$accepted),
  punishment_rate = mean(bargaining$punished),
  mean_total_welfare = mean(bargaining$total_welfare)
)

write.csv(summary, file.path(tables, "r_bargaining_punishment_summary.csv"), row.names = FALSE)
print(summary)
