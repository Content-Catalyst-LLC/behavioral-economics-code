#include <stdio.h>

double user_welfare(
    int joined,
    double baseline_value,
    double reward_intensity,
    double friction_asymmetry,
    double autonomy_preference,
    double privacy_cost,
    double cognitive_overload
) {
    double autonomy_cost = 0.0;
    if (friction_asymmetry > 0.0) {
        autonomy_cost = 0.7 * friction_asymmetry * autonomy_preference;
    }

    return joined * (baseline_value + 0.35 * reward_intensity)
           - autonomy_cost
           - privacy_cost
           - 0.45 * cognitive_overload;
}

int main(void) {
    double w = user_welfare(1, 0.45, 0.35, 0.0, 0.58, 0.05, 0.42);
    printf("Synthetic user welfare: %.3f\n", w);
    return 0;
}
