set.seed(1111)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_investors <- 1200
n_periods <- 100

investors <- data.frame(
  investor_id = 1:n_investors,
  private_signal_weight = pmin(pmax(rnorm(n_investors, 1.0, 0.25), 0.2), 2.0),
  herd_weight = pmin(pmax(rnorm(n_investors, 0.9, 0.30), 0.1), 2.5),
  risk_weight = pmin(pmax(rnorm(n_investors, 0.8, 0.25), 0.1), 2.5),
  loss_aversion = pmin(pmax(rnorm(n_investors, 1.8, 0.35), 1.0), 3.0),
  reputation_pressure = pmin(pmax(rnorm(n_investors, 0.50, 0.20), 0), 1)
)

simulate_herd_market <- function(herd_multiplier = 1.0, fundamental_value = 0.15, shock_period = 65, shock_size = -0.35) {
  price <- 1.0
  prior_buy_rate <- 0.5
  reference_price <- price
  history <- list()

  for (t in 1:n_periods) {
    private_signals <- rnorm(n_investors, mean = fundamental_value, sd = 0.25)
    price_deviation <- abs(price - 1.0)
    market_shock <- ifelse(t == shock_period, shock_size, 0)
    loss_domain <- as.integer(price < reference_price)

    buy_utility <- with(investors,
      private_signal_weight * private_signals +
        herd_multiplier * herd_weight * prior_buy_rate -
        risk_weight * price_deviation -
        loss_aversion * loss_domain * abs(price - reference_price) +
        reputation_pressure * prior_buy_rate +
        market_shock
    )

    buy_prob <- plogis(buy_utility)
    buys <- rbinom(n_investors, 1, buy_prob)
    current_buy_rate <- mean(buys)

    price_impact <- 0.18 * (current_buy_rate - 0.5)
    noise <- rnorm(1, mean = 0, sd = 0.015)

    price <- max(0.10, price + price_impact + noise + market_shock * 0.10)

    history[[t]] <- data.frame(
      period = t,
      mean_private_signal = mean(private_signals),
      herd_signal = prior_buy_rate,
      buy_rate = current_buy_rate,
      price = price,
      price_deviation = price - 1.0,
      volatility_proxy = abs(price_impact + noise),
      shock = market_shock
    )

    prior_buy_rate <- current_buy_rate
  }

  do.call(rbind, history)
}

low_herding <- simulate_herd_market(herd_multiplier = 0.40)
medium_herding <- simulate_herd_market(herd_multiplier = 1.00)
high_herding <- simulate_herd_market(herd_multiplier = 1.60)

low_herding$regime <- "low_herding"
medium_herding$regime <- "medium_herding"
high_herding$regime <- "high_herding"

market_history <- rbind(low_herding, medium_herding, high_herding)

regime_summary <- aggregate(
  cbind(buy_rate, price, price_deviation, volatility_proxy) ~ regime,
  data = market_history,
  FUN = mean
)

write.csv(market_history, file.path(tables, "r_herd_market_history.csv"), row.names = FALSE)
write.csv(regime_summary, file.path(tables, "r_herd_market_regime_summary.csv"), row.names = FALSE)

print(regime_summary)
