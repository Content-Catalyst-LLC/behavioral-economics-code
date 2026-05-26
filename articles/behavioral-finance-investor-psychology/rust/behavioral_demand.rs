fn behavioral_demand(expected_return: f64, perceived_variance: f64, behavioral_term: f64, alpha: f64, beta: f64, gamma: f64) -> f64 {
    alpha * expected_return - beta * perceived_variance + gamma * behavioral_term
}

fn net_return_after_turnover(gross_return: f64, turnover: f64, cost_per_turnover: f64) -> f64 {
    gross_return - cost_per_turnover * turnover
}

fn main() {
    println!(
        "Synthetic behavioral demand: {:.3}",
        behavioral_demand(0.08, 0.03, 0.40, 1.2, 0.7, 0.5)
    );
    println!(
        "Synthetic net return after turnover: {:.3}",
        net_return_after_turnover(0.05, 1.4, 0.0025)
    );
}
