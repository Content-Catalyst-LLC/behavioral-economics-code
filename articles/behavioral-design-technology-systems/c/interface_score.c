#include <math.h>
#include <stdio.h>

double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

double join_probability(
    double baseline_value,
    double salience_sensitivity,
    double default_sensitivity,
    double friction_sensitivity,
    double reward_sensitivity,
    double cognitive_overload,
    double salience,
    double default_on,
    double entry_friction,
    double reward_intensity
) {
    double score =
        baseline_value +
        salience_sensitivity * salience +
        default_sensitivity * default_on -
        friction_sensitivity * entry_friction +
        reward_sensitivity * reward_intensity -
        cognitive_overload * 0.4;

    return logistic(score);
}

int main(void) {
    double p = join_probability(0.45, 0.55, 0.50, 0.60, 0.58, 0.42, 0.55, 0, 0.08, 0.35);
    printf("Synthetic join probability: %.3f\n", p);
    return 0;
}
