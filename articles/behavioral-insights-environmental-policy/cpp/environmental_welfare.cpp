#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double subsidy;
    double friction;
};

double total_welfare(const Regime& r) {
    int adopted = 1;
    double private_benefit = 0.26;
    double environmental_benefit = 0.90;
    double admin_cost = 0.05 + 0.10 * r.friction;
    double friction_cost = 0.50 * r.friction;

    return adopted + private_benefit + environmental_benefit - r.subsidy - admin_cost - 0.20 * friction_cost;
}

int main() {
    std::vector<Regime> regimes = {
        {"price_signal_only", 0.08, 0.20},
        {"norm_plus_default", 0.00, 0.08},
        {"integrated_policy_design", 0.06, 0.08}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": " << total_welfare(regime) << std::endl;
    }

    return 0;
}
