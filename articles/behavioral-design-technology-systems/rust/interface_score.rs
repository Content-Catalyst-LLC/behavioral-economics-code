fn logistic(x: f64) -> f64 {
    1.0 / (1.0 + (-x).exp())
}

fn join_probability(
    baseline_value: f64,
    salience_sensitivity: f64,
    default_sensitivity: f64,
    friction_sensitivity: f64,
    reward_sensitivity: f64,
    cognitive_overload: f64,
    salience: f64,
    default_on: f64,
    entry_friction: f64,
    reward_intensity: f64,
) -> f64 {
    let score = baseline_value
        + salience_sensitivity * salience
        + default_sensitivity * default_on
        - friction_sensitivity * entry_friction
        + reward_sensitivity * reward_intensity
        - cognitive_overload * 0.4;

    logistic(score)
}

fn main() {
    let p = join_probability(0.45, 0.55, 0.50, 0.60, 0.58, 0.42, 0.55, 0.0, 0.08, 0.35);
    println!("Synthetic join probability: {:.3}", p);
}
