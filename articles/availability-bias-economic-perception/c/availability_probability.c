#include <stdio.h>

double subjective_probability(
    double true_probability,
    double availability_sensitivity,
    double availability_score,
    double base_rate_correction
) {
    double p = true_probability + availability_sensitivity * availability_score * 0.25 - base_rate_correction;
    if (p < 0.0) return 0.0;
    if (p > 1.0) return 1.0;
    return p;
}

int main(void) {
    double p = subjective_probability(0.12, 0.70, 0.85, 0.04);
    printf("Synthetic subjective probability under availability bias: %.3f\n", p);
    return 0;
}
