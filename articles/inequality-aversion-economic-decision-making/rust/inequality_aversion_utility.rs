fn fehr_schmidt(self_payoff: f64, other_payoff: f64, alpha: f64, beta: f64) -> f64 {
    self_payoff
        - alpha * (other_payoff - self_payoff).max(0.0)
        - beta * (self_payoff - other_payoff).max(0.0)
}

fn main() {
    println!("Fehr-Schmidt utility: {:.3}", fehr_schmidt(0.30, 0.70, 1.5, 0.6));
}
