#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double salience;
    double default_on;
    double entry_friction;
    double exit_friction;
    double reward_intensity;
    double data_extraction_intensity;
};

double logistic(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

double join_probability(const Regime& r) {
    double baseline_value = 0.45;
    double salience_sensitivity = 0.55;
    double default_sensitivity = 0.50;
    double friction_sensitivity = 0.60;
    double reward_sensitivity = 0.58;
    double cognitive_overload = 0.42;

    double score =
        baseline_value +
        salience_sensitivity * r.salience +
        default_sensitivity * r.default_on -
        friction_sensitivity * r.entry_friction +
        reward_sensitivity * r.reward_intensity -
        cognitive_overload * 0.4;

    return logistic(score);
}

int main() {
    std::vector<Regime> regimes = {
        {"user_supportive_design", 0.55, 0, 0.08, 0.08, 0.35, 0.10},
        {"engagement_maximizing_design", 0.85, 1, 0.03, 0.22, 0.80, 0.45},
        {"friction_heavy_lock_in", 0.75, 1, 0.02, 0.60, 0.55, 0.60}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": "
                  << join_probability(regime) << std::endl;
    }

    return 0;
}
