root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_loss_aversion_panel.csv"))

df$lambda_quartile <- cut(
  df$lambda_loss,
  breaks = quantile(df$lambda_loss, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

df$security_quartile <- cut(
  df$income_security,
  breaks = quantile(df$income_security, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

lambda_het <- aggregate(
  cbind(choose_risky, risky_value) ~ frame + lambda_quartile,
  data = df,
  FUN = mean
)

security_het <- aggregate(
  cbind(choose_risky, risky_value) ~ frame + security_quartile,
  data = df,
  FUN = mean
)

prior_loss_het <- aggregate(
  cbind(choose_risky, risky_value) ~ frame + prior_loss_exposure,
  data = df,
  FUN = mean
)

write.csv(lambda_het, file.path(diagnostics, "r_loss_aversion_lambda_heterogeneity.csv"), row.names = FALSE)
write.csv(security_het, file.path(diagnostics, "r_loss_aversion_security_heterogeneity.csv"), row.names = FALSE)
write.csv(prior_loss_het, file.path(diagnostics, "r_loss_aversion_prior_loss_heterogeneity.csv"), row.names = FALSE)

print(lambda_het)
print(security_het)
print(prior_loss_het)
