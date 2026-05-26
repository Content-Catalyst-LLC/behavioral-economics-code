using Random
using Statistics

Random.seed!(8080)

function trust_welfare(trusted, reciprocated, punished, support, norms, betrayal_cost, monitoring_cost)
    transaction_cost_reduction = 0.30 * support + 0.25 * norms + 0.20 * trusted
    cooperative_benefit = trusted * 0.70 * reciprocated
    betrayal_loss = trusted * betrayal_cost * (1 - reciprocated)
    punishment_value = 0.20 * punished
    institutional_cost = 0.05 * support
    return cooperative_benefit + transaction_cost_reduction + punishment_value - betrayal_loss - monitoring_cost - institutional_cost
end

regimes = [
    ("low_trust_exchange", 0.10, 0.15, 0.70, 0.35),
    ("reciprocal_market_exchange", 0.45, 0.55, 0.50, 0.20),
    ("institutionally_supported_cooperation", 0.80, 0.75, 0.35, 0.10)
]

for regime in regimes
    name, support, norms, betrayal_cost, monitoring = regime
    welfare = [trust_welfare(rand() > 0.35, rand() > 0.35, rand() > 0.75, support, norms, betrayal_cost, monitoring * rand()) for _ in 1:5000]
    println(name, " mean_welfare=", round(mean(welfare), digits=3))
end
