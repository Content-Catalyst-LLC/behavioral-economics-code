#include <cmath>
#include <iostream>

double prospect_value(double x, double lambda_loss, double alpha_gain, double beta_loss) {
    if (x >= 0.0) {
        return std::pow(x, alpha_gain);
    }
    return -lambda_loss * std::pow(-x, beta_loss);
}

int main() {
    double lambda_loss = 2.0;
    double alpha_gain = 0.88;
    double beta_loss = 0.88;

    double mixed_value = 0.5 * prospect_value(240.0, lambda_loss, alpha_gain, beta_loss)
        + 0.5 * prospect_value(-100.0, lambda_loss, alpha_gain, beta_loss);

    std::cout << "Mixed gamble prospect value: " << mixed_value << std::endl;
    std::cout << "Accept mixed gamble: " << (mixed_value > 0.0 ? "yes" : "no") << std::endl;

    return 0;
}
