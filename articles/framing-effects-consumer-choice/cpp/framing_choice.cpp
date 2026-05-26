#include <cmath>
#include <iostream>

double prospect_value(double x, double lambda, double eta) {
    if (x >= 0.0) {
        return std::pow(x, eta);
    }
    return -lambda * std::pow(-x, eta);
}

bool choose_risky_gain_frame(double lambda, double eta, double frame_shift) {
    double certain = prospect_value(200.0, lambda, eta);
    double risky = (1.0/3.0) * prospect_value(600.0, lambda, eta) + (2.0/3.0) * prospect_value(0.0, lambda, eta);
    return (risky + frame_shift) >= certain;
}

int main() {
    std::cout << "Synthetic risky choice under gain frame: "
              << choose_risky_gain_frame(2.0, 0.88, -10.0)
              << std::endl;
    return 0;
}
