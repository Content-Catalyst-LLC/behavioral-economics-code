fn discounted_future_value(beta: f64, delta: f64, benefit: f64, periods: i32) -> f64 {
    beta * delta.powi(periods) * benefit
}

fn choose_commitment(beta: f64, delta: f64, future_benefit: f64, immediate_temptation: f64, commitment_cost: f64, periods: i32) -> bool {
    let patient_value = discounted_future_value(beta, delta, future_benefit, periods);
    let temptation_value = immediate_temptation - commitment_cost;
    patient_value >= temptation_value
}

fn main() {
    println!(
        "Synthetic patient choice under commitment: {}",
        choose_commitment(0.72, 0.97, 1000.0, 600.0, 300.0, 12)
    );
}
