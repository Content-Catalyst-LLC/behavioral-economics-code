using Random
using Statistics

Random.seed!(14140)

function simulate_commitment(commitment_cost, automation_strength, flexibility; n=3000, periods=36)
    beta = rand(n) .* 0.45 .+ 0.55
    delta = rand(n) .* 0.05 .+ 0.94
    income = rand(n) .* 3400 .+ 1800
    savings = zeros(n)
    welfare = zeros(n)

    for t in 1:periods
        income_t = income .* (rand(n) .* 0.2 .+ 0.9)
        temptation = rand(n) .* 1200 .+ 200
        planned = 0.12 .* income_t
        utility_stick = beta .* (delta .^ (periods - t)) .* planned .+ automation_strength .* 100
        utility_deviate = temptation .- commitment_cost
        actual = ifelse.(utility_stick .>= utility_deviate, planned, automation_strength .* flexibility .* planned)
        savings .+= actual
        welfare .+= savings .* 0.01 .+ actual .* 0.05 .- commitment_cost .* 0.0005
    end

    return mean(savings), mean(welfare)
end

regimes = [
    ("low_commitment", 100, 0.15, 0.90),
    ("medium_commitment", 400, 0.55, 0.65),
    ("high_commitment", 800, 0.85, 0.35)
]

for regime in regimes
    name, cost, auto, flex = regime
    mean_savings, mean_welfare = simulate_commitment(cost, auto, flex)
    println(name, " mean_savings=", round(mean_savings, digits=2), " mean_welfare=", round(mean_welfare, digits=2))
end
