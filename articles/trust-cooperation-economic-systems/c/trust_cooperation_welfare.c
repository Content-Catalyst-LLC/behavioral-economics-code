#include <stdio.h>

double trust_welfare(int trusted, int reciprocated, int punished, double support, double norms, double betrayal_cost, double monitoring_cost) {
    double transaction_cost_reduction = 0.30 * support + 0.25 * norms + 0.20 * trusted;
    double cooperative_benefit = trusted * 0.70 * reciprocated;
    double betrayal_loss = trusted * betrayal_cost * (1 - reciprocated);
    double punishment_value = 0.20 * punished;
    double institutional_cost = 0.05 * support;
    return cooperative_benefit + transaction_cost_reduction + punishment_value - betrayal_loss - monitoring_cost - institutional_cost;
}

int main(void) {
    printf("Synthetic trust and cooperation welfare: %.3f\n", trust_welfare(1, 1, 0, 0.80, 0.75, 0.35, 0.05));
    return 0;
}
