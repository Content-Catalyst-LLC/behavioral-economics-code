package main

import (
	"fmt"
	"math"
)

func discountedFutureValue(beta, delta, benefit float64, periods int) float64 {
	return beta * math.Pow(delta, float64(periods)) * benefit
}

func chooseCommitment(beta, delta, futureBenefit, immediateTemptation, commitmentCost float64, periods int) bool {
	patientValue := discountedFutureValue(beta, delta, futureBenefit, periods)
	temptationValue := immediateTemptation - commitmentCost
	return patientValue >= temptationValue
}

func main() {
	fmt.Printf("Synthetic patient choice under commitment: %v\n", chooseCommitment(0.72, 0.97, 1000.0, 600.0, 300.0, 12))
}
