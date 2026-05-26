# Behavioral Economics in Organizational Decision-Making
# R workflow: escalation, incentives, and review structures
# Synthetic data only. This is a research-scaffolding example.

set.seed(101)

root <- normalizePath(getwd(), mustWork = FALSE)
output_tables <- file.path(root, "outputs", "tables")
processed <- file.path(root, "data", "processed")
dir.create(output_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(processed, recursive = TRUE, showWarnings = FALSE)

n_projects <- 4000

projects <- data.frame(
  project_id = seq_len(n_projects),
  expected_payoff = rnorm(n_projects, mean = 0.12, sd = 0.10),
  risk = pmin(pmax(rnorm(n_projects, mean = 0.25, sd = 0.10), 0), 1),
  sunk_cost = rgamma(n_projects, shape = 3, scale = 0.12),
  prestige_value = pmin(pmax(rnorm(n_projects, mean = 0.18, sd = 0.08), 0), 1),
  complexity = pmin(pmax(rnorm(n_projects, mean = 0.35, sd = 0.12), 0), 1),
  overconfidence = pmin(pmax(rnorm(n_projects, mean = 0.20, sd = 0.10), 0), 0.6),
  review_strength = sample(c(0.1, 0.4, 0.8), n_projects, replace = TRUE),
  long_horizon_value = pmin(pmax(rnorm(n_projects, mean = 0.20, sd = 0.12), 0), 1)
)

continuation_score <- with(
  projects,
  expected_payoff +
    prestige_value -
    risk -
    complexity +
    0.9 * sunk_cost +
    0.7 * overconfidence -
    0.8 * review_strength * sunk_cost -
    0.5 * review_strength * overconfidence +
    0.3 * long_horizon_value
)

projects$continue_prob <- plogis(continuation_score)
projects$continue_decision <- rbinom(n_projects, 1, projects$continue_prob)

review_summary <- aggregate(
  cbind(continue_prob, continue_decision) ~ review_strength,
  data = projects,
  FUN = mean
)

print(review_summary)

projects$likely_escalation <- with(
  projects,
  sunk_cost > 0.35 & overconfidence > 0.25
)

subset_summary <- aggregate(
  cbind(continue_prob, continue_decision) ~ review_strength + likely_escalation,
  data = projects,
  FUN = mean
)

print(subset_summary)

model <- glm(
  continue_decision ~ expected_payoff + risk + sunk_cost +
    prestige_value + complexity + overconfidence +
    review_strength + long_horizon_value,
  data = projects,
  family = binomial(link = "logit")
)

print(summary(model))

write.csv(projects, file.path(output_tables, "synthetic_project_portfolio.csv"), row.names = FALSE)
write.csv(review_summary, file.path(output_tables, "review_strength_summary.csv"), row.names = FALSE)
write.csv(subset_summary, file.path(output_tables, "escalation_review_summary.csv"), row.names = FALSE)
