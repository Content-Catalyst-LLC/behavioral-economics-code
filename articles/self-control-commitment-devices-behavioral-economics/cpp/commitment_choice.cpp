#include <cmath>
#include <iostream>

double discounted_future_value(double beta, double delta, double benefit, int periods) {
    return beta * std::pow(delta, periods) * benefit;
}

bool choose_commitment(double beta, double delta, double future_benefit, double immediate_temptation, double commitment_cost, int periods) {
    double patient_value = discounted_future_value(beta, delta, future_benefit, periods);
    double temptation_value = immediate_temptation - commitment_cost;
    return patient_value >= temptation_value;
}

int main() {
    std::cout << "Synthetic patient choice under commitment: "
              << choose_commitment(0.72, 0.97, 1000.0, 600.0, 300.0, 12)
              << std::endl;
    return 0;
}
