using Random
using Statistics

Random.seed!(20200)

function simulate_availability_environment(salience_scale, base_rate_disclosure, emotional_intensity; n=3000)
    true_probability = 0.12

    availability_sensitivity = rand(n) .* 0.80 .+ 0.10
    numeracy = rand(n) .* 0.80 .+ 0.20
    trust = rand(n) .* 0.80 .+ 0.20
    risk_tolerance = rand(n) .* 0.80 .+ 0.10
    prior_experience = rand(n) .< 0.25

    recency = rand(n) .* salience_scale
    vividness = rand(n) .* salience_scale
    media = rand(n) .* salience_scale
    social = rand(n) .* salience_scale

    availability_score = 0.25 .* recency .+ 0.25 .* vividness .+ 0.25 .* media .+ 0.25 .* social .+ 0.20 .* prior_experience .* emotional_intensity
    base_rate_correction = base_rate_disclosure .* numeracy .* trust .* 0.18

    subjective_probability = clamp.(true_probability .+ availability_sensitivity .* availability_score .* 0.25 .- base_rate_correction, 0, 1)
    calibration_error = subjective_probability .- true_probability

    risky_asset = subjective_probability .< (0.18 .+ risk_tolerance .* 0.12)
    insurance = subjective_probability .> (0.16 .- prior_experience .* 0.03)
    policy = subjective_probability .+ 0.10 .* emotional_intensity .+ 0.05 .* trust .> 0.25
    welfare = 1 .- abs.(calibration_error) .- 0.08 .* emotional_intensity .* availability_score .+ 0.05 .* base_rate_disclosure .* numeracy

    return mean(subjective_probability), mean(calibration_error), mean(risky_asset), mean(insurance), mean(policy), mean(welfare)
end

regimes = [
    ("low_availability_with_base_rates", 0.60, 0.80, 0.25),
    ("medium_availability_environment", 1.00, 0.45, 0.55),
    ("high_availability_no_base_rates", 1.50, 0.10, 0.85)
]

for regime in regimes
    name, salience, disclosure, emotion = regime
    subjective, error, risky, insurance, policy, welfare = simulate_availability_environment(salience, disclosure, emotion)
    println(name, " subjective=", round(subjective, digits=3), " calibration_error=", round(error, digits=3), " risky_asset=", round(risky, digits=3), " insurance=", round(insurance, digits=3), " policy=", round(policy, digits=3), " welfare=", round(welfare, digits=3))
end
