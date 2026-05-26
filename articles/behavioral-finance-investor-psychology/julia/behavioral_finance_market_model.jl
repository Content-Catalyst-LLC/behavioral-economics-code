using Random
using Statistics

Random.seed!(13130)

function simulate_market(behavior_scale, trading_friction; periods=120)
    price = 100.0
    fundamental = 100.0
    prev_price = price
    prices = Float64[]
    mispricing = Float64[]
    trade_intensity = Float64[]

    for t in 1:periods
        fundamental += randn() * 1.5 + 0.2
        demand_signal = behavior_scale * (fundamental - price) + behavior_scale * (price - prev_price)
        buy_rate = 1 / (1 + exp(-demand_signal / 10))
        intensity = min(abs(demand_signal / 10), 3.0)
        cost_drag = intensity * trading_friction

        prev_price = price
        price = price + 3 * (buy_rate - 0.5) - cost_drag + randn() * 0.8

        push!(prices, price)
        push!(mispricing, price - fundamental)
        push!(trade_intensity, intensity)
    end

    return mean(prices), mean(abs.(mispricing)), maximum(abs.(mispricing)), mean(trade_intensity)
end

regimes = [
    ("low_behavioral_distortion", 0.60, 0.0030),
    ("medium_behavioral_distortion", 1.00, 0.0025),
    ("high_behavioral_distortion_low_friction", 1.50, 0.0018)
]

for regime in regimes
    name, scale, friction = regime
    mean_price, mean_abs_mispricing, max_abs_mispricing, mean_intensity = simulate_market(scale, friction)
    println(name, " mean_price=", round(mean_price, digits=2), " mean_abs_mispricing=", round(mean_abs_mispricing, digits=2), " max_abs_mispricing=", round(max_abs_mispricing, digits=2), " mean_intensity=", round(mean_intensity, digits=3))
end
