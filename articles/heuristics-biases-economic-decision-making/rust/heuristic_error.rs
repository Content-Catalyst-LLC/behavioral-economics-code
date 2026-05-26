fn heuristic_estimate(
    true_value: f64,
    availability_weight: f64,
    availability_signal: f64,
    representativeness_weight: f64,
    representativeness_signal: f64,
    anchor_weight: f64,
    anchor_signal: f64,
    framing_weight: f64,
    framing_signal: f64,
    correction_capacity: f64,
) -> f64 {
    let raw_error =
        availability_weight * availability_signal
        + representativeness_weight * representativeness_signal
        + anchor_weight * anchor_signal
        + framing_weight * framing_signal;

    let estimate = true_value + raw_error * (1.0 - correction_capacity);
    estimate.clamp(0.0, 1.0)
}

fn main() {
    let estimate = heuristic_estimate(0.35, 0.30, 0.10, 0.25, -0.05, 0.40, 0.12, 0.20, -0.08, 0.55);
    println!("Synthetic heuristic estimate: {:.3}", estimate);
    println!("Synthetic judgment error: {:.3}", estimate - 0.35);
}
