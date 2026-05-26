root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_expected_utility_panel.csv"))

df$rho_quartile <- cut(
  df$rho,
  breaks = quantile(df$rho, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

df$wealth_quartile <- cut(
  df$wealth,
  breaks = quantile(df$wealth, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

risk_het <- aggregate(
  cbind(choose_risky_eu, observed_choose_risky, certainty_equivalent_payoff, risk_premium) ~ rho_quartile,
  data = df,
  FUN = mean
)

wealth_het <- aggregate(
  cbind(choose_risky_eu, observed_choose_risky, certainty_equivalent_payoff, risk_premium) ~ wealth_quartile,
  data = df,
  FUN = mean
)

write.csv(risk_het, file.path(diagnostics, "r_expected_utility_risk_aversion_heterogeneity.csv"), row.names = FALSE)
write.csv(wealth_het, file.path(diagnostics, "r_expected_utility_wealth_heterogeneity.csv"), row.names = FALSE)

print(risk_het)
print(wealth_het)
