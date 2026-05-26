#include <stdio.h>

double total_welfare(
    int adopted,
    double private_benefit,
    double environmental_benefit,
    double fiscal_cost,
    double admin_cost,
    double friction_cost
) {
    return adopted + private_benefit + environmental_benefit - fiscal_cost - admin_cost - 0.20 * friction_cost;
}

int main(void) {
    double w = total_welfare(1, 0.26, 0.90, 0.06, 0.058, 0.04);
    printf("Synthetic environmental policy welfare: %.3f\n", w);
    return 0;
}
