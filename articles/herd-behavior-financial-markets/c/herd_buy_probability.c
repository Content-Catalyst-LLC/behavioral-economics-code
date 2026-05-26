#include <math.h>
#include <stdio.h>

double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

double buy_probability(double fundamental, double private_signal, double herd_signal, double perceived_risk, double alpha, double beta, double gamma) {
    double utility = fundamental + alpha * private_signal + beta * herd_signal - gamma * perceived_risk;
    return logistic(utility);
}

int main(void) {
    double p = buy_probability(0.15, 0.20, 0.70, 0.10, 1.0, 1.4, 0.8);
    printf("Synthetic herd buy probability: %.3f\n", p);
    return 0;
}
