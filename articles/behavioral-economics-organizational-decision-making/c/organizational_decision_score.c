#include <math.h>
#include <stdio.h>

double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

double approval_probability(
    double expected_payoff,
    double risk,
    double sunk_cost,
    double prestige_value,
    double complexity,
    double overconfidence,
    double short_term_pressure,
    double review_strength,
    double long_horizon_value,
    double long_horizon_weight
) {
    double perceived_value =
        expected_payoff +
        prestige_value * short_term_pressure -
        risk -
        complexity +
        0.9 * sunk_cost +
        0.7 * overconfidence -
        0.8 * review_strength * sunk_cost -
        0.5 * review_strength * overconfidence +
        long_horizon_weight * long_horizon_value;

    return logistic(perceived_value);
}

int main(void) {
    double p = approval_probability(0.14, 0.22, 0.31, 0.20, 0.35, 0.18, 0.7, 0.85, 0.26, 0.60);
    printf("Synthetic approval probability: %.3f\n", p);
    return 0;
}
