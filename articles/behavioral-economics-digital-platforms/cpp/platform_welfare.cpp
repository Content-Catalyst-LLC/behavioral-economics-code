#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double exposure_quality;
    double data_extraction;
    double friction;
};

double user_welfare(const Regime& r) {
    double cognitive_overload = 0.42;
    double privacy_sensitivity = 0.55;
    int clicked = 1;
    int consented = 1;

    return clicked * r.exposure_quality
        - 0.30 * cognitive_overload
        - 0.45 * privacy_sensitivity * r.data_extraction * consented
        - 0.15 * r.friction;
}

int main() {
    std::vector<Regime> regimes = {
        {"neutral_discovery", 0.52, 0.10, 0.18},
        {"engagement_optimized", 0.48, 0.45, 0.10},
        {"socially_amplified_ranking", 0.50, 0.35, 0.12}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": " << user_welfare(regime) << std::endl;
    }

    return 0;
}
