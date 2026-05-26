fn prospect_value(x: f64, lambda: f64, eta: f64) -> f64 {
    if x >= 0.0 {
        x.powf(eta)
    } else {
        -lambda * (-x).powf(eta)
    }
}

fn choose_risky_gain_frame(lambda: f64, eta: f64, frame_shift: f64) -> bool {
    let certain = prospect_value(200.0, lambda, eta);
    let risky = (1.0 / 3.0) * prospect_value(600.0, lambda, eta)
        + (2.0 / 3.0) * prospect_value(0.0, lambda, eta);
    risky + frame_shift >= certain
}

fn main() {
    println!(
        "Synthetic risky choice under gain frame: {}",
        choose_risky_gain_frame(2.0, 0.88, -10.0)
    );
}
