using Random
using Statistics

Random.seed!(15150)

function simulate_households(regime_name, windfall_spend_mean, savings_reallocation_base; n=3000)
    monthly_income = rand(n) .* 4000 .+ 2500
    liquid_savings = rand(n) .* 11500 .+ 500
    emergency_reserve = rand(n) .* 8000
    debt = rand(n) .* 9000
    windfall = rand(n) .* 3500
    label_strength = rand(n) .* 1.1 .+ 0.2
    emergency_risk = rand(n) .* 0.23 .+ 0.02

    windfall_spent_share = clamp.(windfall_spend_mean .+ randn(n) .* 0.15, 0, 1)
    windfall_consumption = windfall .* windfall_spent_share
    windfall_debt_payment = windfall .* (1 .- windfall_spent_share) .* 0.75

    protected_liquidity = 3 .* monthly_income .* emergency_risk
    savings_available_for_debt = max.(liquid_savings .- protected_liquidity, 0)
    savings_use_rate = max.(savings_reallocation_base .- 0.22 .* label_strength, 0)

    savings_used_for_debt = savings_available_for_debt .* savings_use_rate
    total_debt_payment = min.(debt, windfall_debt_payment .+ savings_used_for_debt)
    remaining_debt = max.(debt .- total_debt_payment, 0)
    remaining_liquid_savings = max.(liquid_savings .- savings_used_for_debt, 0)
    inefficiency_gap = ifelse.(remaining_debt .> 0, min.(remaining_liquid_savings, remaining_debt), 0)
    annual_interest_cost = remaining_debt .* 0.22
    resilience_index = remaining_liquid_savings .+ emergency_reserve .- remaining_debt .- annual_interest_cost

    println(regime_name,
        " debt_payment=", round(mean(total_debt_payment), digits=2),
        " remaining_debt=", round(mean(remaining_debt), digits=2),
        " ineff_gap=", round(mean(inefficiency_gap), digits=2),
        " resilience=", round(mean(resilience_index), digits=2)
    )
end

simulate_households("segmented_mental_accounts", 0.58, 0.32)
simulate_households("integrated_balance_sheet_prompt", 0.42, 0.46)
simulate_households("unified_fungible_money", 0.25, 0.62)
