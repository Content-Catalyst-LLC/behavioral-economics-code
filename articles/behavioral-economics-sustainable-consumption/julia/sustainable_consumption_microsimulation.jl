# Behavioral Economics and Sustainable Consumption
# Julia workflow: high-performance policy microsimulation scaffold.
# Synthetic data only.

using Random
using Statistics
using DataFrames
using CSV

Random.seed!(20260525)

root = joinpath(@__DIR__, "..")
out_tables = joinpath(root, "outputs", "tables")
mkpath(out_tables)

n = 100_000

income = exp.(randn(n) .* 0.55 .+ log(65_000))
environmental_concern = clamp.(randn(n) .* 0.19 .+ 0.58, 0, 1)
present_bias = clamp.(rand(n) .^ 2, 0.03, 0.98)
loss_aversion = clamp.(randn(n) .* 0.45 .+ 2.05, 1.05, 4.25)
norm_sensitivity = clamp.(randn(n) .* 0.21 .+ 0.50, 0, 1)
friction_sensitivity = clamp.(randn(n) .* 0.20 .+ 0.56, 0, 1)
quality_uncertainty = clamp.(randn(n) .* 0.16 .+ 0.31, 0, 1)
infrastructure_access = clamp.(randn(n) .* 0.22 .+ 0.55, 0, 1)

function evaluate_policy(subsidy, default_green, norm_signal, friction)
    effective_premium = max(0.10 - subsidy, 0)
    affordability = 1.0 ./ log.(income)

    immediate_cost = effective_premium .* affordability .* 100 .+
        friction .* friction_sensitivity

    future_private_benefit = 0.50 .* environmental_concern
    norm_benefit = 0.70 .* norm_sensitivity .* norm_signal
    default_bonus = 0.60 .* default_green
    infrastructure_bonus = 0.45 .* infrastructure_access
    quality_penalty = 0.60 .* quality_uncertainty
    discounted_future_value = (1 .- present_bias .* 0.5) .* future_private_benefit
    perceived_loss = loss_aversion .* immediate_cost

    sustainable_utility = 1.0 .+
        discounted_future_value .+
        norm_benefit .+
        default_bonus .+
        infrastructure_bonus .-
        perceived_loss .-
        quality_penalty

    adopted = sustainable_utility .> 1.0
    private_welfare = ifelse.(adopted, sustainable_utility, 1.0)
    external_benefit = 0.90 .* adopted
    fiscal_cost = subsidy .* adopted
    total_welfare = private_welfare .+ external_benefit .- fiscal_cost

    return (
        adoption_rate = mean(adopted),
        mean_private_welfare = mean(private_welfare),
        mean_external_benefit = mean(external_benefit),
        mean_fiscal_cost = mean(fiscal_cost),
        mean_total_welfare = mean(total_welfare)
    )
end

scenarios = [
    ("information_only", 0.00, 0, 0.50, 0.18),
    ("green_default", 0.00, 1, 0.65, 0.08),
    ("subsidy", 0.05, 0, 0.50, 0.15),
    ("subsidy_plus_default", 0.05, 1, 0.70, 0.08),
    ("regulation_plus_support", 0.04, 1, 0.75, 0.05),
]

rows = DataFrame(
    scenario = String[],
    adoption_rate = Float64[],
    mean_private_welfare = Float64[],
    mean_external_benefit = Float64[],
    mean_fiscal_cost = Float64[],
    mean_total_welfare = Float64[]
)

for (name, subsidy, default_green, norm_signal, friction) in scenarios
    result = evaluate_policy(subsidy, default_green, norm_signal, friction)
    push!(rows, (
        name,
        result.adoption_rate,
        result.mean_private_welfare,
        result.mean_external_benefit,
        result.mean_fiscal_cost,
        result.mean_total_welfare
    ))
end

sort!(rows, :mean_total_welfare, rev = true)
CSV.write(joinpath(out_tables, "julia_policy_microsimulation.csv"), rows)
println(rows)
