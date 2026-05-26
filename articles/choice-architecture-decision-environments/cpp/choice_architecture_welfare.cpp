#include <iostream>
#include <string>
#include <vector>

struct ArchitectureRegime {
    std::string name;
    double complexity;
    double switching_cost;
};

double realized_welfare(const ArchitectureRegime& r) {
    double long_run_value = 0.42;
    double complexity_sensitivity = 0.60;
    double switching_sensitivity = 0.52;
    double digital_literacy = 0.62;

    return long_run_value
        - complexity_sensitivity * r.complexity
        - switching_sensitivity * r.switching_cost
        + 0.03 * digital_literacy;
}

int main() {
    std::vector<ArchitectureRegime> regimes = {
        {"neutral_presentation", 0.20, 0.05},
        {"default_heavy_architecture", 0.12, 0.02},
        {"low_complexity_guided_design", 0.08, 0.04}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": " << realized_welfare(regime) << std::endl;
    }

    return 0;
}
