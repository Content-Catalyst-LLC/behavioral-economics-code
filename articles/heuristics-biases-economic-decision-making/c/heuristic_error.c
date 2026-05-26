#include <stdio.h>
#include <math.h>

double heuristic_estimate(
    double true_value,
    double availability_weight,
    double availability_signal,
    double representativeness_weight,
    double representativeness_signal,
    double anchor_weight,
    double anchor_signal,
    double framing_weight,
    double framing_signal,
    double correction_capacity
) {
    double raw_error =
        availability_weight * availability_signal +
        representativeness_weight * representativeness_signal +
        anchor_weight * anchor_signal +
        framing_weight * framing_signal;

    double estimate = true_value + raw_error * (1.0 - correction_capacity);

    if (estimate < 0.0) return 0.0;
    if (estimate > 1.0) return 1.0;
    return estimate;
}

int main(void) {
    double estimate = heuristic_estimate(0.35, 0.30, 0.10, 0.25, -0.05, 0.40, 0.12, 0.20, -0.08, 0.55);
    printf("Synthetic heuristic estimate: %.3f\n", estimate);
    printf("Synthetic judgment error: %.3f\n", estimate - 0.35);
    return 0;
}
