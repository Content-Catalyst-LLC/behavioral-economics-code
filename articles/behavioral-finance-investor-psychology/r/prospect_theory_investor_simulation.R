set.seed(1313)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_investors <- 1500
n_periods <- 100

investors <- data.frame(
  id = 1:n_investors,
  overconfidence = runif(n_investors, 0.2, 1.2),
  loss_aversion = runif(n_investors, 1.0, 2.5),
  anchoring_strength = runif(n_investors, 0.1, 0.9),
  herd_weight = runif(n_investors, 0.1, 1.0),
  diversification_discipline = runif(n_investors, 0.25, 1.0),
  risk_tolerance = runif(n_investors, 0.50, 1.50)
)

simulate_behavioral_market <- function(behavior_scale = 1.0, trading_friction = 0.0025) {
  price <- 100
  fundamental_value <- 100
  previous_price <- price

  history <- list()

  for (t in 1:n_periods) {
    fundamental_value <- fundamental_value + rnorm(1, mean = 0.20, sd = 1.50)

    private_signal <- rnorm(n_investors, mean = fundamental_value - price, sd = 5)

    anchored_view <- investors$anchoring_strength * behavior_scale * (previous_price - price)
    herd_signal <- investors$herd_weight * behavior_scale * (price - previous_price)

    expected_return <- private_signal *
      (1 + behavior_scale * investors$overconfidence) +
      anchored_view +
      herd_signal

    perceived_loss_penalty <- ifelse(
      expected_return < 0,
      behavior_scale * investors$loss_aversion * abs(expected_return),
      0
    )

    demand_signal <- expected_return - perceived_loss_penalty

    trade_intensity <- abs(demand_signal / 10) *
      investors$risk_tolerance *
      (1.25 - 0.50 * investors$diversification_discipline)

    trade_intensity <- pmin(trade_intensity, 3.0)
    buy_prob <- plogis(demand_signal / 10)
    buys <- rbinom(n_investors, 1, buy_prob)
    mean_buy_rate <- mean(buys)
    trading_cost_drag <- mean(trade_intensity) * trading_friction

    previous_price <- price
    price <- price + 3 * (mean_buy_rate - 0.5) - trading_cost_drag + rnorm(1, mean = 0, sd = 0.8)

    history[[t]] <- data.frame(
      period = t,
      price = price,
      fundamental_value = fundamental_value,
      mean_buy_rate = mean_buy_rate,
      mean_trade_intensity = mean(trade_intensity),
      trading_cost_drag = trading_cost_drag,
      mispricing = price - fundamental_value,
      absolute_mispricing = abs(price - fundamental_value)
    )
  }

  do.call(rbind, history)
}

low_distortion <- simulate_behavioral_market(behavior_scale = 0.60)
medium_distortion <- simulate_behavioral_market(behavior_scale = 1.00)
high_distortion <- simulate_behavioral_market(behavior_scale = 1.50)

low_distortion$regime <- "low_behavioral_distortion"
medium_distortion$regime <- "medium_behavioral_distortion"
high_distortion$regime <- "high_behavioral_distortion"

market_history <- rbind(low_distortion, medium_distortion, high_distortion)

regime_summary <- aggregate(
  cbind(price, fundamental_value, mean_buy_rate, mean_trade_intensity,
        trading_cost_drag, mispricing, absolute_mispricing) ~ regime,
  data = market_history,
  FUN = mean
)

write.csv(market_history, file.path(tables, "r_behavioral_finance_market_history.csv"), row.names = FALSE)
write.csv(regime_summary, file.path(tables, "r_behavioral_finance_regime_summary.csv"), row.names = FALSE)

print(regime_summary)
