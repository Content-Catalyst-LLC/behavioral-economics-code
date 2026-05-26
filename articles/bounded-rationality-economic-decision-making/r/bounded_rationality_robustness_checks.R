root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_bounded_rationality_panel.csv"))

make_quartile <- function(x) {
  cut(
    x,
    breaks = quantile(x, probs = seq(0, 1, 0.25)),
    include.lowest = TRUE,
    labels = paste0("Q", 1:4)
  )
}

df$aspiration_quartile <- make_quartile(df$aspiration)
df$stress_quartile <- make_quartile(df$stress)
df$capacity_quartile <- make_quartile(df$cognitive_capacity)
df$trust_quartile <- make_quartile(df$institutional_trust)

aspiration_het <- aggregate(
  cbind(chosen_value, net_value, optimization_gap, chosen_index) ~ regime + aspiration_quartile,
  data = df,
  FUN = mean
)

stress_het <- aggregate(
  cbind(chosen_value, net_value, optimization_gap, chosen_index) ~ regime + stress_quartile,
  data = df,
  FUN = mean
)

capacity_het <- aggregate(
  cbind(chosen_value, net_value, optimization_gap, chosen_index) ~ regime + capacity_quartile,
  data = df,
  FUN = mean
)

trust_het <- aggregate(
  cbind(chosen_value, net_value, optimization_gap, chosen_index) ~ regime + trust_quartile,
  data = df,
  FUN = mean
)

write.csv(aspiration_het, file.path(diagnostics, "r_bounded_rationality_aspiration_heterogeneity.csv"), row.names = FALSE)
write.csv(stress_het, file.path(diagnostics, "r_bounded_rationality_stress_heterogeneity.csv"), row.names = FALSE)
write.csv(capacity_het, file.path(diagnostics, "r_bounded_rationality_capacity_heterogeneity.csv"), row.names = FALSE)
write.csv(trust_het, file.path(diagnostics, "r_bounded_rationality_trust_heterogeneity.csv"), row.names = FALSE)

print(aspiration_het)
print(stress_het)
print(capacity_het)
print(trust_het)
