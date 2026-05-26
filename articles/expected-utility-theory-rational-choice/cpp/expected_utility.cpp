#include <cmath>
#include <iostream>
#include <string>

double crra_utility(double x, double rho) {
    if (std::abs(rho - 1.0) < 1e-8) {
        return std::log(x);
    }
    return std::pow(x, 1.0 - rho) / (1.0 - rho);
}

int main() {
    double wealth = 50000.0;
    double rho = 1.5;

    double eu_certain = crra_utility(wealth + 100.0, rho);
    double eu_risky = 0.5 * crra_utility(wealth + 40.0, rho) + 0.5 * crra_utility(wealth + 220.0, rho);

    std::cout << "EU certain: " << eu_certain << std::endl;
    std::cout << "EU risky: " << eu_risky << std::endl;
    std::cout << "Choose risky: " << (eu_risky > eu_certain ? "yes" : "no") << std::endl;

    return 0;
}
