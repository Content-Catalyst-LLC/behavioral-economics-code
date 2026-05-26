fn crra_utility(x: f64, rho: f64) -> f64 {
    if (rho - 1.0).abs() < 1e-8 {
        x.ln()
    } else {
        x.powf(1.0 - rho) / (1.0 - rho)
    }
}

fn main() {
    let wealth = 50_000.0;
    let rho = 1.5;

    let eu_certain = crra_utility(wealth + 100.0, rho);
    let eu_risky = 0.5 * crra_utility(wealth + 40.0, rho)
        + 0.5 * crra_utility(wealth + 220.0, rho);

    println!("EU certain: {:.10}", eu_certain);
    println!("EU risky: {:.10}", eu_risky);
    println!("Choose risky: {}", if eu_risky > eu_certain { "yes" } else { "no" });
}
