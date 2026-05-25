#include <math.h>
#include <stdio.h>

double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

double compliance_probability(
    double trust,
    double salience,
    double norm_sensitivity,
    double burden_sensitivity,
    double present_bias,
    double admin_burden,
    double reminder_salience,
    double trust_signal,
    double penalty_strength
) {
    double utility =
        0.8 * reminder_salience * salience +
        0.7 * norm_sensitivity +
        1.0 * trust_signal * trust +
        0.9 * penalty_strength -
        1.2 * admin_burden * burden_sensitivity -
        0.7 * present_bias * admin_burden;

    return logistic(utility - 0.5);
}

int main(void) {
    double p = compliance_probability(0.60, 0.55, 0.45, 0.60, 0.35, 0.12, 0.80, 0.80, 0.30);
    printf("Synthetic compliance probability: %.3f\n", p);
    return 0;
}
