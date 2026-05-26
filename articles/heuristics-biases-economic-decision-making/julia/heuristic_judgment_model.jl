using Random
using Statistics

Random.seed!(22220)

function simulate_environment(signal_scale, disclosure_quality, debiasing_support; n=3000)
    true_value = 0.35

    alpha_availability = rand(n) .* 0.45
    beta_representativeness = rand(n) .* 0.45
    gamma_anchoring = rand(n) .* 0.45
    delta_framing = rand(n) .* 0.35
    numeracy = rand(n) .* 0.80 .+ 0.20
    domain_knowledge = rand(n) .* 0.90 .+ 0.10
    cognitive_load = rand(n) .* 0.60
    confidence = rand(n) .* 0.80 .+ 0.10

    availability_signal = (rand(n) .- 0.5) .* 0.50 .* signal_scale
    representativeness_signal = (rand(n) .- 0.5) .* 0.50 .* signal_scale
    anchor_signal = (rand(n) .- 0.5) .* 0.50 .* signal_scale
    framing_signal = (rand(n) .- 0.5) .* 0.40 .* signal_scale

    correction_capacity = clamp.(
        0.35 .* numeracy .+
        0.30 .* domain_knowledge .+
        0.20 .* disclosure_quality .+
        0.15 .* debiasing_support .-
        0.25 .* cognitive_load,
        0,
        1
    )

    raw_error = alpha_availability .* availability_signal .+
        beta_representativeness .* representativeness_signal .+
        gamma_anchoring .* anchor_signal .+
        delta_framing .* framing_signal

    corrected_error = raw_error .* (1 .- correction_capacity)
    estimated_value = clamp.(true_value .+ corrected_error, 0, 1)
    judgment_error = estimated_value .- true_value
    absolute_error = abs.(judgment_error)
    decision_quality = 1 .- absolute_error
    confidence_adjusted_error = absolute_error .* (1 .+ 0.25 .* confidence)

    welfare = decision_quality .+
        0.06 .* disclosure_quality .+
        0.05 .* debiasing_support .-
        0.08 .* cognitive_load .-
        0.04 .* confidence_adjusted_error

    return mean(estimated_value), mean(judgment_error), mean(absolute_error), mean(correction_capacity), mean(welfare)
end

regimes = [
    ("low_bias_with_context", 0.60, 0.80, 0.75),
    ("medium_bias_environment", 1.00, 0.50, 0.40),
    ("high_bias_low_context", 1.50, 0.20, 0.10)
]

for regime in regimes
    name, signal, disclosure, support = regime
    estimate, error, absolute_error, correction, welfare = simulate_environment(signal, disclosure, support)
    println(name, " estimate=", round(estimate, digits=3), " error=", round(error, digits=3), " abs_error=", round(absolute_error, digits=3), " correction=", round(correction, digits=3), " welfare=", round(welfare, digits=3))
end
