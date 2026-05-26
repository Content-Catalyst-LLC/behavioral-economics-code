fn total_welfare(
    compliance_utility: f64,
    complied: f64,
    admin_burden: f64,
    burden_sensitivity: f64,
    sanction_strength: f64,
) -> f64 {
    let social_benefit = 0.90 * complied;
    let compliance_cost = admin_burden * burden_sensitivity;
    let enforcement_cost = 0.20 * sanction_strength;
    let administrative_cost = 0.10 + 0.25 * admin_burden;

    compliance_utility + social_benefit - compliance_cost - enforcement_cost - administrative_cost
}

fn main() {
    let w = total_welfare(0.70, 1.0, 0.10, 0.60, 0.55);
    println!("Synthetic regulatory policy welfare: {:.3}", w);
}
