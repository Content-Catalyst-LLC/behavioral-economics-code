fn user_welfare(
    clicked: f64,
    exposure_quality: f64,
    cognitive_overload: f64,
    privacy_sensitivity: f64,
    data_extraction_intensity: f64,
    consented: f64,
    friction: f64,
) -> f64 {
    clicked * exposure_quality
        - 0.30 * cognitive_overload
        - 0.45 * privacy_sensitivity * data_extraction_intensity * consented
        - 0.15 * friction
}

fn main() {
    let w = user_welfare(1.0, 0.52, 0.42, 0.55, 0.10, 1.0, 0.18);
    println!("Synthetic platform user welfare: {:.3}", w);
}
