package main

import (
	"fmt"
	"math"
)

func logistic(x float64) float64 {
	return 1.0 / (1.0 + math.Exp(-x))
}

func main() {
	value := 0.18
	defaultBonus := 0.20
	trust := 0.12
	effortCost := 0.22
	administrativeFriction := 0.75

	latent := value + defaultBonus + trust - administrativeFriction*effortCost
	fmt.Printf("policy_uptake_probability,%.4f\n", logistic(latent))
}
