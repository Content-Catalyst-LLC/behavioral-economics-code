fn discounted_delayed_value(beta: f64, delta: f64, reward: f64, delay: i32) -> f64 {
    beta * delta.powi(delay) * reward
}

fn choose_delayed_reward(
    beta: f64,
    delta: f64,
    delayed_reward: f64,
    delay: i32,
    immediate_reward: f64,
    commitment_cost: f64,
) -> bool {
    let delayed_value = discounted_delayed_value(beta, delta, delayed_reward, delay);
    let immediate_value = immediate_reward - commitment_cost;
    delayed_value >= immediate_value
}

fn main() {
    println!(
        "Synthetic delayed choice under present bias: {}",
        choose_delayed_reward(0.72, 0.97, 300.0, 12, 160.0, 70.0)
    );
}
