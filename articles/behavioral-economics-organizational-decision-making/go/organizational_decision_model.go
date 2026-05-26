package main

import (
	"fmt"
	"math"
)

func logistic(x float64) float64 {
	return 1.0 / (1.0 + math.Exp(-x))
}

func approvalProbability(
	expectedPayoff float64,
	risk float64,
	sunkCost float64,
	prestigeValue float64,
	complexity float64,
	overconfidence float64,
	shortTermPressure float64,
	reviewStrength float64,
	longHorizonValue float64,
	longHorizonWeight float64,
) float64 {
	value := expectedPayoff +
		prestigeValue*shortTermPressure -
		risk -
		complexity +
		0.9*sunkCost +
		0.7*overconfidence -
		0.8*reviewStrength*sunkCost -
		0.5*reviewStrength*overconfidence +
		longHorizonWeight*longHorizonValue

	return logistic(value)
}

func main() {
	p := approvalProbability(0.14, 0.22, 0.31, 0.20, 0.35, 0.18, 0.70, 0.85, 0.26, 0.60)
	fmt.Printf("Synthetic approval probability: %.3f\n", p)
}
