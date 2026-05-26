#include <stdio.h>
#include <math.h>

double discounted_delayed_value(double beta, double delta, double reward, int delay) {
    return beta * pow(delta, delay) * reward;
}

int choose_delayed_reward(double beta, double delta, double delayed_reward, int delay, double immediate_reward, double commitment_cost) {
    double delayed_value = discounted_delayed_value(beta, delta, delayed_reward, delay);
    double immediate_value = immediate_reward - commitment_cost;
    return delayed_value >= immediate_value;
}

int main(void) {
    int choice = choose_delayed_reward(0.72, 0.97, 300.0, 12, 160.0, 70.0);
    printf("Synthetic delayed choice under present bias: %d\n", choice);
    return 0;
}
