using Random
using Statistics

Random.seed!(21210)

function simulate_anchor(anchor_value, disclosure_quality, counter_anchor_support; n=3000)
    true_value = 65.0

    adjustment_rate = rand(n) .* 0.75 .+ 0.20
    numeracy = rand(n) .* 0.80 .+ 0.20
    confidence = rand(n) .* 0.80 .+ 0.10
    cognitive_load = rand(n) .* 0.50
    domain_knowledge = rand(n) .* 0.90 .+ 0.10

    effective_adjustment = clamp.(
        adjustment_rate .+
        0.18 .* domain_knowledge .+
        0.12 .* numeracy .+
        0.10 .* disclosure_quality .+
        0.08 .* counter_anchor_support .-
        0.20 .* cognitive_load,
        0,
        1
    )

    estimate = anchor_value .+ effective_adjustment .* (true_value - anchor_value)
    bias = estimate .- true_value
    absolute_error = abs.(bias)
    anchor_distance = max(abs(anchor_value - true_value), 1)

    decision_quality = 1 .- absolute_error ./ anchor_distance .+ 0.05 .* disclosure_quality .+ 0.04 .* counter_anchor_support
    welfare = decision_quality .- 0.10 .* cognitive_load .- 0.05 .* absolute_error .* (1 .+ confidence .* 0.25) ./ 100

    return mean(estimate), mean(bias), mean(absolute_error), mean(effective_adjustment), mean(welfare)
end

regimes = [
    ("low_anchor_low_support", 25.0, 0.25, 0.10),
    ("neutral_anchor_with_context", 65.0, 0.75, 0.65),
    ("high_anchor_low_support", 85.0, 0.25, 0.10),
    ("high_anchor_with_counter_context", 85.0, 0.85, 0.85)
]

for regime in regimes
    name, anchor, disclosure, support = regime
    estimate, bias, error, adjustment, welfare = simulate_anchor(anchor, disclosure, support)
    println(name, " estimate=", round(estimate, digits=3), " bias=", round(bias, digits=3), " error=", round(error, digits=3), " adjustment=", round(adjustment, digits=3), " welfare=", round(welfare, digits=3))
end
