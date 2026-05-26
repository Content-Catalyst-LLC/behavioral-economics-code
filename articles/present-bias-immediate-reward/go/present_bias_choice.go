package main

import (
	"fmt"
	"math"
)

func discountedDelayedValue(beta, delta, reward float64, delay int) float64 {
	return beta * math.Pow(delta, float64(delay)) * reward
}

func chooseDelayedReward(beta, delta, delayedReward float64, delay int, immediateReward, commitmentCost float64) bool {
	delayedValue := discountedDelayedValue(beta, delta, delayedReward, delay)
	immediateValue := immediateReward - commitmentCost
	return delayedValue >= immediateValue
}

func main() {
	fmt.Printf("Synthetic delayed choice under present bias: %v\n", chooseDelayedReward(0.72, 0.97, 300.0, 12, 160.0, 70.0))
}
