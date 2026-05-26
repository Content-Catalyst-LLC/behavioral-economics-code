fn total_welfare(
    adopted: f64,
    private_benefit: f64,
    environmental_benefit: f64,
    fiscal_cost: f64,
    admin_cost: f64,
    friction_cost: f64,
) -> f64 {
    adopted + private_benefit + environmental_benefit - fiscal_cost - admin_cost - 0.20 * friction_cost
}

fn main() {
    let w = total_welfare(1.0, 0.26, 0.90, 0.06, 0.058, 0.04);
    println!("Synthetic environmental policy welfare: {:.3}", w);
}
