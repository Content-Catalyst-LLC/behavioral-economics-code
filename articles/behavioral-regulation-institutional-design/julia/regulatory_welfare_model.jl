# Lightweight regulatory welfare comparison in Julia.

using Random
using Statistics

Random.seed!(5050)

function regulatory_welfare(compliance_utility, complied, admin_burden, burden_sensitivity, sanction_strength)
    social_benefit = 0.90 * complied
    compliance_cost = admin_burden * burden_sensitivity
    enforcement_cost = 0.20 * sanction_strength
    administrative_cost = 0.10 + 0.25 * admin_burden
    return compliance_utility + social_benefit - compliance_cost - enforcement_cost - administrative_cost
end

regimes = [
    ("sanction_heavy_deterrence", 0.28, 0.85),
    ("simplification_plus_trust", 0.08, 0.35),
    ("integrated_behavioral_regulation", 0.10, 0.55)
]

for regime in regimes
    name, burden, sanction = regime
    welfare = [
        regulatory_welfare(rand(), rand() > 0.35, burden, rand(), sanction)
        for _ in 1:5000
    ]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
