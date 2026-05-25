# Synthetic governance-regime comparison in Julia.
# This example uses only Base and standard libraries.

using Random
using Statistics

Random.seed!(123)

n = 8000
trust = clamp.(0.55 .+ 0.20 .* randn(n), 0, 1)
salience = clamp.(0.50 .+ 0.18 .* randn(n), 0, 1)
norm_sensitivity = clamp.(0.45 .+ 0.20 .* randn(n), 0, 1)
burden_sensitivity = clamp.(0.60 .+ 0.16 .* randn(n), 0, 1)
present_bias = clamp.(rand(n) .^ 2, 0.05, 0.99)

function evaluate_regime(admin_burden, reminder_salience, trust_signal, penalty_strength)
    private_benefit = 0.8 .* reminder_salience .* salience
    norm_component = 0.7 .* norm_sensitivity
    trust_component = 1.0 .* trust_signal .* trust
    burden_cost = 1.2 .* admin_burden .* burden_sensitivity
    present_bias_cost = 0.7 .* present_bias .* admin_burden
    enforcement_component = 0.9 .* penalty_strength

    utility = private_benefit .+ norm_component .+ trust_component .+
              enforcement_component .- burden_cost .- present_bias_cost

    compliance_prob = 1.0 ./ (1.0 .+ exp.(-(utility .- 0.5)))
    welfare = mean(utility .+ compliance_prob .- 0.4 * admin_burden .- 0.3 * penalty_strength)

    return mean(compliance_prob), welfare
end

regimes = [
    ("enforcement_heavy", 0.35, 0.30, 0.35, 0.85),
    ("simplification_first", 0.10, 0.55, 0.50, 0.35),
    ("trust_plus_salience", 0.12, 0.80, 0.80, 0.30)
]

for regime in regimes
    name, burden, sal, trust_signal, penalty = regime
    compliance, welfare = evaluate_regime(burden, sal, trust_signal, penalty)
    println(name, " compliance=", round(compliance, digits=3), " welfare=", round(welfare, digits=3))
end
