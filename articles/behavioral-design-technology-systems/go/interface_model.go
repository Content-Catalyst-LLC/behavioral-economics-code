package main

import (
	"fmt"
	"math"
)

func logistic(x float64) float64 {
	return 1.0 / (1.0 + math.Exp(-x))
}

func joinProbability(
	baselineValue float64,
	salienceSensitivity float64,
	defaultSensitivity float64,
	frictionSensitivity float64,
	rewardSensitivity float64,
	cognitiveOverload float64,
	salience float64,
	defaultOn float64,
	entryFriction float64,
	rewardIntensity float64,
) float64 {
	score := baselineValue +
		salienceSensitivity*salience +
		defaultSensitivity*defaultOn -
		frictionSensitivity*entryFriction +
		rewardSensitivity*rewardIntensity -
		cognitiveOverload*0.4

	return logistic(score)
}

func main() {
	p := joinProbability(0.45, 0.55, 0.50, 0.60, 0.58, 0.42, 0.55, 0.0, 0.08, 0.35)
	fmt.Printf("Synthetic join probability: %.3f\n", p)
}
