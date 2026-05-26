#include <stdio.h>

int main(void) {
    double values[] = {0.20, 0.35, 0.62, 0.75, 0.91, 0.55};
    int n = 6;
    double aspiration = 0.70;
    double search_cost = 0.02;

    double optimal = values[0];
    for (int i = 1; i < n; i++) {
        if (values[i] > optimal) {
            optimal = values[i];
        }
    }

    int chosen_index = n;
    double chosen_value = values[n - 1];

    for (int i = 0; i < n; i++) {
        if (values[i] >= aspiration) {
            chosen_index = i + 1;
            chosen_value = values[i];
            break;
        }
    }

    double net_value = chosen_value - search_cost * chosen_index;

    printf("Chosen index: %d\n", chosen_index);
    printf("Chosen value: %.3f\n", chosen_value);
    printf("Optimal value: %.3f\n", optimal);
    printf("Net value: %.3f\n", net_value);
    printf("Optimization gap: %.3f\n", optimal - chosen_value);

    return 0;
}
