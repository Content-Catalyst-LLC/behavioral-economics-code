package main

import "fmt"

func realizedWelfare(longRunValue, complexitySensitivity, complexity, switchingSensitivity, switchingCost, digitalLiteracy float64) float64 {
	return longRunValue -
		complexitySensitivity*complexity -
		switchingSensitivity*switchingCost +
		0.03*digitalLiteracy
}

func main() {
	w := realizedWelfare(0.42, 0.60, 0.08, 0.52, 0.04, 0.62)
	fmt.Printf("Synthetic choice architecture welfare: %.3f\n", w)
}
