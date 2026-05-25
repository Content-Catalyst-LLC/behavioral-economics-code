# Synthetic prospect-theory value function example.
# Educational scaffold only.

function prospect_value(x; alpha=0.88, beta=0.88, lambda=2.25)
    if x >= 0
        return x^alpha
    else
        return -lambda * ((-x)^beta)
    end
end

outcomes = collect(-100.0:10.0:100.0)
values = [prospect_value(x) for x in outcomes]

println("outcome,prospect_value")
for (x, v) in zip(outcomes, values)
    println("$(x),$(v)")
end
