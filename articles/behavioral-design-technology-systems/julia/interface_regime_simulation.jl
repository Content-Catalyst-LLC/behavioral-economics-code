# Synthetic behavioral-design interface comparison in Julia.
# This example uses only Base and standard libraries.

using Random
using Statistics

Random.seed!(202)

n = 7000
baseline_value = 0.45 .+ 0.18 .* randn(n)
salience_sensitivity = clamp.(0.55 .+ 0.18 .* randn(n), 0, 1)
default_sensitivity = clamp.(0.50 .+ 0.20 .* randn(n), 0, 1)
friction_sensitivity = clamp.(0.60 .+ 0.16 .* randn(n), 0, 1)
reward_sensitivity = clamp.(0.58 .+ 0.17 .* randn(n), 0, 1)
cognitive_overload = clamp.(0.42 .+ 0.15 .* randn(n), 0, 1)
privacy_sensitivity = clamp.(0.55 .+ 0.20 .* randn(n), 0, 1)
autonomy_preference = clamp.(0.58 .+ 0.18 .* randn(n), 0, 1)

function evaluate_interface(salience, default_on, entry_friction, exit_friction, reward_intensity, data_extraction_intensity)
    join_score = baseline_value .+
        salience_sensitivity .* salience .+
        default_sensitivity .* default_on .-
        friction_sensitivity .* entry_friction .+
        reward_sensitivity .* reward_intensity .-
        cognitive_overload .* 0.4

    join_prob = 1.0 ./ (1.0 .+ exp.(-join_score))
    friction_asymmetry = exit_friction - entry_friction

    welfare = join_prob .* (baseline_value .+ 0.4 * reward_intensity) .-
        0.8 * max(friction_asymmetry, 0) .-
        0.5 .* cognitive_overload .-
        0.7 .* max(friction_asymmetry, 0) .* autonomy_preference .-
        data_extraction_intensity .* privacy_sensitivity .* join_prob

    platform_value = 1.2 .* join_prob .+ 1.6 .* join_prob .+ data_extraction_intensity .* join_prob

    return mean(join_prob), mean(welfare), mean(platform_value)
end

regimes = [
    ("user_supportive_design", 0.55, 0, 0.08, 0.08, 0.35, 0.10),
    ("engagement_maximizing_design", 0.85, 1, 0.03, 0.22, 0.80, 0.45),
    ("friction_heavy_lock_in", 0.75, 1, 0.02, 0.60, 0.55, 0.60)
]

for regime in regimes
    name, salience, default_on, entry_friction, exit_friction, reward, data_extraction = regime
    join_rate, welfare, platform_value = evaluate_interface(salience, default_on, entry_friction, exit_friction, reward, data_extraction)
    println(name, " join=", round(join_rate, digits=3), " welfare=", round(welfare, digits=3), " platform=", round(platform_value, digits=3))
end
