# Synthetic behavioral friction model in R.
# Educational scaffold only; not empirical behavioral data.

set.seed(2727)

n <- 2200

behavioral_data <- data.frame(
  agent_id = seq_len(n),
  framing_signal = rnorm(n, 0, 0.15),
  loss_signal = rnorm(n, -0.04, 0.16),
  present_bias_signal = rnorm(n, -0.05, 0.14),
  social_signal = rnorm(n, 0.03, 0.12),
  trust_signal = rnorm(n, 0.08, 0.10),
  default_status = rbinom(n, 1, 0.5),
  effort_cost = runif(n, 0.02, 0.35)
)

behavioral_data$latent_choice <- with(
  behavioral_data,
  0.15 +
    framing_signal +
    loss_signal +
    present_bias_signal +
    social_signal +
    trust_signal +
    0.22 * default_status -
    0.75 * effort_cost
)

behavioral_data$uptake_probability <- 1 / (1 + exp(-behavioral_data$latent_choice))
behavioral_data$choose_option <- rbinom(n, 1, behavioral_data$uptake_probability)

model <- glm(
  choose_option ~ framing_signal + loss_signal + present_bias_signal +
    social_signal + trust_signal + default_status + effort_cost,
  family = binomial(link = "logit"),
  data = behavioral_data
)

print(summary(model))
write.csv(behavioral_data, "outputs/tables/r_behavioral_friction_model.csv", row.names = FALSE)
