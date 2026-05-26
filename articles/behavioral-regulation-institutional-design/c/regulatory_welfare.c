#include <stdio.h>

double total_welfare(
    double compliance_utility,
    int complied,
    double admin_burden,
    double burden_sensitivity,
    double sanction_strength
) {
    double social_benefit = 0.90 * complied;
    double compliance_cost = admin_burden * burden_sensitivity;
    double enforcement_cost = 0.20 * sanction_strength;
    double administrative_cost = 0.10 + 0.25 * admin_burden;

    return compliance_utility + social_benefit - compliance_cost - enforcement_cost - administrative_cost;
}

int main(void) {
    double w = total_welfare(0.70, 1, 0.10, 0.60, 0.55);
    printf("Synthetic regulatory policy welfare: %.3f\n", w);
    return 0;
}
