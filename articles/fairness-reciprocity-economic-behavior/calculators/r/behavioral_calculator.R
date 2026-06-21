#!/usr/bin/env Rscript
# Self-contained behavioral calculator for Fairness, Reciprocity, and Social Preferences
# Educational scaffold only; not a validated behavioral or policy model.

logistic <- function(x) {
  1 / (1 + exp(-x))
}

behavioral_score <- function(value = 0.20, default = 1.00, salience = 0.50, effort_cost = 0.20, norm_signal = 0.10) {
  value + 0.60 * default + 0.35 * salience - 0.45 * effort_cost + 0.30 * norm_signal
}

score <- behavioral_score()
probability <- logistic(score)

result <- data.frame(
  series = "Behavioral Economics",
  article = "Fairness, Reciprocity, and Social Preferences",
  model = "transparent_behavioral_score_v1",
  behavioral_score = score,
  choice_probability = probability,
  responsible_use = "Educational scaffold only; not a validated behavioral or policy model.",
  stringsAsFactors = FALSE
)

output_dir <- file.path(dirname(dirname(normalizePath(sys.frame(1)$ofile))), "outputs")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
write.csv(result, file.path(output_dir, "calculator_result_r.csv"), row.names = FALSE)
print(result)
