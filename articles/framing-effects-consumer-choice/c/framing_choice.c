#include <stdio.h>
#include <math.h>

double prospect_value(double x, double lambda, double eta) {
    if (x >= 0.0) {
        return pow(x, eta);
    }
    return -lambda * pow(-x, eta);
}

int choose_risky_gain_frame(double lambda, double eta, double frame_shift) {
    double certain = prospect_value(200.0, lambda, eta);
    double risky = (1.0/3.0) * prospect_value(600.0, lambda, eta) + (2.0/3.0) * prospect_value(0.0, lambda, eta);
    return (risky + frame_shift) >= certain;
}

int main(void) {
    int choice = choose_risky_gain_frame(2.0, 0.88, -10.0);
    printf("Synthetic risky choice under gain frame: %d\n", choice);
    return 0;
}
