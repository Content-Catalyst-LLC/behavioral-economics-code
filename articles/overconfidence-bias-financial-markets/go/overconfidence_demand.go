package main

import "fmt"

func investorDemand(expectedReturn, perceivedVariance, alpha, beta float64) float64 {
	return alpha*expectedReturn - beta*perceivedVariance
}

func netReturnAfterCost(grossReturn, tradingIntensity, costPerTurnover float64) float64 {
	return grossReturn - costPerTurnover*tradingIntensity
}

func main() {
	fmt.Printf("Synthetic investor demand: %.3f\n", investorDemand(0.08, 0.03, 1.2, 0.7))
	fmt.Printf("Synthetic net return after cost: %.3f\n", netReturnAfterCost(0.05, 1.4, 0.0025))
}
