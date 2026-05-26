root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
diagnostics <- file.path(root, "outputs", "model_diagnostics")
dir.create(diagnostics, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(file.path(tables, "synthetic_framing_effects_panel.csv"))

weights <- expand.grid(
  comprehension_weight = c(0.75, 1.00, 1.25),
  autonomy_weight = c(0.75, 1.00, 1.25),
  manipulation_penalty = c(0.75, 1.00, 1.25)
)

rows <- list()

for (i in seq_len(nrow(weights))) {
  w <- weights[i, ]

  alt_welfare <- with(df,
    welfare_proxy +
      w$comprehension_weight * comprehension * 10 +
      w$autonomy_weight * disclosure_quality * numeracy * 5 -
      w$manipulation_penalty * frame_strength * salience * (1 - comprehension) * 8
  )

  tmp <- cbind(df, alt_welfare = alt_welfare)
  means <- aggregate(alt_welfare ~ frame, data = tmp, FUN = mean)

  means$comprehension_weight <- w$comprehension_weight
  means$autonomy_weight <- w$autonomy_weight
  means$manipulation_penalty <- w$manipulation_penalty

  rows[[length(rows) + 1]] <- means
}

robustness <- do.call(rbind, rows)
write.csv(robustness, file.path(diagnostics, "r_framing_effects_welfare_robustness.csv"), row.names = FALSE)
print(head(robustness, 20))
