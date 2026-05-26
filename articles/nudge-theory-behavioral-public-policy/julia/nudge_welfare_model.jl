# Lightweight nudge policy welfare comparison in Julia.

using Random
using Statistics

Random.seed!(7070)

function nudge_welfare(utility, adopted, friction_cost, admin_cost, implementation_cost)
    user_benefit = 0.50 * adopted
    social_benefit = 0.40 * adopted
    return utility + user_benefit + social_benefit - friction_cost - admin_cost - implementation_cost
end

regimes = [
    ("information_only", 0, 0.10, 0.10, 0.22, 0.25),
    ("reminder_plus_norm", 0, 0.70, 0.70, 0.12, 0.15),
    ("default_plus_reminder", 1, 0.70, 0.60, 0.10, 0.10)
]

for regime in regimes
    name, default_on, reminder, norm_signal, friction, burden = regime
    welfare = [
        nudge_welfare(rand(), rand() > 0.35, friction * rand(), burden * rand(), 0.04 + 0.03 * reminder + 0.02 * norm_signal)
        for _ in 1:5000
    ]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
