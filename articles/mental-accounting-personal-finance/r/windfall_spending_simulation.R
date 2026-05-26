set.seed(1515)

root <- normalizePath(getwd(), mustWork = FALSE)
tables <- file.path(root, "outputs", "tables")
dir.create(tables, recursive = TRUE, showWarnings = FALSE)

n_households <- 2500

households <- data.frame(
  household_id = 1:n_households,
  monthly_income = runif(n_households, 2500, 6500),
  liquid_savings = runif(n_households, 500, 12000),
  emergency_reserve = runif(n_households, 0, 8000),
  credit_card_debt = runif(n_households, 0, 9000),
  windfall = runif(n_households, 0, 3500),
  savings_label_strength = runif(n_households, 0.2, 1.3),
  emergency_need_risk = runif(n_households, 0.02, 0.25),
  present_bias = runif(n_households, 0.55, 1.00)
)

households$windfall_spent_share <- pmin(pmax(rnorm(n_households, mean = 0.55, sd = 0.18), 0), 1)
households$windfall_consumption <- households$windfall * households$windfall_spent_share
households$windfall_debt_payment <- households$windfall * (1 - households$windfall_spent_share) * 0.60

households$savings_available_for_debt <- pmax(
  households$liquid_savings - 3 * households$monthly_income * households$emergency_need_risk,
  0
)

households$savings_used_for_debt <- ifelse(
  households$credit_card_debt > 0,
  households$savings_available_for_debt * pmax(0, 0.35 - 0.22 * households$savings_label_strength),
  0
)

households$total_debt_payment <- pmin(
  households$credit_card_debt,
  households$windfall_debt_payment + households$savings_used_for_debt
)

households$remaining_debt <- pmax(households$credit_card_debt - households$total_debt_payment, 0)
households$remaining_liquid_savings <- pmax(households$liquid_savings - households$savings_used_for_debt, 0)

households$inefficiency_gap <- ifelse(
  households$remaining_debt > 0,
  pmin(households$remaining_liquid_savings, households$remaining_debt),
  0
)

households$annual_interest_cost <- households$remaining_debt * 0.22
households$resilience_index <- households$remaining_liquid_savings + households$emergency_reserve - households$remaining_debt - households$annual_interest_cost

households$label_quartile <- cut(
  households$savings_label_strength,
  breaks = quantile(households$savings_label_strength, probs = seq(0, 1, 0.25)),
  include.lowest = TRUE,
  labels = paste0("Q", 1:4)
)

group_summary <- aggregate(
  cbind(windfall_consumption, total_debt_payment, remaining_debt, inefficiency_gap, annual_interest_cost, resilience_index) ~ label_quartile,
  data = households,
  FUN = mean
)

overall_summary <- data.frame(
  mean_windfall = mean(households$windfall),
  mean_windfall_consumption = mean(households$windfall_consumption),
  mean_debt_payment = mean(households$total_debt_payment),
  mean_remaining_debt = mean(households$remaining_debt),
  mean_inefficiency_gap = mean(households$inefficiency_gap),
  mean_interest_cost = mean(households$annual_interest_cost),
  mean_resilience_index = mean(households$resilience_index)
)

write.csv(households, file.path(tables, "r_mental_accounting_households.csv"), row.names = FALSE)
write.csv(overall_summary, file.path(tables, "r_mental_accounting_overall_summary.csv"), row.names = FALSE)
write.csv(group_summary, file.path(tables, "r_mental_accounting_label_quartile_summary.csv"), row.names = FALSE)

print(overall_summary)
print(group_summary)
