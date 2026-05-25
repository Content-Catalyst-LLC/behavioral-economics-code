fn logistic(x: f64) -> f64 {
    1.0 / (1.0 + (-x).exp())
}

fn compliance_probability(
    trust: f64,
    salience: f64,
    norm_sensitivity: f64,
    burden_sensitivity: f64,
    present_bias: f64,
    admin_burden: f64,
    reminder_salience: f64,
    trust_signal: f64,
    penalty_strength: f64,
) -> f64 {
    let utility = 0.8 * reminder_salience * salience
        + 0.7 * norm_sensitivity
        + 1.0 * trust_signal * trust
        + 0.9 * penalty_strength
        - 1.2 * admin_burden * burden_sensitivity
        - 0.7 * present_bias * admin_burden;

    logistic(utility - 0.5)
}

fn main() {
    let p = compliance_probability(0.60, 0.55, 0.45, 0.60, 0.35, 0.12, 0.80, 0.80, 0.30);
    println!("Synthetic compliance probability: {:.3}", p);
}
