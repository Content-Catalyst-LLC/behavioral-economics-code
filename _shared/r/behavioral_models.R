# Shared behavioral-science model helpers.
# Educational scaffolds only; not validated operational models.

logistic <- function(x) {
  1 / (1 + exp(-x))
}

prospect_value <- function(x, alpha = 0.88, beta = 0.88, loss_lambda = 2.25) {
  ifelse(x >= 0, x ^ alpha, -loss_lambda * ((-x) ^ beta))
}

default_effect_score <- function(value, default = 0, salience = 0, effort_cost = 0, norm_signal = 0) {
  value + 0.60 * default + 0.35 * salience - 0.45 * effort_cost + 0.30 * norm_signal
}

choice_probability <- function(value, default = 0, salience = 0, effort_cost = 0, norm_signal = 0) {
  logistic(default_effect_score(value, default, salience, effort_cost, norm_signal))
}
