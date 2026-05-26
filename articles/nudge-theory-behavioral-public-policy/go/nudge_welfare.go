package main

import "fmt"

func totalWelfare(utility, adopted, frictionCost, adminCost, implementationCost float64) float64 {
	userBenefit := 0.50 * adopted
	socialBenefit := 0.40 * adopted

	return utility + userBenefit + socialBenefit - frictionCost - adminCost - implementationCost
}

func main() {
	w := totalWelfare(0.65, 1.0, 0.06, 0.05, 0.073)
	fmt.Printf("Synthetic nudge policy welfare: %.3f\n", w)
}
