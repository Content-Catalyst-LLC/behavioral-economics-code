#include <math.h>
#include <stdio.h>

double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    double value = 0.15;
    double default_bonus = 0.25;
    double effort_cost = 0.18;
    double effort_penalty = 0.80;
    double z = value + default_bonus - effort_penalty * effort_cost;
    printf("uptake_probability,%f\n", logistic(z));
    return 0;
}
