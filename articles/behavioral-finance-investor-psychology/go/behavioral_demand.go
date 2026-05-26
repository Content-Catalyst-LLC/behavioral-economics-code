package main

import "fmt"

func behavioralDemand(expectedReturn, perceivedVariance, behavioralTerm, alpha, beta, gamma float64) float64 {
	return alpha*expectedReturn - beta*perceivedVariance + gamma*behavioralTerm
}

func netReturnAfterTurnover(grossReturn, turnover, costPerTurnover float64) float64 {
	return grossReturn - costPerTurnover*turnover
}

func main() {
	fmt.Printf("Synthetic behavioral demand: %.3f\n", behavioralDemand(0.08, 0.03, 0.40, 1.2, 0.7, 0.5))
	fmt.Printf("Synthetic net return after turnover: %.3f\n", netReturnAfterTurnover(0.05, 1.4, 0.0025))
}
