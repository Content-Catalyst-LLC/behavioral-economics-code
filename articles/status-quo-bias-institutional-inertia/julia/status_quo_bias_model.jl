using Random
using Statistics

Random.seed!(18180)

function simulate_status_quo(default_shift, switching_support, disclosure_quality; n=3000)
    switch_cost = rand(n) .* 0.40 .+ 0.05
    loss_aversion = rand(n) .* 2.25 .+ 1.00
    status_quo_premium = rand(n) .* 0.28 .+ 0.02
    uncertainty = rand(n) .* 0.30 .+ 0.05
    fatigue = rand(n) .* 0.35
    sophistication = rand(n) .* 0.80 .+ 0.20

    value_status_quo = rand(n) .* 0.15 .+ 0.45
    value_alternative = value_status_quo .+ rand(n) .* 0.23 .+ 0.02
    perceived_loss = rand(n) .* 0.18 .+ 0.02

    effective_switch_cost = max.(switch_cost .- switching_support .* sophistication .* 0.20, 0)
    effective_premium = max.(status_quo_premium .+ fatigue .- default_shift .* 0.18 .- disclosure_quality .* sophistication .* 0.12, 0)
    effective_loss = max.(perceived_loss .+ uncertainty .- disclosure_quality .* 0.10, 0)

    utility_status_quo = value_status_quo .+ effective_premium
    utility_alternative = value_alternative .- effective_switch_cost .- loss_aversion .* effective_loss

    choose_alternative = utility_alternative .>= utility_status_quo
    welfare = ifelse.(choose_alternative, value_alternative .- effective_switch_cost, value_status_quo)

    return mean(choose_alternative), mean(welfare), mean(effective_switch_cost), mean(effective_premium)
end

regimes = [
    ("passive_status_quo_default", 0.00, 0.00, 0.10),
    ("active_choice_with_disclosure", 0.35, 0.35, 0.55),
    ("pro_switching_default_with_support", 0.75, 0.70, 0.80)
]

for regime in regimes
    name, default_shift, support, disclosure = regime
    adoption, welfare, switch_cost, premium = simulate_status_quo(default_shift, support, disclosure)
    println(name, " adoption=", round(adoption, digits=3), " welfare=", round(welfare, digits=3), " switch_cost=", round(switch_cost, digits=3), " premium=", round(premium, digits=3))
end
