using Random
using Statistics

Random.seed!(10010)

function fairness_reciprocity_utility(self_payoff, other_payoff, fairness_sensitivity, reciprocity_sensitivity, reciprocity_signal, process_fairness)
    disadvantage_penalty = fairness_sensitivity * max(other_payoff - self_payoff, 0)
    reciprocity_component = reciprocity_sensitivity * reciprocity_signal
    process_component = 0.30 * process_fairness
    return self_payoff - disadvantage_penalty + reciprocity_component + process_component
end

regimes = [
    ("fair_cooperative_regime", 0.50, 0.50, 0.40, 0.85),
    ("unequal_but_cooperative_regime", 0.35, 0.65, 0.40, 0.70),
    ("unequal_noncooperative_regime", 0.35, 0.65, -0.20, 0.45),
    ("exploitative_low_process_fairness_regime", 0.25, 0.75, -0.35, 0.25)
]

for regime in regimes
    name, self_payoff, other_payoff, reciprocity_signal, process_fairness = regime
    utility = [
        fairness_reciprocity_utility(self_payoff, other_payoff, rand() * 3, rand() * 3, reciprocity_signal, process_fairness)
        for _ in 1:5000
    ]
    println(name, " mean_utility=", round(mean(utility), digits=3))
end
