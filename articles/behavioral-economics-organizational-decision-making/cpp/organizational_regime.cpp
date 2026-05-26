#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double short_term_pressure;
    double review_strength;
    double conformity_pressure;
    double long_horizon_weight;
};

double logistic(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

double approval_probability(const Regime& r) {
    double expected_payoff = 0.14;
    double risk = 0.22;
    double sunk_cost = 0.31;
    double prestige_value = 0.20;
    double complexity = 0.35;
    double overconfidence = 0.18;
    double long_horizon_value = 0.26;

    double value =
        expected_payoff +
        prestige_value * r.short_term_pressure -
        risk -
        complexity +
        0.9 * sunk_cost +
        0.7 * overconfidence -
        0.8 * r.review_strength * sunk_cost -
        0.5 * r.review_strength * overconfidence +
        r.long_horizon_weight * long_horizon_value;

    return logistic(value);
}

int main() {
    std::vector<Regime> regimes = {
        {"metric_heavy_short_termism", 1.30, 0.15, 0.65, 0.10},
        {"balanced_governance", 0.90, 0.55, 0.35, 0.35},
        {"high_accountability_adaptive_review", 0.70, 0.85, 0.20, 0.60}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": "
                  << approval_probability(regime) << std::endl;
    }

    return 0;
}
