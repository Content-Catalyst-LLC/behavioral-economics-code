using Random
using Statistics

Random.seed!(23230)

function crra_utility(x, rho)
    if abs(rho - 1.0) < 1e-8
        return log(x)
    else
        return (x^(1 - rho)) / (1 - rho)
    end
end

function simulate_population(name, rho_low, rho_high; n=3000)
    wealth = rand(n) .* 95000 .+ 5000
    rho = rand(n) .* (rho_high - rho_low) .+ rho_low

    payoff_a = 100.0
    payoff_b_low = 40.0
    payoff_b_high = 220.0

    choose_risky = zeros(Int, n)

    for i in 1:n
        eu_a = crra_utility(wealth[i] + payoff_a, rho[i])
        eu_b = 0.5 * crra_utility(wealth[i] + payoff_b_low, rho[i]) + 0.5 * crra_utility(wealth[i] + payoff_b_high, rho[i])
        choose_risky[i] = eu_b > eu_a ? 1 : 0
    end

    println(name, " mean_rho=", round(mean(rho), digits=3), " share_choose_risky=", round(mean(choose_risky), digits=3))
end

simulate_population("low_risk_aversion", 0.10, 0.80)
simulate_population("medium_risk_aversion", 0.80, 1.50)
simulate_population("high_risk_aversion", 1.50, 3.00)
