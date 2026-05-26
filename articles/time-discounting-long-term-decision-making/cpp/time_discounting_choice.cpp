#include <cmath>
#include <iostream>

double present_value(double future_value, double discount_rate, int periods) {
    return future_value / std::pow(1.0 + discount_rate, periods);
}

double quasi_hyperbolic_value(double beta, double delta, double reward, int delay) {
    return beta * std::pow(delta, delay) * reward;
}

bool choose_delayed_reward(double beta, double delta, double delayed_reward, int delay, double immediate_reward, double support) {
    double delayed_value = quasi_hyperbolic_value(beta, delta, delayed_reward, delay);
    double immediate_value = immediate_reward - support;
    return delayed_value >= immediate_value;
}

int main() {
    std::cout << "Present value: " << present_value(1000.0, 0.03, 10) << std::endl;
    std::cout << "Synthetic delayed choice under discounting: "
              << choose_delayed_reward(0.75, 0.97, 300.0, 12, 160.0, 40.0)
              << std::endl;
    return 0;
}
