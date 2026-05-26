#include <iostream>

double anchored_estimate(double anchor, double true_value, double adjustment_rate) {
    return anchor + adjustment_rate * (true_value - anchor);
}

double anchoring_bias(double anchor, double true_value, double adjustment_rate) {
    return anchored_estimate(anchor, true_value, adjustment_rate) - true_value;
}

int main() {
    std::cout << "Anchored estimate: " << anchored_estimate(85.0, 65.0, 0.55) << std::endl;
    std::cout << "Anchoring bias: " << anchoring_bias(85.0, 65.0, 0.55) << std::endl;
    return 0;
}
