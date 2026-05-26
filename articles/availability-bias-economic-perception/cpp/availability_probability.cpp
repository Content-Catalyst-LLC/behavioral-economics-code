#include <algorithm>
#include <iostream>

double subjective_probability(
    double true_probability,
    double availability_sensitivity,
    double availability_score,
    double base_rate_correction
) {
    double p = true_probability + availability_sensitivity * availability_score * 0.25 - base_rate_correction;
    return std::clamp(p, 0.0, 1.0);
}

int main() {
    std::cout << "Synthetic subjective probability under availability bias: "
              << subjective_probability(0.12, 0.70, 0.85, 0.04)
              << std::endl;
    return 0;
}
