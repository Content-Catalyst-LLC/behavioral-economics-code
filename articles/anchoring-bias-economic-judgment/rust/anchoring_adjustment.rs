fn anchored_estimate(anchor: f64, true_value: f64, adjustment_rate: f64) -> f64 {
    anchor + adjustment_rate * (true_value - anchor)
}

fn anchoring_bias(anchor: f64, true_value: f64, adjustment_rate: f64) -> f64 {
    anchored_estimate(anchor, true_value, adjustment_rate) - true_value
}

fn main() {
    println!("Anchored estimate: {:.2}", anchored_estimate(85.0, 65.0, 0.55));
    println!("Anchoring bias: {:.2}", anchoring_bias(85.0, 65.0, 0.55));
}
