#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double admin_burden;
    double reminder_salience;
    double trust_signal;
    double penalty_strength;
};

double logistic(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

double compliance_probability(const Regime& r) {
    double trust = 0.60;
    double salience = 0.55;
    double norm_sensitivity = 0.45;
    double burden_sensitivity = 0.60;
    double present_bias = 0.35;

    double utility =
        0.8 * r.reminder_salience * salience +
        0.7 * norm_sensitivity +
        1.0 * r.trust_signal * trust +
        0.9 * r.penalty_strength -
        1.2 * r.admin_burden * burden_sensitivity -
        0.7 * present_bias * r.admin_burden;

    return logistic(utility - 0.5);
}

int main() {
    std::vector<Regime> regimes = {
        {"enforcement_heavy", 0.35, 0.30, 0.35, 0.85},
        {"simplification_first", 0.10, 0.55, 0.50, 0.35},
        {"trust_plus_salience", 0.12, 0.80, 0.80, 0.30}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": "
                  << compliance_probability(regime) << std::endl;
    }

    return 0;
}
