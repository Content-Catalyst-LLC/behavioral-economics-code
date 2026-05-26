package main

import (
	"fmt"
	"math"
)

func prospectValue(x, lambda, eta float64) float64 {
	if x >= 0 {
		return math.Pow(x, eta)
	}
	return -lambda * math.Pow(-x, eta)
}

func chooseRiskyGainFrame(lambda, eta, frameShift float64) bool {
	certain := prospectValue(200.0, lambda, eta)
	risky := (1.0/3.0)*prospectValue(600.0, lambda, eta) + (2.0/3.0)*prospectValue(0.0, lambda, eta)
	return risky+frameShift >= certain
}

func main() {
	fmt.Printf("Synthetic risky choice under gain frame: %v\n", chooseRiskyGainFrame(2.0, 0.88, -10.0))
}
