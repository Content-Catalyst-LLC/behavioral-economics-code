fn logistic(x: f64) -> f64 {
    1.0 / (1.0 + (-x).exp())
}

fn buy_probability(
    fundamental: f64,
    private_signal: f64,
    herd_signal: f64,
    perceived_risk: f64,
    alpha: f64,
    beta: f64,
    gamma: f64,
) -> f64 {
    let utility = fundamental + alpha * private_signal + beta * herd_signal - gamma * perceived_risk;
    logistic(utility)
}

fn main() {
    println!(
        "Synthetic herd buy probability: {:.3}",
        buy_probability(0.15, 0.20, 0.70, 0.10, 1.0, 1.4, 0.8)
    );
}
