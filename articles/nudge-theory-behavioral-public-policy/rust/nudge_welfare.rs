fn total_welfare(
    utility: f64,
    adopted: f64,
    friction_cost: f64,
    admin_cost: f64,
    implementation_cost: f64,
) -> f64 {
    let user_benefit = 0.50 * adopted;
    let social_benefit = 0.40 * adopted;

    utility + user_benefit + social_benefit - friction_cost - admin_cost - implementation_cost
}

fn main() {
    let w = total_welfare(0.65, 1.0, 0.06, 0.05, 0.073);
    println!("Synthetic nudge policy welfare: {:.3}", w);
}
