#[derive(Debug)]
struct Agent {
    income: f64,
    environmental_concern: f64,
    present_bias: f64,
    loss_aversion: f64,
    norm_sensitivity: f64,
    friction_sensitivity: f64,
    quality_uncertainty: f64,
    infrastructure_access: f64,
}

fn adoption_probability(
    agent: &Agent,
    subsidy: f64,
    default_green: f64,
    norm_signal: f64,
    friction: f64,
) -> f64 {
    let effective_premium = (0.10 - subsidy).max(0.0);
    let affordability = 1.0 / agent.income.ln();

    let immediate_cost =
        effective_premium * affordability * 100.0 + friction * agent.friction_sensitivity;

    let utility_diff = -0.65
        + 1.10 * agent.environmental_concern
        + 0.72 * default_green
        + 0.85 * agent.norm_sensitivity * norm_signal
        + 0.55 * agent.infrastructure_access
        - 1.75 * immediate_cost
        - 0.38 * agent.present_bias
        - 0.35 * agent.loss_aversion * effective_premium
        - 0.62 * agent.quality_uncertainty;

    1.0 / (1.0 + (-utility_diff).exp())
}

fn main() {
    let agent = Agent {
        income: 65000.0,
        environmental_concern: 0.62,
        present_bias: 0.28,
        loss_aversion: 2.0,
        norm_sensitivity: 0.55,
        friction_sensitivity: 0.50,
        quality_uncertainty: 0.25,
        infrastructure_access: 0.60,
    };

    println!(
        "{:.6}",
        adoption_probability(&agent, 0.05, 1.0, 0.70, 0.08)
    );
}
