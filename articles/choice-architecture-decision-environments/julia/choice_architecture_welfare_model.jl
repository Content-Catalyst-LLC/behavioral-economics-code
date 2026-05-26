# Lightweight choice architecture welfare comparison in Julia.

using Random
using Statistics

Random.seed!(6060)

function realized_welfare(long_run_value, complexity_sensitivity, complexity, switching_sensitivity, switching_cost, digital_literacy)
    return long_run_value -
           complexity_sensitivity * complexity -
           switching_sensitivity * switching_cost +
           0.03 * digital_literacy
end

regimes = [
    ("neutral_presentation", 0.20, 0.05),
    ("default_heavy_architecture", 0.12, 0.02),
    ("low_complexity_guided_design", 0.08, 0.04)
]

for regime in regimes
    name, complexity, switching_cost = regime
    welfare = [
        realized_welfare(0.42, rand(), complexity, rand(), switching_cost, rand())
        for _ in 1:5000
    ]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
