fn subjective_probability(
    true_probability: f64,
    availability_sensitivity: f64,
    availability_score: f64,
    base_rate_correction: f64,
) -> f64 {
    let p = true_probability + availability_sensitivity * availability_score * 0.25 - base_rate_correction;
    p.clamp(0.0, 1.0)
}

fn main() {
    println!(
        "Synthetic subjective probability under availability bias: {:.3}",
        subjective_probability(0.12, 0.70, 0.85, 0.04)
    );
}
