package main

import (
	"fmt"
	"math"
)

func crraUtility(x, rho float64) float64 {
	if math.Abs(rho-1.0) < 1e-8 {
		return math.Log(x)
	}
	return math.Pow(x, 1.0-rho) / (1.0 - rho)
}

func main() {
	wealth := 50000.0
	rho := 1.5

	euCertain := crraUtility(wealth+100.0, rho)
	euRisky := 0.5*crraUtility(wealth+40.0, rho) + 0.5*crraUtility(wealth+220.0, rho)

	fmt.Printf("EU certain: %.10f\n", euCertain)
	fmt.Printf("EU risky: %.10f\n", euRisky)
	if euRisky > euCertain {
		fmt.Println("Choose risky: yes")
	} else {
		fmt.Println("Choose risky: no")
	}
}
