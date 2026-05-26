package main

import "fmt"

func subjectiveProbability(trueProbability, availabilitySensitivity, availabilityScore, baseRateCorrection float64) float64 {
	p := trueProbability + availabilitySensitivity*availabilityScore*0.25 - baseRateCorrection
	if p < 0 {
		return 0
	}
	if p > 1 {
		return 1
	}
	return p
}

func main() {
	fmt.Printf("Synthetic subjective probability under availability bias: %.3f\n", subjectiveProbability(0.12, 0.70, 0.85, 0.04))
}
