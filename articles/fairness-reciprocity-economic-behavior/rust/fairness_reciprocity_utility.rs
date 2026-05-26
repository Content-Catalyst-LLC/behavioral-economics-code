fn fairness_reciprocity_utility(
    self_payoff: f64,
    other_payoff: f64,
    fairness_sensitivity: f64,
    reciprocity_sensitivity: f64,
    reciprocity_signal: f64,
    process_fairness: f64,
) -> f64 {
    let disadvantage_penalty = fairness_sensitivity * (other_payoff - self_payoff).max(0.0);
    let reciprocity_component = reciprocity_sensitivity * reciprocity_signal;
    let process_component = 0.30 * process_fairness;
    self_payoff - disadvantage_penalty + reciprocity_component + process_component
}

fn main() {
    println!(
        "Fairness-reciprocity utility: {:.3}",
        fairness_reciprocity_utility(0.35, 0.65, 1.2, 1.0, 0.40, 0.70)
    );
}
