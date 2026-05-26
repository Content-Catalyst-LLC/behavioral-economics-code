#include <stdio.h>

double max_double(double a, double b) {
    return a > b ? a : b;
}

double fairness_reciprocity_utility(
    double self_payoff,
    double other_payoff,
    double fairness_sensitivity,
    double reciprocity_sensitivity,
    double reciprocity_signal,
    double process_fairness
) {
    double disadvantage_penalty = fairness_sensitivity * max_double(other_payoff - self_payoff, 0.0);
    double reciprocity_component = reciprocity_sensitivity * reciprocity_signal;
    double process_component = 0.30 * process_fairness;
    return self_payoff - disadvantage_penalty + reciprocity_component + process_component;
}

int main(void) {
    printf("Fairness-reciprocity utility: %.3f\n",
        fairness_reciprocity_utility(0.35, 0.65, 1.2, 1.0, 0.40, 0.70));
    return 0;
}
