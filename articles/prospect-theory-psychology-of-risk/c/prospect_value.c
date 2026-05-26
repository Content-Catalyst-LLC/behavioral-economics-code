#include <math.h>
#include <stdio.h>

double prospect_value(double x, double lambda_loss, double alpha_gain, double beta_loss) {
    if (x >= 0.0) {
        return pow(x, alpha_gain);
    }
    return -lambda_loss * pow(-x, beta_loss);
}

double probability_weight(double p, double gamma) {
    return pow(p, gamma) / pow(pow(p, gamma) + pow(1.0 - p, gamma), 1.0 / gamma);
}

int main(void) {
    double lambda_loss = 2.0;
    double alpha_gain = 0.88;
    double beta_loss = 0.88;
    double gamma = 0.70;

    double mixed_value = probability_weight(0.5, gamma) * prospect_value(240.0, lambda_loss, alpha_gain, beta_loss)
        + probability_weight(0.5, gamma) * prospect_value(-100.0, lambda_loss, alpha_gain, beta_loss);

    printf("Mixed gamble prospect value: %.4f\n", mixed_value);
    printf("Accept mixed gamble: %s\n", mixed_value > 0.0 ? "yes" : "no");

    return 0;
}
