#include <stdio.h>

double behavioral_demand(double expected_return, double perceived_variance, double behavioral_term, double alpha, double beta, double gamma) {
    return alpha * expected_return - beta * perceived_variance + gamma * behavioral_term;
}

double net_return_after_turnover(double gross_return, double turnover, double cost_per_turnover) {
    return gross_return - cost_per_turnover * turnover;
}

int main(void) {
    double demand = behavioral_demand(0.08, 0.03, 0.40, 1.2, 0.7, 0.5);
    double net = net_return_after_turnover(0.05, 1.4, 0.0025);
    printf("Synthetic behavioral demand: %.3f\n", demand);
    printf("Synthetic net return after turnover: %.3f\n", net);
    return 0;
}
