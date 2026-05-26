package main

import "fmt"

func utilityStatusQuo(valueStatusQuo, statusQuoPremium float64) float64 {
	return valueStatusQuo + statusQuoPremium
}

func utilityAlternative(valueAlternative, switchCost, lossAversion, perceivedLoss float64) float64 {
	return valueAlternative - switchCost - lossAversion*perceivedLoss
}

func chooseAlternative(valueStatusQuo, valueAlternative, premium, switchCost, lossAversion, perceivedLoss float64) bool {
	return utilityAlternative(valueAlternative, switchCost, lossAversion, perceivedLoss) >= utilityStatusQuo(valueStatusQuo, premium)
}

func main() {
	fmt.Printf("Synthetic alternative adoption under status quo bias: %v\n", chooseAlternative(0.50, 0.68, 0.08, 0.05, 1.50, 0.04))
}
