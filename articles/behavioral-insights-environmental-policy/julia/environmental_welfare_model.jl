# Lightweight environmental policy welfare comparison in Julia.

using Random
using Statistics

Random.seed!(4040)

function policy_welfare(adopted, private_benefit, environmental_benefit, fiscal_cost, admin_cost, friction_cost)
    return adopted + private_benefit + environmental_benefit - fiscal_cost - admin_cost - 0.20 * friction_cost
end

regimes = [
    ("price_signal_only", 0.08, 0.20),
    ("norm_plus_default", 0.00, 0.08),
    ("integrated_policy_design", 0.06, 0.08)
]

for regime in regimes
    name, subsidy, friction = regime
    welfare = [
        policy_welfare(1, 0.25 + 0.15 * rand(), 0.90, subsidy, 0.05 + 0.10 * friction, friction * rand())
        for _ in 1:5000
    ]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
