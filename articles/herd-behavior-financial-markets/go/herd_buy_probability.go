package main

import (
	"fmt"
	"math"
)

func logistic(x float64) float64 {
	return 1.0 / (1.0 + math.Exp(-x))
}

func buyProbability(fundamental, privateSignal, herdSignal, perceivedRisk, alpha, beta, gamma float64) float64 {
	utility := fundamental + alpha*privateSignal + beta*herdSignal - gamma*perceivedRisk
	return logistic(utility)
}

func main() {
	fmt.Printf("Synthetic herd buy probability: %.3f\n", buyProbability(0.15, 0.20, 0.70, 0.10, 1.0, 1.4, 0.8))
}
