package main

import (
	"fmt"
	"math"
)

func logistic(x float64) float64 {
	return 1.0 / (1.0 + math.Exp(-x))
}

func complianceProbability(
	trust float64,
	salience float64,
	normSensitivity float64,
	burdenSensitivity float64,
	presentBias float64,
	adminBurden float64,
	reminderSalience float64,
	trustSignal float64,
	penaltyStrength float64,
) float64 {
	utility := 0.8*reminderSalience*salience +
		0.7*normSensitivity +
		1.0*trustSignal*trust +
		0.9*penaltyStrength -
		1.2*adminBurden*burdenSensitivity -
		0.7*presentBias*adminBurden

	return logistic(utility - 0.5)
}

func main() {
	p := complianceProbability(0.60, 0.55, 0.45, 0.60, 0.35, 0.12, 0.80, 0.80, 0.30)
	fmt.Printf("Synthetic compliance probability: %.3f\n", p)
}
