#include <iostream>
#include <string>
#include <vector>

struct Regime {
    std::string name;
    double admin_burden;
    double sanction_strength;
};

double total_welfare(const Regime& r) {
    double compliance_utility = 0.70;
    int complied = 1;
    double burden_sensitivity = 0.60;
    double social_benefit = 0.90 * complied;
    double compliance_cost = r.admin_burden * burden_sensitivity;
    double enforcement_cost = 0.20 * r.sanction_strength;
    double administrative_cost = 0.10 + 0.25 * r.admin_burden;

    return compliance_utility + social_benefit - compliance_cost - enforcement_cost - administrative_cost;
}

int main() {
    std::vector<Regime> regimes = {
        {"sanction_heavy_deterrence", 0.28, 0.85},
        {"simplification_plus_trust", 0.08, 0.35},
        {"integrated_behavioral_regulation", 0.10, 0.55}
    };

    for (const auto& regime : regimes) {
        std::cout << regime.name << ": " << total_welfare(regime) << std::endl;
    }

    return 0;
}
