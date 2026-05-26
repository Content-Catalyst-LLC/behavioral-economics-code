#include <iostream>
#include <string>
#include <vector>

struct NudgeRegime {
    std::string name;
    double friction;
    double administrative_burden;
    double implementation_cost;
};

double total_welfare(const NudgeRegime& r) {
    double utility = 0.65;
    int adopted = 1;
    double user_benefit = 0.50 * adopted;
    double social_benefit = 0.40 * adopted;
    double friction_cost = r.friction * 0.60;
    double admin_cost = r.administrative_burden * 0.58;

    return utility + user_benefit + social_benefit - friction_cost - admin_cost - r.implementation_cost;
}

int main() {
    std::vector<NudgeRegime> regimes = {
        {"information_only", 0.22, 0.25, 0.045},
        {"reminder_plus_norm", 0.12, 0.15, 0.075},
        {"default_plus_reminder", 0.10, 0.10, 0.073}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": " << total_welfare(regime) << std::endl;
    }

    return 0;
}
