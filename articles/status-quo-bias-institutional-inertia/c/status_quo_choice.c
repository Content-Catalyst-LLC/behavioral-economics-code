#include <stdio.h>

double utility_status_quo(double value_status_quo, double status_quo_premium) {
    return value_status_quo + status_quo_premium;
}

double utility_alternative(double value_alternative, double switch_cost, double loss_aversion, double perceived_loss) {
    return value_alternative - switch_cost - loss_aversion * perceived_loss;
}

int choose_alternative(double value_status_quo, double value_alternative, double premium, double switch_cost, double loss_aversion, double perceived_loss) {
    return utility_alternative(value_alternative, switch_cost, loss_aversion, perceived_loss)
        >= utility_status_quo(value_status_quo, premium);
}

int main(void) {
    int adoption = choose_alternative(0.50, 0.68, 0.08, 0.05, 1.50, 0.04);
    printf("Synthetic alternative adoption under status quo bias: %d\n", adoption);
    return 0;
}
