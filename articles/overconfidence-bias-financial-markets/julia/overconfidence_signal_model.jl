using Random
using Statistics

Random.seed!(12120)

function simulate_overconfidence(multiplier, friction, leverage; n=3000, periods=120)
    returns = Float64[]
    intensities = Float64[]
    costs = Float64[]

    for t in 1:periods
        market_return = randn() * 0.075 + 0.008
        signals = market_return .+ randn(n) .* rand(n) .* 0.20
        perceived = signals .* multiplier
        trade_intensity = min.(abs.(perceived) .* leverage, 3.5)
        trading_cost = friction .* trade_intensity
        realized = market_return .* sign.(perceived) .* trade_intensity .- trading_cost

        append!(returns, realized)
        append!(intensities, trade_intensity)
        append!(costs, trading_cost)
    end

    return mean(intensities), mean(costs), mean(returns), std(returns)
end

regimes = [
    ("calibrated_confidence", 1.00, 0.0025, 1.00),
    ("moderate_overconfidence", 1.45, 0.0025, 1.15),
    ("high_overconfidence_low_friction", 2.05, 0.0018, 1.35)
]

for regime in regimes
    name, multiplier, friction, leverage = regime
    intensity, cost, ret, vol = simulate_overconfidence(multiplier, friction, leverage)
    println(name, " intensity=", round(intensity, digits=4), " cost=", round(cost, digits=5), " return=", round(ret, digits=5), " volatility=", round(vol, digits=5))
end
