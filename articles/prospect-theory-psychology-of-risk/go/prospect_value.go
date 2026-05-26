package main

import (
	"fmt"
	"math"
)

func prospectValue(x, lambdaLoss, alphaGain, betaLoss float64) float64 {
	if x >= 0.0 {
		return math.Pow(x, alphaGain)
	}
	return -lambdaLoss * math.Pow(-x, betaLoss)
}

func probabilityWeight(p, gamma float64) float64 {
	return math.Pow(p, gamma) / math.Pow(math.Pow(p, gamma)+math.Pow(1.0-p, gamma), 1.0/gamma)
}

func main() {
	lambdaLoss := 2.0
	alphaGain := 0.88
	betaLoss := 0.88
	gamma := 0.70

	mixedValue := probabilityWeight(0.5, gamma)*prospectValue(240.0, lambdaLoss, alphaGain, betaLoss) +
		probabilityWeight(0.5, gamma)*prospectValue(-100.0, lambdaLoss, alphaGain, betaLoss)

	fmt.Printf("Mixed gamble prospect value: %.4f\n", mixedValue)
	if mixedValue > 0.0 {
		fmt.Println("Accept mixed gamble: yes")
	} else {
		fmt.Println("Accept mixed gamble: no")
	}
}
