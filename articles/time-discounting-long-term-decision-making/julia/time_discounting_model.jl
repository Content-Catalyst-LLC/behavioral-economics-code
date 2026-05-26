using Random
using Statistics

Random.seed!(17170)

function simulate_time_discounting(use_present_bias, commitment_support, flexibility; n=3000, periods=36)
    beta = rand(n) .* 0.45 .+ 0.55
    delta = rand(n) .* 0.06 .+ 0.93
    immediate_reward_base = rand(n) .* 110 .+ 80
    future_goal_value = rand(n) .* 180 .+ 140
    sophistication = rand(n) .* 0.80 .+ 0.20
    liquidity_need = rand(n) .* 0.30 .+ 0.05

    cumulative_delayed = zeros(n)
    cumulative_welfare = zeros(n)

    for t in 1:periods
        delayed_reward = future_goal_value .* (rand(n) .* 0.50 .+ 0.80)
        immediate_reward = immediate_reward_base .* (rand(n) .* 0.40 .+ 0.85)

        delayed_value = if use_present_bias
            beta .* (delta .^ (periods - t)) .* delayed_reward
        else
            (delta .^ (periods - t)) .* delayed_reward
        end

        support_value = commitment_support .* sophistication .* 50
        flexibility_penalty = liquidity_need .* (1 - flexibility) .* 30
        immediate_value = immediate_reward .- support_value .+ flexibility_penalty

        choose_delayed = delayed_value .>= immediate_value
        welfare = choose_delayed .* delayed_reward .- (.!choose_delayed) .* 0.20 .* delayed_reward .- flexibility_penalty

        cumulative_delayed .+= choose_delayed
        cumulative_welfare .+= welfare
    end

    return mean(cumulative_delayed), mean(cumulative_welfare)
end

regimes = [
    ("exponential_discounting", false, 0.00, 1.00),
    ("present_biased_discounting", true, 0.00, 1.00),
    ("present_bias_with_commitment_support", true, 0.70, 0.75)
]

for regime in regimes
    name, pb, support, flex = regime
    delayed, welfare = simulate_time_discounting(pb, support, flex)
    println(name, " delayed_choices=", round(delayed, digits=2), " welfare=", round(welfare, digits=2))
end
