package main

import "fmt"

func anchoredEstimate(anchor, trueValue, adjustmentRate float64) float64 {
	return anchor + adjustmentRate*(trueValue-anchor)
}

func anchoringBias(anchor, trueValue, adjustmentRate float64) float64 {
	return anchoredEstimate(anchor, trueValue, adjustmentRate) - trueValue
}

func main() {
	fmt.Printf("Anchored estimate: %.2f\n", anchoredEstimate(85.0, 65.0, 0.55))
	fmt.Printf("Anchoring bias: %.2f\n", anchoringBias(85.0, 65.0, 0.55))
}
