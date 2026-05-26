#include <stdio.h>
#include <math.h>

double discounted_future_value(double beta, double delta, double benefit, int periods) {
    return beta * pow(delta, periods) * benefit;
}

int choose_commitment(double beta, double delta, double future_benefit, double immediate_temptation, double commitment_cost, int periods) {
    double patient_value = discounted_future_value(beta, delta, future_benefit, periods);
    double temptation_value = immediate_temptation - commitment_cost;
    return patient_value >= temptation_value;
}

int main(void) {
    int patient_choice = choose_commitment(0.72, 0.97, 1000.0, 600.0, 300.0, 12);
    printf("Synthetic patient choice under commitment: %d\n", patient_choice);
    return 0;
}
