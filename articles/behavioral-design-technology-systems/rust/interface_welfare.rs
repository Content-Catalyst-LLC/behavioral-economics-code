fn user_welfare(
    joined: f64,
    baseline_value: f64,
    reward_intensity: f64,
    friction_asymmetry: f64,
    autonomy_preference: f64,
    privacy_cost: f64,
    cognitive_overload: f64,
) -> f64 {
    joined * (baseline_value + 0.35 * reward_intensity)
        - 0.7 * friction_asymmetry.max(0.0) * autonomy_preference
        - privacy_cost
        - 0.45 * cognitive_overload
}

fn main() {
    let w = user_welfare(1.0, 0.45, 0.35, 0.0, 0.58, 0.05, 0.42);
    println!("Synthetic user welfare: {:.3}", w);
}
