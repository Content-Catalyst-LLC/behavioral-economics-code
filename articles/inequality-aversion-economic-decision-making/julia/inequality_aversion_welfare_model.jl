using Random
using Statistics

Random.seed!(9090)

function fehr_schmidt(self_payoff, other_payoff, alpha, beta)
    return self_payoff - alpha * max(other_payoff - self_payoff, 0) - beta * max(self_payoff - other_payoff, 0)
end

regimes = [
    ("equal_distribution", 0.50, 0.50),
    ("advantageous_inequality", 0.70, 0.30),
    ("disadvantageous_inequality", 0.30, 0.70)
]

for regime in regimes
    name, self_payoff, other_payoff = regime
    utility = [
        fehr_schmidt(self_payoff, other_payoff, rand() * 3, rand() * 2)
        for _ in 1:5000
    ]
    println(name, " mean_social_preference_utility=", round(mean(utility), digits=3))
end
