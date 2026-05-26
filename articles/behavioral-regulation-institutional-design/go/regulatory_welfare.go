package main

import "fmt"

func totalWelfare(complianceUtility, complied, adminBurden, burdenSensitivity, sanctionStrength float64) float64 {
	socialBenefit := 0.90 * complied
	complianceCost := adminBurden * burdenSensitivity
	enforcementCost := 0.20 * sanctionStrength
	administrativeCost := 0.10 + 0.25*adminBurden

	return complianceUtility + socialBenefit - complianceCost - enforcementCost - administrativeCost
}

func main() {
	w := totalWelfare(0.70, 1.0, 0.10, 0.60, 0.55)
	fmt.Printf("Synthetic regulatory policy welfare: %.3f\n", w)
}
