# Lightweight welfare comparison for behavioral interface regimes.

using Random
using Statistics

Random.seed!(2026)

function user_welfare(joined, baseline_value, reward_intensity, friction_asymmetry, autonomy_preference, privacy_cost, overload)
    return joined * (baseline_value + 0.35 * reward_intensity) -
           0.7 * max(friction_asymmetry, 0) * autonomy_preference -
           privacy_cost -
           0.45 * overload
end

regimes = [
    ("user_supportive_design", 0.35, 0.00, 0.10),
    ("engagement_maximizing_design", 0.80, 0.19, 0.45),
    ("friction_heavy_lock_in", 0.55, 0.58, 0.60)
]

for regime in regimes
    name, reward, friction_gap, privacy = regime
    welfare = [user_welfare(1, 0.45 + 0.18 * randn(), reward, friction_gap, rand(), privacy * rand(), rand()) for _ in 1:5000]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
