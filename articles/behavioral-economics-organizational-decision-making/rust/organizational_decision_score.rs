fn logistic(x: f64) -> f64 {
    1.0 / (1.0 + (-x).exp())
}

fn approval_probability(
    expected_payoff: f64,
    risk: f64,
    sunk_cost: f64,
    prestige_value: f64,
    complexity: f64,
    overconfidence: f64,
    short_term_pressure: f64,
    review_strength: f64,
    long_horizon_value: f64,
    long_horizon_weight: f64,
) -> f64 {
    let value = expected_payoff
        + prestige_value * short_term_pressure
        - risk
        - complexity
        + 0.9 * sunk_cost
        + 0.7 * overconfidence
        - 0.8 * review_strength * sunk_cost
        - 0.5 * review_strength * overconfidence
        + long_horizon_weight * long_horizon_value;

    logistic(value)
}

fn main() {
    let p = approval_probability(0.14, 0.22, 0.31, 0.20, 0.35, 0.18, 0.70, 0.85, 0.26, 0.60);
    println!("Synthetic approval probability: {:.3}", p);
}
