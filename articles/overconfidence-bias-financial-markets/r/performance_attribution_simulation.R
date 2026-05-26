set.seed(1212)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_investors <- 2500
n_periods <- 120

investors <- data.frame(
  investor_id = 1:n_investors,
  true_signal_sd = runif(n_investors, 0.15, 0.35),
  overconfidence_multiplier = runif(n_investors, 1.0, 2.2),
  risk_tolerance = runif(n_investors, 0.5, 1.5),
  diversification_discipline = runif(n_investors, 0.25, 1.0),
  prior_success_sensitivity = runif(n_investors, 0.0, 0.8)
)

history <- vector("list", n_periods)
rolling_success <- rep(0, n_investors)

for (t in seq_len(n_periods)) {
  true_market_return <- rnorm(1, mean = 0.008, sd = 0.075)

  signals <- rnorm(
    n_investors,
    mean = true_market_return,
    sd = investors$true_signal_sd
  )

  confidence_boost <- 1 + investors$prior_success_sensitivity * pmax(rolling_success, 0)

  perceived_signal <- signals *
    investors$overconfidence_multiplier *
    confidence_boost

  trade_intensity <- abs(perceived_signal) *
    investors$risk_tolerance *
    (1.25 - 0.50 * investors$diversification_discipline)

  trade_intensity <- pmin(trade_intensity, 3.0)
  trading_cost <- 0.0025 * trade_intensity
  gross_position_return <- true_market_return * sign(perceived_signal) * trade_intensity
  realized_return <- gross_position_return - trading_cost

  rolling_success <- 0.80 * rolling_success + 0.20 * realized_return

  history[[t]] <- data.frame(
    period = t,
    investor_id = investors$investor_id,
    true_market_return = true_market_return,
    signal = signals,
    perceived_signal = perceived_signal,
    trade_intensity = trade_intensity,
    trading_cost = trading_cost,
    gross_position_return = gross_position_return,
    realized_return = realized_return,
    rolling_success = rolling_success,
    overconfidence_multiplier = investors$overconfidence_multiplier,
    diversification_discipline = investors$diversification_discipline
  )
}

panel <- do.call(rbind, history)

investor_summary <- aggregate(
  cbind(trade_intensity, trading_cost, gross_position_return, realized_return) ~ investor_id,
  data = panel,
  FUN = mean
)

investor_summary <- merge(investor_summary, investors, by = "investor_id")

investor_summary$overconfidence_quartile <- cut(
  investor_summary$overconfidence_multiplier,
  breaks = quantile(investor_summary$overconfidence_multiplier, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

performance_by_group <- aggregate(
  cbind(trade_intensity, trading_cost, realized_return) ~ overconfidence_quartile,
  data = investor_summary,
  FUN = mean
)

write.csv(panel, file.path(tables, "r_overconfidence_trading_panel.csv"), row.names = FALSE)
write.csv(investor_summary, file.path(tables, "r_overconfidence_investor_summary.csv"), row.names = FALSE)
write.csv(performance_by_group, file.path(tables, "r_overconfidence_quartile_summary.csv"), row.names = FALSE)

print(performance_by_group)
