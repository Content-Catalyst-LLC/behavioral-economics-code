#include <stdio.h>

double max_double(double a, double b) {
    return a > b ? a : b;
}

double fehr_schmidt(double self_payoff, double other_payoff, double alpha, double beta) {
    return self_payoff
           - alpha * max_double(other_payoff - self_payoff, 0.0)
           - beta * max_double(self_payoff - other_payoff, 0.0);
}

int main(void) {
    printf("Fehr-Schmidt utility: %.3f\n", fehr_schmidt(0.30, 0.70, 1.5, 0.6));
    return 0;
}
