root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_prospect_theory_panel.csv"))

df$lambda_quartile <- cut(
  df$lambda_loss,
  breaks = quantile(df$lambda_loss, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

df$gamma_quartile <- cut(
  df$gamma_weight,
  breaks = quantile(df$gamma_weight, probs = seq(0, 1, 0.25)),
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
  cbind(choose_risky_pt, choose_risky_eu, pt_eu_disagreement) ~ frame + lambda_quartile,
  data = df,
  FUN = mean
)

gamma_het <- aggregate(
  cbind(choose_risky_pt, choose_risky_eu, pt_eu_disagreement) ~ frame + gamma_quartile,
  data = df,
  FUN = mean
)

security_het <- aggregate(
  cbind(choose_risky_pt, choose_risky_eu, pt_eu_disagreement) ~ frame + security_quartile,
  data = df,
  FUN = mean
)

write.csv(lambda_het, file.path(diagnostics, "r_prospect_theory_lambda_heterogeneity.csv"), row.names = FALSE)
write.csv(gamma_het, file.path(diagnostics, "r_prospect_theory_probability_weighting_heterogeneity.csv"), row.names = FALSE)
write.csv(security_het, file.path(diagnostics, "r_prospect_theory_security_heterogeneity.csv"), row.names = FALSE)

print(lambda_het)
print(gamma_het)
print(security_het)
