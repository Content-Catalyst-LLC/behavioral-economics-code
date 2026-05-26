package main

import "fmt"

func totalWelfare(adopted, privateBenefit, environmentalBenefit, fiscalCost, adminCost, frictionCost float64) float64 {
	return adopted + privateBenefit + environmentalBenefit - fiscalCost - adminCost - 0.20*frictionCost
}

func main() {
	w := totalWelfare(1.0, 0.26, 0.90, 0.06, 0.058, 0.04)
	fmt.Printf("Synthetic environmental policy welfare: %.3f\n", w)
}
