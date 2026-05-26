set.seed(909)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_agents <- 2500
n_rounds <- 6000

agents <- data.frame(
  id = 1:n_agents,
  alpha = pmin(pmax(rnorm(n_agents, mean = 1.5, sd = 0.5), 0), 3),
  beta = pmin(pmax(rnorm(n_agents, mean = 0.6, sd = 0.3), 0), 2),
  income = exp(rnorm(n_agents, mean = 10.2, sd = 0.55)),
  redistribution_norm = pmin(pmax(rnorm(n_agents, mean = 0.55, sd = 0.20), 0), 1),
  merit_belief = pmin(pmax(rnorm(n_agents, mean = 0.50, sd = 0.22), 0), 1)
)

fs_utility <- function(self_payoff, other_payoff, alpha, beta) {
  self_payoff -
    alpha * max(other_payoff - self_payoff, 0) -
    beta * max(self_payoff - other_payoff, 0)
}

history <- vector("list", n_rounds)

for (t in seq_len(n_rounds)) {
  pair_ids <- sample(agents$id, 2, replace = FALSE)
  proposer <- agents[agents$id == pair_ids[1], ]
  responder <- agents[agents$id == pair_ids[2], ]

  possible_offers <- seq(0.05, 0.95, by = 0.05)

  proposer_utilities <- sapply(possible_offers, function(offer_to_responder) {
    fs_utility(1 - offer_to_responder, offer_to_responder, proposer$alpha, proposer$beta)
  })

  chosen_offer <- possible_offers[which.max(proposer_utilities)]

  responder_accept_utility <- fs_utility(
    chosen_offer,
    1 - chosen_offer,
    responder$alpha,
    responder$beta
  )

  accepted <- as.integer(responder_accept_utility >= 0)

  history[[t]] <- data.frame(
    round = t,
    proposer_id = proposer$id,
    responder_id = responder$id,
    offer_to_responder = chosen_offer,
    proposer_share = 1 - chosen_offer,
    accepted = accepted,
    responder_alpha = responder$alpha,
    responder_beta = responder$beta,
    proposer_alpha = proposer$alpha,
    proposer_beta = proposer$beta
  )
}

bargaining <- do.call(rbind, history)
write.csv(bargaining, file.path(tables, "r_bargaining_history.csv"), row.names = FALSE)

summary <- data.frame(
  mean_offer = mean(bargaining$offer_to_responder),
  median_offer = median(bargaining$offer_to_responder),
  acceptance_rate = mean(bargaining$accepted),
  rejection_rate = 1 - mean(bargaining$accepted)
)

write.csv(summary, file.path(tables, "r_bargaining_summary.csv"), row.names = FALSE)
print(summary)
