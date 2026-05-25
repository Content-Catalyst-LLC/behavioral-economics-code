#include <cmath>
#include <iostream>
#include <vector>

struct Agent {
    double income;
    double environmental_concern;
    double present_bias;
    double loss_aversion;
    double norm_sensitivity;
    double friction_sensitivity;
    double quality_uncertainty;
    double infrastructure_access;
};

double adoption_probability(
    const Agent& a,
    double subsidy,
    int default_green,
    double norm_signal,
    double friction
) {
    double effective_premium = std::max(0.10 - subsidy, 0.0);
    double affordability = 1.0 / std::log(a.income);

    double immediate_cost = effective_premium * affordability * 100.0
        + friction * a.friction_sensitivity;

    double utility_diff =
        -0.65
        + 1.10 * a.environmental_concern
        + 0.72 * default_green
        + 0.85 * a.norm_sensitivity * norm_signal
        + 0.55 * a.infrastructure_access
        - 1.75 * immediate_cost
        - 0.38 * a.present_bias
        - 0.35 * a.loss_aversion * effective_premium
        - 0.62 * a.quality_uncertainty;

    return 1.0 / (1.0 + std::exp(-utility_diff));
}

int main() {
    std::vector<Agent> agents = {
        {45000, 0.55, 0.35, 2.1, 0.50, 0.60, 0.35, 0.40},
        {90000, 0.75, 0.20, 1.8, 0.65, 0.40, 0.20, 0.80}
    };

    for (const auto& a : agents) {
        std::cout << adoption_probability(a, 0.05, 1, 0.70, 0.08) << "\n";
    }

    return 0;
}
