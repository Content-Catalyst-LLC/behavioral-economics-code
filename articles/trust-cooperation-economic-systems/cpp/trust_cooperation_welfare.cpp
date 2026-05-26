#include <iostream>
int main() {
    double support = 0.80, norms = 0.75, betrayal_cost = 0.35, monitoring_cost = 0.05;
    double welfare = 0.70 + (0.30 * support + 0.25 * norms + 0.20) - monitoring_cost - (0.05 * support);
    std::cout << "Synthetic trust and cooperation welfare: " << welfare << std::endl;
    return 0;
}
