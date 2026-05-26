using Random
using Statistics

Random.seed!(19190)

function prospect_value(x, lambda, eta)
    if x >= 0
        return x ^ eta
    else
        return -lambda * ((-x) ^ eta)
    end
end

function simulate_frame(frame_name, frame_strength, disclosure_quality, salience; n=3000)
    loss_aversion = rand(n) .* 2.0 .+ 1.0
    curvature = rand(n) .* 0.30 .+ 0.70
    numeracy = rand(n) .* 0.80 .+ 0.20
    trust = rand(n) .* 0.80 .+ 0.20
    fatigue = rand(n) .* 0.40

    risky_choices = zeros(n)
    comprehension = zeros(n)
    welfare = zeros(n)

    for i in 1:n
        if frame_name == "loss_frame"
            certain = -400
            risky_values = [-600, 0]
            probabilities = [2/3, 1/3]
        else
            certain = 200
            risky_values = [600, 0]
            probabilities = [1/3, 2/3]
        end

        lambda = loss_aversion[i]
        eta = curvature[i]

        certain_value = prospect_value(certain, lambda, eta)
        risky_value = sum(probabilities[j] * prospect_value(risky_values[j], lambda, eta) for j in 1:2)

        c = clamp(disclosure_quality * numeracy[i] + 0.20 * trust[i] - 0.25 * fatigue[i], 0, 1)
        comprehension[i] = c

        if frame_name == "gain_frame"
            shift = -frame_strength * salience * 20
        elseif frame_name == "loss_frame"
            shift = frame_strength * salience * lambda * 22
        else
            shift = 0.05 * salience * 5
        end

        adjusted = risky_value + shift + c * 5
        risky_choices[i] = adjusted >= certain_value ? 1 : 0
        welfare[i] = (risky_choices[i] == 1 ? risky_value : certain_value) + c * 10 - fatigue[i] * 5
    end

    return mean(risky_choices), mean(comprehension), mean(welfare)
end

regimes = [
    ("gain_frame", 0.70, 0.70, 0.75),
    ("loss_frame", 0.70, 0.70, 0.75),
    ("balanced_absolute_risk_frame", 0.15, 0.95, 0.35)
]

for regime in regimes
    name, strength, disclosure, salience = regime
    risk, comp, welfare = simulate_frame(name, strength, disclosure, salience)
    println(name, " risky_choice=", round(risk, digits=3), " comprehension=", round(comp, digits=3), " welfare=", round(welfare, digits=3))
end
