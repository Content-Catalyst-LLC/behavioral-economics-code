#include <stdio.h>

double debt_repayment_gain(double debt_interest_rate, double savings_rate, double repayment_amount) {
    return (debt_interest_rate - savings_rate) * repayment_amount;
}

int repay_debt_from_labeled_savings(double debt_interest_rate, double savings_rate, double repayment_amount, double label_penalty) {
    double gain = debt_repayment_gain(debt_interest_rate, savings_rate, repayment_amount);
    return gain > label_penalty;
}

int main(void) {
    int decision = repay_debt_from_labeled_savings(0.22, 0.02, 1000.0, 150.0);
    printf("Repay debt from labeled savings: %d\n", decision);
    return 0;
}
