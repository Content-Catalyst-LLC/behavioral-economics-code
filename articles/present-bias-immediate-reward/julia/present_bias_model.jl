using Random
using Statistics

Random.seed!(16160)

function simulate_present_bias(commitment_cost, reminder_strength, flexibility; n=3000, periods=36)
    beta = rand(n) .* 0.50 .+ 0.50
    delta = rand(n) .* 0.05 .+ 0.94
    temptation_strength = rand(n) .* 210 .+ 50
    sophistication = rand(n) .* 0.80 .+ 0.20
    liquidity_need = rand(n) .* 0.30 .+ 0.05
    future_goal_value = rand(n) .* 270 .+ 150

    cumulative_delayed = zeros(n)
    cumulative_welfare = zeros(n)

    for t in 1:periods
        delayed_reward = future_goal_value .* (rand(n) .* 0.45 .+ 0.80)
        immediate_temptation = temptation_strength .* (rand(n) .* 0.50 .+ 0.80)
        discounted = beta .* (delta .^ (periods - t)) .* delayed_reward
        support = commitment_cost .+ reminder_strength .* sophistication .* 40
        hardship = liquidity_need .* (1 - flexibility) .* 25
        immediate_value = immediate_temptation .- support .+ hardship
        choose_delayed = discounted .>= immediate_value
        welfare = choose_delayed .* delayed_reward .- (.!choose_delayed) .* 0.25 .* delayed_reward .- hardship
        cumulative_delayed .+= choose_delayed
        cumulative_welfare .+= welfare
    end

    return mean(cumulative_delayed), mean(cumulative_welfare)
end

regimes = [
    ("weak_commitment", 20, 0.10, 0.95),
    ("medium_commitment", 70, 0.45, 0.75),
    ("strong_commitment", 140, 0.80, 0.55)
]

for regime in regimes
    name, cost, reminder, flex = regime
    delayed, welfare = simulate_present_bias(cost, reminder, flex)
    println(name, " delayed_choices=", round(delayed, digits=2), " welfare=", round(welfare, digits=2))
end
