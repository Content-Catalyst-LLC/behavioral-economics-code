#include <cmath>
#include <iostream>

double discounted_delayed_value(double beta, double delta, double reward, int delay) {
    return beta * std::pow(delta, delay) * reward;
}

bool choose_delayed_reward(double beta, double delta, double delayed_reward, int delay, double immediate_reward, double commitment_cost) {
    double delayed_value = discounted_delayed_value(beta, delta, delayed_reward, delay);
    double immediate_value = immediate_reward - commitment_cost;
    return delayed_value >= immediate_value;
}

int main() {
    std::cout << "Synthetic delayed choice under present bias: "
              << choose_delayed_reward(0.72, 0.97, 300.0, 12, 160.0, 70.0)
              << std::endl;
    return 0;
}
