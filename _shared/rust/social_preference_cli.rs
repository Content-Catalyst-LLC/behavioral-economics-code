fn inequality_aversion(payoff_self: f64, payoff_other: f64, alpha: f64, beta: f64) -> f64 {
    let disadvantage = (payoff_other - payoff_self).max(0.0);
    let advantage = (payoff_self - payoff_other).max(0.0);
    payoff_self - alpha * disadvantage - beta * advantage
}

fn main() {
    let utility = inequality_aversion(80.0, 100.0, 0.6, 0.25);
    println!("social_preference_utility,{utility:.3}");
}
