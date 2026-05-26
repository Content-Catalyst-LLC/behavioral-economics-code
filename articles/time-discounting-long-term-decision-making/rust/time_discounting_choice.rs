fn present_value(future_value: f64, discount_rate: f64, periods: i32) -> f64 {
    future_value / (1.0 + discount_rate).powi(periods)
}

fn quasi_hyperbolic_value(beta: f64, delta: f64, reward: f64, delay: i32) -> f64 {
    beta * delta.powi(delay) * reward
}

fn choose_delayed_reward(
    beta: f64,
    delta: f64,
    delayed_reward: f64,
    delay: i32,
    immediate_reward: f64,
    support: f64,
) -> bool {
    let delayed_value = quasi_hyperbolic_value(beta, delta, delayed_reward, delay);
    let immediate_value = immediate_reward - support;
    delayed_value >= immediate_value
}

fn main() {
    println!("Present value: {:.2}", present_value(1000.0, 0.03, 10));
    println!(
        "Synthetic delayed choice under discounting: {}",
        choose_delayed_reward(0.75, 0.97, 300.0, 12, 160.0, 40.0)
    );
}
