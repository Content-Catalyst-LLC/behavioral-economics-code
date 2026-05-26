# Synthetic organizational-regime comparison in Julia.
# This example uses only Base and standard libraries.

using Random
using Statistics

Random.seed!(101)

n = 6000
expected_payoff = 0.12 .+ 0.10 .* randn(n)
risk = clamp.(0.25 .+ 0.10 .* randn(n), 0, 1)
sunk_cost = rand(n) .* 0.7
prestige_value = clamp.(0.18 .+ 0.08 .* randn(n), 0, 1)
complexity = clamp.(0.35 .+ 0.12 .* randn(n), 0, 1)
overconfidence = clamp.(0.20 .+ 0.10 .* randn(n), 0, 0.6)
long_horizon_value = clamp.(0.20 .+ 0.12 .* randn(n), 0, 1)

function evaluate_regime(short_term_pressure, review_strength, conformity_pressure, long_horizon_weight)
    perceived_value = expected_payoff .+
        prestige_value .* short_term_pressure .-
        risk .-
        complexity .+
        0.9 .* sunk_cost .+
        0.7 .* overconfidence .-
        0.8 .* review_strength .* sunk_cost .-
        0.5 .* review_strength .* overconfidence .+
        long_horizon_weight .* long_horizon_value

    consensus = mean(perceived_value)
    adjusted_value = (1 - conformity_pressure) .* perceived_value .+ conformity_pressure .* consensus
    approval_prob = 1.0 ./ (1.0 .+ exp.(-adjusted_value))

    welfare = mean(
        approval_prob .* (expected_payoff .- risk .- 0.5 .* complexity .+ 0.6 .* long_horizon_value) .-
        approval_prob .* 0.4 .* sunk_cost
    )

    return mean(approval_prob), welfare
end

regimes = [
    ("metric_heavy_short_termism", 1.3, 0.15, 0.65, 0.10),
    ("balanced_governance", 0.9, 0.55, 0.35, 0.35),
    ("high_accountability_adaptive_review", 0.7, 0.85, 0.20, 0.60)
]

for regime in regimes
    name, short_term, review, conformity, horizon = regime
    approval, welfare = evaluate_regime(short_term, review, conformity, horizon)
    println(name, " approval=", round(approval, digits=3), " welfare=", round(welfare, digits=3))
end
