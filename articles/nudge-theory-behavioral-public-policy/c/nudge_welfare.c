#include <stdio.h>

double total_welfare(
    double utility,
    int adopted,
    double friction_cost,
    double admin_cost,
    double implementation_cost
) {
    double user_benefit = 0.50 * adopted;
    double social_benefit = 0.40 * adopted;

    return utility + user_benefit + social_benefit - friction_cost - admin_cost - implementation_cost;
}

int main(void) {
    double w = total_welfare(0.65, 1, 0.06, 0.05, 0.073);
    printf("Synthetic nudge policy welfare: %.3f\n", w);
    return 0;
}
