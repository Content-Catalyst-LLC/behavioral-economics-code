#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double reward_intensity;
    double friction_asymmetry;
    double privacy_cost;
};

double user_welfare(const Regime& r) {
    double baseline_value = 0.45;
    double autonomy_preference = 0.58;
    double cognitive_overload = 0.42;

    return baseline_value + 0.35 * r.reward_intensity
        - 0.7 * std::max(r.friction_asymmetry, 0.0) * autonomy_preference
        - r.privacy_cost
        - 0.45 * cognitive_overload;
}

int main() {
    std::vector<Regime> regimes = {
        {"user_supportive_design", 0.35, 0.00, 0.05},
        {"engagement_maximizing_design", 0.80, 0.19, 0.20},
        {"friction_heavy_lock_in", 0.55, 0.58, 0.35}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": " << user_welfare(regime) << std::endl;
    }

    return 0;
}
