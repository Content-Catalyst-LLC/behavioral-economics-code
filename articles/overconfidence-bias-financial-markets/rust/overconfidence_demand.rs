fn investor_demand(expected_return: f64, perceived_variance: f64, alpha: f64, beta: f64) -> f64 {
    alpha * expected_return - beta * perceived_variance
}

fn net_return_after_cost(gross_return: f64, trading_intensity: f64, cost_per_turnover: f64) -> f64 {
    gross_return - cost_per_turnover * trading_intensity
}

fn main() {
    println!("Synthetic investor demand: {:.3}", investor_demand(0.08, 0.03, 1.2, 0.7));
    println!("Synthetic net return after cost: {:.3}", net_return_after_cost(0.05, 1.4, 0.0025));
}
