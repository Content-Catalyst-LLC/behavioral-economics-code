#include <cmath>
#include <iostream>
#include <vector>

double prospect_value(double x, double alpha = 0.88, double beta = 0.88, double lambda = 2.25) {
    if (x >= 0.0) {
        return std::pow(x, alpha);
    }
    return -lambda * std::pow(-x, beta);
}

int main() {
    std::vector<double> outcomes = {-100, -50, -10, 0, 10, 50, 100};
    std::cout << "outcome,prospect_value\n";
    for (double x : outcomes) {
        std::cout << x << "," << prospect_value(x) << "\n";
    }
    return 0;
}
