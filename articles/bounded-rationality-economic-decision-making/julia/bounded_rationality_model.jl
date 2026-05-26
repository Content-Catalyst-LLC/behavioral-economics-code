using Random
using Statistics

Random.seed!(26260)

function simulate_agent(aspiration, search_cost; n_options=30)
    option_values = rand(n_options)
    optimal_value = maximum(option_values)

    chosen_index = n_options
    chosen_value = option_values[end]

    for i in 1:n_options
        if option_values[i] >= aspiration
            chosen_index = i
            chosen_value = option_values[i]
            break
        end
    end

    net_value = chosen_value - search_cost * chosen_index
    optimization_gap = optimal_value - chosen_value

    return chosen_value, optimal_value, net_value, optimization_gap, chosen_index
end

n = 3000
aspirations = rand(n) .* 0.30 .+ 0.55
search_costs = rand(n) .* 0.032 .+ 0.003

chosen_values = Float64[]
net_values = Float64[]
gaps = Float64[]
depths = Int[]

for i in 1:n
    chosen, optimal, net, gap, depth = simulate_agent(aspirations[i], search_costs[i])
    push!(chosen_values, chosen)
    push!(net_values, net)
    push!(gaps, gap)
    push!(depths, depth)
end

println("mean_chosen_value=", round(mean(chosen_values), digits=3))
println("mean_net_value=", round(mean(net_values), digits=3))
println("mean_optimization_gap=", round(mean(gaps), digits=3))
println("mean_search_depth=", round(mean(depths), digits=3))
