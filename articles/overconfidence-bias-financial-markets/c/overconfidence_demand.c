#include <stdio.h>

double investor_demand(double expected_return, double perceived_variance, double alpha, double beta) {
    return alpha * expected_return - beta * perceived_variance;
}

double net_return_after_cost(double gross_return, double trading_intensity, double cost_per_turnover) {
    return gross_return - cost_per_turnover * trading_intensity;
}

int main(void) {
    double demand = investor_demand(0.08, 0.03, 1.2, 0.7);
    double net = net_return_after_cost(0.05, 1.4, 0.0025);
    printf("Synthetic investor demand: %.3f\n", demand);
    printf("Synthetic net return after cost: %.3f\n", net);
    return 0;
}
