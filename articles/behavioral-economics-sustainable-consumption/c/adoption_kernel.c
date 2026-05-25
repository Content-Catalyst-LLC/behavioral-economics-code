#include <math.h>
#include <stdio.h>

typedef struct {
    double income;
    double environmental_concern;
    double present_bias;
    double loss_aversion;
    double norm_sensitivity;
    double friction_sensitivity;
    double quality_uncertainty;
    double infrastructure_access;
} Agent;

double adoption_probability(Agent a, double subsidy, int default_green, double norm_signal, double friction) {
    double effective_premium = fmax(0.10 - subsidy, 0.0);
    double affordability = 1.0 / log(a.income);
    double immediate_cost = effective_premium * affordability * 100.0 + friction * a.friction_sensitivity;

    double utility_diff =
        -0.65
        + 1.10 * a.environmental_concern
        + 0.72 * default_green
        + 0.85 * a.norm_sensitivity * norm_signal
        + 0.55 * a.infrastructure_access
        - 1.75 * immediate_cost
        - 0.38 * a.present_bias
        - 0.35 * a.loss_aversion * effective_premium
        - 0.62 * a.quality_uncertainty;

    return 1.0 / (1.0 + exp(-utility_diff));
}

int main(void) {
    Agent a = {65000, 0.62, 0.28, 2.0, 0.55, 0.50, 0.25, 0.60};
    printf("%0.6f\n", adoption_probability(a, 0.05, 1, 0.70, 0.08));
    return 0;
}
