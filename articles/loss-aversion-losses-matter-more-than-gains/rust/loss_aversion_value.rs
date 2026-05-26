fn prospect_value(x: f64, lambda_loss: f64, alpha_gain: f64, beta_loss: f64) -> f64 {
    if x >= 0.0 {
        x.powf(alpha_gain)
    } else {
        -lambda_loss * (-x).powf(beta_loss)
    }
}

fn main() {
    let lambda_loss = 2.0;
    let alpha_gain = 0.88;
    let beta_loss = 0.88;

    let mixed_value = 0.5 * prospect_value(240.0, lambda_loss, alpha_gain, beta_loss)
        + 0.5 * prospect_value(-100.0, lambda_loss, alpha_gain, beta_loss);

    println!("Mixed gamble prospect value: {:.4}", mixed_value);
    println!("Accept mixed gamble: {}", if mixed_value > 0.0 { "yes" } else { "no" });
}
