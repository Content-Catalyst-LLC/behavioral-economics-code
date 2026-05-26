package main

import (
	"fmt"
	"math"
)

func fehrSchmidt(selfPayoff, otherPayoff, alpha, beta float64) float64 {
	return selfPayoff -
		alpha*math.Max(otherPayoff-selfPayoff, 0.0) -
		beta*math.Max(selfPayoff-otherPayoff, 0.0)
}

func main() {
	fmt.Printf("Fehr-Schmidt utility: %.3f\n", fehrSchmidt(0.30, 0.70, 1.5, 0.6))
}
