fn realized_welfare(
    long_run_value: f64,
    complexity_sensitivity: f64,
    complexity: f64,
    switching_sensitivity: f64,
    switching_cost: f64,
    digital_literacy: f64,
) -> f64 {
    long_run_value
        - complexity_sensitivity * complexity
        - switching_sensitivity * switching_cost
        + 0.03 * digital_literacy
}

fn main() {
    let w = realized_welfare(0.42, 0.60, 0.08, 0.52, 0.04, 0.62);
    println!("Synthetic choice architecture welfare: {:.3}", w);
}
