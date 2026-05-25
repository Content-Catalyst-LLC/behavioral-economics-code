# Behavioral Economics and Sustainable Consumption
# R workflow: adoption under defaults, present bias, and social norms.
# Synthetic data only.

set.seed(20260525)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile %||% "."), ".."), mustWork = FALSE)
data_dir <- file.path(root, "data")
out_tables <- file.path(root, "outputs", "tables")
dir.create(file.path(data_dir, "synthetic"), recursive = TRUE, showWarnings = FALSE)
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

n <- 8000

households <- data.frame(
  household_id = seq_len(n),
  income = rlnorm(n, meanlog = log(65000), sdlog = 0.55),
  environmental_concern = pmin(pmax(rnorm(n, 0.58, 0.19), 0), 1),
  present_bias = pmin(pmax(rbeta(n, 2.2, 5.0), 0.03), 0.98),
  loss_aversion = pmin(pmax(rnorm(n, 2.05, 0.45), 1.05), 4.25),
  norm_sensitivity = pmin(pmax(rnorm(n, 0.50, 0.21), 0), 1),
  friction_sensitivity = pmin(pmax(rnorm(n, 0.56, 0.20), 0), 1),
  quality_uncertainty = pmin(pmax(rnorm(n, 0.31, 0.16), 0), 1),
  infrastructure_access = pmin(pmax(rnorm(n, 0.55, 0.22), 0), 1)
)

households$income_quintile <- cut(
  households$income,
  breaks = quantile(households$income, probs = seq(0, 1, 0.2)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:5)
)

simulate_policy <- function(df, scenario, subsidy, default_green, norm_signal, friction) {
  effective_premium <- pmax(0.10 - subsidy, 0)
  affordability_pressure <- 1 / log(df$income)

  immediate_cost <- effective_premium * affordability_pressure * 100 +
    friction * df$friction_sensitivity

  future_private_benefit <- 0.50 * df$environmental_concern
  norm_benefit <- 0.70 * df$norm_sensitivity * norm_signal
  default_bonus <- 0.60 * default_green
  infrastructure_bonus <- 0.45 * df$infrastructure_access
  quality_penalty <- 0.60 * df$quality_uncertainty

  discounted_future_value <- (1 - df$present_bias * 0.5) * future_private_benefit
  perceived_loss <- df$loss_aversion * immediate_cost

  sustainable_utility <- 1.0 +
    discounted_future_value +
    norm_benefit +
    default_bonus +
    infrastructure_bonus -
    perceived_loss -
    quality_penalty

  conventional_utility <- 1.0
  adopted <- as.integer(sustainable_utility > conventional_utility)

  data.frame(
    scenario = scenario,
    household_id = df$household_id,
    income_quintile = df$income_quintile,
    sustainable_utility = sustainable_utility,
    conventional_utility = conventional_utility,
    adopted = adopted,
    private_welfare = ifelse(adopted == 1, sustainable_utility, conventional_utility),
    external_benefit = 0.90 * adopted,
    fiscal_cost = subsidy * adopted
  )
}

scenarios <- data.frame(
  scenario = c("information_only", "green_default", "subsidy", "subsidy_plus_default"),
  subsidy = c(0.00, 0.00, 0.05, 0.05),
  default_green = c(0, 1, 0, 1),
  norm_signal = c(0.50, 0.65, 0.50, 0.70),
  friction = c(0.18, 0.08, 0.15, 0.08)
)

results <- do.call(
  rbind,
  lapply(seq_len(nrow(scenarios)), function(i) {
    s <- scenarios[i, ]
    simulate_policy(
      households,
      scenario = s$scenario,
      subsidy = s$subsidy,
      default_green = s$default_green,
      norm_signal = s$norm_signal,
      friction = s$friction
    )
  })
)

results$total_welfare <- results$private_welfare + results$external_benefit - results$fiscal_cost

summary <- aggregate(
  cbind(adopted, private_welfare, external_benefit, fiscal_cost, total_welfare) ~ scenario,
  data = results,
  FUN = mean
)

distributional <- aggregate(
  cbind(adopted, total_welfare, fiscal_cost) ~ scenario + income_quintile,
  data = results,
  FUN = mean
)

write.csv(households, file.path(data_dir, "synthetic", "r_synthetic_households.csv"), row.names = FALSE)
write.csv(summary, file.path(out_tables, "r_policy_summary.csv"), row.names = FALSE)
write.csv(distributional, file.path(out_tables, "r_distributional_summary.csv"), row.names = FALSE)

print(summary)
print(distributional)

`%||%` <- function(a, b) if (!is.null(a)) a else b
