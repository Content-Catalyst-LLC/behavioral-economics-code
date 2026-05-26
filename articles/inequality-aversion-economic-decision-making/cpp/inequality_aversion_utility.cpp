#include <algorithm>
#include <iostream>

double fehr_schmidt(double self_payoff, double other_payoff, double alpha, double beta) {
    return self_payoff
        - alpha * std::max(other_payoff - self_payoff, 0.0)
        - beta * std::max(self_payoff - other_payoff, 0.0);
}

int main() {
    std::cout << "Fehr-Schmidt utility: " << fehr_schmidt(0.30, 0.70, 1.5, 0.6) << std::endl;
    return 0;
}
