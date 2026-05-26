#include <stdio.h>

double realized_welfare(
    double long_run_value,
    double complexity_sensitivity,
    double complexity,
    double switching_sensitivity,
    double switching_cost,
    double digital_literacy
) {
    return long_run_value
           - complexity_sensitivity * complexity
           - switching_sensitivity * switching_cost
           + 0.03 * digital_literacy;
}

int main(void) {
    double w = realized_welfare(0.42, 0.60, 0.08, 0.52, 0.04, 0.62);
    printf("Synthetic choice architecture welfare: %.3f\n", w);
    return 0;
}
