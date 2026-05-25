# Event-study template for sustainable-consumption policy rollout.
# Synthetic scaffolding only; replace with validated empirical data for research use.

if (!requireNamespace("fixest", quietly = TRUE)) {
  message("Install fixest for high-quality economist-grade fixed-effects estimation: install.packages('fixest')")
}

panel_path <- file.path("data", "processed", "synthetic_sustainable_consumption_panel.csv")

if (file.exists(panel_path) && requireNamespace("fixest", quietly = TRUE)) {
  library(fixest)
  df <- read.csv(panel_path)

  df$event_time <- ifelse(
    df$treated_locality == 1,
    df$period - df$policy_start_period,
    NA
  )

  did <- feols(
    adopted ~ post_policy | household_id + period,
    cluster = ~locality_id,
    data = df
  )

  event <- feols(
    adopted ~ i(event_time, treated_locality, ref = -1) | household_id + period,
    cluster = ~locality_id,
    data = df
  )

  print(summary(did))
  print(summary(event))
} else {
  message("Panel data not found or fixest unavailable. Run Python data generation first and install fixest.")
}
