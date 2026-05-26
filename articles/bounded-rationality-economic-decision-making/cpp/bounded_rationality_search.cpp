#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<double> values = {0.20, 0.35, 0.62, 0.75, 0.91, 0.55};
    double aspiration = 0.70;
    double search_cost = 0.02;

    double optimal = *std::max_element(values.begin(), values.end());

    int chosen_index = static_cast<int>(values.size());
    double chosen_value = values.back();

    for (std::size_t i = 0; i < values.size(); ++i) {
        if (values[i] >= aspiration) {
            chosen_index = static_cast<int>(i + 1);
            chosen_value = values[i];
            break;
        }
    }

    double net_value = chosen_value - search_cost * chosen_index;

    std::cout << "Chosen index: " << chosen_index << std::endl;
    std::cout << "Chosen value: " << chosen_value << std::endl;
    std::cout << "Optimal value: " << optimal << std::endl;
    std::cout << "Net value: " << net_value << std::endl;
    std::cout << "Optimization gap: " << optimal - chosen_value << std::endl;

    return 0;
}
