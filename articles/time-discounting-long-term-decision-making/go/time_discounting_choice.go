package main

import (
	"fmt"
	"math"
)

func presentValue(futureValue, discountRate float64, periods int) float64 {
	return futureValue / math.Pow(1.0+discountRate, float64(periods))
}

func quasiHyperbolicValue(beta, delta, reward float64, delay int) float64 {
	return beta * math.Pow(delta, float64(delay)) * reward
}

func chooseDelayedReward(beta, delta, delayedReward float64, delay int, immediateReward, support float64) bool {
	delayedValue := quasiHyperbolicValue(beta, delta, delayedReward, delay)
	immediateValue := immediateReward - support
	return delayedValue >= immediateValue
}

func main() {
	fmt.Printf("Present value: %.2f\n", presentValue(1000.0, 0.03, 10))
	fmt.Printf("Synthetic delayed choice under discounting: %v\n", chooseDelayedReward(0.75, 0.97, 300.0, 12, 160.0, 40.0))
}
