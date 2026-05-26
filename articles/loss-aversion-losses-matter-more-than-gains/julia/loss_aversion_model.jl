using Random
using Statistics

Random.seed!(24240)

function prospect_value(x, lambda_loss, alpha_gain, beta_loss)
    if x >= 0
        return x^alpha_gain
    else
        return -lambda_loss * ((-x)^beta_loss)
    end
end

function simulate_agent(lambda_loss, alpha_gain, beta_loss, frame)
    if frame == "gain"
        sure_value = prospect_value(200.0, lambda_loss, alpha_gain, beta_loss)
        risky_value = (1/3) * prospect_value(600.0, lambda_loss, alpha_gain, beta_loss) + (2/3) * prospect_value(0.0, lambda_loss, alpha_gain, beta_loss)
    elseif frame == "loss"
        sure_value = prospect_value(-400.0, lambda_loss, alpha_gain, beta_loss)
        risky_value = (2/3) * prospect_value(-600.0, lambda_loss, alpha_gain, beta_loss) + (1/3) * prospect_value(0.0, lambda_loss, alpha_gain, beta_loss)
    else
        sure_value = 0.0
        risky_value = 0.5 * prospect_value(240.0, lambda_loss, alpha_gain, beta_loss) + 0.5 * prospect_value(-100.0, lambda_loss, alpha_gain, beta_loss)
    end

    return risky_value > sure_value ? 1 : 0
end

n = 3000
frames = ["gain", "loss", "mixed_gamble"]

for frame in frames
    choices = Int[]
    for i in 1:n
        lambda_loss = rand() * 2.0 + 1.0
        alpha_gain = rand() * 0.25 + 0.75
        beta_loss = rand() * 0.25 + 0.75
        push!(choices, simulate_agent(lambda_loss, alpha_gain, beta_loss, frame))
    end
    println(frame, " share_choose_risky=", round(mean(choices), digits=3))
end
