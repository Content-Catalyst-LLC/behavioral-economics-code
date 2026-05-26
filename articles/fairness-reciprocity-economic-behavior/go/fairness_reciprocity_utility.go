package main

import (
	"fmt"
	"math"
)

func fairnessReciprocityUtility(selfPayoff, otherPayoff, fairnessSensitivity, reciprocitySensitivity, reciprocitySignal, processFairness float64) float64 {
	disadvantagePenalty := fairnessSensitivity * math.Max(otherPayoff-selfPayoff, 0.0)
	reciprocityComponent := reciprocitySensitivity * reciprocitySignal
	processComponent := 0.30 * processFairness
	return selfPayoff - disadvantagePenalty + reciprocityComponent + processComponent
}

func main() {
	fmt.Printf("Fairness-reciprocity utility: %.3f\n", fairnessReciprocityUtility(0.35, 0.65, 1.2, 1.0, 0.40, 0.70))
}
