#include <math.h>
#include <stdio.h>

double crra_utility(double x, double rho) {
    if (fabs(rho - 1.0) < 1e-8) {
        return log(x);
    }
    return pow(x, 1.0 - rho) / (1.0 - rho);
}

int main(void) {
    double wealth = 50000.0;
    double rho = 1.5;

    double eu_certain = crra_utility(wealth + 100.0, rho);
    double eu_risky = 0.5 * crra_utility(wealth + 40.0, rho) + 0.5 * crra_utility(wealth + 220.0, rho);

    printf("EU certain: %.10f\n", eu_certain);
    printf("EU risky: %.10f\n", eu_risky);
    printf("Choose risky: %s\n", eu_risky > eu_certain ? "yes" : "no");

    return 0;
}
