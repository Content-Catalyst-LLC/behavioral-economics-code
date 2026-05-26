# Lightweight platform welfare comparison in Julia.

using Random
using Statistics

Random.seed!(3030)

function user_welfare(clicked, exposure_quality, overload, privacy_sensitivity, data_extraction, consented, friction)
    return clicked * exposure_quality -
           0.30 * overload -
           0.45 * privacy_sensitivity * data_extraction * consented -
           0.15 * friction
end

regimes = [
    ("neutral_discovery", 0.45, 0.20, 0.10, 0.18),
    ("engagement_optimized", 0.85, 0.55, 0.45, 0.10),
    ("socially_amplified_ranking", 0.70, 0.90, 0.35, 0.12)
]

for regime in regimes
    name, recommendation, social_proof, data_extraction, friction = regime
    welfare = [
        user_welfare(1, 0.45 + 0.18 * randn(), rand(), rand(), data_extraction, rand() > 0.5, friction)
        for _ in 1:5000
    ]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
