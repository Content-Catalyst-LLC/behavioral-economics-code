fn utility_status_quo(value_status_quo: f64, status_quo_premium: f64) -> f64 {
    value_status_quo + status_quo_premium
}

fn utility_alternative(value_alternative: f64, switch_cost: f64, loss_aversion: f64, perceived_loss: f64) -> f64 {
    value_alternative - switch_cost - loss_aversion * perceived_loss
}

fn choose_alternative(
    value_status_quo: f64,
    value_alternative: f64,
    premium: f64,
    switch_cost: f64,
    loss_aversion: f64,
    perceived_loss: f64,
) -> bool {
    utility_alternative(value_alternative, switch_cost, loss_aversion, perceived_loss)
        >= utility_status_quo(value_status_quo, premium)
}

fn main() {
    println!(
        "Synthetic alternative adoption under status quo bias: {}",
        choose_alternative(0.50, 0.68, 0.08, 0.05, 1.50, 0.04)
    );
}
