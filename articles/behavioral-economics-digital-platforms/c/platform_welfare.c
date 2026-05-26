#include <stdio.h>

double user_welfare(
    int clicked,
    double exposure_quality,
    double cognitive_overload,
    double privacy_sensitivity,
    double data_extraction_intensity,
    int consented,
    double friction
) {
    return clicked * exposure_quality
           - 0.30 * cognitive_overload
           - 0.45 * privacy_sensitivity * data_extraction_intensity * consented
           - 0.15 * friction;
}

int main(void) {
    double w = user_welfare(1, 0.52, 0.42, 0.55, 0.10, 1, 0.18);
    printf("Synthetic platform user welfare: %.3f\n", w);
    return 0;
}
