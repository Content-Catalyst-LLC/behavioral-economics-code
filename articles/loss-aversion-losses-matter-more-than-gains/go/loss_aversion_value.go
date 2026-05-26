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

func main() {
	lambdaLoss := 2.0
	alphaGain := 0.88
	betaLoss := 0.88

	mixedValue := 0.5*prospectValue(240.0, lambdaLoss, alphaGain, betaLoss) +
		0.5*prospectValue(-100.0, lambdaLoss, alphaGain, betaLoss)

	fmt.Printf("Mixed gamble prospect value: %.4f\n", mixedValue)
	if mixedValue > 0.0 {
		fmt.Println("Accept mixed gamble: yes")
	} else {
		fmt.Println("Accept mixed gamble: no")
	}
}
