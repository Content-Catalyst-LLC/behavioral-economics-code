using Random
using Statistics

Random.seed!(11110)

function simulate_market(herd_weight, liquidity_depth, periods)
    price = 1.0
    prior_buy_rate = 0.5
    prices = Float64[]
    buy_rates = Float64[]

    for t in 1:periods
        private_signal = randn() * 0.25 + 0.15
        buy_utility = private_signal + herd_weight * prior_buy_rate - abs(price - 1.0)
        buy_rate = 1 / (1 + exp(-buy_utility))
        price = max(0.10, price + (0.16 / liquidity_depth) * (buy_rate - 0.5))
        push!(prices, price)
        push!(buy_rates, buy_rate)
        prior_buy_rate = buy_rate
    end

    return mean(prices), maximum(prices), minimum(prices), mean(buy_rates)
end

regimes = [
    ("low_herding_deep_liquidity", 0.25, 1.40),
    ("moderate_herding", 0.85, 1.00),
    ("high_herding_crowded_trade", 1.45, 0.65)
]

for regime in regimes
    name, herd_weight, liquidity_depth = regime
    mean_price, max_price, min_price, mean_buy_rate = simulate_market(herd_weight, liquidity_depth, 120)
    println(name, " mean_price=", round(mean_price, digits=3), " range=", round(max_price - min_price, digits=3), " buy_rate=", round(mean_buy_rate, digits=3))
end
